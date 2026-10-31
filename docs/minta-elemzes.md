# Minta-elemzés: VIK TDK, Intelligens rendszerek, I. helyezett dolgozatok és előadások (2019–2025)

Forrás: `plantdocs/docs/private/90-thesis/mintak/tdk-vik-intelligens-rendszerek/` (16 dolgozat, 4 prezentáció; a README szerint 3 I. helyezett dolgozat privát, ezek kimaradtak). Az elemzés 2026-10-31-én készült.

**Mérési módszer.** A szöveget PyMuPDF-fel nyertem ki oldalanként. Minden számot megszámoltam, egyiket sem becsültem.

- **Oldalszám:** PDF-oldalakban értendő.
- **Főszöveg:** a Bevezetés/Introduction első oldalától az első hátsó elem (köszönetnyilvánítás, irodalomjegyzék, ábrajegyzék) előtti utolsó oldalig tart. Ha az összefoglalás és az irodalomjegyzék egy oldalon van (Bálint, Finta), azt az oldalt is beszámoltam.
- **Ábra és táblázat:** az egyedi feliratszámokat számoltam (`2.1. ábra`, `Figure 3:`, `5.1-1. Táblázat:` stb.), kézzel kiszűrve a szövegközi hivatkozásokat.
- **Hivatkozás:** az irodalomjegyzék tételeinek száma (`[n]` vagy `n.` sorkezdet; a legnagyobb sorszám egyezett a darabszámmal).
- **Fejezetszám:** csak a számozott főfejezeteket számoltam, függelék és hátsó anyag nélkül.
- **Margó és sortáv:** a 9–20. oldal hosszú sorainak befoglaló téglalapjából mértem.
- **Prezentációk:** a `.pptx` fájlok XML-jét bontottam ki (diaszöveg, képek, SmartArt, jegyzetek), a PDF-et oldalanként elemeztem. A Juhász-diákat renderelve meg is néztem.

---

## 1. Összesítő táblázat (16 dolgozat)

| # | Év, szerző | Nyelv | Előállítás / sablon | Össz. old. | Főszöveg old. | Fej. | Ábra | Tábl. | Hiv. | Kivonat / Abstract | Hangnem (fő) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 2019 Alekszejenkó | HU | LaTeX, VIK-sablon (12 pt változat) | 40 | 26 | 5 | 10 | 1 | 27 | – / – | E/1 + szerzői többes |
| 2 | 2019 Nagy S. J. | EN | LaTeX, VIK-sablon | 70 | 59 | 7 | 31 | 4 | 44 | – / EN | „we” (egyszerzős) |
| 3 | 2019 Szabó D. | HU | LaTeX, VIK-sablon | 60 | 51 | 6 | 29 | 2 | 41 | – / – | E/1 |
| 4 | 2020 Finta | EN | Word (saját) | 60 | 55 | 4 | 47 | 4 | 14 | – / EN | „we” + passzív |
| 5 | 2020 Kádár, Szalai (2 szerző) | EN | LaTeX, CM 10 pt, Letter (nem sablon) | 41 | 37 | 6 | 26 | 5 | 15 | – / – | „we” |
| 6 | 2020 Sándor D. | EN | LaTeX, VIK-sablon (3,0/2,0 cm margó) | 46 | 32 | 7 | 24 | 3 | 42 | HU / EN | „I” |
| 7 | 2022 Abonyi-Tóth | EN | XeLaTeX, VIK-sablon | 54 | 46 | 7 | 36 | 6 | 28 | HU / EN | „we” + sok passzív |
| 8 | 2022 Charaf | HU | Word, VIK Word-sablon | 50 | 43 | 8 | 19 | 0* | 22 | HU / EN | E/1 + „nézzük meg” |
| 9 | 2022 Sándor D. | EN | LaTeX, VIK-sablon | 58 | 35 | 10 | 21 | 2 | 43 | HU / EN | „I/my” |
| 10 | 2023 Czimber | HU | Google Docs | 41 | 32 | 5** | 19 | 1 | 65 | HU / EN | E/1 |
| 11 | 2023 Kisida | HU | LaTeX, VIK-sablon | 47 | 40 | 5 | 19 | 5 | 17 | HU / EN | E/1 |
| 12 | 2024 Bálint | EN | LaTeX, CM 10 pt, Letter (cikkszerű) | 42 | 24 | 5 | 14 | 10 | 40 | – / EN | „we/our” |
| 13 | 2024 Tarnay | EN | LaTeX, VIK-sablon | 46 | 31 | 7 | 17 | 5 | 36 | HU / EN | passzív, ritka „I” |
| 14 | 2025 Bunda | EN | Word, VIK Word-sablon | 40 | 33 | 7 | 19 | 0 | 38 | – / – | vegyes „I've built” / „we” |
| 15 | 2025 Juhász | HU | Word, VIK Word-sablon | 47 | 34 | 8 | 17 | 17 | 33 | HU („Összefoglaló”) / EN | E/1 + személytelen + T/1 |
| 16 | 2025 Tömöri | EN | LaTeX, VIK-sablon | 52 | 42 | 7 | 16 | 1 | 51 | HU / EN | „I” (+ „we” a példákban) |

\* Charafnál legalább 2 felirat nélküli táblázat van („az alábbi táblázat”). \*\* Czimbernél a tartalomjegyzék számozása hibás: a 3. után az 5. fejezet jön.
Egyéb feliratozott blokkok: Tarnay 19 Listing, Tömöri 7 Algorithm, Nagy 6, Szabó 6, Sándor 2022 5.

---

## 2. Dolgozatonkénti adatlapok

Jelölés: **Sz** = főfejezetek sorrendben, **C** = a célkitűzés egy mondata (szó szerint), **K** = a kiértékelés módja.

1. **2019 Alekszejenkó – Intelligens városi közlekedési rendszerek (ECN-jelzéskoordináció).**
   - **Sz:** Bevezetés (benne irodalmi áttekintés) · Feltételezések · Megvalósítás · Mérési eredmények és összehasonlításuk · Összefoglalás (az Irodalomjegyzék 5.1 alfejezetként szerepel) · A–C függelék.
   - **C:** „Dolgozatom célja egy jármű–infrastruktúra (V2I) és az infrastruktúra elemei közötti kommunikáción alapuló új jelzéskoordinációs módszer megvalósítása, illetve szimulációval történő ellenőrzése.”
   - **K:** SUMO-szimuláció; az ECN-bírót RR-alapú és fix időzítésű vezérléssel hasonlítja össze. 4 ábra és 1 táblázat (1x/2x/5x forgalom), statisztikai próba nincs.
2. **2019 Nagy Simon József – Reliability models of complex CPS.**
   - **Sz:** Introduction · Background · Overview · Modelling methodology · Safety analysis · Evaluation · Conclusion and future work.
   - **C:** „In this paper, we introduce a new safety analysis approach for complex cyber-physical systems.”
   - **K:** autóipari esettanulmány és benchmarkmodellek a skálázódáshoz. Futásidő-táblázat (6.2) és eloszlásábrák, a szimulációt FFSA-val és illesztett Weibull-modellel veti össze. Próba nincs. A címlapon 2014-es évszám áll: bent maradt a sablon alapértéke.
3. **2019 Szabó Dániel – Pálya- és trajektóriatervezés robotkarokhoz.**
   - **Sz:** Bevezetés · Robotkar kinematikai leírása · Használt technológia ismertetése · Pálya- és trajektóriatervezés statikus környezetben · Dinamikus objektumelkerülés · Eredmények, továbbfejlesztési lehetőségek.
   - **C:** „Célom az volt a feladat megoldása során, hogy robotkarok esetén akár valós időben is használható algoritmust fejlesszek.”
   - **K:** az eredmények a 4–5. fejezetbe ágyazva szerepelnek (szimulációs ábrák, futásidő például 5 ms), a külön eredményfejezet 2 oldal. Egy összehasonlító táblázat van (fuzzy és Gauss), baseline nincs.
4. **2020 Finta – Kétszabadságfokú robusztus szabályozó.**
   - **Sz:** Introduction · Theoretical Background · Control architecture to robustify the exact linearization · Conclusion · References.
   - **C:** „This thesis is concerned with a method to robustly control such nonlinear systems, despite these parameter uncertainties.”
   - **K:** három esettanulmány (rugó–tömeg, robotkar, kvadkopter), a robotkaron valós laborkísérlettel. Robusztus és nem robusztus szabályozót hasonlít össze időtartomány-ábrákon (47 ábra). A táblázatok csak paramétereket tartalmaznak, próba nincs.
5. **2020 Kádár & Szalai – TiliNG (az egyetlen kétszerzős minta).**
   - **Sz:** Introduction · Related works · TiliNG · Proposed approximation of parameter R · Evaluation and results · Applications. Nincs Conclusion fejezet és nincs abstract.
   - **C:** „We propose a GNG based algorithm, that can cope with the above mentioned problems, therefore resulting in a better state-space representation.”
   - **K:** szintetikus eloszlásokon és MNIST-en hasonlítja össze GNG-változatokkal (GNG, GNG-U, AING). 5 táblázat (R-becslés, futásidő más klaszterezőkkel szemben), próba nincs. A szerzők közötti munkamegosztást nem írja le.
6. **2020 Sándor Dániel – Transzfer tanulás DTI-predikcióban.**
   - **Sz:** Introduction · Background · The data set · Methodology · Evaluation in multi-party learning · Evaluation in the single-partner joint use… · Conclusion.
   - **C:** „Finally, I propose novel DTI prediction method exploiting the multitask effect.” A bevezető hozzájárulás-listát is tartalmaz („My main contributions…”).
   - **K:** 3 AUC-ROC táblázat a tanítási módszerek összevetésével, ismételt kísérletek, szignifikanciapróba nincs.
7. **2022 Abonyi-Tóth – Tree-based exploration, car-like robot.**
   - **Sz:** Introduction · Hardware and program components · Related work · Classical frontier-based exploration · The tree-based method · Experimental results · Conclusion.
   - **C:** „The focus of this paper is to review a classical frontier-based method and then propose a new tree-based goal selection method in response to the issues of the first.”
   - **K:** Gazebo, 2 világ. Az explore_lite (baseline) és a cluster_tree összevetése ismételt futtatásokkal; a progressziógörbéken vastag átlagvonal, futásonkénti idő- és úthossz-táblázatok (4 db). Átlagok vannak, próba nincs.
8. **2022 Charaf – Anomália-detektálás logfájlokban.**
   - **Sz:** Bevezetés · Felhasznált ismeretek és meglévő megoldások · Jelenlegi eljárások és algoritmusok · DeepLog alapú megoldás · KNN algoritmus · HDFS mint címkézett logfájl · Értékelés · Konklúzió.
   - **C:** „A TDK dolgozatomban én is egy ilyen feladatra vállalkoztam nevezetesen, hogy hogyan lehet a mesterséges intelligencia lehetőségeit felhasználni a logfájlok-beli anomáliák detektálására.”
   - **K:** HDFS-adathalmazon a DeepLog és a KNN (több távolságmetrikával) F1-score-ját veti össze. Az eredmények ábrák és felirat nélküli táblázatok, próba nincs.
9. **2022 Sándor Dániel – Federated boosting.**
   - **Sz:** Introduction · Related work · Boosting · Federated learning · Multitask learning and multitask boosting · Missing data · Federated multitask boosting · Evaluation settings · Results · Conclusion · Appendix.
   - **C:** „In my work, my main goal is to combine these approaches and create a federated multitask boosting scheme, which can handle MNAR data.”
   - **K:** a legszigorúbb kiértékelés a mintában. Baseline-ok (NN, FedAvg), 5-fold, AUROC, DeLong-féle p-értékek: **egyedül ez a dolgozat végez szignifikanciapróbát.** Előtte külön „Evaluation settings” fejezet áll.
10. **2023 Czimber – Valós idejű pontfelhő-feldolgozó és önvezető szoftver.**
    - **Sz:** Bevezetés · Irodalmi áttekintés · Anyag és módszer · Eredmények értékelése · Összefoglalás és továbbfejlesztési lehetőségek.
    - **C:** „A kutatásom fő célja egy valós idejű pontfelhő-feldolgozó és szimulációs modul elkészítése, melyben az autó navigálása megtanítható megerősítéses tanulás segítségével.”
    - **K:** komponensenként mér. Egy táblázat (R-fa, nyolcasfa, C-Tree-P: építés, lekérdezés, memória), a virtuális oktató és az RL kvalitatív ábrákon, átlagosan 33 ciklus/s. Próba nincs. Szerző–év hivatkozásokat használ, az irodalomjegyzék ábécérendben számozott.
11. **2023 Kisida – Federált Bayes-háló tanulás (NIC).**
    - **Sz:** Bevezetés · Adatok és módszerek · A kiterjesztett elemzési keretrendszer · Eredmények · Diszkusszió.
    - **C:** „A dolgozatomban átfogó módon vizsgálom az oksági Bayes-háló tanuló módszerek alkalmazásának lehetőségét a magyar koraszülött (NIC) adatbázisban…”
    - **K:** bootstrap és ismételt futtatások, a gráfok eltérését táblázatba foglalja (Levenshtein-távolság, élgyakoriság). A centralizált és a federált változatot (NOTEARS és NOTEARS-ADMM) veti össze.
12. **2024 Bálint – Ingatlanár-becslés (ML + LLM).**
    - **Sz:** Introduction · Data and methods · Results and discussion · Web application · Conclusion · Függelék (Abbreviations, Features, Case study, Prompt Templates).
    - **C:** „An important contribution of this paper is that we present a unique description processing method, based on LLMs, can be utilized in property price prediction.”
    - **K:** 3 baseline (BL1–3), összevetve XGBoost, TabNet, Elastic stb. modellekkel. MAPE, RMSE és R² táblázatok (7 eredménytábla), jellemzőcsoport-ablációk, SHAP, hiba ár-kvintilisenként. Cikkformátumú: a kapcsolódó munkák táblázatban.
13. **2024 Tarnay – Kvalitatív következtetésen alapuló hibadiagnosztika.**
    - **Sz:** Introduction · Microservice Architecture and Observability · Logic Reasoning · Modeling and Fault Diagnosis · Rule Extraction with Inductive Learning · Evaluation · Conclusion · Appendix.
    - **C:** „This report aims to tackle two challenges [2] in the field of observability and fault diagnosis of microservice systems…” Ezt egy „Contributions” ábra (1.1) követi, amely a kihívásokat fejezetekhez rendeli.
    - **K:** nyilvános benchmark (Online Boutique), A@1 = 37,5%, A@3 = 50%. A 6.1. táblázat irodalmi SOTA-eszközökkel veti össze (Nezha stb.), a kiértékelés 3 oldal. Próba nincs.
14. **2025 Bunda – Autonóm robotok federált RL-tanítása.**
    - **Sz:** Introduction · Background · Related Work · Proposed Solution · Implementation · Evaluation · Conclusion. Nincs abstract.
    - **C:** „The aim is not merely to show that multiple robots can “learn together”, but to do so under realistic network constraints and in industrial, and field-like topologies…”
    - **K:** kísérleti felállás: 2 gép, 4 kliens, 250/500/750 kbit/s uplink. A dense és a sparse módot tanulási görbéken hasonlítja össze (Fig. 18–19). Táblázat és próba nincs.
15. **2025 Juhász – Hallucinációk kezelése fejlett RAG rendszerekben (témában a legközelebbi minta).**
    - **Sz:** Bevezetés (5 számozott célkitűzés alfejezetként) · RAG működésének áttekintése · Hallucinációdetekciós módszerek áttekintése · Korrekciós stratégiák áttekintése · Kiértékelési módszertan · Eredmények · Végleges architektúra az eredmények tükrében · Összefoglalás és továbbfejlesztési lehetőségek · A. függelék (promptok).
    - **C:** „A kutatás központi célja a RAG-rendszerek hallucinációs jelenségeinek feltérképezése, valamint olyan módszerek részletes vizsgálata, illetve integrálása ezen rendszerekbe, amelyek képesek a hibás, nem alátámasztott állítások automatikus felismerésére és korrekciójára minél nagyobb hatásfokkal.”
    - **K:** saját, LLM-mel generált kérdés–válasz készlet Wikipédiából, 3 kérdéstípussal. A készlet méretét a szöveg nem közli. LLM-bíró, RAGAS-metrikák, precision/recall/F1. 13 eredménytábla (módszer × modell × kérdéstípus); a végleges architektúra „több mint 20%-kal” növeli a helyes válaszok arányát. Hogy ez mihez képest értendő, azt csak az előadás bírálói válasza pontosítja („detekció és korrekció nélküli architektúra”). A kiértékelés a főszöveg fele (22–38. o.: módszertan 9, eredmények 5, architektúra 3 oldal). A dolgozatban nincs próba; az előadás bírálói válaszában bootstrap-szignifikancia szerepel.
16. **2025 Tömöri – Gráfalapú logikai megoldók és genetikus algoritmusok.**
    - **Sz:** Introduction · Preliminaries · Overview · Elaboration · Evaluation · Related Work (a kiértékelés után!) · Conclusion and Future Work.
    - **C:** „To address this gap, this work proposes a novel approach that integrates a rule-based logic solver with a multi-objective genetic algorithm and a custom graph-based crossover operator.”
    - **K:** **explicit RQ1–RQ3** (célfüggvény-alakulás, futásidő-eloszlás, a keresztezés sikeraránya), 2 esettanulmány, ismételt futások mediánja, a bemelegítő futásokat kizárja. Ábrák és 1 Pareto-táblázat. Más módszerekkel nem hasonlít össze, és a bírálói kérdés pontosan ezt kérte számon.

---

## 3. Tipikus tartományok (n = 16)

| Mutató | Medián | Min–max | Megjegyzés |
|---|---|---|---|
| Összes oldal | 47 | 40–70 | |
| Főszöveg oldal | 36 | 24–59 | a 10 pontos, cikkszerű LaTeX (Bálint, Kádár) sűrűbb |
| Bevezetés hossza (oldal) | 2 | 1–6 | |
| Kiértékelő fejezet(ek) hossza (oldal) | 9 | 3–17 | n = 14 (Finta és Szabó beágyazva) |
| Számozott főfejezet | 7 | 4–10 | |
| Ábra | 19 | 10–47 | ≈ 0,5 ábra/főszöveg-oldal |
| Táblázat | 3,5 | 0–17 | az LLM/ML-témájúaknál több (Juhász 17, Bálint 10) |
| Irodalomjegyzék-tétel | 37 | 14–65 | |
| Nyelv | | HU 6 / EN 10 | mind a 4 előadás magyar, a 3 angol dolgozaté is |
| Kivonat (HU) + Abstract (EN) együtt | | 9/16 | csak EN abstract 3, semmi 4 (Alekszejenkó, Szabó, Kádár, Bunda) |
| Összevetés referencia- vagy alapmegoldással | | 13/16 | nincs: Nagy, Szabó, Tömöri; külön „baseline” sor az eredménytáblában csak Sándor 2022 és Bálint dolgozatában van; Tarnay irodalmi számokkal vet össze |
| Szignifikanciapróba | | 1/16 | Sándor 2022 (DeLong) |
| Explicit RQ-k | | 1/16 | Tömöri; a többiek célkitűzés-mondattal vagy hozzájárulás-listával dolgoznak |
| Hozzájárulás-lista a bevezetőben | | 3/16 | Sándor 2020, Tarnay (ábrával), Tömöri („(I) … (II)”) |
| Köszönetnyilvánítás | | 9/16 | |
| Függelék | | 6/16 | Bálint és Juhász a promptokat teszi függelékbe |
| Ábra- és táblázatjegyzék | | 2/16 | mindkettő Sándor |
| Nyilatkozat | | 0/16 | a TDK-dolgozatokban nincs hallgatói nyilatkozat |

**Hangnem.** A magyar dolgozatok jellemzően E/1-ben íródnak („Dolgozatom célja…”, „megvalósítottam”), itt-ott szerzői többessel („nézzük meg”). Az angolok fele „we”-t használ egyszerzős munkában is, a többi „I” vagy passzív szerkezet. Az egyetlen kétszerzős munka (Kádár–Szalai) következetesen „we”-t ír.

---

## 4. Formai konvenciók

**Címlap mezői** (16-ból):

| Mező | Előfordulás | Megjegyzés |
|---|---|---|
| BME „Műegyetem 1782” logó | 15 | hiányzik: Czimber |
| Egyetem | 16 | |
| Kar | 14 | |
| Tanszék | 13 | |
| Cím | 16 | |
| Dokumentumtípus | 14 | „TDK dolgozat” / „Scientific Students' Association Report” / „Tudományos Diákköri Konferencia dolgozat” |
| Szerző(k) | 16 | „Készítette:” / „Author:” |
| Konzulens(ek) | 16 | 1–3 fő, külső konzulens is előfordul |
| Év vagy dátum | 16 | pontos dátum 4 esetben |

Angol címet magyar dolgozat címlapja ritkán közöl (Finta mindkét nyelven adja meg).

**Elülső rész sorrendje** (VIK LaTeX-sablon): címlap → Tartalomjegyzék → Kivonat (i) → Abstract (ii) → 1. fejezet. A Word- és Google Docs-os dolgozatoknál a sorrend vegyes: Juhász esetében Tartalom → Összefoglaló → Abstract, Charafnál és Czimbernél előbb jön a kivonat és az abstract, utána a tartalomjegyzék, Bundánál csak tartalomjegyzék van. A Kivonat és az Abstract egyaránt 1 oldal körüli, egyes szám első személyben vagy személytelenül.

**Betű és tükör:**

| Csoport | Dolgozatok | Betű, sortáv | Margó |
|---|---|---|---|
| VIK LaTeX-sablon | Nagy, Szabó, Abonyi, Sándor 2022, Kisida, Tarnay, Tömöri | Latin Modern 11 pt (LMRoman10 10,9 pt törzs, LMRoman12-Bold címsorok), sortáv 13,5 pt | A4, bal 3,5 cm / jobb 2,5 cm |
| Word-sablon | Charaf, Bunda, Juhász | Times New Roman 12 pt | |
| Cikkszerű LaTeX | Kádár, Bálint | CMR 10 pt | US Letter |

- A sablonos dolgozatok fejezetcíme „N. fejezet” / „Chapter N”, a címsor nagy és kétsoros, az oldalszám középen alul áll. A sablon 7 dolgozatban azonos.
- A Word-sablonos dolgozatok címlapja: név, NAGYBETŰS cím, „KONZULENS” kiskapitálissal, „BUDAPEST, 2025”.

**LaTeX-sablonra utaló jelek.**

- 11 dolgozat LaTeX (egy XeLaTeX), 4 Word, 1 Google Docs.
- A BME VIK diplomaterv/TDK sablon jegyei 9 dolgozatban láthatók: a fenti 7, valamint Sándor 2020 (3,0/2,0 cm margó) és Alekszejenkó (12 pt, egymás melletti Készítette/Konzulens mezők).
  - BME-logós címlap.
  - „Scientific Students' Association Report” vagy „TDK dolgozat” felirat.
  - A PDF `Creator` mezőjében a szerző neve áll (a sablon a hyperref `pdfcreator` értékét a szerzőre állítja).
  - Latin Modern betűtípus, 3,5/2,5 cm margó.
  - Római számozású Kivonat és Abstract.
- **Következtetés:** az I. helyezettek többsége a VIK-sablont használja; az eltérés (Word, Google Docs) sem kizáró ok.

---

## 5. Javasolt vázlat: „Tudásgráf-építés műszaki rajzokból és adatlapokból skálázható Q&A rendszerhez”

**Keret.**

- Nyelv: magyar.
- Sablon: BME VIK LaTeX-sablon TDK-változata.
- Címlap: két szerző a „Készítette:” mezőben, konzulens(ek), tanszék, év.
- Elülső rész: Kivonat (HU) és Abstract (EN), egy-egy oldal.
- Célterjedelem: kb. 36–40 oldal főszöveg (medián 36), 7 főfejezet, 18–22 ábra, 6–10 táblázat (kiértékelés-központú téma, lásd Juhász és Bálint), 35–45 hivatkozás.
- Hangnem: következetes T/1 („megvalósítottuk”) vagy személytelen szerkezet. Az E/1 két szerzőnél nem használható.

| # | Fejezet | Oldal | Tartalom | Mintából átvett elem |
|---|---|---|---|---|
| – | Kivonat / Abstract | 1 + 1 | probléma, M1/M2/M3, 60 kérdés, fő számok | |
| 1 | Bevezetés | 2–3 | motiváció (ipari P&ID és gyártói adatlap), **RQ1–RQ3** (pl. RQ1: javít-e az egyesített gráf (M1) a gráf nélküli baseline-hoz (M3) képest; RQ2: a router (M2) eléri-e M1 pontosságát kisebb költséggel; RQ3: mely kérdéstípusokon segít a gráf), hozzájárulás-lista, felépítés, **szerzői munkamegosztás** (egy bekezdés) | RQ-k: Tömöri; hozzájárulás-lista: Sándor 2020, Tarnay; munkamegosztást egyik minta sem ír, kétszerzős munkánál ajánlott |
| 2 | Háttér és kapcsolódó munkák | 6–7 | P&ID-jelölések, adatlapok, RAG → GraphRAG, tudásgráf-építés dokumentumokból, kapcsolódó munkák rövid összevető táblázattal | kapcsolódó munkák táblában: Bálint |
| 3 | Adatok és feladat | 3–4 | rajz- és adatlapkorpusz, a 60 kérdéses készlet felépítése, típusai és befagyasztása (hash), a pontozás elve | külön módszertani fejezet: Juhász, Sándor 2022 |
| 4 | Tudásgráf-építés | 7–8 | rajz-kaszkád (cascade_v4_iso), adatlap-réteg sémája, egyesítés, `datasheet_fact`-primitív; sok ábra (pipeline, séma, példa részgráf) | |
| 5 | Kérdés-megválaszolási módszerek | 4–5 | M1 egyesített gráf, M2 router, M3 baseline (ContextRAG + adatlap-chunkok); egy közös összehasonlító ábra | |
| 6 | Kiértékelés | 9–11 | beállítás (modellek, pinek, költségmérés); fő táblázat M1/M2/M3 × kérdéstípus; **bootstrap-CI vagy páros próba** (a mintában ez ritka, 1/16, ezért megkülönböztető); költség és késleltetés; hibaelemzés példákkal; az RQ-k megválaszolása | táblás eredmények: Juhász, Bálint; szignifikancia: Sándor 2022; RQ-zárás: Tömöri |
| 7 | Összefoglalás és továbbfejlesztés | 1–2 | válasz az RQ-kra, korlátok, skálázás | |
| – | Köszönetnyilvánítás (opcionális), Irodalomjegyzék | | | |
| A | Függelék | | promptok, kérdéskészlet-részlet, gráfséma | Bálint, Juhász |

Tanulság a bírálói kérdésekből (Juhász, Tömöri): kérdés jön arra, hogy mihez képest mértük a javulást, van-e szignifikanciapróba, összevetettük-e más módszerekkel, és reprodukálható-e a munka (kód, seed, adathalmaz). Ezekre érdemes a dolgozatban előre válaszolni.

---

## 6. Prezentációk (4 db)

Előadás-időtartam egyik mintában sincs megadva (README, info.md, diák). A javaslat ezért a feladat szerinti 10–12 percre készült.

### 6.1 Mérőszámok

| | 2024 Tarnay (pptx) | 2025 Bunda (pptx) | 2025 Juhász (pdf) | 2025 Tömöri (pptx) |
|---|---|---|---|---|
| Diák összesen | 33 | 20 | 19 | 22 |
| Fő rész (címtől az összefoglalásig) | 24 (ebből 4 szakaszelválasztó) | 19 | 14 | 17 |
| Bírálói kérdések diák | 1 elválasztó + 7 válasz | 1 (81 szó, a kérdések szövege) | 5 válasz („Kérdések”) | 1 elválasztó + 3 válasz |
| Záró/extra | 1 záró kép | – | – | 1 áttekintő dia |
| Ábra/diagram-domináns : szöveges (fő rész, cím és elválasztók nélkül) | 16 : 3 | 11 kép/diagram + 7 SmartArt : 0 | 6 : 7 | 15 : 1 |
| Szó/dia, medián (fő rész) | 22 (ebből 5 szó lábléc) | 15,5 (SmartArt-szöveggel) | 25 (oldalszámmal) | 33 |
| Szó/dia, válaszdiák | 57–87 | 81 | 39–61 | 58–84 |
| Előadói jegyzet | 7 dián, 93 szó | nincs | PDF-ből nem állapítható meg | 17 dián, 887 szó (a fő részben 16 dián 756 szó) |
| Formátum | 16:9, lábléc „TDK 2024” + oldalszám | 16:9, „x/20” | 16:9, „x / 18” | 16:9, PowerPoint-szakaszok |
| Nyelv | HU (a dolgozat EN) | HU (a dolgozat EN) | HU | HU (a dolgozat EN) |

### 6.2 Szerkezet sorrendben

- **Tarnay:** Cím → Kontextus (mikroszolgáltatások) → Célok → 3 kontribúció-dia (egy-egy nagy ábra, 64% képterület) → [elválasztó] Heterogén metamodell (6 dia, ASP-leképezés 3 lépésben) → [elválasztó] Diagnosztika (2) → [elválasztó] Induktív szabálytanulás (3) → [elválasztó] Eredmények (benchmark, „Pontosság@1 – 37,5%, @3 – 50%”) → Összefoglalás → [elválasztó] Bírálói kérdések (7) → záró kép.
- **Bunda:** Cím → Motiváció → Célok → teljes képes dia → RL → FL → Felhasznált technológiák → Rendszerarchitektúra → Szerveroldal → Kliensoldal → Sávszélesség-adaptív szűrés (+ rajzolt delta-szűrő ábra, 89 alakzat) → teljes kép → Kísérleti felállás → Kommunikációs eredmények → Tanulási teljesítmény → 2 teljes képes eredménydia → Összefoglalás → Bírálói kérdések.
- **Juhász:** Cím → Motiváció → Kutatás céljai (5 pont, mint a dolgozatban) → RAG működése (ábra) → Detektálás → Korrekció → Kiértékelő pipeline (4 lépés, mindegyik külön diagramos dián) → Végleges architektúra (ábra, „~20% / ~10%” javulás) → Konklúzió → 5 válaszdia (az egyiken vonaldiagram). **A fő részben nincs eredménytáblázat és számos grafikon**; a számszerű eredmény két mondat.
- **Tömöri** (szakaszok): Intro & Opti (cím, motiváció, tervezési tér) → GA (2) → Partial modelling (1) → Algo & Crossover (koncepcióábra, majd 7 dián lépésenként felépülő keresztezés-példa) → Evaluation (RQ1–RQ3 dia, eredménydia ábrákkal és táblázattal) → Summary (1) → Q&A (elválasztó, 3 válasz, áttekintő dia).

**Közös minták:**

1. Cím → motiváció → célok az első 3 dián.
2. A módszer vizuálisan jelenik meg: a 2025-ös két pptx-ben a fő diák több mint 85%-a ábra vagy diagram.
3. Az eredményekre 1–3 dia jut.
4. Egydiás összefoglalás.
5. **Mindegyik előadásban vannak előre elkészített bírálói válaszdiák.** Ezek a legszövegesebbek (60–90 szó).

### 6.3 Javasolt diaterv (10–12 perc, kb. 45 mp/dia → 14 fő dia + tartalék)

| # | Dia | Típus | Idő |
|---|---|---|---|
| 1 | Cím (két szerző, konzulens, TDK 2026) | – | 0:15 |
| 2 | Motiváció: egy valós kérdés P&ID-ből és adatlapból, amit ma kézzel keresünk | kép/példa | 0:45 |
| 3 | Célok és RQ1–RQ3 | szöveg (≤ 35 szó) | 0:45 |
| 4 | Rendszer-áttekintés: rajz → gráf, adatlap → gráf, kérdés → válasz | pipeline-ábra | 0:50 |
| 5 | Gráfépítés P&ID-ből (kaszkád, példa részgráf) | ábra | 0:50 |
| 6 | Adatlap-réteg (séma, `datasheet_fact`) | ábra | 0:45 |
| 7 | A három módszer: M1 egyesített gráf, M2 router, M3 baseline | összehasonlító ábra | 1:00 |
| 8 | Egy kérdés útja végig a rendszeren (alkalmazás-screenshot) | kép | 0:45 |
| 9 | Kiértékelés: 60 kérdés, típusok, pontozás (programos + vak bíráló) | ábra/tábla | 0:45 |
| 10 | Fő eredmény: M1/M2/M3 kérdéstípusonként (oszlopdiagram, CI-vel) | grafikon | 1:00 |
| 11 | Költség és késleltetés, illetve a pontosság–költség kompromisszum | grafikon | 0:45 |
| 12 | Hibaelemzés: 2–3 tipikus hiba | ábra | 0:40 |
| 13 | Összefoglalás: válasz az RQ-kra, egy mondat hozzájárulásonként | szöveg | 0:40 |
| 14 | Köszönöm / kérdések | – | 0:05 |
| T1–T5 | Bírálói kérdések: elválasztó + 3–5 válaszdia (a kapott kérdések szövegével), tartalék táblák (teljes eredménymátrix, kérdéskészlet-részlet, munkamegosztás) | szöveg/tábla | – |

**Arányok:** a 12 tartalmi diából (2–13) 2 szöveges és 10 ábra/grafikon (kb. 83%, a 2025-ös minták szintje). Medián legfeljebb 25 szó/dia.

**Kiegészítések:**

- Jegyzetbe érdemes leírni a teljes szöveget (Tömöri-minta: 16 dián 756 szó).
- Ha mindkét szerző beszél, a 8. dia utáni váltás a módszert és az eredményt választja ketté. Kétszerzős előadásra nincs minta.
- Juhásszal ellentétben a fő számokat grafikonon mutassuk meg, ne csak mondatban. A bírálói kérdések nála is a kontrollcsoportra és a szignifikanciára irányultak.
