# STATUS

## 2026-10-31 09:20 — 0. és 1. fázis kész, 2. fázis részben

- **Kész:** felmérés (`docs/felmeres.md`); projektváz (uv path-függőségek, tesztek, ruff, mypy
  zöld); közös költségnapló és keret (`plantqa.costlog`); példa P&ID (seed 6, 26 tagelt elem,
  4 lap) és tag → adatlap hozzárendelés (`data/plant/`); rajzexport PDF; összevont gráf
  betöltője (`python -m plantqa.graph.load`), egyelőre a 3 kész Opus-eszközgráffal.
- **Folyamatban:** 4 adatlap Opus-feldolgozása al-sessionökben (Rosemount 3051, Worcester
  F51/F52, Swagelok MS-01-176, Alfa Laval M3).
- **Következő:** kérdéssor (3. fázis), M1/M2/M3 (4. fázis); a betöltés újrafuttatása, amint az
  Opus-gráfok elkészülnek.
- **Költés eddig:** 0,30 USD (Azure, listaár) / 20 USD.

## 2026-10-31 10:05 — 2. és 3. fázis kész, 4. fázis: módszerek kész, első dev-mérés fut

- **Kész:** összevont gráf 6 eszközgráffal (a Rosemount Opus-feldolgozása még fut) + vektorok;
  kérdéssor (60 kérdés, teszt befagyasztva, hash az `eredmenyek.md`-ben); közös LLM-réteg
  (pinek, mérő, cache, költségnapló); M1 (kiegészített cascade), M2 (router), M3 (baseline);
  futtató, pontozó, összesítő, ábramodul; demó-váz (`python -m plantqa.app`).
- **Fut:** EXP-010 (dev, GLM, mindhárom módszer); minta-elemzés (subagent).
- **Következő:** bírálat → EXP-010 sor; Rosemount-gráf betöltése; további dev iterációk.
- **Költés eddig:** ~0,33 USD / 20 USD.

## 2026-10-31 10:48 — 4. fázis kész (dev iterációk), 5. fázis: végső teszt fut

- **Kész:** mind a 7 adatlap Opus-gráfja; összevont gráf (EXP-005); dev iterációk: EXP-010
  (kiindulás), EXP-011 (M1 A2-szabályok, M2/M3 válaszszabály), EXP-012 (+ Rosemount) GLM-mel,
  EXP-013 Lunával (bírálat fut); módszerek befagyasztva; dolgozat 1–5. fejezet és függelék
  vázlata; minta-elemzés; irodalomjegyzék-alap; demó működik.
- **Fut:** EXP-020 (befagyasztott teszt, 6 párosítás); EXP-013 bírálata.
- **Következő:** bírálat → végső táblázat és ábrák; demó-képernyőképek; 6–7. fejezet, kivonat;
  előadás.
- **Költés eddig:** spent 0.7411 USD / 20 USD.

## 2026-10-31 13:36 — KÉSZ: minden fázis lezárva

- **Dolgozat:** `dolgozat/dolgozat.pdf` (50 oldal; forrás: `dolgozat/src/*.md`, építés:
  `node dolgozat/build/build.js` + `dolgozat/build/to_pdf.ps1`); számellenőrzés lefutott
  (`docs/szamellenorzes.md`: 209 OK, 9 probléma, mind javítva).
- **Előadás:** `eloadas/eloadas.pptx` (17 dia: 13 fő + 4 tartalék, előadói jegyzettel, natív
  diagramok az eredmény-CSV-kből; validálva), `eloadas/eloadas.pdf`.
- **Demó:** `uv run python -m plantqa.app` (http://127.0.0.1:8010), alapértelmezés M2 + GLM (a
  teszten legjobb, EXP-020: 31/40); 6 kérdés minden családból képernyőképpel (`figures/demo/`,
  EXP-040).
- **Mérések:** dev EXP-010–013, végső teszt EXP-020 (6 párosítás), kiegészítő (e) család EXP-030;
  minden sor a `docs/eredmenyek.md`-ben; ábrák: `uv run python -m plantqa.figures`.
- **Ellenőrzések:** pytest (18), ruff, ruff format, mypy zöld.
- **Költés:** 1,6342 USD / 20 USD (EXP-050).

### Ami kimaradt vagy eltér a tervtől, és miért
- **Tartály-, szint- és hőmérséklet-távadó-adatlap nincs:** a v1 generátor üzemét szivattyú,
  hőcserélő, globe-, gömb- és visszacsapó szelep, valamint P/F távadó alkotja; ehhez 3 új adatlap
  elég volt (`dontesek.md`).
- **A szabályozófunkciókhoz (FIC/PIC) nincs adatlap:** DCS-funkciók, gyártói adatlapjuk nem
  létezik (`data/plant/tags.json`).
- **Az adatlapok LLM-lépéseit Opus végezte, nem GLM:** a felhasználó kérése (a PROMPT 4. szabálya
  helyett); a meglévő eszközöknél az Opus-gráfok.
- **A POSC Caesar régi SPARQL-végpontja nem volt elérhető:** az új adatlapgráfokban csak az rds-
  és CFIHOS-illesztések szerepelnek.
- **(b)/(c) kérdés csak a 4 korábbi eszközről:** a gold pároknak a PROMPT szerint a plantdocs
  EXP-0026/0039-ből kell jönniük; a 3 új adatlapot az (e) család kérdezi (EXP-008/009/030).
- **LaTeX helyett docx → PDF:** a gépen nincs LaTeX, a PROMPT ilyenkor a docx utat írja elő.
- **Ember nem ellenőrizte** a referenciaválaszokat és a bírálatot (modell, vak subagent); ezt a
  dolgozat korlátként kimondja.
- **Futás közbeni javítások** (mind naplózva a `dontesek.md`-ben, a mérések újrapontozva): a
  jelzés + magyarázat megjelenítése és bírálói exportja; a TAG_PATH pontozás gold élei; egy
  hálózati hiba miatti újrapróbálás az M2/M3-ban.

## 2026-10-31 14:06 — v2: a főszöveg 31 oldal
- A BME VIK GYIK szerint a TDK-dolgozat „tipikus terjedelme 30–35 oldal + szükség esetén
  melléklet”. A főszöveg (Bevezetés → Összefoglalás) 40 oldalról 31-re csökkent; a részletek a
  Függelékbe kerültek: D. a két forrásfolyamat, E. a módszerek részletei, F. további
  demóképek. Szám nem változott, tartalom nem veszett el. Összesen 50 oldal.
- Az első változat: `dolgozat/v1/` (pdf, docx, forrás, előadás).
- Az MI-munkafolyamatról szóló mondat kikerült a dolgozatból és az előadásból.
- Építési javítás: a számozott listák mindig 1-től indulnak, és a többsoros listaelemek egy
  bekezdésben maradnak.

## 2026-10-31 22:16 — v4: közös kiértékelés két nagy üzemen
- A felhasználó és a konzulens kérésére a közös mérés nagyobb üzemeken is lefutott: 27 lap (PQB,
  EXP-051..063) és 98 lap (PQC, EXP-064..071), ugyanazzal a generátorral és hét adatlappal, a kis
  üzemen befagyasztott módszerekkel. A 6. fejezet a két nagy üzemet skálázási sorként mutatja be,
  a kis üzem a Függelék G-be került. Fő eredmény: mindkét méretnél az M2 GLM a legjobb (51 és 49 /
  60); a gráf nélküli M3 költsége a rajzzal nő (Lunával 0,00680 → 0,02409 USD/kérdés), a gráfos
  módszereké nem.
- Bevezetés, kivonat és abstract átírva (két rész, definiálatlan szakszavak nélkül); a v1, v2
  változat megmaradt (`dolgozat/v1`, `dolgozat/v2`).
- Számellenőrzés: `docs/szamellenorzes-v4.md` (119 OK, 8 probléma, mind javítva).
- Dolgozat: 59 oldal, ebből a főszöveg 34; előadás: 17 dia, validálva.
- Költés: 6,8879 USD / 20 USD (EXP-068). Tesztek, ruff, mypy zöld.
