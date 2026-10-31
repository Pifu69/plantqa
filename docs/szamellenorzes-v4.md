# Számellenőrzés – dolgozat v4 (független ellenőr)

Dátum: 2026-10-31. Ellenőrzött fájlok (`dolgozat/src/`): `01-bevezetes.md`, `03-adatok.md`,
`06-kiertekeles.md`, `06-z-demo.md`, `07-osszefoglalas.md`, `kivonat.md`, `abstract.md`.
A dolgozatfájlokat nem módosítottam.

Módszer: minden számot összevetettem a `docs/eredmenyek.md` megfelelő EXP-sorával, és ahol
lehetett, az alatta lévő fájlokkal is: `runs/EXP-0xx/summary.csv` (EXP-060/070: `dev+test`,
EXP-020: `test`, EXP-061/071: `complex`), `pairs.csv`, `routes.csv`, `scored.jsonl`;
`data/plant*/tags.json`, `tag_to_datasheet.json`, `seed_search.json`, `drawings/*/drawings.index.json`,
`load_report.json`; `data/questions*/complex.jsonl`; `figures/demo/screens.csv`;
`data/app/default_method.json`; a kódbeli paraméterek (`src/plantqa/plant/spec.py`,
`src/plantqa/eval/report.py`, `src/plantqa/methods/m3.py`); a plantdocs `_results.md` és
EXP-0038 README. A hibafajtákat (EXP-062/067) a `scripts/failure_kinds.py` újrafuttatásával
is ellenőriztem (csak olvas): mind az öt futás kimenete egyezik a naplósorral. A kérdésenkénti
költség = `cost_usd / n` (a summary.csv-ből újraszámolva), a projektköltség-különbségek a
`spent_usd` oszlopok összegével is egyeznek (EXP-060+061: 1,8411 USD; EXP-070+071: 3,4126 USD).
Szignifikancia: a CI nem tartalmazza a 0-t; a 0-t pontosan érintő CI határeset.

## Táblázat

| fájl:sor | szám (kontextussal) | forrás | státusz | megjegyzés |
|---|---|---|---|---|
| 01:28 | „több száz, akár ezer lapos üzemen” | – (a rajzoldali rész kutatási kérdése) | OK | nem mérési állítás, hanem a kérdés megfogalmazása |
| 01:31 | „csak 100 °F alatt” | – | OK | szemléltető példa, nem mért érték |
| 01:36 | „kis, négylapos üzemen” | EXP-002; `data/plant/drawings/PQA/drawings.index.json` (4 oldal) | OK | |
| 01:37 | „egy 27 lapos és egy 98 lapos üzemen” | EXP-051, EXP-064; drawings.index.json (27, 98 oldal) | OK | |
| 01:45–46 | RQ2: „(27 és 98 lap)” | EXP-051, EXP-064 | OK | |
| 01:51 | „négylapos (26 tagelt elem)” | EXP-002; `data/plant/tags.json` (26) | OK | |
| 01:51–52 | „27 lapos (190)” | EXP-051; `data/plant-pqb/tags.json` (190) | OK | |
| 01:52 | „98 lapos (765)” | EXP-064; `data/plant-pqc/tags.json` (765) | OK | |
| 01:52, 54 | „hét eszköz gyártói adatlapját”, „hét eszköz adatlapgráfja” | EXP-005/053/066 (`documents_loaded`: 7) | OK | |
| 01:59 | „60 kérdéses, négy családra bontott kérdéssor” | EXP-004, EXP-052, EXP-065 | OK | |
| 01:59–60 | „12 több adatlapot összevető kérdés” | EXP-009, EXP-052, EXP-065 | OK | |
| 01:61 | „két modellel mindhárom üzemen” | EXP-020/030, EXP-060/061, EXP-070/071 | OK | |
| 03:4 | „üzemenként 60 kérdésből álló kérdéssor” | EXP-004/052/065 | OK | |
| 03:16–18 | „Az 1-es seedtől”, tagelt elemek „20 és 40”, lapok „2 és 4” közé | `spec.py` PROFILES `pqa: (2, (20, 40), (2, 4))`; `data/plant/seed_search.json` | OK | kódbeli paraméter, az EXP-002 sor nem írja ki; javasolt az EXP-002 sorba felvenni |
| 03:19 | „6-os seed” | EXP-002; seed_search.json `accepted_seed: 6` | OK | |
| 03:19–20 | „26 tagelt elem, 4 lap, 4 lapközi csatlakozópár, 36 csúcs és 116 kapcsolat (EXP-002)” | EXP-002 (és EXP-005: 36/116) | OK | |
| 03:29 | „hét adatlappal 15 egységes üzemet” | EXP-051; `spec.py` `pqb: (15, …)` | OK | |
| 03:29–30 | elfogadási határ „120–400 tagelt elem és 24–40 lap” | `spec.py` `pqb: (15, (120, 400), (24, 40))` | OK | kódbeli paraméter, nincs EXP-sorban; javasolt az EXP-051 sorba felvenni |
| 03:34 | „seed (1) … 27 lapos, 190 tagelt elemmel, … 164-hez tartozik adatlap” | EXP-051; seed_search.json, tags.json, tag_to_datasheet.json (164) | OK | |
| 03:35 | „18 szabályozófunkció és 8 szint- vagy hőmérséklet-távadó (EXP-051)” | EXP-051; tags.json (PIF 18, PSGF adatlap nélkül 8) | OK | |
| 03:36 | „58 szivattyú ugyanazt a Gorman-Rupp adatlapot” | EXP-051; tag_to_datasheet.json (58) | OK | |
| 03:39 | „55 egységgel egy kb. 100 lapos üzemet” | EXP-064; `spec.py` `pqc: (55, …)` | OK | |
| 03:39–40 | elfogadási határ „500–1500 tagelt elem és 90–115 lap” | `spec.py` `pqc: (55, (500, 1500), (90, 115))` | OK | kódbeli paraméter, nincs EXP-sorban; javasolt az EXP-064 sorba felvenni |
| 03:40–41 | „seed (1) … 98 lapos, 765 tagelt elemmel, … 640-hez tartozik adatlap” | EXP-064; tags.json, tag_to_datasheet.json (640) | OK | |
| 03:41–42 | „83 szabályozófunkció és 42 … távadó (EXP-064)” | EXP-064; tags.json | OK | |
| 03:42–43 | „körülbelül 7-szer, illetve 25-ször nagyobb a kis üzemnél” | EXP-002/051/064 (származtatott) | ELTÉRÉS | a mérőszám nincs megnevezve, és a két arány más-más mérőszámhoz illik: lapszám 27/4 = 6,75 és 98/4 = 24,5; tagelt elem 190/26 = 7,3 és 765/26 = 29,4; üzemi csúcs 252/36 = 7,0 és 1003/36 = 27,9. A „25-ször” csak a lapszámra igaz |
| 03:51 | „A két szabályozófunkcióhoz (FIC, PIC)” | `data/plant/tags.json` (FIC-2-2, PIC-2-1) | OK | |
| 03:54–63 | táblázat, tagszám: 8, 4, 2, 3, 1, 4, 2 db | EXP-002; `data/plant/tags.json` / tag_to_datasheet.json | OK | osztályonként és adatlaponként egyezik |
| 03:54–63 | táblázat, oldalszám: 6, 2, 36, 6, 12, 16, 114 | EXP-007 | OK | |
| 03:65 | „a plantdocs tíz lépéses folyamata” | EXP-006 („01–10. lépés”) | OK | |
| 03:67–68 | „A korábban feldolgozott négy eszköz közül a Fisher, a GF 165 és a Gorman-Rupp gráfja … (plantdocs EXP-0030)” | plantdocs `_results.md` EXP-0030 | OK | hivatkozott forrás |
| 03:69 | „a három új adatlapot” | EXP-001 | OK | |
| 03:71 | „91 202 tripletből és 3538 … tényből” | EXP-006 | OK | |
| 03:72–73 | „20 973 triplet, 626 tény, a plantdocs saját jelentése szerint” (EXP-0038) | EXP-006; plantdocs `EXP-0038-rosemount-folyamat/README.md` (20 973 hármas, 626 eszköz-tény) | OK | hivatkozott forrás |
| 03:73–74 | „1102, 16 281 és 66 747 tripletes” | EXP-006 | OK | |
| 03:78 | „60 kérdésből áll, négy családban” | EXP-004 | OK | |
| 03:78–79 | „Családonként 5 … dev, 10 a teszthalmazba” | EXP-004 (dev 20 / teszt 40) | OK | |
| 03:81–82 | „27 lap: EXP-052, 98 lap: EXP-065” | EXP-052, EXP-065 | OK | |
| 03:82–83 | „ott mind a 60 kérdés tesztkérdés” | EXP-052/065 | OK | |
| 03:83–84 | „12 további, több adatlapot összevető kérdés (EXP-009, EXP-052, EXP-065)” | EXP-009/052/065 | OK | |
| 03:89–92 | táblázat „5 / 10” (×4) | EXP-004 | OK | |
| 03:110 | „plantdocs EXP-0029 bírálati promptjával” | plantdocs `_results.md`; EXP-010/060/070 sor | OK | azonosító, nem mért szám |
| 06:3 | „egy 27 lapos és egy 98 lapos üzemen” | EXP-051, EXP-064 | OK | |
| 06:5 | „mind a 60-60 kérdése tesztkérdés” | EXP-052/065 | OK | |
| 06:13–14 | „6,8879 USD … a 20 USD-s keretből (EXP-068)” | EXP-068 | OK | |
| 06:14 | „a 27 lapos üzem mérése 1,8411 USD (EXP-063)” | EXP-063; a summary.csv `spent_usd` összege EXP-060+061 = 1,8411 | OK | |
| 06:15 | „a 98 lapos üzemé 3,4126 USD (EXP-068)” | EXP-068; `spent_usd` összege EXP-070+071 = 3,4126 | OK | |
| 06:15–16 | „10 000 ismétléses, seedelt percentilis-bootstrap” | `src/plantqa/eval/report.py` `BOOTSTRAP = 10000` | OK | kódbeli paraméter |
| 06:21 | „20 kérdéses fejlesztési halmazán négy iterációt (EXP-010–EXP-013)” | EXP-010…013 | OK | |
| 06:24–26 | „40 kérdéses teszthalmazán … M2 … GLM-mel (31 helyes), … M3 30, az M1 25 (EXP-020)” | EXP-020; summary.csv test/all | OK | az M3 és M1 értéke a GLM-es (Lunával 26 és 27); javasolt kiírni: „GLM-mel az M3 30, az M1 25” |
| 06:31–32 | „60 kérdése (családonként 15) … (27 lap: EXP-060, 98 lap: EXP-070)” | EXP-060/070 | OK | |
| 06:37 | M1 GLM 27: 42/9/8/1, 0,700 [0,583–0,817], 12/11/7/12 | EXP-060; summary.csv | OK | |
| 06:38 | M1 GLM 98: 38/11/10/1, 0,633 [0,517–0,750], 12/6/9/11 | EXP-070; summary.csv | OK | |
| 06:39 | M2 GLM 27: 51/4/5/0, 0,850 [0,750–0,933], 13/13/11/14 | EXP-060 | OK | |
| 06:40 | M2 GLM 98: 49/4/7/0, 0,817 [0,717–0,917], 12/13/11/13 | EXP-070 | OK | |
| 06:41 | M3 GLM 27: 35/5/20/0, 0,583 [0,450–0,700], 6/6/8/15 | EXP-060 | OK | |
| 06:42 | M3 GLM 98: 42/4/14/0, 0,700 [0,583–0,817], 11/8/9/14 | EXP-070 | OK | |
| 06:43 | M1 Luna 27: 43/12/5/0, 0,717 [0,600–0,833], 14/7/8/14 | EXP-060 | OK | |
| 06:44 | M1 Luna 98: 43/13/4/0, 0,717 [0,600–0,833], 14/6/9/14 | EXP-070 | OK | |
| 06:45 | M2 Luna 27: 41/14/4/1, 0,683 [0,567–0,800], 11/8/8/14 | EXP-060 | OK | |
| 06:46 | M2 Luna 98: 42/12/6/0, 0,700 [0,583–0,817], 12/8/8/14 | EXP-070 | OK | |
| 06:47 | M3 Luna 27: 39/7/14/0, 0,650 [0,533–0,767], 12/5/9/13 | EXP-060 | OK | |
| 06:48 | M3 Luna 98: 30/10/20/0, 0,500 [0,383–0,633], 8/4/7/11 | EXP-070 | OK | |
| 06:52 | „51, illetve 49 helyes válasz a 60-ból” | EXP-060/070 | OK | |
| 06:53–55 | 27 lap GLM: M2−M3 „+0,267, 95% CI +0,133 és +0,400”, M1−M2 „−0,150; −0,267 és −0,033”, „szignifikánsan” | EXP-060; pairs.csv | OK | mindkét CI kizárja a 0-t |
| 06:55 | „Lunával ott egyik különbség sem szignifikáns (EXP-060)” | EXP-060 pairs.csv (mindhárom luna-CI tartalmazza a 0-t) | OK | |
| 06:56 | 98 lap GLM M1−M2 „−0,183; −0,317 és −0,050”, „szignifikánsan” | EXP-070 pairs.csv | OK | |
| 06:57 | 98 lap GLM M2−M3 „a határon (+0,117; 0,000 és +0,233)” | EXP-070 pairs.csv [0,0; 0,2333] | OK | helyesen határesetként szerepel |
| 06:57–58 | 98 lap Luna M1−M3 „+0,217, +0,100 és +0,333”, M2−M3 „+0,200, +0,050 és +0,350”, „szignifikánsan” | EXP-070 pairs.csv | OK | |
| 06:58–61 | „A gráfos módszerek pontossága a két méret között alig változott (az M2 GLM-mel 51-ről 49-re, Lunával 41-ről 42-re, az M1 Lunával 43 maradt)” | EXP-060/070 | ELTÉRÉS | a felsorolt számok helyesek, de a negyedik gráfos párosítás, az M1 GLM-mel, kimaradt, pedig ott változott a legtöbbet: 42 → 38 (0,700 → 0,633). Az „alig változott” így szelektív |
| 06:61 | M3 „GLM-mel 35-ről 42-re …, Lunával 39-ről 30-ra” | EXP-060/070 | OK | |
| 06:61–62 | „A 720 válaszból három hallucinált” | EXP-060/070 (2 × 6 × 60 = 720; halluc.: 27 lap 1+1, 98 lap 1) | OK | csak a 60 kérdéses sorokra igaz; az (e) családdal együtt 864-ből 4 (EXP-061 M2 GLM +1) |
| 06:66 | „tizenkét adatlap-darabot kap promptban” | `src/plantqa/methods/m3.py` `TOP_K = 12` | OK | kódbeli paraméter |
| 06:69–70 | „M3 GLM … rajzi kérdések közül csak 6-ot … a 15-ből, … a 9 nem helyes válaszból 8 téves „nincs benne”” | EXP-060 (a=6/15), EXP-062; failure_kinds újrafuttatva | OK | |
| 06:70 | „a kis üzemen egyetlen ilyen eset sem (EXP-062)” | EXP-062 | OK | |
| 06:70–72 | „A 98 lapos üzemen ugyanez a párosítás 11 rajzi kérdést oldott meg, téves „nincs benne” nélkül, a Luna viszont 12-ről 8-ra esett (EXP-067)” | a 11 és a 8: EXP-070; a 12: EXP-060; a „nincs benne” hiánya: EXP-067 | ELTÉRÉS | a számok helyesek, de a hivatkozás hiányos: a 11, a 12 és a 8 helyes válaszszám nem az EXP-067-ből, hanem az EXP-060-ból és EXP-070-ből jön (az EXP-067 csak a hibafajtákat adja) |
| 06:82 | M1 GLM: 0,00335 / 0,00345 USD; 17,9 / 18,0 s | EXP-060/070 (0,200893/60; 0,206715/60; 17,94; 17,95) | OK | |
| 06:83 | M2 GLM: 0,00344 / 0,00355; 12,4 / 15,4 | EXP-060/070 | OK | |
| 06:84 | M3 GLM: 0,00133 / 0,00844; 15,9 / 3,2 | EXP-060/070 | OK | |
| 06:85 | M1 Luna: 0,01027 / 0,00649; 14,7 / 14,5 | EXP-060/070 | OK | |
| 06:86 | M2 Luna: 0,00227 / 0,00220; 16,9 / 15,7 | EXP-060/070 | OK | |
| 06:87 | M3 Luna: 0,00680 / 0,02409; 6,4 / 6,5 | EXP-060/070 | OK | |
| 06:91–92 | „A gráfos módszerek kérdésenkénti költsége a 27 és a 98 lap között gyakorlatilag nem változott (az M2 GLM-mel 0,00344 és 0,00355 USD, Lunával 0,00227 és 0,00220 USD)” | EXP-060/070 | ELTÉRÉS | a zárójeles számok helyesek, de az általánosítás az M1 Lunával párosításra nem igaz: 0,01027 → 0,00649 USD (−37%). A bekezdés 95–96. sora ezt maga is kimondja, így a szöveg önellentmondó |
| 06:93–94 | „GLM-mel 0,00133-ról 0,00844 USD-re, Lunával 0,00680-ról 0,02409 USD-re” | EXP-060/070 | OK | az arány 6,3×, illetve 3,5× |
| 06:94–95 | „Lunával több mint tízszer drágább kérdésenként, mint az M2, és kevesebb helyes választ ad” | EXP-070: 0,02409 / 0,00220 = 10,95; helyes 30 < 42 | OK | |
| 06:95–96 | „Az M1 Lunával a 98 lapos üzemen olcsóbb volt, mert több kérdést zárt le már a Cypher-szinten” | EXP-060/070 summary.csv (0,01027 → 0,00649); routes.csv (cypher-v2t 35 → 40) | OK | |
| 06:97 | „3,2 s-os medián késleltetés” | EXP-070 (3,20 s) | OK | |
| 06:101–103 | M1 útvonalak: GLM 32/8/20 és 29/10/21; Luna 35/5/20 és 40/7/13 | `runs/EXP-060/routes.csv`, `runs/EXP-070/routes.csv` | OK | az EXP-sor szövege nem írja ki, de a kimeneti mappában van |
| 06:105 | M2 útvonalak: GLM 20/20/20 és 20/21/19; Luna 20/21/19 és 22/19/19 | routes.csv (drawing / datasheet / datasheet+drawing) | OK | |
| 06:110 | „a 12 kérdéses (e) családot” | EXP-052, EXP-065 | OK | |
| 06:111–112 | „két-három különböző adatlapot kell összevetni” | EXP-009 sor: „kérdésenként 2–3 különböző adatlap” (csak a kis üzem); `data/questions-pqb/complex.jsonl`, `data/questions-pqc/complex.jsonl` | ELTÉRÉS | a nagy üzemeken kérdésenként 2–6 különböző adatlap kell: 27 lapon 8 kérdésnél 2, 1-nél 3, 2-nél 5, 1-nél 6 (e01: 5, e02: 6, e03: 5); 98 lapon 9 kérdésnél 2, 1-nél 4, 1-nél 5, 1-nél 6 (e01: 4, e02: 6, e03: 5). A „2–3” csak a kis üzemre (EXP-009) igaz. Ez a szám egyik EXP-sorban sincs rögzítve |
| 06:112–113 | példakérdés: „Along the process flow path from E-1-1 to CHV-2-1, …” | `data/questions/complex.jsonl` e01 (kis üzem, EXP-009) | ELTÉRÉS | a példa a kis üzem kérdéssorából való, a bekezdés viszont a nagy üzemek (e) családjáról szól, EXP-052/065 hivatkozással. A nagy üzemen az e01: „Along the process flow path from P-1-1 to P-10-2, …” (PQB), illetve „from CHV-46-3 to CHV-50-1, …” (PQC) |
| 06:114 | „(EXP-008, EXP-052, EXP-065)” | EXP-008/052/065 | OK | |
| 06:119–124 | (e) táblázat: 6/2, 2/2; 5/3, 6/2; 0/0, 0/3; 6/3, 3/4; 6/2, 1/4; 0/0, 0/2 | EXP-061/071; summary.csv complex | OK | mind a 24 érték egyezik |
| 06:126 | „a kérdések felénél (5–6 kérdés a 12-ből)” | EXP-061 | OK | a zárójel pontosít (az M2 GLM-mel 5) |
| 06:127–128 | „az M1 és az M3 különbsége mindkét modellel +0,5 (95% CI +0,25 és +0,75), szignifikánsan (EXP-061)” | EXP-061 pairs.csv | OK | |
| 06:130 | „csak az M2 GLM-mel … (6 kérdés), szignifikánsan többet, mint az M3 (+0,5; +0,25 és +0,75)” | EXP-071; pairs.csv | OK | |
| 06:131 | „a többi párosítás 0–3 kérdést oldott meg (EXP-071)” | EXP-071 (2, 3, 1, 0, 0) | OK | |
| 06:133 | „az M2 mindkét modellel 3-3 kérdésnél üres választ adott mindkét méretnél (EXP-062, EXP-067)” | EXP-062/067; failure_kinds újrafuttatva | OK | megfogalmazás: mivel az üres válaszok száma a két méretnél azonos (3-3), az előző mondat „itt hamarabb elfogy” része nem a méret hatását mutatja; javasolt: „a lépés- és időkorlát ezeken a kérdéseken elfogyhat” |
| 06:138–140 | M3 GLM „27 lapon rajzi 8, több adatlapos 9; 98 lapon rajzi egyszer sem, több adatlapos 7” | EXP-062/067; failure_kinds újrafuttatva | OK | |
| 06:146–149 | „a 2 hüvelykes szabályozószelep teljesen nyitott Cv-értékére az M1 … feltétel nélkül” | `runs/EXP-060/scored.jsonl` b05, M1 GLM és Luna, „partial” | OK | |
| 06:160–161 | „egy következetlenséget is láttunk” | `docs/dontesek.md` 2026-10-31 21:45 | OK | döntésnapló, nem EXP-sor |
| 06z:5–8 | „két képernyőképen”, „további négy kérdését”, „hat kérdést … (a), (a), (b), (c), (d) és (e) … M1, M2 és M3 … GLM-mel; mind a hat … érdemi válasz” | EXP-040; `figures/demo/screens.csv` | OK | |
| 06z:22–23 | „6-os seedű üzeme, EXP-002”, „a négy lap között” | EXP-002 | OK | |
| 06z:30–31 | „EXP-020: 31 helyes a 40-ből”, „a nagy üzemen is (EXP-060: 51 helyes a 60-ból); ezt az oldal ki is írja” | EXP-020, EXP-060; `data/app/default_method.json` | OK | a számok helyesek. Két apróság: (1) most két nagy üzem van, mindkettőn az M2 GLM-mel a legjobb (49/60, EXP-070); (2) az oldal csak az EXP-020-at írja ki („best on the frozen test, EXP-020: 31/40”), az EXP-060-at nem |
| 06z:58–60 | „háromszor kérdezte a rajzeszközt, ebből kétszer … az ágensig jutott, egyszer a Cypher-szinten zárult; ezután az FT-2-2 adatlapját” | EXP-040; screens.csv útvonal: `drawing:cypher-v2t+agent-v2t` ×2, `drawing:cypher-v2t`, `datasheet:FT-2-2` | OK | |
| 06z:74 | „útvonal: `datasheet:GV-1-1`” | EXP-040; screens.csv | OK | |
| 06z:78–80 | idézett válasz („lists only a CE approval …”) | EXP-040; screens.csv | OK | |
| 07:103–104 | „négylapos …, 27 lapos és egy 98 lapos üzemen, üzemenként 60 kérdésen és 12 több adatlapos kérdésen” | EXP-002/051/064, EXP-052/065 | OK | |
| 07:108–110 | M1 „27 lapon GLM-mel 42, Lunával 43, a 98 lapon 38, illetve 43 helyes … a 60-ból” | EXP-060/070 | OK | |
| 07:111 | „GLM-mel mindkét méretnél … a legjobb (51, illetve 49 helyes)” | EXP-060/070 | OK | |
| 07:111–112 | „mindkét méretnél szignifikánsan megelőzte az M1-et” | EXP-060/070 pairs.csv (GLM M1−M2: [−0,267; −0,033], [−0,317; −0,050]) | OK | csak GLM-mel igaz (Lunával nem); a mondat GLM-ről szól, de érdemes kiírni |
| 07:112–113 | „az M2 előnye [az M3-mal szemben] a 27 lapon GLM-mel, mindkét gráfos módszeré a 98 lapon Lunával szignifikáns” | EXP-060/070 pairs.csv | OK | |
| 07:115–116 | RQ2: „A gráfos módszerek pontossága és kérdésenkénti költsége a 27 és a 98 lap között alig változott (az M2 GLM-mel 0,00344 és 0,00355 USD)” | EXP-060/070 | ELTÉRÉS | a zárójeles szám helyes, az általánosítás nem: az M1 Lunával kérdésenként 0,01027 → 0,00649 USD (−37%), az M1 GLM-mel pontosság 42 → 38 |
| 07:117 | „Lunával 0,00680-ról 0,02409 USD-re” | EXP-060/070 | OK | |
| 07:118 | „GLM-mel 35-ről 42-re …, Lunával 39-ről 30-ra” | EXP-060/070 | OK | |
| 07:125–127 | „A több adatlapos kérdések felét a 27 lapos üzemen a két gráfos módszer teljesen megoldotta” | EXP-061 (M1 6/6, M2 GLM 5, Luna 6) | ELTÉRÉS | kisebb pontatlanság: az M2 GLM-mel 5/12 (0,417), nem a fele |
| 07:127 | „csak az M2 GLM-mel oldott meg hatot (EXP-061, EXP-071)” | EXP-071 | OK | |
| 07:128–129 | „A 720 válaszból három volt hallucinált” | EXP-060/070 | OK | az RQ3 bekezdés az (e) családról is szól; a 720 csak a 60 kérdéses sorokra igaz (az (e)-vel együtt 864-ből 4). Javasolt kiírni: „a 60 kérdéses sorok 720 válaszából” |
| 07:133–135 | „három szintetikus üzemre (4, 27 és 98 lap)”, „a hét adatlap” | EXP-002/051/064; EXP-005 | OK | |
| 07:139 | „Üzemenként és családonként 15 kérdés” | EXP-004/052/065 | OK | |
| kivonat:5 | „négylapos …, 27 lapos és egy 98 lapos …, üzemenként 60 kérdésen és 12 …, két modellel” | EXP-002/051/064/052/065 | OK | |
| kivonat:5 | „GLM-5.3 Flash … (51, illetve 49 helyes válasz a 60-ból), szignifikánsan megelőzve az összevont gráfon dolgozó módszert” | EXP-060/070 + pairs.csv | OK | |
| kivonat:5 | „A gráfos módszerek pontossága és kérdésenkénti költsége a két méret között alig változott” | EXP-060/070 | ELTÉRÉS | ugyanaz, mint a 07:115-nél (M1 Luna költség −37%, M1 GLM pontosság 42 → 38) |
| kivonat:5 | „a gráf nélküli alapmódszer költsége … nőtt (az egyik modellel 3,5-szeresére)” | EXP-060/070: Luna 0,02409 / 0,00680 = 3,54 | OK | igaz, de a kisebbik arányt mondja; GLM-mel 0,00844 / 0,00133 = 6,3×. Javasolt: „3,5-, illetve 6,3-szorosára” |
| kivonat:5 | „A több adatlapos kérdések felét a 27 lapos üzemen a gráfos módszerek teljesen megoldották, a gráf nélküli egyet sem” | EXP-061 | ELTÉRÉS | kisebb pontatlanság: az M2 GLM-mel 5/12 |
| abstract:5 | „four-sheet …, 27-sheet and a 98-sheet …, on 60 questions and 12 questions …, with two models” | mint fent | OK | |
| abstract:5 | „router with GLM-5.3 Flash was best (51 and 49 of 60 correct), significantly ahead of the merged-graph method” | EXP-060/070 + pairs.csv | OK | |
| abstract:5 | „The accuracy and per-question cost of the graph-based methods barely changed” | EXP-060/070 | ELTÉRÉS | mint a kivonatnál |
| abstract:5 | „(3.5-fold with one model)” | EXP-060/070 | OK | mint a kivonatnál: GLM-mel 6.3-fold |
| abstract:5 | „the graph-based methods fully solved half of the multi-datasheet questions, the graph-free baseline none” | EXP-061 | ELTÉRÉS | kisebb pontatlanság: az M2 GLM-mel 5/12 |

## Összesítés státuszonként

- **OK:** 119 táblázatsor. Ebben benne van a 06:37–48 fősoros táblázat 12 sora (soronként 11 érték), a költség- és késleltetéstáblázat 6 sora (soronként 4 érték) és az (e) táblázat egy sorban (24 érték). Egyenként számolva az ellenőrzött számértékek száma kb. 350.
- **ELTÉRÉS:** 12 tétel (8 különböző probléma, P1–P8; a P5 és a P6 a 07-ben, a kivonatban és az abstractban is előfordul).
- **NINCS FORRÁS:** 0 tétel. Négy kódbeli paraméternek nincs EXP-sora, de a kódban megvan: a kis üzem 20–40 / 2–4 határa, a 120–400 / 24–40 és az 500–1500 / 90–115 elfogadási határ, a bootstrap 10 000, valamint az M3 12 darabja. Ugyanez igaz az útvonalszámokra (`routes.csv`) és a demóútvonal részleteire (`screens.csv`): ezek az EXP-sor kimeneti mappájában vannak, csak az eredmény szövegében nem. Az egyetlen szám, amelynek a jelenlegi alakja egyik forrással sem egyezik, a „két-három adatlap” (P4).

A táblázat soraiban a szignifikanciára vonatkozó minden állítás egyezik a `pairs.csv` CI-ivel. A 98 lapos GLM M2−M3 különbség ([0,000; 0,233]) helyesen határesetként szerepel. Az EXP-071 határesetes CI-it (GLM M1−M2, M1−M3; Luna M1−M2, M1−M3, M2−M3) a szöveg nem nevezi szignifikánsnak.

## Problémák és javasolt javítások

**P1 – 03-adatok.md:42–43, nem egyértelmű arány.**
Jelenleg: „A két nagy üzem így körülbelül 7-szer, illetve 25-ször nagyobb a kis üzemnél.”
Javasolt: „A két nagy üzem így lapszámban körülbelül 7-szer, illetve 25-ször, a tagelt elemek
számában 7-szer, illetve 29-szer nagyobb a kis üzemnél.” (27/4 = 6,75; 98/4 = 24,5; 190/26 = 7,3;
765/26 = 29,4; EXP-002, EXP-051, EXP-064.)

**P2 – 06-kiertekeles.md:58–61, szelektív felsorolás.**
Jelenleg: „A gráfos módszerek pontossága a két méret között alig változott (az M2 GLM-mel 51-ről
49-re, Lunával 41-ről 42-re, az M1 Lunával 43 maradt), …”
Javasolt: „A gráfos módszerek pontossága a két méret között kevéssé változott (az M2 GLM-mel
51-ről 49-re, Lunával 41-ről 42-re, az M1 Lunával 43 maradt, GLM-mel 42-ről 38-ra csökkent), …”

**P3 – 06-kiertekeles.md:72, hiányos hivatkozás.**
Jelenleg: „… a Luna viszont 12-ről 8-ra esett (EXP-067).”
Javasolt: „… a Luna viszont 12-ről 8-ra esett (EXP-060, EXP-070; a hibafajták: EXP-062, EXP-067).”

**P4 – 06-kiertekeles.md:111–113, az adatlapok száma és a példakérdés nem a nagy üzemekre vonatkozik.**
Jelenleg: „… és két-három különböző adatlapot kell összevetni (például „Along the process flow path
from E-1-1 to CHV-2-1, which item has the lowest maximum allowable pressure according to its
datasheet?”).”
Javasolt: „… és kérdésenként két–hat különböző adatlapot kell összevetni (a 27 lapos üzemen 8, a
98 lapos üzemen 9 kérdésnél kettőt, a leghosszabb utaknál négyet–hatot; például „Along the process
flow path from P-1-1 to P-10-2, which item has the lowest maximum allowable pressure according to its
datasheet?”, amely öt adatlapot érint).” Forrás: `data/questions-pqb/complex.jsonl` és
`data/questions-pqc/complex.jsonl` `documents` mezője. Az adatlapszámot érdemes az EXP-052 és az
EXP-065 eredménysorába is felvenni (pl. „kérdésenként 2–6 különböző adatlap”), mert jelenleg egyik
sor sem rögzíti. Ha a kis üzem példáját akarjátok megtartani, írjátok mellé: „(a kis üzem
kérdéssorából, EXP-009)”.

**P5 – a költség általánosítása (06-kiertekeles.md:91; 07-osszefoglalas.md:115–116; kivonat.md:5;
abstract.md:5).** Az M1 Lunával párosítás kérdésenkénti költsége 0,01027 → 0,00649 USD (−37%), ezért a
„gráfos módszerek költsége alig / gyakorlatilag nem változott” állítás nem igaz minden gráfos
párosításra. A pontos állítás az, hogy egyik gráfos párosítás költsége sem nőtt érdemben (legfeljebb +3%).
- 06:91 javasolt: „A gráfos módszerek kérdésenkénti költsége a 27 és a 98 lap között nem nőtt (az
  M2 GLM-mel 0,00344 és 0,00355 USD, Lunával 0,00227 és 0,00220 USD; az M1 GLM-mel 0,00335 és
  0,00345 USD, Lunával 0,01027-ről 0,00649 USD-re csökkent), mert …”
- 07:115 javasolt: „A gráfos módszerek pontossága kevéssé változott, kérdésenkénti költségük pedig
  nem nőtt a 27 és a 98 lap között (az M2 GLM-mel 0,00344 és 0,00355 USD), …”
- kivonat javasolt: „A gráfos módszerek pontossága kevéssé változott, kérdésenkénti költségük nem
  nőtt a két méret között, …”
- abstract javasolt: „The accuracy of the graph-based methods changed little and their per-question
  cost did not grow between the two sizes, …”

**P6 – „felét” a több adatlapos kérdéseknél (07-osszefoglalas.md:125–127; kivonat.md:5;
abstract.md:5).** A 27 lapos üzemen a négy gráfos párosításból három 6/12, de az M2 GLM-mel 5/12
(EXP-061).
- 07 javasolt: „A több adatlapos kérdések közel felét (5–6-ot a 12-ből) a 27 lapos üzemen a két
  gráfos módszer teljesen megoldotta, …”
- kivonat javasolt: „A több adatlapos kérdések közel felét (5–6-ot a 12-ből) …”
- abstract javasolt: „… fully solved about half (5–6 of 12) of the multi-datasheet questions …”

**P7 – kisebb pontosítások (nem hibák, a számok helyesek):**
- kivonat/abstract „3,5-szeresére” / „3.5-fold”: igaz (Luna), de GLM-mel 6,3×. Javasolt: „(a két
  modellel 6,3-, illetve 3,5-szeresére)” / „(6.3- and 3.5-fold with the two models)”.
- 06:24–26: „a gráf nélküli M3 30, az M1 25” → „GLM-mel a gráf nélküli M3 30, az M1 25”.
- 07:128: „A 720 válaszból” → „A 60 kérdéses sorok 720 válaszából”.
- 06z:30–31: „és a nagy üzemen is (EXP-060: 51 helyes a 60-ból)” → „és mindkét nagy üzemen is
  (EXP-060: 51, EXP-070: 49 helyes a 60-ból)”. Az „ezt az oldal ki is írja” csak az EXP-020-as
  indoklásra igaz (`data/app/default_method.json`).
- 06:132–133: az M2 üres válaszai mindkét méretnél 3-3-at tesznek ki, ezért az „itt hamarabb elfogy”
  nem a méret hatását mutatja; javasolt: „… és a lépés- és időkorlát ezeken a kérdéseken elfogyhat:”.

**P8 – naplózási javaslat (nem a dolgozat hibája).** A 03-ban idézett elfogadási határok (20–40 / 2–4,
120–400 / 24–40, 500–1500 / 90–115) csak a `src/plantqa/plant/spec.py`-ban szerepelnek; érdemes
az EXP-002, EXP-051 és EXP-064 sorába is beírni. Ugyanez igaz a P4-ben említett adatlapszámra.

## Javítások (alkalmazva 2026-11-01)

Mind a 8 problémát a javaslat szerint javítottuk: (1) a méretarány lapszámban és tagszámban külön;
(2) az M1 GLM 42 → 38 bekerült, „alig” helyett „kevéssé”; (3) a hivatkozás EXP-060/070 + a
hibafajták EXP-062/067; (4) „két–hat különböző adatlap” és a 27 lapos üzem e01 példája (öt
adatlap), az adatlapszám az EXP-052/065 sorban; (5) „nem nőtt” / „did not grow”, az M1 két
párosításának költsége a 6. fejezetben; (6) „közel felét (5–6-ot a 12-ből)”; (7) GLM-értékek
megjelölve, 6,3- és 3,5-szeres, „a 60 kérdéses sorok 720 válaszából”, a demó-mondat, az üres
válaszok értelmezése; (8) az elfogadási határok az EXP-051 és EXP-064 sorban. Az előadás szövege
is igazítva.
