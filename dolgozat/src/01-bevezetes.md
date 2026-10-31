# Bevezetés

Egy ipari üzemet több ezer oldalnyi, sokféle dokumentum ír le. A csővezeték- és műszerezési
rajzok (P&ID) megmutatják, hogyan kapcsolódnak egymáshoz a berendezések, szelepek és műszerek; a
gyártói adatlapok megadják, mire képes az egyes eszköz. Egy üzemeltető vagy tervező mérnök
kérdései gyakran mindkét dokumentumfajtát érintik. „Mekkora a megengedett legnagyobb nyomás
azon a szelepen, amely a P-101 szivattyú nyomóoldalát elzárja?” A válaszhoz előbb a rajzon kell
megtalálni a szelepet (ez akár egy másik lapon is folytatódhat), majd a tagje alapján az
adatlapját, és abban a megfelelő feltételhez tartozó értéket. Ma ezt kézzel végzik.

A nagy nyelvi modellek (LLM) kézenfekvő eszköznek tűnnek, de az üzemi dokumentáció nehéz terep
számukra. A lényeges információ gyakran nem egyetlen elemben van, hanem a kontextusban: egy
táblázat fejlécében, egy értéket korlátozó lábjegyzetben, vagy egy lapközi csatlakozóban, amely
egy csővezetéket egy másik lapon folytat. A gráfalapú visszakeresés-kiterjesztett generálás
(GraphRAG) ezt a szerkezetet teszi explicitté, de csak akkor, ha a gráf megőrzi a kontextust.

A két szerző egyéni munkája ugyanennek a dokumentációnak két oldalát dolgozta fel. Kiszely Benedek
munkája (plantgraph) a rajzoldalt vizsgálja üzemi méretben: seedelt, többlapos szintetikus üzemeket
generál, lapokra bontja őket, a lapokból tudásgráfot épít, és egy szabályozott kaszkáddal (előbb
egy Cypher-lekérdezés, szükség esetén gráfeszközöket hívó ágens) válaszol rajta. Szabó Zsombor
munkája (plantdocs) egy-egy eszköz gyártói adatlapjából épít ISO 15926 / QUDT szerinti
tudásgráfot, amelyben a feltételek és a kereszthivatkozások megmaradnak, és ezen kérdez
Cypher-rel. Ez a dolgozat a két munka összevonásáról és annak méréséről szól.

## Kutatási kérdések

- **RQ1.** Megválaszolhatók-e a rajzot és az adatlapot összekötő kérdések egyetlen összevont
  tudásgráfon (M1), és hogyan viszonyul ennek pontossága a két meglévő rendszert külön hívó
  routeréhez (M2) és egy gráf nélküli baseline-éhoz (M3)?
- **RQ2.** Mennyibe kerül az egyes módszer (token, költség, késleltetés), és hogyan függ ez a
  kérdés-válaszoló modelltől?
- **RQ3.** Mely kérdéscsaládokon segít a gráf, és milyen hibák jellemzők az egyes módszerekre?

## Hozzájárulások

1. Egy bemutatható példaüzem: egy seedelt, négylapos P&ID 26 tagelt elemmel, amelynek minden
   tagelt fizikai eleméhez gyártói adatlap tartozik; a hozzárendelést program állítja elő.
2. Az összevont tudásgráf: a rajzi üzemi réteg és hét eszköz adatlapgráfja egy
   Neo4j-adatbázisban, egy tagalapú kapcsolattal összekötve, egy paranccsal újratölthetően.
3. Három kérdés-válaszoló módszer a meglévő kódra építve: a kaszkád kiegészítése az
   adatlapréteggel és egy új adatlap-primitívvel (M1), egy router a két rendszer fölött (M2) és
   egy gráf nélküli baseline (M3).
4. Egy 60 kérdéses, négy családra bontott kérdéssor programmal előállított referenciaválaszokkal,
   befagyasztott teszthalmazzal, és ezen a három módszer mért összehasonlítása két modellel.
5. Egy webes demó, amely bármely módszerrel válaszol, és megmutatja az útvonalat, a
   lekérdezéseket és az adatlapi forrásoldalakat.

## Munkamegosztás és eszközhasználat

A rajzoldali rendszer (generátor, lapokra bontás, üzemi gráf, kaszkád) Kiszely Benedek, az
adatlapoldali rendszer (feldolgozó folyamat, ISO 15926 gráf, A2-lekérdezés) Szabó Zsombor egyéni
munkájának eredménye; ezeket változtatás nélkül használjuk. Az összevonást, a kérdéssort, a három
módszert, a mérést és a demót közösen készítettük. Mindkét egyéni munka és ez az összevonás is
mesterséges intelligenciával támogatott munkafolyamatban készült: a kódot, a méréseket és a szöveg
első változatát Claude Code (Anthropic) ügynök készítette a megadott feladatleírás alapján, a
döntéseket és a mért számokat a projekt naplói rögzítik (`docs/dontesek.md`,
`docs/eredmenyek.md`). A dolgozat minden száma egy ténylegesen lefutott mérésből származik.

## A dolgozat felépítése

A 2. fejezet a hátteret és a kapcsolódó munkákat foglalja össze. A 3. fejezet bemutatja a
példaüzemet, az adatlapokat és a kérdéssort, a 4. fejezet az összevont tudásgráfot, az 5. fejezet a
három módszert. A 6. fejezet a mérési eredményeket, a 7. fejezet a következtetéseket és a
korlátokat tárgyalja.
