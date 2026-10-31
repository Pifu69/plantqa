"""Seedkeresés: az első seed, amelynek üzeme minden elfogadási feltételt teljesít."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass

import networkx as nx
from plantgraph.ingest.pipeline import SyntheticCorpus, build_synthetic_corpus

from plantqa.plant import spec
from plantqa.plant.datasheets import controlled_valves, datasheet_for, tag_rows


@dataclass(frozen=True)
class Candidate:
    """Egy kipróbált seed és a hibás feltételek listája (üres = elfogadva)."""

    seed: int
    failures: list[str]
    corpus: SyntheticCorpus


def loop_variables(plant: nx.DiGraph[str]) -> set[str]:
    """A távadók (PSGF) tagjének első betűje: a szabályozott változók halmaza."""
    classes = nx.get_node_attributes(plant, "node_class")
    tags = nx.get_node_attributes(plant, "tag")
    return {tags[n][0] for n, c in classes.items() if c == "ProcessSignalGeneratingFunction"}


def failures(corpus: SyntheticCorpus) -> list[str]:
    """Az elfogadási feltételek közül a nem teljesülők."""
    plant = corpus.plant
    rows = tag_rows(plant)
    controlled = controlled_valves(plant)
    documents = Counter(
        datasheet_for(n, d, controlled) for n, d in plant.nodes(data=True) if d.get("tag")
    )
    checks = {
        "loop variables outside F/P": not loop_variables(plant) <= spec.ALLOWED_LOOP_VARIABLES,
        "tagged count out of range": not spec.MIN_TAGGED <= len(rows) <= spec.MAX_TAGGED,
        "sheet count out of range": not spec.MIN_SHEETS <= len(corpus.sheets) <= spec.MAX_SHEETS,
        "a datasheet type is missing": len([d for d in documents if d]) < 7,
        "fewer than two pumps": documents.get("gorman-rupp-0700286", 0) < 2,
    }
    return [name for name, failed in checks.items() if failed]


def try_seed(seed: int) -> Candidate:
    """Egy seed kipróbálása."""
    corpus = build_synthetic_corpus(spec.generator_config(seed), spec.split_config(seed))
    return Candidate(seed=seed, failures=failures(corpus), corpus=corpus)


def first_accepted(start: int = 1, limit: int = 500) -> Candidate:
    """Az első elfogadott seed `start`-tól; hiba, ha `limit` próbálkozáson belül nincs."""
    for seed in range(start, start + limit):
        candidate = try_seed(seed)
        if not candidate.failures:
            return candidate
    raise RuntimeError(f"no accepted seed in [{start}, {start + limit})")
