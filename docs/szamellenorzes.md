# Számellenőrzés (a dolgozat minden száma és a forrása)

Készült: 2026-10-31, független ellenőrzés, a dolgozat fájljait nem módosítottam. Ellenőrzött fájlok:
`dolgozat/src/01-bevezetes.md`, `02-hatter.md`, `03-adatok.md`, `04-tudasgraf.md`, `05-modszerek.md`,
`06-kiertekeles.md`, `06-z-demo.md`, `07-osszefoglalas.md`, `09-fuggelek.md`, `kivonat.md`, `abstract.md`.

Források, amelyekkel összevetettem: `docs/eredmenyek.md` (EXP-sorok); `runs/<EXP>/summary.csv`, `pairs.csv`,
`routes.csv`, `scored.jsonl`; `data/plant/load_report.json`, `tags.json`, `tag_to_datasheet.json`,
`seed_search.json`; `data/questions/dev.jsonl`, `test.jsonl`, `complex.jsonl` (darabszám családonként és
sha256 újraszámolva: egyezik az EXP-004 / EXP-009 értékével); `figures/*.csv`, `figures/demo/screens.csv`,
`data/app/ask-log.jsonl` (az EXP-040 teljes válaszszövegei); a kód (`src/plantqa/...`, a plantdocs és a
plantgraph megfelelő fájljai); a plantdocs `docs/private/30-experiments/_results.md` és tervezési
jegyzetei; a plantgraph `README.md`, `data/runs/exp0007/inputs/params_*.json` és ADR-0034; a
`docs/irodalom.md`.

Mentes: évszámok, szabvány- és típusazonosítók (ISO 15926, ISO 10628, DEXPI 2.0, 3051, F51/F52 stb.),
EXP-, ADR- és tervezési jegyzet-azonosítók, tagnevek, URI-k és PCA-azonosítók, a fejezetek saját számozása
(ezt csak a kereszthivatkozásoknál néztem meg).

Kerekítési szabály: egy kerekített érték akkor OK, ha a forrásérték helyes kerekítése (pl. 0,181079/40 =
0,0045270 → 0,00453).

## Ellenőrzési tábla

| fájl:sor | szám (kontextussal) | forrás | státusz | megjegyzés |
|---|---|---|---|---|
| 01-bevezetes.md:3 | „Egy ipari üzemet **több ezer oldalnyi** … dokumentum ír le” | – | NINCS FORRÁS | Sem eredmenyek.md, sem a két repó, sem irodalmi jegyzet nem ad ilyen számot. A plantgraph README-je csak annyit mond: „A real plant needs hundreds of sheets”. |
| 01-bevezetes.md:36 | „seedelt, **négylapos** P&ID” | EXP-002 (4 lap) | OK | |
| 01-bevezetes.md:36 | „**26** tagelt elemmel” | EXP-002; `tags.json` (26 sor) | OK | |
| 01-bevezetes.md:38 | „**hét** eszköz adatlapgráfja” | EXP-005; `load_report.json` (7 dokumentum) | OK | |
| 01-bevezetes.md:40 | „**Három** kérdés-válaszoló módszer” | EXP-010…EXP-030 (M1, M2, M3) | OK | |
| 01-bevezetes.md:43 | „Egy **60** kérdéses, **négy** családra bontott kérdéssor” | EXP-004; `dev.jsonl` 20 + `test.jsonl` 40, családok a–d | OK | |
| 01-bevezetes.md:44 | „**két** modellel” | EXP-020 (glm, luna) | OK | |
| 01-bevezetes.md:61–64 | fejezetszámok: 2. háttér … 7. demó, 8. következtetések | `dolgozat/build/build.js` (a `NN-*.md` fájlok rendezve, az irodalom és a függelék számozatlan) | OK | 06-z-demo a 7., 07-osszefoglalas a 8. fejezet. |
| kivonat.md:3 | „**négylapos** példaüzem” | EXP-002 | OK | |
| kivonat.md:3 | „mind a **24** tagelt fizikai eleméhez” | `tags.json`: 26 tag, ebből 2 szabályozófunkció (FIC-2-2, PIC-2-1) adatlap nélkül; EXP-005: 24 `DESCRIBED_BY` él | OK | |
| kivonat.md:3 | „**hét** eszköz adatlapgráfja” | EXP-005 | OK | |
| kivonat.md:3 | „**Három** módszert” | EXP-020 | OK | |
| kivonat.md:3 | „**60** kérdést … **négy** családban” | EXP-004 | OK | |
| kivonat.md:3 | „a **40** kérdéses teszthalmazt” | EXP-004, EXP-020 | OK | |
| kivonat.md:5 | „router … GLM-5.3 Flash (**31** helyes válasz a **40**-ből)” | EXP-020 summary.csv: M2 glm 31/6/3/0 | OK | |
| kivonat.md:5 | „a gráf nélküli baseline **30**” | EXP-020: M3 glm 30 | OK | |
| kivonat.md:5 | „az M1 **25** helyes” | EXP-020: M1 glm 25 | OK | |
| kivonat.md:5 | „GPT-6 Lunával … különbség nem volt szignifikáns” | EXP-020 pairs.csv: mindhárom Luna-CI tartalmazza a 0-t | OK | |
| kivonat.md:5 | „Egyik módszer sem hallucinált” | EXP-020: hallucinált = 0 mind a 6 párosításon | OK | |
| kivonat.md:5 | „a megválaszolhatatlan kérdéseket **mindegyik** felismerte” | EXP-020 summary.csv, (d) család: GLM 10/10 mindhárom módszer; Luna M1 9/10 (1 részben), M2 9/10 (1 rossz), M3 9/10 (1 rossz) | ELTÉRÉS | Lunával mindhárom módszer elrontott egyet-egyet (scored.jsonl: M1-luna d08 részben, M2-luna d11 rossz, M3-luna d06 rossz). |
| kivonat.md:5 | „**12** több adatlapot összevető kérdésen … csak a router (GLM-mel **3**-at)” | EXP-009 (12 kérdés); EXP-030: M2 glm 3, M2 luna 1, a többi 0 | OK | |
| kivonat.md:5 | „az M1 volt a legdrágább, az M3 a legolcsóbb” (kérdésenként) | EXP-020 cost_usd: GLM 0,1811 / 0,0935 / 0,0116; Luna 0,2155 / 0,0854 / 0,0729 | OK | Mindkét modellnél igaz. |
| abstract.md:3 | „seeded **four**-sheet example plant” | EXP-002 | OK | |
| abstract.md:3 | „every one of the **24** tagged physical items” | `tags.json`, EXP-005 | OK | |
| abstract.md:3 | „datasheet graphs of **seven** devices” | EXP-005 | OK | |
| abstract.md:3 | „**three** methods” | EXP-020 | OK | |
| abstract.md:3 | „**60** questions in **four** families” | EXP-004 | OK | |
| abstract.md:3 | „a **40**-question test set” | EXP-004 | OK | |
| abstract.md:5 | „GLM-5.3 Flash was best (**31** of **40** correct)” | EXP-020 | OK | |
| abstract.md:5 | „baseline answered **30** and … M1 **25**” | EXP-020 | OK | |
| abstract.md:5 | „with GPT-6 Luna the differences were not significant” | EXP-020 pairs.csv | OK | |
| abstract.md:5 | „No method hallucinated” | EXP-020 | OK | |
| abstract.md:5 | „**all** of them recognised the unanswerable questions” | EXP-020 (d): GLM 10/10, Luna 9/10 mindhárom módszer | ELTÉRÉS | Lásd kivonat.md:5. |
| abstract.md:5 | „supplementary set of **12** questions … (**3** with GLM)” | EXP-009, EXP-030 | OK | |
| abstract.md:5 | „M1 … most expensive per question and M3 the cheapest” | EXP-020 | OK | |
| 02-hatter.md:21–22 | „a `P-1-3` az **1.** egység **harmadik** szivattyúja, az `FT-2-2` a **2.** egység **második** szabályozókörének áramlástávadója” | `tags.json` (P-1-1…P-1-5; FT-2-2 / FIC-2-2 / FV-2-2 egy kör) | OK | A tagkonvenció szemléltetése. |
| 02-hatter.md:40–41 | „az ISO 15926 **4.** részének referenciakönyvtárából” | irodalom.md [DEXPI2025] („ISO 15926-4”) | OK | |
| 02-hatter.md:61–62 | „Egy adatlap tipikusan **több tíz oldalas** PDF” | – | NINCS FORRÁS | Forrás nincs rá, és a saját mérés mást mutat: EXP-007 szerint a 7 adatlapból 5 legfeljebb 16 oldalas (2, 6, 6, 12, 16), csak kettő hosszabb (36, 114). |
| 02-hatter.md:63 | „a példaüzem adatlapjai **2** és **114** oldal közöttiek” | EXP-007 | OK | |
| 02-hatter.md:69–71 | „a **31** feltételes kérdésből az A1 **21**-re, az A2 **28**-ra” | plantdocs _results.md, EXP-0041 („conditional 21 vs 28/31”) | OK | |
| 02-hatter.md:70–71 | „a **17** több feltételt kombináló kérdésből **7**-re, illetve **15**-re” | plantdocs _results.md, EXP-0041 („multi_condition 7 vs 15/17”) | OK | |
| 02-hatter.md:78 | „korábban ISO/TR 15926-14 volt, ma ISO 23726-3” | irodalom.md [IDO] | OK | Azonosító, a jegyzettel egyezik. |
| 02-hatter.md:120 | „**négy** visszakeresési eszköz” (ChatP&ID) | irodalom.md [Alimin2026] | OK | |
| 02-hatter.md:126 | „Egyetlen lapon, **19** kérdésen a ContextRAG” | irodalom.md [Alimin2026] | OK | |
| 02-hatter.md:128–129 | „egy folyamatábrán, **három** kérdésen” | irodalom.md [Alimin2025] | OK | |
| 02-hatter.md:133 | „csak **hét**, tényt visszaadó gráfoperátoron” | irodalom.md [Gadekar2026] | OK | |
| 02-hatter.md:135 | „LangGraph-ágens **hét** általános gráfeszközzel … kérdésenként **egy** fájlon” | irodalom.md [PidGraphAgent2026] | OK | |
| 02-hatter.md:149 | „az OPEN100 sorozat **12** lapja” | irodalom.md [OPEN100], [PID2Graph2025] | OK | |
| 02-hatter.md:157 | „a lezárt teszten (**460** kérdés …)” | plantgraph README („n = 460”) | OK | |
| 02-hatter.md:158 | „**100** lapos üzemen **0,937**, **1000** lapos üzemen **0,917**” | plantgraph README | OK | |
| 02-hatter.md:158–159 | „ContextRAG … **1**-ről **30** lapra **0,824**-ről **0,658**-ra … kaszkádé **0,941**-ről **0,947**-re” | plantgraph README | OK | |
| 02-hatter.md:160 | „relatív költsége … **1,8**-szorosról **41,5**-szeresre” | plantgraph README („×1.8 → ×41.5”) | OK | |
| 02-hatter.md:161 | „körülbelül **143** lap fölött” | plantgraph README („≈143 sheets”) | OK | |
| 02-hatter.md:180–181 | „EXP-0041, a Rosemount 3051 adatlap **200** befagyasztott kérdésén … az A1 **141**, az A2 **172**” | plantdocs _results.md, EXP-0041 (141/34/24/1, 172/21/6/1) | OK | |
| 02-hatter.md:203–204 | „A KBQA-Agent **hét** tudásbázis-eszközt ad” | irodalom.md [KBQAAgent2024] | OK | A felsorolt hét eszköz is egyezik. |
| 02-hatter.md:207 | Neo4j MCP: sémalekérdező, olvasó és író (**három**) Cypher-eszköz | irodalom.md [MCPNeo4j] | OK | |
| 02-hatter.md:210 | „**hat** általános, egymással komponálható üzemi primitívet” | plantgraph README („six plant primitives”), ADR-0034 | OK | |
| 02-hatter.md:231 | táblázat, ChatP&ID: „**19** kérdés”, „egy lap” | [Alimin2026] | OK | |
| 02-hatter.md:232 | táblázat, Talking like P&IDs: „**3** kérdés, egy folyamatábra” | [Alimin2025] | OK | |
| 02-hatter.md:233 | táblázat, Gadekar: „**7** operátor”, „**3000** kérdés” | [Gadekar2026] | OK | |
| 02-hatter.md:234 | táblázat, pid-graph-agent: „**15 + 37** saját kérdés” | [PidGraphAgent2026] | OK | |
| 02-hatter.md:236 | táblázat, Lopomo: „**126** rajz” | [Lopomo2026] | OK | |
| 02-hatter.md:238 | táblázat, Enginuity: „**6940** oldal” | [Kumar2026] | OK | |
| 02-hatter.md:239 | táblázat, plantgraph: „kb. **100** és **1000** lap”, „**460** kérdés” | plantgraph README | OK | |
| 02-hatter.md:240 | táblázat, plantdocs: „**200** kérdés” | plantdocs EXP-0039 / EXP-0041 | OK | |
| 02-hatter.md:241 | táblázat, jelen munka: „**4** lap”, „**7** adatlap”, „**20** dev + **40** teszt”, „**12** (e) kérdés” | EXP-002, EXP-005, EXP-004, EXP-009 | OK | |
| 03-adatok.md:4 | „a **60** kérdésből álló kérdéssort” | EXP-004 | OK | |
| 03-adatok.md:15 | „Az **1**-es seedtől indulva” | EXP-002; `seed_search.json` (1–5 elvetve) | OK | |
| 03-adatok.md:16–17 | „a tagelt elemek száma **20** és **40** közé, a lapoké **2** és **4** közé” | `src/plantqa/plant/spec.py` (MIN/MAX_TAGGED = 20, 40; MIN/MAX_SHEETS = 2, 4) | OK | |
| 03-adatok.md:17 | „minden adatlaptípus szerepel” (7 típus) | `src/plantqa/plant/search.py` (`< 7` feltétel) | OK | |
| 03-adatok.md:18 | „a **6**-os seed lett” | EXP-002; `seed_search.json` | OK | |
| 03-adatok.md:18 | „**26** tagelt elem, **4** lap, **4** lapközi csatlakozópár, **36** csúcs és **116** kapcsolat” | EXP-002 (és EXP-005: 36 / 116) | OK | |
| 03-adatok.md:33 | táblázatcím: „(EXP-002, EXP-006)” – a táblázat „Oldal” oszlopa | az oldalszámok forrása EXP-007 | ELTÉRÉS | A számok helyesek (lásd lent), de a cím nem azt a mérést nevezi meg, amelyből az oldalszámok jönnek. |
| 03-adatok.md:36 | CentrifugalPump: „P-1-1 … P-2-3 (**8** db)”, **6** oldal | `tag_to_datasheet.json` (8 P-tag); EXP-007 (Gorman-Rupp 6) | OK | |
| 03-adatok.md:37 | HeatExchanger: **4** tag, **2** oldal | `tag_to_datasheet.json`; EXP-007 (Alfa Laval M3 2) | OK | |
| 03-adatok.md:38 | GlobeValve (körben): **2** tag, **36** oldal | `tag_to_datasheet.json`; EXP-007 (Fisher ET 36) | OK | |
| 03-adatok.md:39 | GlobeValve (kör nélkül): **3** tag, **6** oldal | `tag_to_datasheet.json`; EXP-007 (GF 165 6) | OK | |
| 03-adatok.md:40 | BallValve: **1** tag, **12** oldal | `tag_to_datasheet.json`; EXP-007 (Worcester 12) | OK | |
| 03-adatok.md:41 | CheckValve: „CHV-1-1 … CHV-2-2 (**4** db)”, **16** oldal | `tag_to_datasheet.json`; EXP-007 (Swagelok 16) | OK | |
| 03-adatok.md:42 | ProcessSignalGeneratingFunction: **2** tag, **114** oldal | `tag_to_datasheet.json`; EXP-007 (Rosemount 114) | OK | A hét sor összesen 24 tag = a `DESCRIBED_BY` élek száma. |
| 03-adatok.md:44 | „a plantdocs **tíz** lépéses folyamata” | plantdocs 40-design/0007 (01–10. lépés) | OK | |
| 03-adatok.md:46 | „A korábban feldolgozott **négy** eszköz közül …” (Fisher, GF 165, Gorman-Rupp, Rosemount) | plantdocs _results.md EXP-0030 (GF, Gorman-Rupp, Fisher Opus-gráfja), EXP-0038 (Rosemount); EXP-001 (3 új adatlap) | OK | |
| 03-adatok.md:48 | „a **három** új adatlapot” | EXP-001 | OK | |
| 03-adatok.md:50 | Rosemount Opus-gráf: „**91 202** tripletből és **3538**, az eszközről szóló tényből” | EXP-006 | OK | |
| 03-adatok.md:51–52 | „plantdocs EXP-0038 … (**20 973** triplet, **626** tény)” | plantdocs _results.md EXP-0038 („Graph triples 20973, device facts 626”); EXP-006 is idézi | OK | |
| 03-adatok.md:52–53 | „**1102**, **16 281** és **66 747** tripletes (Alfa Laval M3, Worcester, Swagelok)” | EXP-006 | OK | |
| 03-adatok.md:57 | „**60** kérdésből áll, **négy** családban” | EXP-004 | OK | |
| 03-adatok.md:57–58 | „Családonként **5** kérdés a dev, **10** a teszt” | `dev.jsonl` (a–d: 5-5), `test.jsonl` (a–d: 10-10) | OK | |
| 03-adatok.md:64–67 | táblázat: „**5** / **10**” mind a négy családnál | ugyanaz | OK | |
| 04-tudasgraf.md:67 | „A példaüzem **4** lapja között **4** lapközi csatlakozópár” | EXP-002 | OK | |
| 04-tudasgraf.md:67–68 | „mind a **8** lapközi jel összekötött” | EXP-003 | OK | |
| 04-tudasgraf.md:110–111 | „üzemi rétege **36** csúcsból és **116** kapcsolatból” | EXP-005; `load_report.json` | OK | |
| 04-tudasgraf.md:115 | „**tíz** számozott lépésben” | plantdocs 0007 | OK | |
| 04-tudasgraf.md:122–134 | lépéstáblázat **01–10** | plantdocs 40-design/0007 (a sorok tartalma egyezik) | OK | |
| 04-tudasgraf.md:166–167 | „**négy** dokumentum … **88/133**-hoz … CFIHOS-szal együtt **101/133**-hoz” | plantdocs _results.md EXP-0022 (GF 165, Swagelok, Gorman-Rupp, Maximator; „RDL exact+broad 88/133”, „RDL or CFIHOS 101/133”, PRELIMINARY) | OK | Az „előzetes, kézi ellenőrzésre váró” jelzés is egyezik. |
| 04-tudasgraf.md:169–170 | „HTTP **404**-et adott” | EXP-006 | OK | |
| 04-tudasgraf.md:174 | „**négy** adatlapon mind a **24** nyelvimodell-kimenet elsőre átment” | EXP-006 | OK | |
| 04-tudasgraf.md:179 | „**Öt** elvre épül” | plantdocs 40-design/0003 („Principles” 1–5) | OK | |
| 04-tudasgraf.md:210 | „A kimeneti fájl **hat** listát tartalmaz” | plantdocs 0003 („six lists: facts, footnotes, figures, links, charts, skipped”) | OK | |
| 04-tudasgraf.md:270–271 | „A **hét** eszközgráf együtt **27 615** csúcsból és **103 366** kapcsolatból” | EXP-005; `load_report.json` | OK | |
| 04-tudasgraf.md:272 | „közös szókészlet-csúcsok … száma **221**” | EXP-005 | OK | |
| 04-tudasgraf.md:279–280 | „a **26** tagelt elemből **24**-nek van adatlapja, ennyi `DESCRIBED_BY` él” | EXP-002, EXP-005 (`described_by_edges: 24`) | OK | |
| 04-tudasgraf.md:281 | „a **nyolc** szivattyú ugyanazt a Gorman-Rupp adatlapot kapja” | `tag_to_datasheet.json` | OK | |
| 04-tudasgraf.md:312–313 | „a helyi Neo4j Community kiadás csak **egy** felhasználói adatbázist enged” | `docs/dontesek.md` (2026-10-31 08:45), `docs/felmeres.md` | OK | Projektnapló, nem mérés. |
| 04-tudasgraf.md:326 | „A teljes betöltés **243,2** s” | EXP-005 (243,18 s) | OK | |
| 04-tudasgraf.md:326 | „nagy része (**222,4** s) a **14 489** beágyazás tárolása és indexelése” | EXP-005 (vektorok 222,4 s; 14 489 db; `load_report.json` összeg 14 489) | OK | Megfogalmazás: a vektorlépés ideje a hiányzó beágyazások kiszámítását is tartalmazza (EXP-005: „+ qwen … a hiányzó vektorokhoz”; `load.py` `load_vectors`). Javasolt: „előállítása és tárolása”. |
| 04-tudasgraf.md:327 | „az üzemi réteg **3,6** s alatt töltődik be” | EXP-005 (3,64 s) | OK | |
| 04-tudasgraf.md:327–328 | „csak **egy** felhasználói adatbázist enged” | `docs/dontesek.md` | OK | |
| 05-modszerek.md:3 | „**Három** módszert” | EXP-020 | OK | |
| 05-modszerek.md:7 | „mindkét (**két**) kérdés-válaszoló modellel” | EXP-020 | OK | |
| 05-modszerek.md:23 | „**két** szintből áll” | `src/plantqa/methods/cascade.py` (cypher_rag_lines, graph_agent_lines) | OK | |
| 05-modszerek.md:37–38 | „**30** s időkorláttal és legfeljebb **1000** sorral” | plantgraph `data/runs/exp0007/inputs/params_cypher_v2t_a.json`; `cascade.py` CYPHER_PARAMS | OK | |
| 05-modszerek.md:38 | „**egy** javítókörben” | plantgraph `qa/strategies/cypher_rag_lines.py` („One repair round”) | OK | |
| 05-modszerek.md:49 | „lépésenként, legfeljebb **40**-szer” | `params_agent_v2t.json` (max_steps 40); `cascade.py` | OK | |
| 05-modszerek.md:62 | „**két** kaszkádot futtatunk” | `cascade.py` (AGENT_FIRST_LABELS) | OK | |
| 05-modszerek.md:73 | „**hat** általános, egymással komponálható primitívet” | plantgraph ADR-0034 („six generic, composable primitives”) | OK | A táblázat (81–86. sor) 6 primitívet sorol fel, egyezik. |
| 05-modszerek.md:89 | „mind a **hat** primitívnél” | ADR-0034 („shared by all six”) | OK | |
| 05-modszerek.md:92 | „a **hat** primitív” | ADR-0034 | OK | |
| 05-modszerek.md:107 | „legfeljebb **három** forrásszakaszt” | plantdocs `src/plantdocs/qa/sections.py` (MAX_SECTIONS = 3); plantdocs EXP-0031 | OK | |
| 05-modszerek.md:113–115 | „**egy** javítókörben” (A2) | plantdocs `qa/run.py` (query, retry) | OK | |
| 05-modszerek.md:120 | „legközelebbi **30** adatpont” | `src/plantqa/methods/datasheet.py` (TOP_K = 30); plantdocs EXP-0032 | OK | |
| 05-modszerek.md:141 | „mind a **hét** eszköz gráfja” | EXP-005 | OK | |
| 05-modszerek.md:162–163 | „a **második** fejlesztési iterációban kerültek be (EXP-011)” | EXP-011 | OK | |
| 05-modszerek.md:183 | „egy ágens **két** eszközzel” | `src/plantqa/methods/m2.py` | OK | |
| 05-modszerek.md:185 | „legfeljebb **hat** eszközhívással” | `m2.py` (MAX_STEPS = 6) | OK | |
| 05-modszerek.md:190 | „a **három** megengedett JSON-alakot” | `m2.py` rendszerüzenete (09-fuggelek B) | OK | |
| 05-modszerek.md:194–195 | „a hívás **egyszer** újrapróbálkozik” | `src/plantqa/methods/base.py` (PROVIDER_ATTEMPTS = 2) | OK | |
| 05-modszerek.md:199 | „A **második** fejlesztési iterációtól (EXP-011)” | EXP-011 | OK | |
| 05-modszerek.md:203–204 | „a dev halmazon az M2 és az M3 hallucinációi eltűntek (EXP-011)” | EXP-010: M2 2, M3 1 hallucinált → EXP-011: 0, 0 | OK | |
| 05-modszerek.md:212 | „legalább **két** egymás utáni eszközhívást” | a router felépítése (rajz → adatlap); EXP-020 routes.csv datasheet+drawing | OK | Logikai következmény. |
| 05-modszerek.md:218–219 | „a **hét** adatlap … **12** legközelebbi darab” | `src/plantqa/methods/m3.py` (TOP_K = 12) | OK | |
| 05-modszerek.md:220 | „`qwen/qwen3-embedding-8b`, **512** dimenzió” | plantdocs `src/plantdocs/llm/embeddings.py` (DIMENSIONS = 512); `chunks.py` | OK | |
| 05-modszerek.md:290–291 | „a teljes keret **20** USD (**18** USD felett új mérés nem indul)” | `src/plantqa/costlog.py` (TOTAL_CAP_USD = 20.0, NEW_RUN_STOP_USD = 18.0) | OK | |
| 06-kiertekeles.md:12 | „a **20** USD-s keret” | `costlog.py` | OK | |
| 06-kiertekeles.md:12–13 | „a teljes projekt költsége jóval a 20 USD-s keret alatt maradt (**a pontos összeget az összefoglalás adja**)” | – | NINCS FORRÁS | A 07-osszefoglalas.md nem ad összköltséget, és az eredmenyek.md-ben nincs ilyen sor. A `logs/koltseg.jsonl` összege most 1,634 USD (2694 sor, az Azure listaárával együtt), de ez nincs EXP-sorban rögzítve. |
| 06-kiertekeles.md:14 | „**10 000** ismétléses, seedelt percentilis-bootstrap” | `src/plantqa/eval/report.py` (BOOTSTRAP = 10000, BOOTSTRAP_SEED = 20261031, 2,5–97,5% percentilis) | OK | |
| 06-kiertekeles.md:19 | „A dev halmazon (**20** kérdés) **négy** iterációt” | EXP-010, -011, -012, -013 | OK | |
| 06-kiertekeles.md:26 | „az M1 pontossága **0,60**-ról **0,75**-re, az M2-é **0,85**-ről **0,95**-re” | EXP-011 → EXP-012 summary.csv | OK | |
| 06-kiertekeles.md:26–27 | „az M3-é nem változott” | EXP-011 = EXP-012: M3 0,70 | OK | |
| 06-kiertekeles.md:28 | EXP-013: „M1 **0,60**, M2 **0,70**, M3 **0,60**” | EXP-013 | OK | |
| 06-kiertekeles.md:34 | „**40** kérdés, családonként **10**” | EXP-020, `test.jsonl` | OK | |
| 06-kiertekeles.md:40 | M1 GLM: 25 / 9 / 6 / 0; 0,625 [0,475–0,775]; 8/10, 3/10, 4/10, 10/10 | EXP-020 summary.csv | OK | |
| 06-kiertekeles.md:41 | M2 GLM: 31 / 6 / 3 / 0; 0,775 [0,625–0,900]; 8/10, 7/10, 6/10, 10/10 | EXP-020 | OK | |
| 06-kiertekeles.md:42 | M3 GLM: 30 / 1 / 9 / 0; 0,750 [0,600–0,875]; 9/10, 5/10, 6/10, 10/10 | EXP-020 | OK | |
| 06-kiertekeles.md:43 | M1 Luna: 27 / 6 / 7 / 0; 0,675 [0,525–0,825]; 9/10, 5/10, 4/10, 9/10 | EXP-020 | OK | |
| 06-kiertekeles.md:44 | M2 Luna: 28 / 7 / 5 / 0; 0,700 [0,550–0,850]; 8/10, 5/10, 6/10, 9/10 | EXP-020 | OK | |
| 06-kiertekeles.md:45 | M3 Luna: 26 / 6 / 8 / 0; 0,650 [0,500–0,800]; 8/10, 4/10, 5/10, 9/10 | EXP-020 | OK | |
| 06-kiertekeles.md:49 | „az M2 GLM-mel (**31** helyes a **40**-ből)” | EXP-020 | OK | |
| 06-kiertekeles.md:50 | M1−M2 GLM: „**−0,150**, 95% CI **−0,275** és **−0,025** között” | EXP-020 pairs.csv | OK | |
| 06-kiertekeles.md:51 | M1−M3 GLM: „**−0,125**; **−0,225** és **−0,025** között” | EXP-020 pairs.csv | OK | |
| 06-kiertekeles.md:51–52 | M2−M3 GLM: „**+0,025**; **−0,075** és **+0,125** között” | EXP-020 pairs.csv | OK | |
| 06-kiertekeles.md:52 | „Lunával egyik különbség sem szignifikáns” | EXP-020 pairs.csv (Luna: −0,175–0,125; −0,100–0,150; −0,075–0,175) | OK | |
| 06-kiertekeles.md:53 | „Egyik párosítás sem hallucinált” | EXP-020 | OK | |
| 06-kiertekeles.md:53–54 | „(d) mindegyik módszer **9** vagy **10** helyes választ adott” | EXP-020 | OK | |
| 06-kiertekeles.md:54–55 | „az M2 GLM-mel **7/10**, az M1 GLM-mel **3/10**” (b) | EXP-020 | OK | |
| 06-kiertekeles.md:62 | M1 GLM: 0,00453 USD; 12,9 s; 81 492; 3 940 | EXP-020: 0,181079/40 = 0,004527; 12,88; 3 259 665/40 = 81 491,6; 157 588/40 = 3 939,7 | OK | |
| 06-kiertekeles.md:63 | M2 GLM: 0,00234; 16,2; 33 068; 2 221 | 0,093528/40 = 0,002338; 16,21; 33 067,7; 2 220,9 | OK | |
| 06-kiertekeles.md:64 | M3 GLM: 0,00029; 13,2; 13 264; 1 820 | 0,011646/40 = 0,000291; 13,18; 13 264,4; 1 820,1 | OK | |
| 06-kiertekeles.md:65 | M1 Luna: 0,00539; 13,7; 56 398; 1 578 | 0,21545/40 = 0,005386; 13,68; 56 397,95; 1 578,0 | OK | |
| 06-kiertekeles.md:66 | M2 Luna: 0,00213; 17,6; 35 765; 1 115 | 0,085354/40 = 0,002134; 17,62; 35 764,9; 1 114,6 | OK | |
| 06-kiertekeles.md:67 | M3 Luna: 0,00182; 4,2; 12 901; 425 | 0,072868/40 = 0,001822; 4,23; 12 900,6; 424,9 | OK | A táblázat a `cost_usd` (szolgáltatói ár) oszlopot használja, ahogy az 5. fejezet leírja. |
| 06-kiertekeles.md:71 | „A legdrágább az M1” | EXP-020 | OK | Mindkét modellnél. |
| 06-kiertekeles.md:72–73 | „Az M2 **körülbelül feleannyiba** kerül” | EXP-020: GLM 0,00234/0,00453 = 0,52; Luna 0,00213/0,00539 = 0,40 | ELTÉRÉS | GLM-mel igaz, Lunával az M2 az M1 költségének 40%-a. |
| 06-kiertekeles.md:73–74 | „Az M3 a legolcsóbb, és Lunával a leggyorsabb” | EXP-020: Luna M3 4,23 s (M1 13,68, M2 17,62) | OK | |
| 06-kiertekeles.md:74 | „**tizenkét** adatlap-darabot” | `m3.py` (TOP_K = 12) | OK | |
| 06-kiertekeles.md:75 | „a rajz kicsi (**36** csúcs)” | EXP-005 | OK | |
| 06-kiertekeles.md:81–82 | M1 GLM: „**40** tesztkérdésből **21** … **7** … **12**” | EXP-020 routes.csv | OK | |
| 06-kiertekeles.md:82–83 | M1 Luna: „**22**, **7** és **11**” | EXP-020 routes.csv | OK | |
| 06-kiertekeles.md:83–84 | M2 GLM: „**13** … rajz, **14** … adatlap, **13** … mindkettő”; Luna „**14**, **13** és **13**” | EXP-020 routes.csv | OK | |
| 06-kiertekeles.md:90 | „**12** olyan kérdésen” | EXP-009 | OK | |
| 06-kiertekeles.md:91 | „**két-három** különböző adatlapot” | EXP-009 („kérdésenként 2–3 különböző adatlap”) | OK | |
| 06-kiertekeles.md:95 | „**négy** kérdésnél … a legkisebb érték nem dönthető el” | EXP-009 („4-nél a referencia a változattól függést mondja ki”) | OK | |
| 06-kiertekeles.md:102 | M1 GLM: 0 / 5 / 6 / 1; 0,0636; 61,9 | EXP-030 summary.csv (0,063615; 61,87) | OK | |
| 06-kiertekeles.md:103 | M2 GLM: 3 / 6 / 3 / 0; 0,0537; 34,3 | EXP-030 (0,053721; 34,30) | OK | |
| 06-kiertekeles.md:104 | M3 GLM: 0 / 2 / 10 / 0; 0,0046; 25,6 | EXP-030 (0,004584; 25,56) | OK | |
| 06-kiertekeles.md:105 | M1 Luna: 0 / 6 / 6 / 0; 0,0880; 28,2 | EXP-030 (0,087963; 28,17) | OK | |
| 06-kiertekeles.md:106 | M2 Luna: 1 / 9 / 2 / 0; 0,1280; 38,6 | EXP-030 (0,127979; 38,63) | OK | |
| 06-kiertekeles.md:107 | M3 Luna: 0 / 0 / 12 / 0; 0,0276; 13,6 | EXP-030 (0,027618; 13,63) | OK | |
| 06-kiertekeles.md:110 | „csak a router adott (GLM-mel **3**, Lunával **1**)” | EXP-030 | OK | |
| 06-kiertekeles.md:111–113 | legalább részben jó: router **9** / **10**, M1 **5** / **6**, M3 **2** / **0** | EXP-030: 3+6, 1+9, 0+5, 0+6, 0+2, 0+0 | OK | |
| 06-kiertekeles.md:120 | „Az M1 hibáinak nagy része „részben helyes” válasz” | EXP-020: GLM 9 részben / 15 nem helyes; Luna 6 / 13 | OK | Lunával a nem helyes válaszoknak csak 46%-a „részben”; a „nagy része” még vállalható, a „többsége” már nem volna az. |
| 06-kiertekeles.md:123 | „a szivattyú **266** psi-s burkolatnyomása megvolt, a **100** °F-ig érvényes **250** psi-s üzemi határ nem” | EXP-012 scored.jsonl, b03 M1-glm „partial”; a gold a `dev.jsonl` b03-ban | OK | |
| 06-kiertekeles.md:127 | „(a) családjában **három** kérdést több módszer is elrontott” | EXP-020 scored.jsonl: a12 (M2 mindkét modell), a13 (mind a 6 párosítás), a15 (M1-glm, M3-luna) | OK | Az a12-t csak egy módszer (az M2) rontotta el, két modellel; pontosabb: „több párosítás”. |
| 06-kiertekeles.md:129–130 | izolációs kérdés: „a gold válasz **egyetlen** szelep, a módszerek többsége a felfelé eső összes szelepet felsorolta” | EXP-020 a13: gold [GV-1-2]; 5 párosítás 2–3 szelepet adott, M2-luna üreset | OK | |
| 06-kiertekeles.md:131 | „az M2 mindkét modellel a szelepet (PV-2-1) adta meg a kör (PIC-2-1) helyett” | EXP-020 a12 | OK | |
| 06-kiertekeles.md:132–133 | „az M1 GLM-mel és az M3 Lunával hiányos listát adott” | EXP-020 a15 (8, ill. 10 elem a 11-ből) | OK | |
| 06-kiertekeles.md:135–136 | „Mindegyik módszer jól kezelte: a nem létező tagekre és a dokumentumban nem szereplő tényekre „nincs benne” válasz jött, egyetlen hallucináció nélkül.” | EXP-020 scored.jsonl, (d) | ELTÉRÉS | Hallucináció valóban nem volt, de Lunával mindhárom módszer elrontott egy kérdést: M3-luna d06 (a nem létező P-2-4-hez utat adott: P-1-3, P-2-1, rossz), M2-luna d11 (a nem létező FV-2-3-ra üres listát adott „nincs benne” jelzés nélkül, rossz), M1-luna d08 (jelzés nélküli válasz, részben). |
| 06-z-demo.md:4 | „a dolgozat **ötödik** hozzájárulását” | 01-bevezetes.md 45. sor (5. pont) | OK | |
| 06-z-demo.md:5 | „**négy** képernyőképen végigkövetünk **négy** kérdést” | a fejezetben 4 kép van (01-c, 02-a, 04-d, 05-e) | OK | |
| 06-z-demo.md:5–7 | „**hat** kérdést … (a), (a), (b), (c), (d) és (e) … mind a **hat** kérdésre érdemi válasz” | EXP-040; `figures/demo/screens.csv` (6 sor) | OK | |
| 06-z-demo.md:21 | „a plantgraph **6**-os seedű üzeme” | EXP-002 | OK | |
| 06-z-demo.md:21–22 | „a **négy** lap között” | EXP-002 | OK | |
| 06-z-demo.md:29–30 | „(EXP-020: **31** helyes a **40**-ből)” | EXP-020 | OK | |
| 06-z-demo.md:56–57 | „a router **háromszor** kérdezte a rajzeszközt, ebből **kétszer** … az ágensig jutott, **egyszer** a Cypher-szinten zárult” | `screens.csv` (01-c-M2 útvonala) | OK | Az eredmenyek.md EXP-040-sora csak „drawing → datasheet:FT-2-2”-t ír; a részletek az EXP-040 kimenetéből jönnek. |
| 06-z-demo.md:72 | útvonal: „CHV-1-2, P-1-3, P-2-1, P-2-2, CHV-2-1” | `screens.csv` (02-a-M1) | OK | |
| 06-z-demo.md:91–93 | idézett válasz a GV-1-1-ről | `screens.csv` (04-d-M2) | OK | |
| 06-z-demo.md:112–113 | „**egy** rajzeszköz-hívás … majd **három** adatlap-hívás” | `screens.csv` (05-e-M2); EXP-040 | OK | |
| 06-z-demo.md:115–116 | „Of the **three** items … only P-2-2 …”; „a másik **két** elem” | `data/app/ask-log.jsonl` (teljes válasz) | OK | |
| 06-z-demo.md:127 | „A próba másik **két** kérdése” (03-b-M1, 06-a-M3) | `screens.csv` | OK | |
| 07-osszefoglalas.md:4 | „négylapos példaüzemen” | EXP-002 | OK | |
| 07-osszefoglalas.md:6–8 | „**Három** … módszert … **két** modellel egy **60** kérdéses, **négy** családra bontott kérdéssoron” | EXP-004, EXP-020 | OK | |
| 07-osszefoglalas.md:13 | „az M1 … GLM-mel **25**, Lunával **27** helyes választ adott a **40**-ből” | EXP-020 | OK | |
| 07-osszefoglalas.md:14 | „GLM-mel **31** helyes válasszal” | EXP-020 | OK | |
| 07-osszefoglalas.md:15–16 | „az M1 elmaradása … statisztikailag is kimutatható”; „Lunával … nem szignifikáns” | EXP-020 pairs.csv | OK | |
| 07-osszefoglalas.md:19 | „az M1 … (GLM-mel **0,00453**, Lunával **0,00539** USD)” | EXP-020 (0,004527; 0,005386) | OK | |
| 07-osszefoglalas.md:19–20 | „az M2 **körülbelül fele ennyi**” | EXP-020: 0,52 (GLM), 0,40 (Luna) | ELTÉRÉS | Mint 06-kiertekeles.md:72–73. |
| 07-osszefoglalas.md:20 | „az M3 a legolcsóbb (GLM-mel **0,00029** USD)” | EXP-020 (0,000291) | OK | |
| 07-osszefoglalas.md:20 | „a medián késleltetés **4** és **18** s között” | EXP-020: 4,23 … 17,62 s | OK | |
| 07-osszefoglalas.md:27 | „Egyik módszer sem hallucinált a teszten” | EXP-020 | OK | |
| 07-osszefoglalas.md:29 | „GLM-mel **3**, Lunával **1** a **12**-ből” | EXP-030 | OK | |
| 07-osszefoglalas.md:29–30 | „legalább részben jót GLM-mel **9**, Lunával **10** …, a gráf nélküli baseline **2**, illetve **0**” | EXP-030 | OK | |
| 07-osszefoglalas.md:34–35 | „egyetlen, **26** tagelt elemes, négylapos szintetikus üzemre” | EXP-002 | OK | |
| 07-osszefoglalas.md:38 | „Családonként **10** tesztkérdés” | EXP-004, `test.jsonl` | OK | |
| 09-fuggelek.md:3 | „**Két** példakérdés családonként a dev halmazból” | `dev.jsonl` | OK | 8 sor, családonként 2. |
| 09-fuggelek.md:10 | (b) gold: „**160** °F (**71** °C) … **250** psi … **100** °F (**37** °C)” | `dev.jsonl` b01, szó szerint | OK | |
| 09-fuggelek.md:12 | (c) gold: „**316** stainless shaft sleeve” | `dev.jsonl` c01 (a rövidítés helyes) | OK | |
| 09-fuggelek.md:14 | (d) gold: „at least **0.5** bar …; (**±10** %)” | `dev.jsonl` d01 | OK | |
| 09-fuggelek.md:27 | „Items with a datasheet: <**24** tags>” | `tag_to_datasheet.json` (24 kulcs) | OK | |

## Összesítés

| Státusz | Darab (táblasor) |
|---|---|
| OK | 209 |
| ELTÉRÉS | 6 |
| NINCS FORRÁS | 3 |
| **Összesen** | **218** |

Egy táblasorban gyakran több összetartozó szám áll (például a táblázatok egy sora); a darabszám a sorokat
számolja.

## Javítandó helyek (a pontos javaslattal)

1. **01-bevezetes.md:3** – „több ezer oldalnyi” (NINCS FORRÁS). Javaslat: „Egy ipari üzem rajza több száz
   lapból áll (a plantgraph README-je szerint), és ehhez jön a sokféle gyártói dokumentum”, vagy a szám
   elhagyása: „Egy ipari üzemet nagy terjedelmű, sokféle dokumentum ír le.”
2. **02-hatter.md:61–62** – „Egy adatlap tipikusan több tíz oldalas PDF” (NINCS FORRÁS, és az EXP-007
   ellentmond neki). Javaslat: „Egy adatlap néhány oldalastól több mint száz oldalasig terjedő PDF … a
   példaüzem adatlapjai 2 és 114 oldal közöttiek (EXP-007)”, vagy a „tipikusan több tíz oldalas” törlendő.
3. **03-adatok.md:33** – a táblázatcím forrásmegjelölése hiányos (ELTÉRÉS). Javaslat: „(EXP-002, EXP-006,
   EXP-007)”, mert az „Oldal” oszlop az EXP-007-ből jön.
4. **06-kiertekeles.md:12–13** – „(a pontos összeget az összefoglalás adja)” (NINCS FORRÁS). Az összefoglalás
   nem ad összköltséget, és az eredmenyek.md-ben nincs ilyen sor. Javaslat: vagy egy új EXP-sor a
   `logs/koltseg.jsonl` összegével (most 1,634 USD, 2694 tétel, az Azure-listaárat is beleértve), amelyre
   a 6. és a 8. fejezet hivatkozik, vagy a zárójeles rész törlendő, és a „jóval a 20 USD-s keret alatt”
   is, amíg nincs EXP-sor.
5. **06-kiertekeles.md:72–73** – „Az M2 körülbelül feleannyiba kerül” (ELTÉRÉS). Javaslat: „Az M2 GLM-mel
   körülbelül feleannyiba (0,00234 vs. 0,00453 USD), Lunával 40%-ába (0,00213 vs. 0,00539 USD) kerül”
   (EXP-020).
6. **07-osszefoglalas.md:19–20** – „az M2 körülbelül fele ennyi” (ELTÉRÉS). Javaslat: „az M2 GLM-mel
   körülbelül fele, Lunával 0,4-szerese ennyi (0,00234, illetve 0,00213 USD)” (EXP-020).
7. **kivonat.md:5** – „a megválaszolhatatlan kérdéseket mindegyik felismerte” (ELTÉRÉS). Javaslat: „a
   megválaszolhatatlan kérdések közül GLM-mel mindegyik módszer mind a 10-et, Lunával 9-et ismert fel”
   (EXP-020).
8. **abstract.md:5** – „all of them recognised the unanswerable questions” (ELTÉRÉS). Javaslat: „with GLM
   every method recognised all 10 unanswerable questions, with GPT-6 Luna 9 of 10” (EXP-020).
9. **06-kiertekeles.md:135–136** – „Mindegyik módszer jól kezelte: a nem létező tagekre és a dokumentumban
   nem szereplő tényekre „nincs benne” válasz jött” (ELTÉRÉS). Javaslat: „GLM-mel mindhárom módszer mind a
   10 kérdést felismerte, Lunával 9-et: az M3 a nem létező P-2-4-hez utat adott (d06), az M2 a nem
   létező FV-2-3-ra üres listát adott jelzés nélkül (d11), az M1 a GV-1-1 tanúsításairól jelzés nélkül
   válaszolt (d08, részben helyes). Hallucináció egyik esetben sem volt.” (EXP-020, `scored.jsonl`)

## Egyéb észrevételek (nem számhibák, ezért nincsenek a fenti darabszámban)

- **01-bevezetes.md:43, kivonat.md:3, abstract.md:3** – „programmal előállított referenciaválaszokkal” /
  „programmatically assembled reference answers”: az EXP-004 szerint csak az (a) család és a (c)
  topológiai része jön programból, a (b)–(d) referenciái modellkészítésűek (a 3. fejezet 72–75. sora
  és a 8. fejezet korlátai ezt helyesen mondják). Javaslat: „részben programmal, részben modellel
  előállított referenciaválaszokkal”.
- **01-bevezetes.md:57** – „A dolgozat minden száma egy ténylegesen lefutott mérésből származik”: a dolgozat
  a két forrásrepó eredménynaplójából és irodalmi jegyzetekből is idéz (megjelölve). Javaslat: „… egy
  ténylegesen lefutott mérésből vagy megjelölt forrásból (a két forrásrepó eredménynaplója, irodalmi
  jegyzet) származik.”
- **04-tudasgraf.md:326** – a 222,4 s a hiányzó beágyazások kiszámítását is tartalmazza, nemcsak a
  tárolást és az indexelést (EXP-005, `src/plantqa/graph/load.py`). Javaslat: „előállítása és tárolása”.
- **06-kiertekeles.md:127** – az a12-t csak az M2 rontotta el (két modellel), ezért a „több módszer is”
  helyett pontosabb: „több párosítás is”.

## Javítások (alkalmazva 2026-10-31)

Mind a 9 problémát a javaslat szerint javítottuk: (1) a „több ezer oldalnyi” törölve; (2) az
adatlapok terjedelme az EXP-007 alapján (2–114 oldal); (3) a 03. fejezet táblázatfelirata
kiegészítve az EXP-007-tel; (4) a teljes költés új EXP-050 sorból (1,6342 USD); (5–6) az M2/M1
költségarány modellenként (GLM ~0,5, Luna 0,4), az előadás összefoglaló diáján is; (7–9) a
megválaszolhatatlan kérdéseknél GLM-mel 10/10, Lunával 9/10, a három Luna-hiba megnevezve. A
további megjegyzések is átvezetve (a referenciák „részben programmal, részben modellel”; „vagy
megjelölt forrásból”; a beágyazási idő „előállítása, tárolása és indexelése”; „több párosítás”).
