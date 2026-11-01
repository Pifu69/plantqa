# Bevezetés

Egy ipari üzemet sokféle dokumentum ír le. A csővezeték- és műszerezési rajzok (angol rövidítéssel
P&ID) megmutatják, hogyan kapcsolódnak egymáshoz a berendezések, szelepek és műszerek; a gyártói
adatlapok megadják, mire képes az egyes eszköz. A rajzon minden elemnek egyedi azonosítója, tag-je
van (például P-101 egy szivattyú), és ez köti össze a rajzot az eszköz adatlapjával. Egy
üzemeltető vagy tervező mérnök kérdései gyakran mindkét dokumentumfajtát érintik: „Mekkora a
megengedett legnagyobb nyomás azon a szelepen, amely a P-101 szivattyú nyomóoldalát elzárja?” A
válaszhoz előbb a rajzon kell megtalálni a szelepet (a vezeték akár egy másik rajzlapon is
folytatódhat), majd a tag-je alapján az adatlapját, és abban a megfelelő feltételhez tartozó
értéket. Ma ezt kézzel végzik.

A nagy nyelvi modellek (LLM) kézenfekvő eszköznek tűnnek, de az üzemi dokumentáció nehéz terep
számukra. A lényeges információ gyakran nem egyetlen elemben van, hanem a kontextusban: egy
táblázat fejlécében, egy értéket korlátozó lábjegyzetben, vagy egy lapközi csatlakozóban, amely
egy csővezetéket egy másik lapon folytat. Ezt a szerkezetet egy tudásgráf teheti explicitté:
olyan adatbázis, amelyben a dolgok csúcsok, a köztük lévő kapcsolatok élek, és amelyből a modell
a kérdéshez tartozó részt visszakeresve válaszol (az angol szakirodalomban: GraphRAG). Ez azonban
csak akkor működik, ha a gráf megőrzi a kontextust.

A munka két részből épül fel, mindkettő az egyik szerző egyéni munkája.

- **A rajzoldali rész** (Kiszely Benedek rendszere, a továbbiakban **plantgraph**) az egész
  üzemet leíró tudásgráfot épít a rajzlapokból: a berendezések és műszerek csúcsok, a csövek és
  jelvezetékek élek, és a lapok határán megszakadó vezetékek újra összekapcsolódnak. Erre a
  gráfra építve egy kétlépcsős rendszer, a **kaszkád** (lépcsőzetes módszer) válaszol a
  kérdésekre: először egyetlen adatbázis-lekérdezéssel próbálkozik, és ha ez nem elég, egy
  gráfbejáró eszközöket hívó LLM-ágens veszi át a kérdést. A rész fő kérdése, hogy ez a
  megközelítés több száz, akár ezer lapos üzemen is működik-e.
- **Az adatlapoldali rész** (Szabó Zsombor rendszere, a továbbiakban **plantdocs**) egy-egy
  eszköz PDF-adatlapjából épít tudásgráfot, amelyben minden érték mellett megmarad a
  mértékegysége, az érvényességi feltétele (például „csak 100 °F alatt”) és a forrásoldala, vagyis
  az adatlap PDF-jének az az oldala, ahol az érték nyomtatva szerepel, hogy a válasz az eredeti
  dokumentumban ellenőrizhető legyen. A feltételt azért kell megőrizni, mert egy feltétel nélküli
  érték nem hiányos, hanem hibás. A gráf nemzetközi ipari szabványok szókészletére épül, ezeket a
  2. fejezet mutatja be. A plantdocs két lekérdezési módszert hasonlított össze: az **A1** a gráf
  RDF-formáját SPARQL-lekérdezéssel kérdezi, az **A2** a Neo4j-adatbázisba töltött gráfra egy
  nyelvi modell által írt Cypher-lekérdezéssel és vektoros (jelentés szerinti) kereséssel
  válaszol. Ebben a munkában az A2-t használjuk.

A két rendszer felépítését a 4. és az 5. fejezet foglalja össze, részletes leírásuk a Függelék
D-ben található.

Ebben a dolgozatban a két részt összekapcsoljuk: a rajzi gráf elemeit a tag-jük alapján az
adatlapgráfokhoz kötjük, és megmérjük, mennyire jól válaszolnak a rendszerek a két
dokumentumfajtát együtt igénylő kérdésekre. Az első prototípus egy kis, négylapos üzemen készült;
a közös rendszert ezután két fejlesztési üzemen (30 és 50 lap) hangoltuk, végül a hangolt és
befagyasztott rendszert két olyan üzemen mértük meg (100 és 1000 lap), amelyeket a hangolás során
nem használtunk.

## Kutatási kérdések

- **RQ1.** Megválaszolhatók-e a rajzot és az adatlapot összekötő kérdések egyetlen összevont
  tudásgráfon (M1), és hogyan viszonyul ennek pontossága egy olyan irányítóéhoz (router, M2),
  amely a két rész meglévő rendszerét külön hívja, illetve egy gráf nélküli alapmódszeréhez
  (baseline, M3)?
- **RQ2.** Hogyan változik a módszerek pontossága és költsége, ha az üzem mérete nő? A
  módszereket a 30 és 50 lapos fejlesztési üzemen hangoltuk, és a hangolt, befagyasztott
  módszereket a 100 és 1000 lapos tesztüzemen mértük, további változtatás nélkül.
- **RQ3.** Mely kérdéscsaládokon segít a gráf, és milyen hibák jellemzők az egyes módszerekre?

## Hozzájárulások

1. Öt példaüzem ugyanazzal a generátorral: egy négylapos prototípus-üzem (26 tagelt elem), két
   fejlesztési üzem pontosan 30 (206) és 50 lappal (378), valamint két tesztüzem pontosan 100 (772)
   és 1000 lappal (7854). Az üzemek elemeihez program rendeli hozzá hét eszköz gyártói adatlapját. Az, hogy több száz vagy ezer rajzi elemhez csak hét
   adatlap tartozik, nem ellentmondás: egy adatlap egy eszköztípust (egy gyártó katalógusában
   szereplő modellt) ír le, és az azonos típusú rajzi elemek (például az összes
   centrifugálszivattyú) ugyanazt az adatlapot kapják, ahogy egy valódi üzemben is ugyanaz a
   szivattyúmodell sok helyen be van építve. A rajzok szintetikusak, a hét adatlap viszont valódi
   gyártói PDF (3. fejezet; a fájlok helyét a Függelék D adja meg).
2. Az összevont tudásgráf: a rajzi üzemi réteg és hét eszköz adatlapgráfja egy
   Neo4j-adatbázisban, egy tagalapú kapcsolattal összekötve, egy paranccsal újratölthetően.
3. Három kérdés-válaszoló módszer a két rész meglévő kódjára építve: a rajzoldali rendszer
   kiegészítése az adatlapréteggel és egy új adatlap-eszközzel (M1), egy irányító a két rendszer
   fölött (M2) és egy gráf nélküli alapmódszer (M3).
4. Üzemenként egy 60 kérdésből álló, négy családra bontott kérdéssor, és ezen felül 12 olyan
   kérdés, amelyhez több adatlapot kell összevetni. A rajzra vonatkozó kérdések referenciaválaszát
   program számolja ki a generátor megoldókulcsként szolgáló üzemgráfjából; az adatlapi kérdések
   referenciaválaszát egy nyelvi modell írta az adatlap PDF-jéből, és ezeket ember nem
   ellenőrizte; a kettőt kombináló kérdések referenciáját program rakja össze ezekből (3. fejezet).
   Ehhez tartozik a három módszer mért összehasonlítása két modellel a két tesztüzemen (az 1000
   lapos üzemen a gráf nélküli alapmódszer nélkül, mert annak promptja ott nem fér a modellek
   kontextusába).
5. Egy webes demó, amely bármely módszerrel válaszol, és megmutatja az útvonalat, a
   lekérdezéseket és az adatlapi forrásoldalakat.

## Munkamegosztás

A rajzoldali rendszer (generátor, lapokra bontás, üzemi gráf, kaszkád) Kiszely Benedek, az
adatlapoldali rendszer (feldolgozó folyamat, ISO 15926 gráf, A2-lekérdezés) Szabó Zsombor egyéni
munkájának eredménye; a kódjukat nem módosítottuk. Az összevonást, a kérdéssort, a három
módszert, a mérést és a demót közösen készítettük.

## A dolgozat felépítése

A 2. fejezet a hátteret és a kapcsolódó munkákat foglalja össze. A 3. fejezet bemutatja a
példaüzemeket (a prototípus-üzemet, a két fejlesztési és a két tesztüzemet), az adatlapokat és a
kérdéssort, a 4. fejezet az összevont tudásgráfot, az 5. fejezet a
három módszert. A 6. fejezet a mért eredményeket, a 7. fejezet a demót és egy esettanulmányt, a 8. fejezet a következtetéseket és a
korlátokat tárgyalja. A Függelék a példakérdéseket (A), a két módszer promptjainak részleteit (B, C),
a két forrásfolyamat részletes leírását (D), a módszerek lépéseinek részleteit (E), további
demó-képernyőképeket (F) és az első prototípus kis üzemen végzett méréseinek teljes leírását (G)
tartalmazza.
