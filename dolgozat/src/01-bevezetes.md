# Bevezetés

Egy ipari üzemet sokféle dokumentum ír le. A csővezeték- és műszerezési rajzok (angol rövidítéssel
P&ID) megmutatják, hogyan kapcsolódnak egymáshoz a berendezések, szelepek és műszerek; a gyártói
adatlapok megadják, mire képes az egyes eszköz. A rajzon minden elemnek egyedi azonosítója, tagje
van (például P-101 egy szivattyú), és ez köti össze a rajzot az eszköz adatlapjával. Egy
üzemeltető vagy tervező mérnök kérdései gyakran mindkét dokumentumfajtát érintik: „Mekkora a
megengedett legnagyobb nyomás azon a szelepen, amely a P-101 szivattyú nyomóoldalát elzárja?” A
válaszhoz előbb a rajzon kell megtalálni a szelepet (a vezeték akár egy másik rajzlapon is
folytatódhat), majd a tagje alapján az adatlapját, és abban a megfelelő feltételhez tartozó
értéket. Ma ezt kézzel végzik.

A nagy nyelvi modellek (LLM) kézenfekvő eszköznek tűnnek, de az üzemi dokumentáció nehéz terep
számukra. A lényeges információ gyakran nem egyetlen elemben van, hanem a kontextusban: egy
táblázat fejlécében, egy értéket korlátozó lábjegyzetben, vagy egy lapközi csatlakozóban, amely
egy csővezetéket egy másik lapon folytat. Ezt a szerkezetet egy tudásgráf teheti explicitté:
olyan adatbázis, amelyben a dolgok csúcsok, a köztük lévő kapcsolatok élek, és amelyből a modell
a kérdéshez tartozó részt visszakeresve válaszol (az angol szakirodalomban: GraphRAG). Ez azonban
csak akkor működik, ha a gráf megőrzi a kontextust.

A munka két részből épül fel, mindkettő az egyik szerző egyéni munkája.

- **A rajzoldali rész** (Kiszely Benedek) az egész üzemet leíró tudásgráfot épít a rajzlapokból:
  a berendezések és műszerek csúcsok, a csövek és jelvezetékek élek, és a lapok határán
  megszakadó vezetékek újra összekapcsolódnak. Erre a gráfra építve egy kétlépcsős rendszer
  válaszol a kérdésekre: először egyetlen adatbázis-lekérdezéssel próbálkozik, és ha ez nem
  elég, egy gráfbejáró eszközöket hívó LLM-ágens veszi át a kérdést. A rész fő kérdése, hogy ez
  a megközelítés több száz, akár ezer lapos üzemen is működik-e.
- **Az adatlapoldali rész** (Szabó Zsombor) egy-egy eszköz PDF-adatlapjából épít tudásgráfot,
  amelyben minden érték mellett megmarad a mértékegysége, az érvényességi feltétele (például
  „csak 100 °F alatt”) és a forrásoldala, mert egy feltétel nélküli érték nem hiányos, hanem
  hibás. A gráf nemzetközi ipari szabványok szókészletére épül, ezeket a 2. fejezet mutatja be.

Ebben a dolgozatban a két részt összekapcsoljuk: a rajzi gráf elemeit a tagjük alapján az
adatlapgráfokhoz kötjük, és megmérjük, mennyire jól válaszolnak a rendszerek a két
dokumentumfajtát együtt igénylő kérdésekre. A módszereket egy kis, négylapos üzemen fejlesztettük,
majd változtatás nélkül egy hétszer nagyobb, 27 lapos üzemen mértük meg.

## Kutatási kérdések

- **RQ1.** Megválaszolhatók-e a rajzot és az adatlapot összekötő kérdések egyetlen összevont
  tudásgráfon (M1), és hogyan viszonyul ennek pontossága egy olyan irányítóéhoz (router, M2),
  amely a két rész meglévő rendszerét külön hívja, illetve egy gráf nélküli alapmódszeréhez
  (baseline, M3)?
- **RQ2.** Hogyan változik a módszerek pontossága és költsége, ha a négylapos üzemről a 27
  laposra lépünk, a módszerek változtatása nélkül?
- **RQ3.** Mely kérdéscsaládokon segít a gráf, és milyen hibák jellemzők az egyes módszerekre?

## Hozzájárulások

1. Két közös példaüzem: egy négylapos, 26 tagelt elemes és egy 27 lapos, 190 tagelt elemes P&ID
   ugyanazzal a generátorral, amelyek elemeihez program rendeli hozzá hét eszköz gyártói
   adatlapját.
2. Az összevont tudásgráf: a rajzi üzemi réteg és hét eszköz adatlapgráfja egy
   Neo4j-adatbázisban, egy tagalapú kapcsolattal összekötve, egy paranccsal újratölthetően.
3. Három kérdés-válaszoló módszer a két rész meglévő kódjára építve: a rajzoldali rendszer
   kiegészítése az adatlapréteggel és egy új adatlap-eszközzel (M1), egy irányító a két rendszer
   fölött (M2) és egy gráf nélküli alapmódszer (M3).
4. Üzemenként egy 60 kérdéses, négy családra bontott kérdéssor és 12 több adatlapot összevető
   kérdés, részben programmal, részben modellel előállított referenciaválaszokkal; a három módszer
   mért összehasonlítása két modellel mindkét üzemen.
5. Egy webes demó, amely bármely módszerrel válaszol, és megmutatja az útvonalat, a
   lekérdezéseket és az adatlapi forrásoldalakat.

## Munkamegosztás

A rajzoldali rendszer (generátor, lapokra bontás, üzemi gráf, kaszkád) Kiszely Benedek, az
adatlapoldali rendszer (feldolgozó folyamat, ISO 15926 gráf, A2-lekérdezés) Szabó Zsombor egyéni
munkájának eredménye; ezeket változtatás nélkül használjuk. Az összevonást, a kérdéssort, a három
módszert, a mérést és a demót közösen készítettük. A döntéseket és a mért számokat a projekt
naplói rögzítik (`docs/dontesek.md`, `docs/eredmenyek.md`).

## A dolgozat felépítése

A 2. fejezet a hátteret és a kapcsolódó munkákat foglalja össze. A 3. fejezet bemutatja a
két példaüzemet, az adatlapokat és a kérdéssort, a 4. fejezet az összevont tudásgráfot, az 5. fejezet a
három módszert. A 6. fejezet a nagy üzemen mért eredményeket, a 7. fejezet a demót és egy esettanulmányt, a 8. fejezet a következtetéseket és a
korlátokat tárgyalja. A Függelék a példakérdéseket (A), a két módszer promptjainak részleteit (B, C),
a két forrásfolyamat részletes leírását (D), a módszerek lépéseinek részleteit (E), további
demó-képernyőképeket (F) és a kis üzemen végzett mérések teljes leírását (G) tartalmazza.
