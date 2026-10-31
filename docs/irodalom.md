# Irodalomjegyzék (TDK) – csak a két forrásrepó irodalmi jegyzeteiből

Összeállítva: 2026-10-31. **Minden tétel szerepel legalább egy irodalmi jegyzetben** a két csak
olvasható repóban. Webet nem használtam, és emlékezetből semmit sem adtam hozzá. A szerzők, a címek és
az azonosítók úgy szerepelnek, ahogy a jegyzet írja őket. Ha a jegyzetből hiányzik valami (például a
szerző), az itt is üresen marad, és ezt jelzem. Az évszámot csak akkor vezettem le az arXiv-azonosítóból
(`YYMM.`), ha a jegyzet nem adta meg; ezt „(az arXiv-azonosító szerint)” jelöli.

**Útvonal-rövidítések**

| Rövidítés | Teljes útvonal |
|---|---|
| `PD/` | `C:/Users/Zsombi/plantdocs/docs/private/10-literature/` |
| `TL/` | `C:/Users/Zsombi/Thesis/docs/private/10-literature/` |
| `TN/` | `C:/Users/Zsombi/Thesis/docs/Notes/` (a TL-jegyzetek magyar nyelvű tanító változatai) |

**Használhatóság**

- **idézhető**: a jegyzetből látszik, hogy a mű tényleg olvasva volt (módszer, eredmények, számok,
  korlátok).
- **csak említés**: a jegyzet szerint csak az absztrakt, egy kivonat vagy egy README volt olvasva, a mű
  „skimmed”/„not read”, vagy a forrás másodlagos. Létezésének megemlítésére jó, tartalmi állítás
  alátámasztására nem, amíg a teljes szöveg nincs meg.
- **NE idézd**: a jegyzet kifejezetten tiltja az idézést, vagy a mű nem azonosítható.

---

## 1. P&ID-kérdésmegválaszolás és P&ID-gráfok

- **[Alimin2026]** Alimin & Schweidtmann (2026): *GraphRAG for Engineering Diagrams: ChatP&ID Enables LLM Interaction with P&IDs*. arXiv 2603.22528; a folyóiratváltozat: AIChE Journal, doi 10.1002/aic.70540 (a TL/_novelty-log.md szerint ezt kell idézni).
  - Forrás: `PD/chatpid-2603.22528.md`, `PD/00-reading-list.md`, `TL/2603.22528.md`, `TL/00-reading-list.md`, `TL/_novelty-log.md`, `TL/ontology-landscape.md`, `TL/real-pid-data-sweep-2026-10.md`, `TN/graphrag-lekeresi-strategiak.md`, `TN/ontologia-pid.md`
  - Mit csinál: DEXPI P&ID-ket alakít pyDEXPI-vel Neo4j-gráffá, és egy LangGraph-ágens négy eszköz (ContextRAG, VectorRAG, PathRAG, CypherRAG) közül választ; egyetlen lapon, 19 kérdésen a ContextRAG nyert (0,91), a szerzők szerint viszont ez a módszer többlapos rajzoknál nem skálázódik.
  - Használhatóság: **idézhető**. Mindkét repóban teljes összefoglaló van, a TL szó szerinti idézetekkel. Figyelem: a TL szerint így kell hivatkozni rá: „iteratív ágens, eszközönként egy hívással kiértékelve”, nem „egyhívásos rendszer”.

- **[Alimin2025]** Alimin, Goldstein, Schulze Balhorn, Schweidtmann (2025): *Talking like Piping and Instrumentation Diagrams (P&IDs)*. arXiv 2502.18928.
  - Forrás: `TL/2502.18928.md`, `TL/00-reading-list.md`, `TL/ontology-landscape.md`, `TN/ontologia-pid.md`; csak listázva: `PD/pid-image-interpretation-2411.13929-2502.18928.md`, `PD/00-reading-list.md`
  - Mit csinál: DEXPI → pyDEXPI → Neo4j chatbot, amely a sűrített gráfot (212 → 53 csúcs, kb. 86%-kal kevesebb token) GraphML-ként, visszakeresés nélkül teszi a promptba; egy folyamatábrán, három kérdésen értékelték.
  - Használhatóság: **idézhető** (a TL alapján; a PD-jegyzet csak felsorolja).

- **[Gupta2025]** Mohit Gupta, Chialing Wei, Thomas Czerniawski, Ricardo Eiris (2025): *PIDQA - Question Answering on Piping and Instrumentation Diagrams*. Machine Learning and Knowledge Extraction 7(2), article 39, doi 10.3390/make7020039.
  - Forrás: `PD/pidqa-gupta-2025.md`, `PD/00-reading-list.md`, `TL/make7020039-pidqa.md`, `TL/00-reading-list.md`, `TL/ontology-landscape.md`, `TL/_novelty-log.md`, `TL/real-pid-data-sweep-2026-10.md`, `TN/ontologia-pid.md`
  - Mit csinál: képből entitásgráfot épít, ebből címkézett tulajdonsággráf lesz Neo4j-ben, a kérdésekre pedig az LLM Cypher-lekérdezést ír; 500 szintetikus lapon 64 000 sablonos kérdés-válasz párt ad, programmal előállított gold válaszokkal és kizárólag egylapos kérdésekkel.
  - Használhatóság: **csak említés**. A TL szerint a teljes szöveg nem volt olvasható (MDPI, HTTP 403); a számok az absztraktból és a GitHub README-ből származnak. A TL szerint viszont a kapcsolódó munkákban kötelező idézni, ezért a teljes szöveget be kell szerezni a könyvtárból.

- **[Gadekar2026]** Gadekar, Sakhinana, Runkana (2026): *Grounded and Faithful P&ID Reasoning: Constraining Vision-Language Models with Recovered Evidence Graphs*. arXiv 2609.05880v1.
  - Forrás: `TL/2609.05880.md`, `TL/00-reading-list.md`, `TL/_novelty-log.md`, `TL/real-pid-data-sweep-2026-10.md`
  - Mit csinál: raszteres P&ID-ből folyamatgráfot nyer vissza, majd egy VLM a topológiai kérdésekre csak hét, tényt visszaadó gráfoperátoron keresztül válaszolhat; a TopoPID-VQA 3000 kérdésén a pontos egyezést 36,7–41,3%-ról 74,3–76,0%-ra emeli, egylapos, szintetikus rajzokon.
  - Használhatóság: **idézhető** (a jegyzet a teljes HTML-szövegen alapul, a függelékkel együtt). Szerzőnév: a TL/_novelty-log.md korábban „Srinivas”-t írt, a javított forma „Sakhinana”.

- **[SchulzeBalhorn2025]** Schulze Balhorn, Seijsener, Dao, Kim, Goldstein, Driessen, Schweidtmann (2025): *Rule-based autocorrection of Piping and Instrumentation Diagrams (P&IDs) on graphs*. arXiv 2502.18493.
  - Forrás: `TL/2502.18493.md`, `TL/00-reading-list.md`, `TL/_novelty-log.md`, `TL/ontology-landscape.md`, `TL/pid-structural-rules.md`, `TN/pid-szerkezeti-szabalyok.md`, `TN/lpg-vs-rdf.md`, `TN/ontologia-pid.md`
  - Mit csinál: kézzel írt szabálygráfokat (hibás minta és javított minta) illeszt VF2 részgráf-izomorfizmussal a pyDEXPI-gráfra, és fixpontig javít; 33 szabályt mutat be egyetlen szemléltető P&ID-n.
  - Használhatóság: **idézhető**.

- **[Zhu2026a]** Baikai Zhu, Samuel Duong, Javal Vyas, Mehmet Mercangoez (2026): *From P&ID Drawings to Process Graphs: A Multimodal Language Model Approach*. arXiv 2607.19568.
  - Forrás: `TL/2607.19568.md`, `TL/00-reading-list.md`, `TL/_novelty-log.md`, `TL/ontology-landscape.md`
  - Mit csinál: a P&ID-digitalizálást címkekinyerésre és topológia-következtetésre bontja egy kétlépcsős MLLM-folyamatban, két ANSI-szabványos esettanulmányon.
  - Használhatóság: **csak említés**. A státusza „skimmed”, a teljes szöveget nem olvasták; a szerzőket a TL/ontology-landscape.md adja, a TL/2607.19568.md szerint még megerősítendők.

- **[PidGraphAgent2026]** GitHub `shaaz1000/pid-graph-agent` (2026), szoftver, nem lektorált.
  - Forrás: `TL/_novelty-log.md`, `TL/real-pid-data-sweep-2026-10.md`
  - Mit csinál: LangGraph-ágens hét általános gráfeszközzel DEXPI-fájlokon; 15 + 37 saját kérdésen futtatták, kérdésenként egy DEXPI-fájlon.
  - Használhatóság: **idézhető**, szoftverként (a README-t végig elolvasták); tudományos előzményként nem.

- **[Kochanski2026]** Kochański et al. (2026): „How Everllence Scaled P&ID Intelligence…”. AWS Industries blog, 2026-05-27.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: kereskedelmi Neo4j-tudásgráf, amely helyreállítja a lapok közötti kapcsolatokat, rajta LangGraph ReAct-ágens előre definiált gráflekérdező eszközökkel, Cypher-eszközzel és LightRAG-gel; kiértékelést nem közöl.
  - Használhatóság: **idézhető**, kereskedelmi előzményként (a blogot olvasták); módszerként nem.

- **[Kokubo2026]** H. Kokubo (JGC): „What Connects to This Pump?”, Neo4j NODES 2026 előadás (2026-11-12-re ütemezve).
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: Claude Agent SDK és csak olvasható Neo4j MCP-szerver; az ágens maga írja a Cyphert, a demó több összekapcsolt rajzot fed le.
  - Használhatóság: **csak említés** (csak az előadás oldalát olvasták).

- **[Sakhinana2024]** Sakhinana, Sannidhi, Runkana (2024): többágenses ReAct VQA PFD- és P&ID-képeken. arXiv 2409.00082.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: képalapú, gráfeszközök nélküli kérdésmegválaszolás folyamatábrákon.
  - Használhatóság: **csak említés** (absztrakt).

- **[Shinde2026]** Shinde, Chachad, Bhosale (2026): neuro-szimbolikus P&ID-auditálás. ACS Chem. Health Saf., doi 10.1021/acs.chas.6c00094.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: három forgatókönyvön, csak fogalmi szinten vizsgált P&ID-auditálás.
  - Használhatóság: **csak említés** (absztrakt).

- **[Mandarapu2026]** Mandarapu, Kunkunuru (2026): *KGs as the Missing Data Layer for LLM-Based Industrial Asset Operations*. arXiv 2605.26874.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: a kérdéseket LLM-Cypher, determinisztikus gráfprimitívek vagy generált tudás felé irányítja karbantartási eszközadatokon (AssetOpsBench).
  - Használhatóság: **csak említés** (absztrakt).

- **[Ma2026]** Ma et al. (2026): *Artificial intelligence for piping and instrumentation diagrams: a review and perspective*. Front. Chem. Sci. Eng., doi 10.1007/s11705-026-2685-z.
  - Forrás: `TL/_novelty-log.md`, `TL/pid-structural-rules.md`
  - Mit csinál: áttekintő cikk a P&ID-ekkel kapcsolatos MI-kutatásról; a jegyzetek szerint idézhető forrás lehet arra, hogy a többlapos feldolgozás nyitott probléma, ha ezt valóban kimondja.
  - Használhatóság: **csak említés**. Zárt hozzáférésű, sem az absztraktot, sem a teljes szöveget nem olvasták; könyvtári kérés van rá.

- **[Zakarin2026]** Zakarin et al. (2026): LLMs in Process Diagram Engineering, PFD → P&ID. arXiv 2608.11220.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: P&ID-generálás PFD-ből, korlátozott SDK-n keresztül.
  - Használhatóság: **csak említés** (absztrakt).

- **[Zhu2026b]** Zhu, Tong, Ren (2026): DEXPI serialization in LLM greenfield design. arXiv 2609.12656.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: DEXPI-szerializáció LLM-alapú zöldmezős tervezésben, három eseten.
  - Használhatóság: **csak említés** (absztrakt).

- **[Mankodiya2026]** Mankodiya et al. (2026): AEC-Bench. arXiv 2603.29199.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: 196 feladatos benchmark valódi építőipari tervdokumentációkon, köztük „egy rajzsorozat több lapján átívelő” feladatokkal (P&ID és tudásgráf nélkül).
  - Használhatóság: **csak említés**. Az olvasottságot a jegyzet nem rögzíti. Fontos a megfogalmazáshoz: emiatt csak azt lehet állítani, hogy *P&ID-k / folyamatüzemek* esetén vizsgálatlan a lapok közötti következtetés.

## 2. GraphRAG, visszakeresési stratégiák, gráfeszközös ágensek

- **[HyperGraphRAG2025]** szerzők a jegyzetben nincsenek (2025): HyperGraphRAG. arXiv 2503.21322, NeurIPS 2025.
  - Forrás: `PD/hypergraphrag-2503.21322.md`, `PD/00-reading-list.md`
  - Mit csinál: az n-áris tényeket LLM-es relációkinyeréssel hiperélekként ábrázolja egy kétrészes gráfban, külön vektortárral az entitásoknak és a hiperéleknek; négy területen (orvoslás, mezőgazdaság, informatika, jog) értékelték.
  - Használhatóság: **idézhető**.

- **[HyperRAG2026]** szerzők a jegyzetben nincsenek (2026): HyperRAG. arXiv 2602.14470, WWW 2026.
  - Forrás: `PD/hyperrag-2602.14470.md`, `PD/00-reading-list.md`
  - Mit csinál: n-áris hipergráfokon keres vissza, és amellett érvel, hogy az összetett tények bináris hármasokra bontása szemantikai széttöredezéshez vezet.
  - Használhatóság: **idézhető**. A PD-jegyzet a HyperGraphRAG-gel együtt javasolja idézni: „a reprezentációs probléma elvben megoldott”.

- **[GoldenRetriever2024]** szerzők a jegyzetben nincsenek (2024, az arXiv-azonosító szerint): Golden-Retriever. arXiv 2408.00798.
  - Forrás: `PD/golden-retriever-2408.00798.md`, `PD/00-reading-list.md`
  - Mit csinál: ipari tudásbázison RAG-ot futtat egy reflexiós lépéssel, amely a szakzsargont és a rövidítéseket a visszakeresés előtt azonosítja és tisztázza.
  - Használhatóság: **idézhető**.

- **[Xiang2025]** Xiang et al. (2025, az arXiv-azonosító szerint): GraphRAG-Bench, „When to use Graphs in RAG”. arXiv 2506.05690v3.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: méretfüggő keresztezést mutat ki a sima RAG és a HippoRAG2 között szöveges korpuszon (kb. 56k / 603k / 1132k token); kis korpuszon a sima RAG nyer, közepes és nagy korpuszon visszaesik.
  - Használhatóság: **idézhető** (a G.5 függeléket teljes szövegben olvasták).

- **[Fan2026]** Fan et al. (2026): GraphRAG-Router. arXiv 2604.16401.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: RL-lel tanított, kérdésenkénti útválasztás GraphRAG-módszerek és LLM-ek között hat Wikipedia-alapú QA-benchmarkon, kb. 30%-kal kevesebb nagy-LLM hívással.
  - Használhatóság: **idézhető** (a jegyzetben „read” jelöléssel).

- **[Li2024]** Li et al. (2024, az arXiv-azonosító szerint): Self-Route. arXiv 2407.16833.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: elegendő erőforrással a hosszú kontextus jobb a RAG-nál, de a RAG sokkal olcsóbb; kérdésenként választ a kettő között.
  - Használhatóság: **csak említés** (absztrakt).

- **[Finkelshtein2025]** Finkelshtein et al. (2025, az arXiv-azonosító szerint). arXiv 2509.18487.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: hosszú szöveges vagy nagy fokszámú gráfokon a kódgenerálás jobb a promptolásnál, mert a prompt gyorsan túllépi a tokenkeretet.
  - Használhatóság: **csak említés** (absztrakt).

- **[A2RAG2026]** szerzők a jegyzetben nincsenek: A2RAG. arXiv 2601.21162.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: fokozatosan növeli a visszakeresési erőfeszítést, ezzel kb. 50%-kal csökkenti a tokenszámot és a késleltetést.
  - Használhatóság: **csak említés** (absztrakt).

- **[LASTCQ2026]** szerzők a jegyzetben nincsenek: LAST-CQ. arXiv 2609.12746.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: ágensalapú text-to-Cypher 2471 lekérdezésen; az eredménye az, hogy a hiba felismerése és újrapróbálásra irányítása működik.
  - Használhatóság: **csak említés** (absztrakt).

- **[CypherBench2024]** szerzők a jegyzetben nincsenek: CypherBench. arXiv 2412.18702.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: text-to-Cypher benchmark (a jegyzet csak megnevezi).
  - Használhatóság: **csak említés** (absztrakt).

- **[RAGvsGraphRAG2025]** szerzők a jegyzetben nincsenek: RAG vs GraphRAG. arXiv 2502.11371.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: a sima RAG és a GraphRAG összehasonlítása (a jegyzet csak megnevezi).
  - Használhatóság: **csak említés** (absztrakt).

- **[KBQAAgent2024]** szerzők a jegyzetben nincsenek: Middleware / KBQA-Agent. arXiv 2402.14672.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: hét tudásbázis-eszköz (`get_relations`, `get_neighbors`, `get_attributes`, `argmax`, `argmin`, `intersection`, `count`), amelyek korábbi eredményeket megnevező változókon dolgoznak; 500 kérdésen értékelték. A jegyzet szerint ez a legközelebbi általános előzménye a primitívek és hivatkozások (handle-ök) tervnek.
  - Használhatóság: **idézhető** (teljes szöveg).

- **[KGAgent2024]** szerzők a jegyzetben nincsenek: KG-Agent. arXiv 2402.11163.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: kinyerő, logikai és szemantikai eszköztár tudásgráfon; LLaMA2-7B, 10 ezer mintán finomhangolva.
  - Használhatóság: **idézhető** (teljes szöveg).

- **[GraphCoT2024]** szerzők a jegyzetben nincsenek: Graph-CoT. arXiv 2404.07103.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: négy gráfeszköz és egy befejező lépés; a GRBench 1740 kérdést ad 10 gráfon (kb. 47 ezertől 84 millió csúcsig), méret szerinti elemzés nélkül.
  - Használhatóság: **idézhető** (teljes szöveg).

- **[StructGPT2023]** StructGPT. arXiv 2305.09645. Forrás: `TL/_novelty-log.md`. Mit csinál: iteratív, előbb olvasó, aztán következtető működés strukturált interfészeken. Használhatóság: **csak említés** (absztrakt).
- **[ToG2023]** Think-on-Graph. arXiv 2307.07697. Forrás: `TL/_novelty-log.md`. Mit csinál: az LLM nyalábkereséssel (beam search) halad egy tudásgráfon. Használhatóság: **csak említés** (absztrakt).
- **[ToG2_2024]** ToG-2. arXiv 2407.10805. Forrás: `TL/_novelty-log.md`. Mit csinál: a Think-on-Graph továbbfejlesztése (a jegyzet csak megnevezi). Használhatóság: **csak említés** (absztrakt).
- **[AgentBench2023]** AgentBench. arXiv 2308.03688. Forrás: `TL/_novelty-log.md`. Mit csinál: ágensbenchmark, benne tudásgráf-környezettel. Használhatóság: **csak említés** (absztrakt).
- **[InteractiveKBQA2024]** Interactive-KBQA. arXiv 2402.15131. Forrás: `TL/_novelty-log.md`. Mit csinál: három általános tudásbázis-API-val dolgozó kérdésmegválaszolás. Használhatóság: **csak említés** (absztrakt).
- **[TreeOfTraversals2024]** Tree-of-Traversals. arXiv 2407.21358. Forrás: `TL/_novelty-log.md`. Mit csinál: tudásgráf-bejárás LLM-mel (a jegyzet csak megnevezi). Használhatóság: **csak említés** (absztrakt).
- **[QueryAgent2024]** QueryAgent. arXiv 2403.11886. Forrás: `TL/_novelty-log.md`. Mit csinál: ágensalapú tudásbázis-kérdésmegválaszolás (a jegyzet csak megnevezi). Használhatóság: **csak említés** (absztrakt).
- **[KBQAo1_2025]** KBQA-o1. arXiv 2501.18922. Forrás: `TL/_novelty-log.md`. Mit csinál: ágensalapú tudásbázis-kérdésmegválaszolás (a jegyzet csak megnevezi). Használhatóság: **csak említés** (absztrakt).
- **[RoG2023]** RoG. arXiv 2310.01061. Forrás: `TL/_novelty-log.md`. Mit csinál: előbb relációs útvonalakat tervez, aztán visszakeres, eszközök nélkül. Használhatóság: **csak említés** (absztrakt).
- **[KnowGPT2023]** KnowGPT. arXiv 2312.06185. Forrás: `TL/_novelty-log.md`. Mit csinál: tudásgráfból épít promptot, eszközök nélkül. Használhatóság: **csak említés** (absztrakt).
- **[GraphOTTER2024]** GraphOTTER. arXiv 2412.01230. Forrás: `TL/_novelty-log.md`. Mit csinál: táblázatot gráffá alakít, és előre definiált műveletekkel dolgozik rajta. Használhatóság: **csak említés** (absztrakt).
- **[GraphDancer2026]** GraphDancer. arXiv 2602.02518. Forrás: `TL/_novelty-log.md`. Mit csinál: gráffeltáró ágens (a jegyzet csak megnevezi). Használhatóság: **csak említés** (absztrakt).
- **[GraphReAct2026]** GraphReAct. arXiv 2605.07357. Forrás: `TL/_novelty-log.md`. Mit csinál: ReAct-stílusú gráfágens (a jegyzet csak megnevezi). Használhatóság: **csak említés** (absztrakt).
- **[GraphScout2026]** GraphScout. arXiv 2603.01410. Forrás: `TL/_novelty-log.md`. Mit csinál: amellett érvel, hogy egy kis, előre definiált eszközkészlet jelentősen korlátozza a gráffeltárást; ez a fix primitívkészlettel szembeni ellenvélemény. Használhatóság: **csak említés** (absztrakt).
- **[GABench2026]** GABench. arXiv 2608.01684. Forrás: `TL/_novelty-log.md`. Mit csinál: 84 gráfeszköz és 10 400 feladat. Használhatóság: **csak említés** (absztrakt).
- **[BYOKGRAG2025]** BYOKG-RAG. arXiv 2507.04127. Forrás: `TL/_novelty-log.md`. Mit csinál: több stratégiát (köztük OpenCyphert) kombináló tudásgráf-RAG. Használhatóság: **csak említés** (absztrakt).
- **[RLMonKG2026]** RLM-on-KG. arXiv 2604.17056. Forrás: `TL/_novelty-log.md`. Mit csinál: fix eszközkészlet, először heurisztikákkal. Használhatóság: **csak említés** (absztrakt).

- **[MCPNeo4j]** Neo4j `mcp-neo4j-cypher` (neo4j-contrib/mcp-neo4j), szoftver.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: MCP-n keresztüli gráfelérés három eszközzel (`get_neo4j_schema`, `read_neo4j_cypher`, `write_neo4j_cypher`), vagyis szabad Cypherrel.
  - Használhatóság: **idézhető**, szoftverként (a README-t olvasták).

- **[R2Adapter2026]** R²Adapter. arXiv 2609.02894. Forrás: `TL/_novelty-log.md`. Mit csinál: adaptív RAG-útválasztás általános szövegen. Használhatóság: **csak említés** (csak keresési kivonat).
- **[RAGRouterBench2026]** RAGRouter-Bench. arXiv 2604.03455 / 2602.00296 (a jegyzet két azonosítót ad egy névhez). Forrás: `TL/_novelty-log.md`. Mit csinál: RAG-útválasztási benchmark. Használhatóság: **csak említés** (csak keresési kivonat; az azonosítót is tisztázni kell).
- **[PracticalGraphRAG2025]** „Towards Practical GraphRAG: Efficient KG Construction and Hybrid Retrieval at Scale”. arXiv 2507.03226. Forrás: `TL/00-reading-list.md`, `TL/_novelty-log.md`. Mit csinál: gyakorlati, nagy léptékű GraphRAG (KG-építés és hibrid visszakeresés). Használhatóság: **csak említés** (sorban áll, nem olvasták).
- **[MSGraphRAG]** Microsoft GraphRAG (közösségi összefoglalás). Azonosító nincs. Forrás: `TL/00-reading-list.md`, `TL/_novelty-log.md`. Mit csinál: a skálázáshoz szükséges technikák egyike a jegyzet szerint. Használhatóság: **csak említés** (nem olvasták).
- **[LightRAG]** LightRAG. Azonosító nincs. Forrás: `TL/00-reading-list.md`, `TL/_novelty-log.md`. Mit csinál: skálázási technika (a jegyzet csak megnevezi). Használhatóság: **csak említés** (nem olvasták).
- **[HippoRAG2]** HippoRAG-2. Azonosító nincs. Forrás: `TL/00-reading-list.md`, `TL/_novelty-log.md`. Mit csinál: skálázási technika (a jegyzet csak megnevezi). Használhatóság: **csak említés** (nem olvasták).
- **[KETRAG]** KET-RAG. Azonosító nincs. Forrás: `TL/00-reading-list.md`, `TL/_novelty-log.md`. Mit csinál: skálázási technika (a jegyzet csak megnevezi). Használhatóság: **csak említés** (nem olvasták).
- **[MegaRAG2025]** MegaRAG. arXiv 2512.20626. Forrás: `TL/_novelty-log.md`. Mit csinál: általános multimodális, oldalankénti KG-RAG. Használhatóság: **csak említés**.
- **[Liu2023]** Liu et al.: „Lost in the Middle”. arXiv 2307.03172. Forrás: `TN/graphrag-lekeresi-strategiak.md`. Mit csinál: a hosszú kontextus közepére került információt a modellek rosszabbul használják. Használhatóság: **csak említés**. A jegyzet szerint nem olvasták be, és a projekt saját gráfjain mérni kell.

## 3. Dokumentum-QA, táblázatos és n-áris tények

- **[Knollmeyer2025]** Knollmeyer, Caymazer, Grossmann (2025): Document GraphRAG. Electronics 2025, 14(11):2102.
  - Forrás: `PD/document-graphrag-electronics-2025.md`, `PD/00-reading-list.md`
  - Mit csinál: gyártási dokumentumokon kérdésmegválaszolás olyan tudásgráffal, amely a dokumentum saját szerkezetéből és egy automatikusan épített, könnyű példány-KG-ből áll; a cikk elismeri, hogy szakterületen az automatikus KG-építés pontatlan, ezért ma is főleg kézi munka.
  - Használhatóság: **idézhető**.

- **[HierMARL2025]** szerzők, cím és azonosító a jegyzetben nincsenek (2025): Hierarchical multi-agent RL for industrial document QA.
  - Forrás: `PD/hierarchical-multiagent-rl-industrial-qa-2025.md`, `PD/00-reading-list.md`
  - Mit csinál: multimodális ipari dokumentumokon (kézikönyvek, kapcsolási rajzok, paramétertáblák) hierarchikus, többágenses megerősítéses tanulással hangolja össze a visszakeresést és a következtetést.
  - Használhatóság: **NE idézd**. A jegyzet szerint: „track it down before citing in the final thesis text”, vagyis idézés előtt azonosítani kell.

- **[StructRAG2025]** szerzők a jegyzetben nincsenek (2025, az arXiv-azonosító szerint): Structured-data-aware RAG for technical documents. arXiv 2506.23136.
  - Forrás: `PD/structured-data-aware-rag-2506.23136.md`, `PD/00-reading-list.md`
  - Mit csinál: olyan RAG műszaki dokumentumokra, amely a beágyazott strukturált adatokat (táblázatok, sémák) nem lapos prózaként kezeli.
  - Használhatóság: **csak említés**. A jegyzet csak általános összefoglalót ad, és maga írja, hogy egy kulcskérdést „needs re-checking on a closer read”, vagyis alaposabb olvasással ellenőrizni kell.

- **[Kumar2026]** Kumar, Motiyani, Kasturi, Seefried, Movva, Ghosal (2026): *Enginuity: A Dataset and Benchmark for Vision-Language Understanding of Engineering Diagrams*. arXiv 2606.03410.
  - Forrás: `PD/enginuity-2606.03410.md`, `PD/00-reading-list.md`, `TL/2606.03410.md`, `TL/00-reading-list.md`, `TL/ontology-landscape.md`, `TL/real-pid-data-sweep-2026-10.md`
  - Mit csinál: VLM-benchmark katonai szervizkézikönyvek 6940 oldalán, alkatrésztábla-kinyeréssel és VQA-val; kimutatja, hogy a modellek megtalálják a tételeket, de pontatlanul írják le őket, és hogy a tokenátfedéses metrikák 2–6-szorosan alulmérik a képességet. Keresztbírálós (cross-judge) LLM-bírálatot használ.
  - Használhatóság: **idézhető**.

- **[Enginuity2026b]** „Enginuity” néven futó másik munka. arXiv 2601.13299.
  - Forrás: `TL/_novelty-log.md`, `TL/real-pid-data-sweep-2026-10.md`
  - Mit csinál: autóipari robbantott alkatrészrajzokra vonatkozó javaslat, nem P&ID; a Kaggle-linkje kézzel rajzolt áramköri adatkészlet.
  - Használhatóság: **NE idézd**. A TL/real-pid-data-sweep szerint „Exclude. Not the same as the Enginuity VLM benchmark (2606.03410)”; a novelty log korábban összekeverte a kettőt.

- **[StarE2020]** szerzők a jegyzetben nincsenek (2020, az arXiv-azonosító szerint): StarE. arXiv 2009.10847.
  - Forrás: `PD/hyper-relational-kg-literature.md`, `PD/00-reading-list.md`
  - Mit csinál: a minősítők (qualifiers) használata a sima hármasalapú ábrázoláshoz képest akár 25 MRR-ponttal javítja a hiper-relációs linkpredikciót.
  - Használhatóság: **idézhető** (konkrét eredményt rögzít). A jegyzet szerint ez a terület kiindulópontja, ezért nem szabad újdonságként bemutatni.

- **[HINGE]** HINGE. Év és azonosító nincs. Forrás: `PD/hyper-relational-kg-literature.md`. Mit csinál: hiper-relációs KG-modellcsalád (csak megnevezve). Használhatóság: **csak említés**.
- **[NeuInfer]** NeuInfer. Év és azonosító nincs. Forrás: `PD/hyper-relational-kg-literature.md`. Mit csinál: hiper-relációs KG-modellcsalád (csak megnevezve). Használhatóság: **csak említés**.
- **[QUAD]** QUAD. Év és azonosító nincs. Forrás: `PD/hyper-relational-kg-literature.md`. Mit csinál: hiper-relációs KG-modellcsalád (csak megnevezve). Használhatóság: **csak említés**.
- **[HyperMono]** HyperMono. Év és azonosító nincs. Forrás: `PD/hyper-relational-kg-literature.md`. Mit csinál: hiper-relációs KG-modellcsalád (csak megnevezve). Használhatóság: **csak említés**.
- **[WD50K]** WD50K benchmark-adatkészlet. Forrás: `PD/hyper-relational-kg-literature.md`. Mit csinál: hiper-relációs linkpredikciós benchmark (csak megnevezve). Használhatóság: **csak említés**.
- **[JF17K]** JF17K benchmark-adatkészlet. Forrás: `PD/hyper-relational-kg-literature.md`. Mit csinál: hiper-relációs linkpredikciós benchmark (csak megnevezve). Használhatóság: **csak említés**.
- **[RDFstar]** RDF-star. Forrás: `PD/hyper-relational-kg-literature.md`. Mit csinál: állítások minősítésére szolgáló RDF-kiterjesztés (csak megnevezve). Használhatóság: **csak említés** (nincs megadott forrás).
- **[Wikidata]** Wikidata (minősítő-mechanizmus; fogalomazonosítók, pl. `Q1890459`, `P2789`).
  - Forrás: `PD/hyper-relational-kg-literature.md`, `TL/ontology-landscape.md`
  - Mit csinál: a PD-jegyzet a minősítő-mechanizmust a hiper-relációs terület őseként említi; a TL szerint a Wikidata enciklopédikus szinten tartalmazza a P&ID-fogalmakat, de mérnöki példányszókészlete nincs.
  - Használhatóság: **csak említés** (a TL az API-t ellenőrizte, de publikáció nincs megadva).

- **[Gjerver2025]** A. Gjerver, R. Frostad, V. Barisic, M. Hodkiewicz, C. Woods, M. Fekete, A. B. Torjusen, J. W. Kluwer (2025): *Machine-interpretable Engineering Design Standards for Valve Specification*. arXiv:2510.01736, 2025-10-02. Kód és ontológia: `github.com/PCA-POSC-Caesar-Association/IDO_Use_Case_Valve_Ontology_Public` (CC BY-SA 4.0).
  - Forrás: `PD/valve-spec-ido-2510.01736.md`
  - Mit csinál: tervezési szabványokat (pl. ASME B16.34) moduláris, az IDO-ra épülő OWL-ontológiákká alakít, és következtetéssel ellenőrzi, hogy egy gyártói termék megfelel-e a szelep-adatlap előírásainak.
  - Használhatóság: **csak említés**. A jegyzet szerint csak az absztraktot, a README-t és a `valve-core.ttl`-t olvasták, a teljes cikket nem. A jegyzet szerint a 2. szakaszban hivatkozni kell rá, ezért idézés előtt el kell olvasni.

## 4. P&ID-digitalizálás, adatkészletek, eszközök

- **[Sturmer2024]** Stürmer, Graumann, Koch (DLR) (2024): *From Engineering Diagrams to Graphs: Digitizing P&IDs with Transformers*. arXiv 2411.13929, IEEE DSAA 2025.
  - Forrás: `TL/2411.13929.md`, `TL/00-reading-list.md`, `TL/pid2graph.md`, `TL/ontology-landscape.md`, `TL/real-pid-composition-2026-10.md`, `TL/real-pid-data-sweep-2026-10.md`, `TN/uzemgenerator-es-grafsema.md`; csak listázva: `PD/pid-image-interpretation-2411.13929-2502.18928.md`, `PD/00-reading-list.md`
  - Mit csinál: egy Relationformer-transzformer együtt jósolja a szimbólumokat és a kapcsolataikat; valódi rajzokon 75,46% él-mAP-t ér el, szemben a moduláris folyamat 45,89%-ával, és kiadja a PID2Graph benchmarkot.
  - Használhatóság: **idézhető** (a TL alapján).

- **[PID2Graph2025]** Stürmer, Graumann, Koch (DLR) (2025): PID2Graph adatkészlet. Zenodo, doi 10.5281/zenodo.14803338, CC BY-SA 4.0.
  - Forrás: `TL/pid2graph.md`, `TL/00-reading-list.md`, `TL/ontology-landscape.md`, `TL/real-pid-composition-2026-10.md`, `TL/real-pid-data-sweep-2026-10.md`
  - Mit csinál: P&ID-képek GraphML gráf-gold párokkal (Dataset-PID, OPEN100 12 valódi lappal, Synthetic); a GraphML tisztán geometriai, címkék és lapok közötti gold nélkül.
  - Használhatóság: **idézhető** (a fájlokat közvetlenül megvizsgálták).

- **[OPEN100]** Energy Impact Center: OPEN 100 atomerőmű-terv P&ID-jei (www.open-100.com).
  - Forrás: `TL/pid2graph.md`, `TL/real-pid-data-sweep-2026-10.md`, `TL/real-pid-composition-2026-10.md`
  - Mit csinál: egyetlen nyilvános, többlapos valódi P&ID-sorozat (12 PNG-lap, valódi lapközi csatlakozókkal és lógó hivatkozásokkal); licenc nincs megadva, a PID2Graph CC BY-SA 4.0 alatt terjeszti.
  - Használhatóság: **idézhető**, adatforrásként (a lapokat megvizsgálták).

- **[Paliwal2021]** Paliwal, Jain, Sharma, Vig (2021): *Digitize-PID*. arXiv 2109.03794 (a Dataset-P&ID forrása).
  - Forrás: `TL/real-pid-composition-2026-10.md`, `TL/real-pid-data-sweep-2026-10.md`, `TL/00-reading-list.md` (ott még sorban álló tételként), `TL/2411.13929.md`, `TL/make7020039-pidqa.md`
  - Mit csinál: 500 szintetikus lapból álló, 32 szimbólumosztályos adatkészlet; a kiértékelésben használt 12 valódi lap privát, nincs kiadva.
  - Használhatóság: **idézhető** (a TL/real-pid-composition a PDF-et olvasta).

- **[Rahul2019]** Rahul, Paliwal, Sharma, Vig (2019): *Automatic Information Extraction from P&IDs*. arXiv 1901.11383.
  - Forrás: `TL/real-pid-composition-2026-10.md`
  - Mit csinál: egy olajipari cég valódi lapjain 10 szimbólumosztályt ismer fel, és bemeneteket, kimeneteket és vezetékkódokat nyer ki.
  - Használhatóság: **idézhető** (PDF).

- **[Mani2020]** Mani, Haddad, Constantini, Douhard, Li, Poirier (C3.ai) (2020): *Automatic Digitization of Engineering Diagrams Using Deep Learning and Graph Search*. CVPRW 2020.
  - Forrás: `TL/real-pid-composition-2026-10.md`, `TL/00-reading-list.md` (ott még sorban álló tételként)
  - Mit csinál: 18 tanító és 11 teszt P&ID-n dolgozik; kimondja, hogy a rajzok közötti kapcsolatok „arrow box” szimbólumai jól strukturált rajzszámot hordoznak, és reguláris kifejezésekkel összeköthetők.
  - Használhatóság: **idézhető** (PDF). A cím pontos alakja a jegyzetben csak a PDF-URL-ből olvasható ki.

- **[Hirtreiter2022]** Hirtreiter, Schulze Balhorn, Schweidtmann (2022): *Towards automatic generation of P&IDs with AI*. arXiv 2211.05583; a jegyzet szerint AIChE J. 70(1) e18259.
  - Forrás: `TL/pid-structural-rules.md`, `TL/real-pid-composition-2026-10.md`, `TN/pid-szerkezeti-szabalyok.md`
  - Mit csinál: SFILES 2.0 mintákon alapuló, Markov-jellegű P&ID-generálás; a valódi adatok szókészlete 390 token, a generáltaké 113, és a generátor több kimenetű mintákkal hoz létre elágazásokat.
  - Használhatóság: **idézhető** (a preprint 3. szakasza és a PDF).

- **[Prasad2026]** Prasad & Mahapatra (2026): *SynthPID: P&ID digitization from Topology-Preserving Synthetic Data*. arXiv 2604.16513v1.
  - Forrás: `TL/pid-structural-rules.md`, `TL/real-pid-composition-2026-10.md`, `TL/real-pid-data-sweep-2026-10.md`, `TL/_novelty-log.md`
  - Mit csinál: a 12 OPEN100-lap topológiájából 665 szintetikus P&ID-t állít elő, és ezeken tanítva 63,8 ± 3,1% él-mAP-t ér el OPEN100-on; a teszt- és a magképek átfedése nincs kizárva.
  - Használhatóság: **idézhető** (a 3.1–3.2, az 5. és a 6. szakaszt olvasták).

- **[Lopomo2026]** Lopomo et al. (2026): *Leveraging LLMs and Object Detection for Automated KG Generation from Industrial Schematics*. Big Data Cogn. Comput. 10(7):210, doi 10.3390/bdcc10070210.
  - Forrás: `TL/real-pid-composition-2026-10.md`
  - Mit csinál: 126 valódi és CAD-ből készült P&ID-ből (24 osztály, 5400 szimbólum, átlagosan kb. 43 komponens rajzonként) automatikusan tudásgráfot generál.
  - Használhatóság: **idézhető** (PDF).

- **[daCunha]** da Cunha et al. (év nincs a jegyzetben): *On P&ID Symbol Recognition using Transformers*. SBC ERAMIA/RS.
  - Forrás: `TL/real-pid-composition-2026-10.md`
  - Mit csinál: transzformeres szimbólumfelismerés 40 osztályos szintetikus tanítóadaton, OPEN100-on és két belső lapon tesztelve.
  - Használhatóság: **idézhető** (PDF).

- **[Kim2022]** Kim, Kim, Moon, Lee, Mun (2022): *End-to-end digitization of image format piping and instrumentation diagrams at an industrially applicable level*. J. Comput. Des. Eng. 9(4):1298–1326, doi 10.1093/jcde/qwac056.
  - Forrás: `TL/real-pid-composition-2026-10.md`
  - Mit csinál: 83 képes P&ID-n végez digitalizálást 76 szimbólumcímkével, és közli a szabványos szimbólumkészletek méretét (ISO 10628-2, PIP PIC001, ANSI/ISA-5.1).
  - Használhatóság: **idézhető**, fenntartással: az olvasás összefoglaló eszközön keresztül történt ([V-S]); a számokat két független lekérés megerősíti.

- **[Prusty2025]** Prusty, Agarwal, Iyenger (2025): *Advanced Integration of Discrete Line Segments in Digitized P&ID for Continuous Instrument Connectivity*. arXiv 2505.11976.
  - Forrás: `TL/2505.11976.md`, `TL/00-reading-list.md`, `TL/_novelty-log.md`
  - Mit csinál: a gépi látás által széttöredezve felismert csővonal-darabokat összefűzi, és folytonos kapcsolati gráfot épít egyetlen rajzon belül.
  - Használhatóság: **csak említés** (státusz: „skimmed”, csak az absztrakt alapján).

- **[Bailo2025]** Bailo et al. (2025): transzformeres digitalizálás SNAM-gázüzemeken. arXiv 2511.08609.
  - Forrás: `TL/_novelty-log.md`
  - Mit csinál: kb. 1500 dokumentumon tervezési adatokat, komponenseket és hierarchiát nyer ki, lapközi összekapcsolás és kérdésmegválaszolás nélkül.
  - Használhatóság: **csak említés** (a teljes szöveget csak átfutották).

- **[Yu2019]** Yu, Cha, Lee, Kim, Mun (2019). Energies 12(23):4425.
  - Forrás: `TL/real-pid-composition-2026-10.md`
  - Mit csinál: P&ID-felismerés két teszt-P&ID-n; az osztálylista nem volt elérhető.
  - Használhatóság: **csak említés** (nem olvasták, MDPI 403).

- **[MorenoGarcia2020]** Moreno-García / Elyan: SiED (EANN 2020).
  - Forrás: `TL/real-pid-composition-2026-10.md`
  - Mit csinál: szimbólumadatkészlet 2432 példánnyal.
  - Használhatóság: **csak említés** (csak absztrakt szinten).

- **[Gao2020]** Gao, Zhao, Smidts: atomerőművi P&ID-komponensfelismerés (Prog. Nucl. Energy 2020).
  - Forrás: `TL/real-pid-composition-2026-10.md`
  - Mit csinál: a jegyzet szerint nem sikerült megtalálni.
  - Használhatóság: **NE idézd** („Not located; not read”).

- **[GuptaPIDdataset]** Gupta et al.: „PID_dataset”. Zenodo, records/8028570, CC BY 4.0.
  - Forrás: `TL/real-pid-data-sweep-2026-10.md`
  - Mit csinál: iparból és webes gyűjtésből származó P&ID-képek szimbólumkeretekkel (92 nyers lap).
  - Használhatóság: **csak említés** (a ZIP-listát ellenőrizték, a címkék tartalmát nem).

- **[Oeing2023]** Oeing et al. (2023): *Graph Learning in Machine-Readable Plant Topology Data*. Chem. Ing. Tech. 95, 1049–1060, doi 10.1002/cite.202200223.
  - Forrás: `TL/00-reading-list.md`, `TL/_novelty-log.md`, `TL/ontology-landscape.md`, `TL/real-pid-data-sweep-2026-10.md`
  - Mit csinál: GNN-ek üzemi topológia konzisztenciájának ellenőrzésére (a sorban álló tételek listája szerint).
  - Használhatóság: **NE idézd**. A TL/ontology-landscape „Cannot claim” listája szerint semmit nem szabad belőle állítani, amíg a szöveg nincs meg (Wiley 403).

- **[Oeing2022]** Oeing et al. (2022). Digital Chemical Engineering 4:100038, doi 10.1016/j.dche.2022.100038.
  - Forrás: `TL/pid-structural-rules.md`
  - Mit csinál: RNN a következő berendezés jóslására és GNN konzisztencia-ellenőrzésre DEXPI-adatokon.
  - Használhatóság: **csak említés** (nem olvasták, ScienceDirect 403; nyílt hozzáférésű, tehát beszerezhető).

- **[Khella2026]** Khella et al. (2026), Digital Chemical Engineering (bpmn2dexpi).
  - Forrás: `TL/real-pid-data-sweep-2026-10.md`
  - Mit csinál: BPMN-ből DEXPI 2.0 Process modellt készít, csak a TEP PFD-n.
  - Használhatóság: **csak említés** (a repót ellenőrizték, a cikket nem olvasták).

- **[pyDEXPI]** process-intelligence-research/pyDEXPI, szoftver (AGPL-3.0).
  - Forrás: `TL/ontology-landscape.md`, `TL/pid-structural-rules.md`, `TL/real-pid-composition-2026-10.md`
  - Mit csinál: a DEXPI 1.3 adatmodell Pydantic-osztályai (514 osztály, 105 docstring PCA RDL IRI-vel), Proteus XML betöltő és NetworkX-export.
  - Használhatóság: **idézhető**, szoftverként (a kódot és a README-t közvetlenül olvasták).

- **[pyDEXPI2025]** a pyDEXPI ESCAPE35-cikke, LAPSE:2025.0371 (CC BY-SA 4.0, 6 oldal); szerzők a jegyzetben nincsenek.
  - Forrás: `TL/pid-structural-rules.md`
  - Mit csinál: a pyDEXPI bemutató cikke; a jegyzet szerint semmit nem mond a szintetikus generálásról és a minták eredetéről.
  - Használhatóság: **csak említés** (a teljes szövegben csak célzottan kerestek, összefoglaló nincs).

- **[DEXPITestCases]** DEXPI e.V.: TrainingTestCases / „Public Example PIDs”. `gitlab.com/dexpi/TrainingTestCases`, CC BY 4.0.
  - Forrás: `TL/pid-structural-rules.md`, `TL/real-pid-composition-2026-10.md`, `TL/real-pid-data-sweep-2026-10.md`
  - Mit csinál: egylapos DEXPI/Proteus példa- és tesztfájlok több szállító exportjából (C01 referencia-P&ID); a C08 Covestro „Two connected P&IDs” az egyetlen jogtiszta kétlapos példa, de csak PDF-ben.
  - Használhatóság: **idézhető**, adatforrásként.

## 5. Szabványok, információs modellek, szókészletek

Ide csak olyan szabvány vagy szókészlet került, amelyhez valamelyik jegyzet idézhető forrást ad.
A kiválasztás alapja a feladatban felsorolt kör, kiegészítve azokkal, amelyeket a TL/ontology-landscape.md
ellenőrzött hivatalos forrással ([V]) vizsgált és „mérlegelt, de elvetett” megoldásként kezel.

- **[DEXPI2025]** DEXPI e.V.: DEXPI Specification 2.0 (benne a DEXPI P&ID Specification 1.4), 2025. október. Forrás: `dexpi.org/specifications/`, `gitlab.com/dexpi/Specification`.
  - Forrás: `TL/ontology-landscape.md`, `TN/ontologia-pid.md`
  - Mit csinál: UML információs modell DEXPI XML szerializációval P&ID-khez, OWL/RDF forma nélkül; az osztálydefiníciók az ISO 15926-4 referenciakönyvtárból származnak, és egy DEXPI-modell egyetlen rajz.
  - Használhatóság: **idézhető** (a hivatalos oldalakat és a GitLab-repót ellenőrizték, [V]).

- **[DEXPI2026news]** DEXPI e.V. hír, 2026-03-23: a TotalEnergies a DEXPI szemantikus (BFO- és IDO-igazított) változatán dolgozik. Forrás: dexpi.org.
  - Forrás: `TL/ontology-landscape.md`, `TL/_novelty-log.md`, `TN/ontologia-pid.md`
  - Mit csinál: bejelenti, hogy ipari OWL-DEXPI készül; ezért nem állítható hozzájárulásként, hogy „mi építjük a DEXPI-ontológiát”.
  - Használhatóság: **idézhető** (szó szerint idézve, [V]).

- **[ISO15926]** ISO 15926 (1:2004, 2:2003, ISO/TS 15926-4 Ed. 4, 6:2024; a Wikipédia szerint a 8. és a 12. rész OWL).
  - Forrás: `TL/ontology-landscape.md`, `TN/ontologia-pid.md`; említi még: `PD/valve-spec-ido-2510.01736.md`
  - Mit csinál: a folyamatüzemi életciklus-adatok szabványcsaládja (adatmodell és referenciaadatok); a DEXPI ennek a 4. részét használja referenciakönyvtárként.
  - Használhatóság: **csak említés**. A szabványszöveget senki sem olvasta. A részlistát a PCA Arrowhead-kézikönyv ([V]) és a Wikipédia ([R]) adja; tartalmi állításhoz az [IDO], a [PCARDL] és az [ArrowheadHandbook] idézhető.

- **[IDO]** IDO (Industrial Data Ontology), korábban ISO/TR 15926-14, most ISO 23726-3 (ISO DIS / FDIS 23726-3; „IDO v4.2 (FDIS, April 2026)”). Forrás: `rds.posccaesar.org/ontology/lis14/`.
  - Forrás: `TL/ontology-landscape.md`, `PD/valve-spec-ido-2510.01736.md`, `TN/ontologia-pid.md`
  - Mit csinál: W3C OWL 2 felső ontológia ipari eszköz- és folyamatadatokhoz (`lis:` előtag); a plantdocs ISO 15926-rétege és a Gjerver-féle szelep-ontológia is erre épül.
  - Használhatóság: **idézhető** (a hivatalos PCA-oldalt olvasták, [V]).

- **[PCARDL]** POSC Caesar Association Reference Data Library: a régi `data.posccaesar.org/rdl/RDS…` és az új `rds.posccaesar.org/ontology/plm/rdl/` (equipment modul 0.9.1, CC BY-SA 4.0).
  - Forrás: `TL/ontology-landscape.md`; említi: `PD/valve-spec-ido-2510.01736.md` („RDL/CFIHOS-fogalmak”)
  - Mit csinál: berendezés-, cső- és műszerosztályok referenciakönyvtára; a régi IRI-k Turtle-re oldódnak fel, az új, gépileg olvasható forma hitelesítéshez kötött (HTTP 401), és 198 „(DEXPI symbol)” osztályt tartalmaz.
  - Használhatóság: **idézhető** ([V], content negotiationnel tesztelve).

- **[QUDT]** QUDT (qudt.org), Release 2.1, CC BY 4.0.
  - Forrás: `TL/ontology-landscape.md`
  - Mit csinál: mértékegységek, mennyiségfajták és dimenziók szemantikus specifikációja (berendezést és topológiát nem modellez); az Arrowhead/IDO keretrendszer kötelezővé teszi az egységekhez.
  - Használhatóság: **idézhető** ([V]).

- **[CFIHOS]** IOGP JIP36: CFIHOS (Capital Facilities Information Handover Specification), „Version 2.0”. Forrás: `jip36-cfihos.org/cfihos-standards/`.
  - Forrás: `TL/ontology-landscape.md`; említi: `PD/valve-spec-ido-2510.01736.md`
  - Mit csinál: átadási adatkövetelmények (tag- és berendezésosztály-attribútumok, dokumentum-metaadatok); az RDL csak Excelben és CSV-ben jelenik meg, az IDO-kompatibilis változat még munkacsoporti feladat.
  - Használhatóság: **idézhető**, de **verziódátum nélkül**: a CFIHOS-oldal szerint 2025. november, az Arrowhead-kézikönyv szerint 2024. október, és a jegyzet tiltja a dátum idézését, amíg ez nincs tisztázva.

- **[ISA5.1]** ANSI/ISA-5.1 (műszerszimbólumok és azonosító betűk; a jegyzet szerint ANSI/ISA-5.1-2022, egy 2024-es kiadás nem ellenőrzött).
  - Forrás: `TL/ontology-landscape.md`, `TL/real-pid-composition-2026-10.md`, `TN/ontologia-pid.md`, `TN/pid-szerkezeti-szabalyok.md`
  - Mit csinál: rajzi konvenció a műszerjelekre és a címkebetűkre, nem adatmodell; a TL szerint a generátor műszerváltozatosságát ISA-5.1 címkenyelvtanból kell előállítani.
  - Használhatóság: **csak említés**. Primer forrást senki sem olvasott ([R] ANSI webáruház, [X] ANSI-blog 403); a szimbólumszám (176) a [Kim2022]-ből jön.

- **[ISO10628-1]** ISO 10628-1:2014 (folyamatábrák és P&ID-k), hivatalos előnézet, 1–5.4.3. fejezet.
  - Forrás: `TL/pid-structural-rules.md`, `TN/pid-szerkezeti-szabalyok.md`
  - Mit csinál: rajzi szabályok, például a fő áramlási irány, a tartalék berendezés feltüntetése és a többlapos rajzok vezetékvégeinek kölcsönös hivatkozása.
  - Használhatóság: **idézhető**, de csak az előnézet fejezeteire.

- **[ISO10628-2]** ISO 10628-2 (grafikus szimbólumok).
  - Forrás: `TL/real-pid-composition-2026-10.md`, `TL/2411.13929.md`, `TL/ontology-landscape.md`
  - Mit csinál: 198 berendezés-, 60 cső- és 52 műszerszimbólum, a [Kim2022] összesítése szerint.
  - Használhatóság: **csak említés** (csak másodlagos forrásból).

- **[PIPPIC001]** PIP PIC001 (Process Industry Practices, P&ID dokumentációs kritériumok).
  - Forrás: `TL/pid-structural-rules.md`, `TL/real-pid-composition-2026-10.md`, `TN/pid-szerkezeti-szabalyok.md`
  - Mit csinál: az amerikai iparági P&ID-gyakorlat; a jegyzet szerint valószínűleg ez lenne a legjobb egyetlen forrás.
  - Használhatóság: **csak említés**. Nem olvasták: a hivatalos előnézet 403-at adott, az online teljes példányok jogosulatlanok, és a jegyzet szerint a dolgozat nem hivatkozhat rájuk. Könyvtárból kell beszerezni.

- **[ArrowheadHandbook]** POSC Caesar Association: Arrowhead fPVN Handbook és Use Cases (`docs.posccaesar.org/libraries-and-standards/arrowhead-handbook/`).
  - Forrás: `TL/ontology-landscape.md`, `TL/_novelty-log.md`
  - Mit csinál: igazítja a DEXPI életciklus-zónáit és tulajdonságmodelljét az IDO-hoz, de csak egy kézzel írt, egyszivattyús példán; a „connector” szó nem szerepel benne.
  - Használhatóság: **idézhető** (a DEXPI-igazítás szakaszát teljesen elolvasták, [V]).

- **[IMF]** Information Modelling Framework (READI JIP / TechnipFMC; ISO/IEC 81346-alapú, RDF/OWL/SHACL).
  - Forrás: `TL/ontology-landscape.md`
  - Mit csinál: `partOf`, `connectedTo` és `fulfills` relációk; a jegyzet szerint ez a legközelebbi topológiai reláció egy OWL-alapú ipari keretrendszerben.
  - Használhatóság: **csak említés** (csak az Arrowhead-kézikönyvön keresztül, a primer IMF-kézikönyvet nem olvasták).

- **[OPC30250]** OPC Foundation: OPC UA for DEXPI (OPC 30250 v1.0).
  - Forrás: `TL/ontology-landscape.md`
  - Mit csinál: a DEXPI-t OPC UA címtérre képezi le (kb. 179 ObjectType), a többszörös öröklődést pedig egy külön táblával oldja fel.
  - Használhatóság: **idézhető** ([V]).

- **[OntoCAPE]** RWTH Aachen AVT: OntoCAPE 2.0 (62 OWL-fájl, GPL).
  - Forrás: `TL/ontology-landscape.md`, `TN/ontologia-pid.md`
  - Mit csinál: vegyipari folyamattervezési ontológia; a jegyzet szerint 2009 óta szunnyad, ezért mérlegelt, de elvetett szókészletként kell idézni.
  - Használhatóság: **idézhető** (a hivatalos oldalt olvasták, [V]).

- **[SOSASSN2017]** W3C: SOSA/SSN, W3C Recommendation, 2017. október 19.
  - Forrás: `TL/ontology-landscape.md`
  - Mit csinál: szenzor-, megfigyelés- és aktuátorminta, amely nem modellez berendezést, csőtopológiát és szabályozási hurkot (elvetve).
  - Használhatóság: **idézhető** ([V]).

- **[IOF]** Industrial Ontologies Foundry: IOF, release 202603 (BFO-alapú, MIT).
  - Forrás: `TL/ontology-landscape.md`
  - Mit csinál: gyártási ontológia 999 osztállyal, folyamatüzemi vagy P&ID-modul nélkül (elvetve).
  - Használhatóság: **idézhető** ([V]).

- **[SchemaOrg]** schema.org, V30.0 (2026-03-19).
  - Forrás: `TL/ontology-landscape.md`
  - Mit csinál: webes strukturált adatokra szolgáló szókészlet szivattyú-, szelep- és csőtípus nélkül (`schema.org/Pump` → 404), mert a P&ID nem tartozik a hatókörébe.
  - Használhatóság: **idézhető** ([V]).

- **[IDTA02012]** IDTA 02012-1-0: „Information Model for P&I Diagrams based on DEXPI Standard” (AAS submodel).
  - Forrás: `TL/ontology-landscape.md`, `TL/_novelty-log.md`
  - Mit csinál: a DEXPI-re épülő AAS-almodell; egy keresési kivonat szerint hiánynak tartja több DEXPI-fájl összefogását.
  - Használhatóság: **csak említés** (csak PDF-ben érhető el, nem nyitották meg, [X]).

- **[IEC62424]** IEC 62424 (CAEX).
  - Forrás: `TL/ontology-landscape.md`
  - Mit csinál: adatátviteli nyelv PCE-kérések cseréjéhez P&ID- és PCE-CAE-eszközök között; az AutomationML ebből származik.
  - Használhatóság: **csak említés** ([R], csak szabványkatalógus-oldalakból).

- **[IECCDD]** IEC 61987 / IEC Common Data Dictionary (cdd.iec.ch).
  - Forrás: `TL/ontology-landscape.md`
  - Mit csinál: tulajdonságszótárak folyamatmérő eszközökhöz, online adatbázis-szabványként.
  - Használhatóság: **csak említés** (csak a Wikipédián keresztül).

- **[Westermann2025]** Westermann, Ramonat, Hujer, Gehlhoff, Fay (2025): *Automatic Mapping of AutomationML Files to Ontologies for Graph Queries and Validation*. arXiv 2504.21694.
  - Forrás: `TL/ontology-landscape.md`, `TL/_novelty-log.md`
  - Mit csinál: AutomationML-ből OWL-t készít SPARQL-lekérdezéshez és SHACL-validációhoz; a jegyzet szerint ez a legközelebbi deklaratív validációs előzmény.
  - Használhatóság: **csak említés** (csak az absztrakt-oldal; „I did not read the full text”).

## 6. Gyakorlati P&ID-szabályforrások

- **[Toghraei2019]** M. Toghraei (2019): *Piping and Instrumentation Diagram Development*. Wiley/AIChE (2. kiadás: ISBN 9781394368587).
  - Forrás: `TL/pid-structural-rules.md`, `TN/pid-szerkezeti-szabalyok.md`
  - Mit csinál: P&ID-fejlesztési kézikönyv; a szerző szavaival az „ökölszabályok könyve”, amely leírja a P&ID szerepét, kiadási mérföldköveit és lapkonvencióit.
  - Használhatóság: **idézhető**, de csak az olvasott részekre (előszó, 1–2. fejezet, 3.1–3.4); a szabályokat tartalmazó 4–19. fejezetet nem olvasták.

- **[Christensen2020]** B. A. Christensen (2020): *Preparation of Process Flow Diagrams and Piping and Instrumentation Diagrams*, HNF-64103 Rev. 0. Mission Support Alliance, US DOE (Hanford).
  - Forrás: `TL/pid-structural-rules.md`, `TL/real-pid-data-sweep-2026-10.md`, `TN/pid-szerkezeti-szabalyok.md`
  - Mit csinál: telephelyi PFD/P&ID-készítési eljárás, amely saját szavaival „a kivételektől eltekintve” egyezik a PIP gyakorlatával; a jegyzet szerint ez a legkonkrétabb nyilvános, jogtiszta szabálygyűjtemény.
  - Használhatóság: **idézhető** (teljes szöveg).

- **[KLM2011]** KLM Technology Group (2011): *Piping and Instrumentation Diagrams (P&ID) (Project Standards and Specifications)*, Rev 01.
  - Forrás: `TL/pid-structural-rules.md`, `TN/pid-szerkezeti-szabalyok.md`
  - Mit csinál: oktatócégi projektszabvány olaj-, gáz- és petrolkémiai P&ID-khez (például a tartalék berendezés „Spare” jelölése).
  - Használhatóság: **idézhető**, de csak az ingyenes 1–23. oldalra (a 146-ból).

- **[FBD2019]** Ford, Bacon & Davis LLC (2019): „Art of the P&ID”. AIChE, 94 diás előadás.
  - Forrás: `TL/real-pid-composition-2026-10.md`
  - Mit csinál: oktatási előadás az „ISA typical” betűkészlettel és lapelrendezési javaslatokkal (egy oszlop P&ID-nként, a szivattyúk a szívóoldali tartályukkal együtt).
  - Használhatóság: **idézhető** (olvasták; diasor, nem szabvány).

- **[AIChE2010a]** AIChE ChEnected (2010): „P&ID Part 3 – Symbology Primer”.
  - Forrás: `TL/pid-structural-rules.md`
  - Mit csinál: gyakorló mérnöki blogsorozat a P&ID-jelölésekről (például hogy a címkebetűk és a hurokszám együtt egyediek).
  - Használhatóság: **idézhető**, de másodlagos forrásként (teljes HTML; a jegyzet SEC-nek minősíti).

- **[AIChE2010b]** AIChE ChEnected (2010): „P&ID Part 4: Codes, Tags and Labels”.
  - Forrás: `TN/pid-lapkozi-csatlakozok.md`, `TL/pid-structural-rules.md`
  - Mit csinál: a vezetékszám-mezők konvenciója (névleges átmérő, közegkód, sorszám, csőosztály, szigetelés).
  - Használhatóság: **idézhető**, de másodlagos forrásként (egy korábbi ülésen olvasták; 2026-09-12-én 403-at adott).

## 7. Egyéb, a novelty logban említett munkák (Jev, routing, ipar)

- **[Deusser2026]** Deußer, Sparrenberg, Sifa (2026): *Evaluating and Benchmarking the System One Model Jev*. arXiv 2609.37647. Forrás: `TL/_novelty-log.md`. Mit csinál: zero-shot benchmark 37 adatkészleten. Használhatóság: **csak említés** (absztrakt).
- **[Tang2026]** Tang, Zheng (2026): *Typed Decision Models: An Early Evidence Audit and Evaluation Checklist*. arXiv 2609.32160. Forrás: `TL/_novelty-log.md`. Mit csinál: 28 cikket auditál; a típusos kimenet nem ad önálló pontosságelőnyt, csak késleltetésben és költségben nyer, és egy 14 pontos ellenőrzőlistát javasol. Használhatóság: **csak említés** (az olvasottság nincs rögzítve).
- **[Arxiv2610.00346]**, **[Arxiv2609.33401]**, **[Arxiv2609.28940]**: System One modellek döntési kapukhoz, ágensbiztonsághoz és pentest-keretekhez. Forrás: `TL/_novelty-log.md`. Mit csinál: a jegyzet csak a témájukat adja meg. Használhatóság: **csak említés** („titles/snippets only, not read”). (Három külön tétel.)
- **[Sarkar2026]** P. Sarkar (2026): „GraphRAG with TypeSafe Jev”, TDS-oktatóanyag. Forrás: `TL/_novelty-log.md`. Mit csinál: Jev-et javasol entitásfeloldásra és részgráf-metszésre általános GraphRAG-ban, mérés nélkül. Használhatóság: **idézhető**, de csak blogként (olvasták).
- **[Southbridge2026]** Southbridge blog: „Jev entity resolution”. Forrás: `TL/_novelty-log.md`. Mit csinál: Jev entitásillesztésre kampányfinanszírozási rekordokon. Használhatóság: **csak említés** (nem olvasták).
- **[SemGraphUnif2026]** *Semantic Graph Unification for Industrial Digital Threads*. arXiv 2608.24918. Forrás: `TL/_novelty-log.md`. Mit csinál: ontológiavezérelt integráció 11 gyártási IT-rendszer között. Használhatóság: **csak említés**.
- **[ChemRxiv10001546]** ChemRxiv, doi 10.26434/chemrxiv.10001546. Forrás: `TL/_novelty-log.md`. Mit csinál: anyagtudományi irodalom, átfedés nélkül. Használhatóság: **csak említés**.

---

## Javasolt idézések fejezetenként

Csak **idézhető** kulcsok szerepelnek idézésre javasolva. A *csak említés* tételeket legfeljebb
„létezik ilyen munka” formában érdemes megemlíteni, a **NE idézd** tételeket egyáltalán nem.

### Bevezetés

- A probléma, vagyis hogy a P&ID-QA egylapos, és a ContextRAG nem skálázódik: [Alimin2026] (ennek
  a 6.2. szakaszát szó szerint idézni), [Alimin2025].
- Kis kiértékelések a területen, nagyobb kérdéskészletekkel szemben: [Alimin2026], [Gadekar2026];
  a [Gupta2025] csak a teljes szöveg beszerzése után.
- A rajz mellett az adatlapok is számítanak (attribútumok és feltételek): [Knollmeyer2025]; a
  [Gjerver2025] csak említésként.
- A P&ID mint az üzem központi dokumentuma: [Toghraei2019], [Christensen2020].

### Kapcsolódó munkák

**P&ID-QA és P&ID-gráfok**
- Idézhető: [Alimin2026], [Alimin2025], [Gadekar2026], [SchulzeBalhorn2025], [Sturmer2024],
  [PID2Graph2025], [Lopomo2026], [Hirtreiter2022], [PidGraphAgent2026] (szoftver),
  [Kochanski2026] (kereskedelmi).
- Csak említés: [Gupta2025] (beszerzendő, de a TL szerint kötelező), [Zhu2026a], [Ma2026],
  [Mankodiya2026], [Sakhinana2024], [Mandarapu2026].
- Digitalizálás röviden: [Sturmer2024], [Paliwal2021], [Rahul2019], [Mani2020], [Kim2022],
  [Prasad2026], [daCunha].

**GraphRAG és visszakeresési stratégiák**
- Méretfüggő stratégiaválasztás: [Xiang2025], [Alimin2026], [Fan2026].
- Gráfeszközös ágensek (a primitíveket hívó ágens előzményei): [KBQAAgent2024], [KGAgent2024],
  [GraphCoT2024], [Gadekar2026]; eszközként [MCPNeo4j].
- n-áris tények és hipergráfok: [HyperGraphRAG2025], [HyperRAG2026], [StarE2020]. A PD szerint
  így kell bemutatni: „a reprezentáció elvben megoldott, a szerkezetben kódolt feltételek kinyerése nem”.
- Csak említés: [Li2024] (Self-Route), [GraphScout2026] (ellenvélemény a fix eszközkészlettel
  szemben), [MSGraphRAG], [LightRAG], [HippoRAG2], [Liu2023].

**Dokumentum-QA (adatlapok, műszaki dokumentumok)**
- Idézhető: [Knollmeyer2025], [GoldenRetriever2024], [Kumar2026] (a „megtalálja, de pontatlanul
  írja le” hibamód).
- Csak említés: [StructRAG2025].
- Kerülendő: [HierMARL2025] (NE idézd, amíg nincs azonosítva), [Enginuity2026b] (NE idézd, ez egy
  másik mű).

**Ontológiák és szókészletek**
- Idézhető: [DEXPI2025], [DEXPI2026news], [IDO], [PCARDL], [QUDT], [CFIHOS] (dátum nélkül),
  [ArrowheadHandbook], [OPC30250]; elvetett alternatívaként [OntoCAPE], [SOSASSN2017], [IOF],
  [SchemaOrg]; szoftver: [pyDEXPI].
- Csak említés: [ISO15926] (az [IDO] és a [PCARDL] mellett), [ISA5.1], [Gjerver2025] (a
  legközelebbi ISO 15926/IDO és adatlap előzmény; idézés előtt el kell olvasni),
  [Westermann2025], [IMF], [IDTA02012].

### Módszer

- Adatlap-réteg (ISO 15926 / IDO, PCA RDL, CFIHOS, QUDT): [IDO], [PCARDL], [CFIHOS], [QUDT],
  [DEXPI2025].
- Rajzréteg, DEXPI → gráf: [pyDEXPI], [Alimin2026] (pyDEXPI → LPG leképezés, sűrítés), [Alimin2025].
- Baseline (M3: ContextRAG-szerializálás és vektoros darabok): [Alimin2026].
- Gráfeszközös ágens és Cypher-lépcső: [Gadekar2026], [KBQAAgent2024], [MCPNeo4j].
- Szintetikus üzem és rajzszabályok: [ISO10628-1], [Christensen2020], [Toghraei2019], [KLM2011],
  [Hirtreiter2022], [DEXPITestCases], [FBD2019], [AIChE2010a], [AIChE2010b].
- Lapközi csatlakozók, valódi minta: [OPEN100], [PID2Graph2025], [Mani2020].

### Kiértékelés

- LLM-bíráló rubrika (négy szempont) és kérdéskategóriák: [Alimin2026].
- Keresztbírálat, büntetett metrikák, a megtalálás és a hű leírás külön mérése: [Kumar2026].
- Programmal előállított gold, felső korlát gold lekérdezéssel (gold-query ceiling), klaszteres
  bootstrap, többségi és véletlen alsó korlát, kitalált igaz válaszok aránya: [Gadekar2026].
- Méretfüggő összehasonlítás: [Xiang2025].
- Hibamodell (digitalizálási élhiba, 75,46% él-mAP): [Sturmer2024].
- Valódi validációs halmaz: [OPEN100], [PID2Graph2025].
- Csak említés, beszerzés után: [Gupta2025] (sablonos kérdések végrehajtható gold lekérdezéssel).

---

## Összesítés

| | Tételek | ebből idézhető | csak említés | NE idézd |
|---|---|---|---|---|
| plantdocs (`PD/`) | 25 | 12 | 12 | 1 |
| Thesis (`TL/`, `TN/`) | 117 | 46 | 68 | 3 |
| Összesen (egyedi) | 132 | 51 | 77 | 4 |

A két repó közös tételei (10): [Alimin2026], [Alimin2025], [Gupta2025], [Sturmer2024], [Kumar2026],
[Wikidata], [ISO15926], [IDO], [PCARDL], [CFIHOS].

Ha egy tételt mindkét repó említ, a jelölése a jobban dokumentált jegyzetet követi. Így az [Alimin2025]
és a [Sturmer2024] idézhető, bár a PD csak felsorolja őket. Ugyanez az oka annak, hogy a plantdocs
oszlop 12 idézhető tétele között a TL alapján idézhetők is szerepelnek. Ha csak a plantdocs saját
jegyzeteit nézzük, 7 tétel idézhető: [Alimin2026], [HyperGraphRAG2025], [HyperRAG2026],
[GoldenRetriever2024], [Knollmeyer2025], [Kumar2026], [StarE2020].

**Szándékosan kimaradt** (a jegyzetekben szerepel, de nem irodalmi mű, vagy kívül esik a megadott körön):

- Wikipédia-cikkek (P&ID, KKS, IEC 81346, ISO 15926), a zeroinstrument.com blog és az Autodesk
  támogatási oldalak: a jegyzetek is másodlagosnak tartják őket, a dolgozatban nem idézendők.
- Kereskedelmi termékek (SymphonyAI, Acuvate DiagramIQ, Cognite): a novelty log szerint
  „not citable as method”.
- A `TL/real-pid-samples-2026-10.md` rajzmintái (Hanford WTP/HWVP, önkormányzati tendercsomagok,
  E. Chen 2007-es disszertációja, CSB, Wikimedia): elsődleges rajzadatok, nem irodalom.
- Az eszközrepók (`TUDoAD/DEXPI2graphML`, `dexpi-viewer`, `equinor/Dexpi2Imf` és társaik) és a
  más cikkeken belüli másodlagos hivatkozások (Pan 2009, Barrasa & Webber 2023, Cordella et al. 2004).
- `Thesis/docs/Technology_research/2026-10-10-faster-openrouter-models.md`: modellár- és
  szolgáltatói források (OpenRouter, Artificial Analysis), nem irodalom.
- A plantdocs repóban, de nem a `10-literature/` alatt említve, ezért itt nem szerepel: Kong és
  társai, Future Internet 2026, 18(8):442, doi 10.3390/fi18080442
  (`plantdocs/docs/private/50-progress/2026-W38.md`), és a POSC Caesar Datasheet Ontology 0.1
  (`plantdocs/docs/private/40-design/0006-rdf-modell.md`). Mindkettő fontos az adatlap-réteghez,
  ezért érdemes irodalmi jegyzetet írni róluk, mielőtt bekerülnek a dolgozatba.
