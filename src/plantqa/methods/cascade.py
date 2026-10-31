"""Benedek legújabb mért cascade-je (`cascade_v4_iso`, V2T-A) a plantqa mérő kliensével.

A tierek ugyanazok, mint az R4 létrán (Thesis `data/runs/exp0007`): `cypher_rag_lines`
(30 s, 1000 sor) és `graph_agent_lines` (`params_agent_v2t.json`), primerrel, 120 s-os
kérdéskerettel. A live változat a címke szerinti útválasztást elutasítja, ezért két
`LiveCascade` van: a teljes (Cypher, majd ágens) és a csak-ágens (az „első szelep” kérdésekhez).
Az összevont gráf miatt a nézet a `DESCRIBED_BY` éleket nem számolja a tárolt korpuszhoz, és
(M1-nél) a sémaszöveg az adatlapréteggel bővül.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Any

from plantgraph.llm.client import ChatClient
from plantgraph.qa.cascade.live import LiveCascade, LiveTier
from plantgraph.qa.cascade.live_models import FreeTextQuestion, LiveAnswer, NeedsPaidCall
from plantgraph.qa.cascade.models import CascadePolicy, Decision, TierSpec
from plantgraph.qa.corpus import CorpusArtifacts, load_corpus_artifacts
from plantgraph.qa.graph_view import GraphView, NetworkxGraphView
from plantgraph.qa.harness.attempt import active_remaining_s, sender_for_run
from plantgraph.qa.harness.attempt_models import AttemptSettings
from plantgraph.qa.harness.registry import CypherDeps, LlmDeps, build_strategy
from plantgraph.qa.harness.spend_cap import SpendGuard
from plantgraph.qa.models import AnswerType
from plantgraph.qa.neo4j_view import Neo4jGraphView
from plantgraph.qa.strategies.base import AskedQuestion, Strategy
from plantgraph.store.neo4j_plan import LoadPlan

from plantqa.graph.load import INGEST_JSON
from plantqa.graph.sources import neo4j_settings
from plantqa.llm.pins import ModelKey, pin
from plantqa.plant.spec import CORPUS_ID

CYPHER = "cypher_rag_lines"
AGENT = "graph_agent_lines"
#: Thesis `data/runs/exp0007/inputs/params_cypher_v2t_a.json` és `params_agent_v2t.json`.
CYPHER_PARAMS: dict[str, Any] = {"timeout_s": 30, "row_cap": 1000}
AGENT_PARAMS: dict[str, Any] = {
    "max_steps": 40,
    "step_effort": "low",
    "observation_chars": 32000,
    "max_items_listed": 400,
    "max_prompt_chars_total": 600000,
}
CYPHER_ACCEPT = ["answered", "not_abstained", "rows", "complete"]
#: A `cascade_v4_iso` `start_tier_by_label` címkéi: ezek az ágensnél indulnak.
AGENT_FIRST_LABELS = frozenset({"UPSTREAM_TO_FIRST_VALVE", "DOWNSTREAM_TO_FIRST_VALVE"})
CUTOFF_S = 120.0
PRIMER = True

StrategyFactory = Callable[[str, dict[str, Any], LlmDeps, CypherDeps], Strategy]


class MergedPlantView(Neo4jGraphView):
    """Benedek Neo4j-nézete az összevont gráfon: a `DESCRIBED_BY` nem a rajzkorpusz éle."""

    def __init__(self, plan: LoadPlan, extra_schema: str = "") -> None:
        """`extra_schema` a sémaszöveg után fűzött rész (M1: az adatlapréteg)."""
        super().__init__(neo4j_settings(), plan)
        self._extra = extra_schema

    def schema_text(self) -> str:
        """Benedek sémaszövege, és ha van, a kiegészítés."""
        base = super().schema_text()
        return f"{base}\n\n{self._extra}" if self._extra else base

    def stored_relationship_counts(self) -> dict[str, int]:
        """A tárolt kapcsolatszámok a `DESCRIBED_BY` nélkül (a tárellenőrzéshez)."""
        counts = super().stored_relationship_counts()
        counts.pop("DESCRIBED_BY", None)
        return counts


class TracingCascade(LiveCascade):
    """`LiveCascade`, amely megőrzi a lefutott tierek nyomát (Cypher, ágenslépések)."""

    last_traces: list[dict[str, Any]]

    def _assemble(
        self,
        asked: AskedQuestion,
        runs: list[Any],
        decision: Decision | None,
        accepted: str | None,
    ) -> LiveAnswer:
        self.last_traces = [{"tier": r.tier.spec.name, "trace": r.answer.trace} for r in runs]
        return super()._assemble(asked, runs, decision, accepted)


def policy(model: ModelKey, agent_only: bool) -> CascadePolicy:
    """A `cascade_v4_iso` tierjei a modell pinjeivel (csak-ágens változat is)."""
    cypher = {"name": "cypher-v2t", "strategy": CYPHER, "accept": CYPHER_ACCEPT}
    agent = {"name": "agent-v2t", "strategy": AGENT, "accept": ["answered"]}
    cypher["pin_sha256"] = pin(model, "low").pin_hash()
    agent["pin_sha256"] = pin(model, "high").pin_hash()
    tiers = [agent] if agent_only else [cypher, agent]
    name = f"cascade_v4_iso-{model}{'-agent' if agent_only else ''}"
    return CascadePolicy.model_validate({"name": name, "tiers": tiers})


def _settings(spec: TierSpec, model: ModelKey, run_id: str) -> AttemptSettings:
    answer_pin = pin(model, "low") if spec.strategy == CYPHER else pin(model, "high")
    return AttemptSettings(run_id, answer_pin, None, PRIMER, None)


def default_strategies(view: GraphView) -> StrategyFactory:
    """Benedek regisztrált stratégiái, változtatás nélkül."""

    def make(name: str, params: dict[str, Any], llm: LlmDeps, cypher: CypherDeps) -> Strategy:
        return build_strategy(name, params, view, cypher, llm)

    return make


class DrawingCascade:
    """A rajzoldali cascade a PQA korpuszon, az összevont Neo4j-adatbázison."""

    def __init__(
        self,
        model: ModelKey,
        client: ChatClient,
        run_id: str,
        *,
        extra_schema: str = "",
        guard: SpendGuard | None = None,
        strategies: Callable[[GraphView], StrategyFactory] = default_strategies,
    ) -> None:
        """A tárat ellenőrzi, a stratégiákat egyszer építi fel."""
        self.artifacts: CorpusArtifacts = load_corpus_artifacts(CORPUS_ID, INGEST_JSON)
        a = self.artifacts
        self.view = NetworkxGraphView(CORPUS_ID, a.localized_sheets, a.resolution)
        self.source = MergedPlantView(a.load_plan, extra_schema)
        self.source.check_store()
        self.model, self.client, self.run_id = model, client, run_id
        self._make = strategies(self.view)
        self._guard = guard or SpendGuard(None)
        self.full = self._cascade(policy(model, agent_only=False))
        self.agent_only = self._cascade(policy(model, agent_only=True))

    def _tier(self, spec: TierSpec) -> LiveTier:
        settings = _settings(spec, self.model, self.run_id)
        send = sender_for_run(self.client, self.run_id)(spec.strategy)
        cypher = CypherDeps(self.source, settings.answer_pin, send, PRIMER)
        llm = LlmDeps(settings.answer_pin, send, PRIMER, active_remaining_s)
        params = CYPHER_PARAMS if spec.strategy == CYPHER else AGENT_PARAMS
        strategy = self._make(spec.strategy, params, llm, cypher)
        return LiveTier(spec, strategy, settings, self.client)

    def _cascade(self, p: CascadePolicy) -> TracingCascade:
        tiers: Sequence[LiveTier] = [self._tier(spec) for spec in p.tiers]
        return TracingCascade(CORPUS_ID, p, tiers, cutoff_s=CUTOFF_S, guard=self._guard)

    def ask(
        self, question_id: str, text: str, answer_type: str = "FREE_TEXT", label: str | None = None
    ) -> tuple[LiveAnswer | NeedsPaidCall, list[dict[str, Any]]]:
        """Egy kérdés; a címke csak az útválasztáshoz kell (a `cascade_v4_iso` szabálya)."""
        asked = FreeTextQuestion(
            question_id=question_id, text=text, answer_type=AnswerType(answer_type)
        )
        cascade = self.agent_only if label in AGENT_FIRST_LABELS else self.full
        cascade.last_traces = []
        result = cascade.ask(asked)
        return result, cascade.last_traces

    def close(self) -> None:
        """A Neo4j-kapcsolat lezárása."""
        self.source.close()
