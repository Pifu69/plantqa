
# Feladat: közös P&ID + adatlap kérdés-válasz rendszer és TDK-dolgozat, ember nélkül

MEGALLAS_IRAS_ELOTT: nem
<!-- "igen" esetén a 6. fázis előtt állj meg, és írj összefoglalót a STATUS.md-be. -->

Ma 2026-10-31 (szombat) van. **Határidő: 2026-11-01 (vasárnap) 10:00**, ekkorra a dolgozatnak és az előadásnak késznek és commitolva kell lennie. Az időt a rendszeróra alapján követed (`date`). A fázisoknál megadott időpontok a legkésőbbi határok, nem célok. Ha egy fázis végén késésben vagy, azonnal alkalmazod a „Ha csúszol” rész vágásait. Végig önállóan dolgozol, emberi ellenőrzés nincs. Ha döntést kell hoznod, döntsd el, és egy sorban rögzítsd a `docs/dontesek.md`-ben (mit, miért, mi lett volna a másik út). Kérdezni nem kell.

## Kiinduló helyzet

Két kész szakdolgozati kódbázis van, mindkettő Python + uv + Neo4j + OpenRouter.

- **`../plantdocs`** (Szabó Zsombor István): egyetlen eszköz gyártói adatlap PDF-jéből ISO 15926 tudásgráfot épít (01–10. lépés), és kérdezhető webappot ad hozzá (`python -m plantdocs.app`). A kérdésekre két módszerrel válaszol: A1 (RDF + SPARQL) és A2 (Neo4j + Cypher). Ebben a munkában **az A2 az alap**. Kész, feldolgozott eszközök a `data/documents/` alatt: `fisher-et-d100022x012` (szabályozószelep), `gfps-165-solenoid-valve` (mágnesszelep), `gorman-rupp-0700286` (szivattyú), `rosemount-3051-00813-0100-4001` (nyomástávadó). Olvasd el: `README.md`, `docs/private/00-index.md`, `docs/private/30-experiments/_results.md` (EXP-0026…0042), `src/plantdocs/qa/`, `src/plantdocs/graph/neo4j_load.py`, `src/plantdocs/app/`.
- **`../Thesis`** (Kiszely Benedek, csomag: `plantgraph`): seedelt pyDEXPI-generátor taggel ellátott üzemekhez, lapokra bontás off-page csatlakozókkal (a bontás egyben a megoldókulcs), Neo4j-betöltés, és cascade QA: először Cypher, ha az bizonytalan, üzemi primitívekkel dolgozó ágens. A README `cascade_v3`-at ír, de a legfrissebb commitokban már `cascade_v4_iso` szerepel. A legújabb, mért policy-t használd, és a git logból meg a `docs/`-ból döntsd el, melyik az. Baseline: ContextRAG. Benedek még dolgozik a repón. Van webes demója és rajzexportja is (`plantgraph.demo`). Olvasd el: `README.md`, `data/README.md`, `src/plantgraph/benchmark/`, `qa/`, `store/`, `llm/` (spend guard, válaszcache), `demo/`.

**A két forrásrepó csak olvasható.** Nem módosítod őket. Ami kell belőlük, azt uv path-függőségként importálod (`plantdocs = { path = "../plantdocs", editable = true }`, `plantgraph = { path = "../Thesis", editable = true }`). Kódot csak akkor másolsz át, ha importálni nem lehet, és ezt a `docs/dontesek.md`-ben rögzíted.

## A cél

Egyetlen bemutatható példa: egy közepesen bonyolult P&ID, amelynek **minden tagelt eleméhez tartozik egy adatlap PDF**. Bármit lehet róla kérdezni, akár csak a rajzról („mi van a P-101 után?”), akár csak egy eszközről („mekkora a PT-101 méréshatára?”), akár a kettőt összekötve („mekkora a maximális nyomás azon a szelepen, amely a P-101 nyomóoldalát elzárja?”). Ugyanúgy kipróbálható legyen, mint ma a plantdocs app. Ehhez kell három módszer, mért összehasonlítás, a dolgozatba írható közbenső számok és ábrák, végül a dolgozat és az előadás.

## Kemény szabályok

1. **Nincs kitalált szám.** Minden szám, ami dokumentumba, ábrára vagy diára kerül, egy ténylegesen lefutott mérésből jön, és egy sorként szerepel a `docs/eredmenyek.md`-ben (EXP-azonosító, dátum, modell ID, parancs, kimeneti mappa). Minden ábra és táblázat felirata megnevezi az EXP-et. Amit nem mértél meg, arra azt írod, hogy nincs mérve. A két forrásrepó számait csak a saját `_results.md`-jükre, illetve README-jükre hivatkozva idézheted.
2. **Költségkorlát: összesen 20 USD** fizetős hívásra, az adatlap-pipeline futásokkal együtt. Minden LLM-hívás közös spend guardon megy át (Benedek `llm/` spend guardja vagy egy azonos elvű saját), és a `logs/koltseg.jsonl`-ba kerül. 18 USD-nál már nem indítasz új mérést, csak a meglévő cache-ből dolgozol. Ahol lehet, cache-t használsz, és ismételt futásnál nem fizetsz újra.
3. **Kulcs:** `OPENROUTER_API_KEY` a `.env`-ből (Benedek kulcsa). Soha nem írod ki, nem logolod, nem commitolod. A `.env` a `.gitignore`-ba kerül.
4. **Modellek:** az új adatlapok pipeline-jának LLM-lépéseit (02/03/04/06/08) te és a subagentjeid végzitek `claude-opus-5-5`-tel, ugyanazokkal a plantdocs promptfájlokkal; a 09. lépés és az összekötés `z-ai/glm-5.3-flash` OpenRouteren át (felhasználói döntés, 2026-10-31). A kérdés-válaszolást **mindkét** modellel méred: `z-ai/glm-5.3-flash` és GPT-6 Luna. A GPT-6 Luna Benedek futásaiban `openai/gpt-6-luna`. A teljes pint (ID és paraméterek) az ő pin JSON-jából veszed. Minden futás jelentése megnevezi a modell ID-t.
5. **Bírálat:** a válaszokat vakon, Claude Code subagentek pontozzák (ahogy a plantdocs EXP-0026/0039-ben). A subagent nem látja, melyik módszer és melyik modell adta a választ. Ahol a válasz programmal ellenőrizhető (tagek halmaza, számérték és mértékegység), ott programmal pontozol, és a subagent csak a maradékot bírálja.
6. **Stílus** (mindkét forrásrepóval egyezően): azonosítók, hibaüzenetek, commit-üzenetek angolul; docstringek, kommentek és a `docs/` próza magyarul. Kis függvények, type hintek, fájlonként legfeljebb 400 sor. `uv run pytest`, `ruff check`, `ruff format --check` és `mypy` zöld legyen, mielőtt egy fázist késznek mondasz.
7. **Git:** helyben commitolsz, a felhasználó nevében, Claude-trailer nélkül. Nem pusholsz.
8. **Nincs kitalált szókészlet:** az adatlapoldali fogalmak a plantdocs ISO 15926 / QUDT leképezését követik, a rajzoldaliak Benedek DEXPI-sémáját.

## Fázisok

Minden fázis végén frissíted a `STATUS.md`-t: mi kész, mi a következő, és mennyi pénz fogyott eddig.

### 0. Felmérés (időkeret: ~45 perc)

Olvasd el a két repót, és írd meg a `docs/felmeres.md`-t: a két Neo4j-séma (címkék, kapcsolatok, kulcsok), a két QA belépési pont, melyik plantdocs-eszköztípushoz milyen DEXPI-osztály tartozik, Benedek generátora milyen elemosztályokat tud, és hol van a két spend guard, illetve cache. Ellenőrizd, hogy a helyi Neo4j fut-e, és hogy a két csomag importálható-e.

### 1. A példa P&ID (legkésőbb szombat 13:00)

1. **Adatlap-leltár:** a 4 kész eszköz típusa (szivattyú, szabályozószelep, mágnesszelep, nyomástávadó). Ha a P&ID így nem elég sokszínű, keress **2–4 további nyilvános gyártói adatlapot** más elemtípusokra (pl. áramlásmérő, szintmérő, hőmérséklet-távadó, visszacsapó szelep, hőcserélő, tartály). A plantdocs `corpus/sources.py`-ban már szereplő jelöltekkel kezdd. Futtasd le rajtuk a plantdocs pipeline-t a 4. szabály szerinti modellekkel, a költséget logold. Csak megbízható gyártói oldalról tölts le, minden fájlt külön mappába.
2. **Generálás:** Benedek generátorával (seedelt, reprodukálható) olyan üzemet generálsz, amely **csak** olyan elemosztályokból áll, amelyekhez van adatlap. Ha a generátor nem korlátozható így, írj vékony szűrőt vagy saját, pyDEXPI-ra épülő specifikációt, és ezt rögzítsd. Célméret: kb. 20–40 tagelt elem, 2–4 lap, hogy legyen benne lapok közötti csatlakozó is. Közepesen bonyolult, de minden adatlaptípus legalább egyszer szerepeljen, és legyen több példány is ugyanabból a típusból (pl. P-101 és P-102 ugyanazzal az adatlappal).
3. **Hozzárendelés:** `data/plant/tag_to_datasheet.json` (tag → plantdocs document_id). Ezt a generátor kimenetéből program állítja elő, nem kézzel írod.
4. Rajzexport Benedek `demo.drawing` moduljával PDF-be. Ez kell a demóhoz és a dolgozat ábrájához is.

### 2. Összevont gráf (legkésőbb szombat 15:00)

Egy Neo4j-adatbázisba betöltöd Benedek összevont üzemrétegét és minden szükséges eszköz plantdocs A2-gráfját. Az eszközgráfok névtérrel kerülnek be, hogy ne ütközzenek. A kettőt egy, a tagen alapuló kapcsolat köti össze (pl. `(:Equipment {tag})-[:DESCRIBED_BY]->(eszköz-gyökércsúcs)`). A pontos címkéket a felmérésből veszed. A betöltés egyetlen paranccsal újrafuttatható legyen. Mérd és logold: csúcs- és élszám rétegenként, betöltési idő.

### 3. Kérdéssor és referenciaválaszok (párhuzamosan a 2. fázissal)

Kb. 60 kérdés, négy családban:

- **(a) csak rajz:** Benedek kérdéscsaládjai, az ő generátorával előállítva a gold gráfból;
- **(b) csak adatlap, tagen át:** „mekkora a PT-101 …?”. A válasz a plantdocs meglévő kérdés-válasz párjaiból (EXP-0026, EXP-0039) jön, a tagre leképezve;
- **(c) összetett, többlépéses:** egy topológiai lépés és egy adatlapi tény, pl. „a P-101 nyomóoldali elzárószelepének max. hőmérséklete”. A referenciaválaszt **program állítja össze** az (a) és (b) gold részekből, nem LLM találja ki;
- **(d) megválaszolhatatlan:** a dokumentumokban nincs benne, ilyenkor az elvárt válasz „nincs benne”.

Kettébontod: **dev (kb. 20)** a fejlesztéshez és a közbenső mérésekhez, **teszt (kb. 40)**, amelyet befagyasztasz (hash a `docs/eredmenyek.md`-ben), és csak a végső mérésnél futtatsz. A referenciaválaszok modellkészítésűek. Ezt a dolgozat módszertana kimondja.

### 4. Három módszer, a meglévő kódra építve (legkésőbb szombat 21:00)

- **M1 — egy gráf, egy lekérdezés:** az összevont Neo4j-gráfon egy LLM ír Cypher-t, mindkét réteg sémáját látva. Benedek legújabb cascade-jére épül: a meglévő Cypher-lépés és ágens kiegészül egy új primitívvel, amely egy tag eszközgráfjából a plantdocs A2 logikájával kér le tényt.
- **M2 — router:** egy ágens két eszközt hív: Benedek cascade-jét a rajzrészre és a plantdocs A2 `ask`-ot a tagből feloldott eszközre, majd összerakja a választ.
- **M3 — baseline:** ContextRAG / vektoros RAG. A P&ID szerializálva és az összes adatlap darabolva kerül be, gráf nélkül (Benedek ContextRAG-ja és a plantdocs vektoros keresése alapján).

Mindhárom módszer × két QA-modell. A dev halmazon iterálsz, és **minden iterációs mérést külön EXP-sorként rögzítesz**: ezek a közbenső számok a dolgozat „fejlődés” ábrájához kellenek. Kérdésenként mérd: helyesség (kérdéscsaládonként is), token, költség, késleltetés, és M1/M2 esetén a használt útvonal.

### 5. Végső mérés és demó (legkésőbb vasárnap 00:00)

1. A befagyasztott teszthalmaz egyszer fut le minden módszer × modell párosításon. Az eredmények táblázatba és ábrákba kerülnek (matplotlib, `figures/`, az ábrák forrásadata CSV-ben mellette). Minden ábra legenerálható egy paranccsal az eredményfájlokból.
2. **Demó:** a plantdocs app mintájára működő webapp. Bal oldalon a P&ID rajza, jobb oldalon a kérdés és a válasz. Látszik, melyik módszer és útvonal válaszolt, a Cypher-lekérdezés, és az adatlapi forrás (oldalszám vagy kivágás, ahogy a plantdocs app mutatja). Alapértelmezett módszer a teszten legjobb, a többi kiválasztható. Egy paranccsal induljon, és a `README.md` leírja, hogyan. Indítsd el, és saját magad kérdezz meg rajta legalább 5 kérdést, mindegyik családból. A képernyőképek a `figures/demo/`-ba kerülnek (dolgozatba és előadásba).

Ha `MEGALLAS_IRAS_ELOTT: igen`, itt megállsz.

### 6. Dolgozat (legkésőbb vasárnap 07:00)

1. **Mintaelemzés:** a `../plantdocs/docs/private/90-thesis/mintak/tdk-vik-intelligens-rendszerek/` mappában 16 díjazott BME VIK TDK-dolgozat van (Intelligens rendszerek szekció, 2019–2025), mindegyik saját almappában: `dolgozat.pdf`, `info.md`, és ahol van, `prezentacio.pptx` vagy `.pdf`. A mappa `README.md`-je az áttekintés. Ebből írd meg a `docs/minta-elemzes.md`-t. Szempontok: fejezetszerkezet, terjedelem, ábrák és táblázatok száma, a kutatási kérdés megfogalmazása, a kiértékelés bemutatása, hangnem, irodalomjegyzék mérete. Ebből írsz vázlatot.
2. **Dolgozat magyarul**, a minták formátumában (ha LaTeX-sablon van közöttük vagy elérhető LaTeX, akkor LaTeX → PDF; különben a docx skill, majd PDF). Cím: *Tudásgráf-építés műszaki rajzokból és adatlapokból skálázható Q&A rendszerhez*. Szerzők: Szabó Zsombor István, Kiszely Benedek. A témavezető neve helyén `[TÉMAVEZETŐ]` helyőrző áll, ha nincs meg a forrásokban. Kiindulópont az absztrakthoz: `../plantdocs/docs/private/90-thesis/absztrakt-tdk-kozos.md`, mért számokkal frissítve. A két egyéni munka saját eredményei (Benedek skálázási mérései, a plantdocs Stage 1–4 mérései) háttérként szerepelnek, a saját forrásukra hivatkozva. A súlypont az összevonás és annak mérése. Irodalom: a két repó irodalmi jegyzeteiből (`plantdocs/docs/private/10-literature/`, `Thesis/docs/`), csak ténylegesen ott szereplő művek.
3. **Önellenőrzés:** egy subagent végigmegy a kész dolgozaton, és minden számot visszakeres a `docs/eredmenyek.md`-ben vagy a hivatkozott forrásban. Ami nem található meg, azt javítod vagy törlöd.

### 7. Előadás (legkésőbb vasárnap 09:00)

Ugyanebből a mintamappából a 4 előadás alapján (Tarnay 2024, Bunda 2025, Juhász 2025, Tomori 2025; `prezentacio.*`) (diaszám, időtartam, szerkezet, ábrák aránya) pptx a pptx skill-lel. A dolgozat ábráiból és a demó képernyőképeiből dolgozz, minden szám ugyanabból a forrásból jöjjön. Előadói jegyzet diánként, magyarul.

### Tartalék (vasárnap 09:00–10:00)

Új munkát nem kezdesz. Lezárod a számellenőrzést, frissíted a `STATUS.md`-t, és mindent commitolsz.

## Ha csúszol

A határidő nem mozdul. Ebben a sorrendben vágj, és a vágást írd be a `docs/dontesek.md`-be:

1. GPT-6 Luna csak a teszthalmazon fut, a dev iterációk csak GLM-mel;
2. kevesebb új adatlap (szélső esetben csak a 4 meglévő típus);
3. kisebb teszthalmaz (de minden családból legalább 6 kérdés);
4. egyszerűbb demó (a plantdocs app minimális kiterjesztése).

Nem vágható: a három módszer mért összehasonlítása, a működő demó, a „nincs kitalált szám” szabály, a dolgozat és az előadás.

## Késznek akkor számít, ha

- `uv run python -m plantqa.app` (vagy a README-ben leírt parancs) elindítja a demót a példa üzemen, és mindegyik kérdéscsaládra érdemi választ ad;
- a `docs/eredmenyek.md` tartalmazza a dev iterációkat és a végső teszteredményt mind a 6 párosításra, a költséggel együtt;
- a `figures/` minden ábrája egy paranccsal újragenerálható;
- `dolgozat/` alatt kész PDF, `eloadas/` alatt kész pptx, és a számellenőrzés lefutott;
- tesztek, ruff és mypy zöld, minden helyben commitolva;
- a `STATUS.md` utolsó bejegyzése felsorolja, mi maradt ki és miért.

