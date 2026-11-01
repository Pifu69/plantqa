# Háttér és kapcsolódó munkák

Ebben a fejezetben összefoglaljuk a dokumentumokat, a szabványokat és a nyelvimodell-alapú
kérdezési módszereket, amelyekre a dolgozat épül, majd egy táblázatban vetjük össze a kapcsolódó
munkákat.

## P&ID-k és gyártói adatlapok

### A P&ID mint dokumentum

A csővezeték- és műszerezési rajz (P&ID) az üzem központi tervdokumentuma: megmutatja, mely
berendezések, szelepek és műszerek vannak az üzemben, és hogyan kapcsolódnak egymáshoz
[Toghraei2019], [Christensen2020].

A rajzi elemeket a tag azonosítja (pl. P-101, FT-202). A tag betűi az elem fajtáját és szerepét
jelölik, a műszereknél az első betű a mért változót (F áramlás, P nyomás, L szint, T hőmérséklet),
a további betűk a funkciót (például T távadó, IC szabályozó); a betűk a hurokszámmal együtt adnak
egyedi azonosítót [AIChE2010a]. Az `FT-202` például így olvasható: F = a mért változó az áramlás,
T = a műszer funkciója távadó, 202 = a szabályozókör (hurok) száma; ugyanennek a körnek a
szabályozója `FIC-202`. A csővezetékek azonosítója, a vezetékszám szokás szerint névleges
átmérőből, közegkódból, sorszámból, csőosztályból és szigetelésből áll [AIChE2010b]. Egy ilyen
vezetékszám lehet például (csak szemléltető, kitalált példa) a `3"-CW-1012-CS1-N`: 3 hüvelyk
névleges átmérő, CW (hűtővíz) közegkód, 1012-es sorszám, CS1 csőosztály, N (szigetelés nélkül).
A példaüzemek tag-jei ugyanezt a betűrendszert követik, de a hurokszám helyett az egység és a
sorszám áll bennük: a `P-1-3` az 1. egység harmadik szivattyúja (P = szivattyú), az `FT-2-2` a 2.
egység második szabályozókörének áramlástávadója (F = áramlás, T = távadó).

Egy valódi üzem rajza sok lapra tagolódik. A laphatáron átmenő vezetéket lapközi csatlakozó
(off-page connector) folytatja egy másik lapon: a lap szélén álló, feliratozott jel, amely
megnevezi a másik lapot, és amelyhez a másik lapon egy párja tartozik. A rajzi szabályok szerint
a többlapos rajzok vezetékvégei kölcsönösen hivatkoznak egymásra [ISO10628-1], és a rajzok közötti
hivatkozó jelek jól strukturált rajzszámot hordoznak, amely akár reguláris kifejezésekkel is
összeköthető [Mani2020]. A laphatár két különböző kapcsolatot vághat el. Az egyik egy cső: ekkor
két csatlakozó jelzi, hogy a vezeték a másik lapon folytatódik. A másik egy elem: ugyanaz a
berendezés több lapon is megjelenik, az egyik lapon teljes adataival, a többin csak a tag-jével.
Mindkét esetben a gráf építőjének kell a két lap darabjait összekötnie, és ha ez elmarad, más-más
hiba keletkezik. Ha a csatlakozópár nincs összekötve, a cső két fele nem kapcsolódik: az út
megszakad, a csatlakozó párja nélkül marad, és ez egy egyszerű ellenőrzéssel észrevehető. Ha
viszont a berendezés előfordulásait nem vonja össze egy elemmé, ugyanaz a berendezés két külön
csúcsként kerül a gráfba: az egyik lapon bekötött csövek az egyik csúcshoz, a másikon bekötöttek a
másikhoz tartoznak. Mindkét csúcsnak vannak kapcsolatai, ezért a gráf épnek látszik, nincs
párosítatlan jel, amely a hibát elárulná. Egy, a berendezésről szóló kérdés (például „mi táplálja
ezt a hőcserélőt?”) azonban csak az egyik csúcs kapcsolatait látja, így a válasz hiányos lesz,
és ezt semmi nem jelzi.

### A DEXPI és a pyDEXPI

A rajz digitális cseréjének szabványa a DEXPI, amely UML információs modell saját
XML-szerializációval [DEXPI2025]. A rajzi szabvány (például az ISO 10628) azt mondja meg, hogyan
néz ki egy szimbólum; az információs modell azt, milyen osztályok és attribútumok vannak; az
ontológia ugyanezt formális logikával, globális azonosítókkal írja le. A DEXPI információs modell: OWL- vagy RDF-formája nincs, de az
osztálydefiníciói az ISO 15926 4. részének referenciakönyvtárából származnak, így szemantikailag
le van horgonyozva [DEXPI2025]. Egy DEXPI-modell egyetlen rajzot ír le; rajzkészletet, és azt,
hogy két lapon lévő elem ugyanaz, nem modellez.

A DEXPI szemantikus változata épül: a DEXPI egyesület hírei szerint a TotalEnergies a BFO-hoz és
az IDO-hoz igazított DEXPI-n dolgozik [DEXPI2026news], a POSC Caesar Arrowhead-kézikönyve pedig a
DEXPI életciklus-zónáit és tulajdonságmodelljét igazítja az IDO-hoz, egyelőre egyetlen, kézzel
írt szivattyús példán [ArrowheadHandbook]. Az OPC UA felé is van leképezés [OPC30250]. Ezért ebben
a dolgozatban nem építünk P&ID-ontológiát; a rajzoldalon a DEXPI osztályneveit használjuk
címkeként, ahogy a kapcsolódó munkák is.

A DEXPI Python-megvalósítása a pyDEXPI: a DEXPI adatmodell Pydantic-osztályai, Proteus XML
betöltő és NetworkX-gráffá alakító export [pyDEXPI]. A ChatP&ID és elődje a pyDEXPI osztálynevét
teszi a gráfcsúcsok címkéjébe [Alimin2026], [Alimin2025]; Benedek generátora is pyDEXPI-modellt
épít, ezért a példaüzem elemei is ezeket az osztályneveket viselik (`CentrifugalPump`,
`CheckValve`).

### A gyártói adatlap

A rajz csak a kapcsolatokat mutatja; az egyes eszközök műszaki jellemzőit (nyomás- és
hőmérséklethatár, anyag, méret, opciók) a gyártói adatlapok tartalmazzák. Egy adatlap néhány
oldalastól több mint száz oldalasig terjedő PDF táblázatokkal, lábjegyzetekkel, feltételekhez
kötött értékekkel és diagramokkal.

Az adatlapi tény ritkán egyetlen szám. Egy szabályozószelep adatlapján egy hőmérsékleti határ
csak egy adott testanyagra és csatlakozóméret-tartományra érvényes, egy lábjegyzet tovább
szűkíti, és ugyanaz az érték két mértékegységben is ki van nyomtatva. Ha egy rendszer ebből csak
a számot és az egységet őrzi meg, a válasza nem hiányos, hanem hibás lehet. A plantdocs végső
mérésén éppen a feltételes kérdéseken volt nagy a két lekérdezési módszer különbsége: a 31
feltételes kérdésből az A1 21-re, az A2 28-ra, a 17 több feltételt kombináló kérdésből 7-re,
illetve 15-re adott helyes választ.

### Szabványok az adatlapi tények ábrázolására

Az adatlapi tények gépileg értelmezhető leírására több, egymásra épülő szabvány létezik. A
fontosabbak:

- Az **IDO** (Industrial Data Ontology) az alapfogalmakat adja: fizikai tárgy, rész és egész,
  információ, érték és mértékegység. OWL 2 nyelven írt ontológia; korábban ISO/TR 15926-14 volt,
  ma ISO 23726-3 néven szabványosítják [IDO].
- A **PCA RDL** (a POSC Caesar szervezet referenciakönyvtára) a konkrét berendezés-, cső- és
  műszerosztályok és tulajdonságok listája [PCARDL].
- A **CFIHOS** azt írja le, milyen adatokat kell átadni egy üzem átadásakor (tag-ek,
  berendezésosztályok jellemzői, dokumentumadatok) [CFIHOS].
- A **QUDT** a mértékegységeket és a mennyiségfajtákat írja le; berendezést nem [QUDT].

Más szókészletek (OntoCAPE [OntoCAPE], SOSA/SSN [SOSASSN2017], IOF [IOF], schema.org [SchemaOrg])
erre a célra nem alkalmasak: vagy régóta nem frissülnek, vagy nem írják le a folyamatüzemi
berendezéseket. A plantdocs ezért az ISO 15926 vonalat választotta (4. fejezet). Ugyanerre épül
egy friss munka is, amely a szelepek tervezési szabványait (például az ASME B16.34-et) IDO-alapú
ontológiává alakítja [Gjerver2025]. Mivel a DEXPI osztályai is az ISO 15926-ból származnak, a
rajzi és az adatlapi oldal ugyanarra a szemantikai alapra épül.

### Tulajdonsággráf és RDF

Az RDF-ben minden állítás egy alany–állítmány–tárgy hármas, az azonosítók globálisak (IRI), és az
élnek nincs saját tulajdonsága. A tulajdonsággráfban (labeled property graph, LPG; legismertebb
megvalósítása a Neo4j) a csúcsoknak és az éleknek is lehetnek tulajdonságaik, az azonosítók
lokálisak. A ChatP&ID szerzői mérlegelték az RDF-et, de az attribútumokban gazdag mérnöki adat
miatt a tulajdonsággráfot választották [Alimin2026], és Benedek rendszere is Neo4j-re épül. A
plantdocs adatlapgráfja RDF-ben készül (mert az IDO OWL 2), de a neosemantics (n10s) bővítménnyel
Neo4j-be is betölthető; ez a híd teszi lehetővé, hogy a két réteg egy adatbázisba kerüljön.

### Feltételes, n-áris tények

Az adatlapi tények jelentős része n-áris: egy érték egy alanyról, egy tulajdonságról és több
feltételről egyszerre szól. Az ilyen tények bináris hármasokra bontása elveszíti a feltételt, és
szemantikai széttöredezéshez vezet [HyperRAG2026]. Erre a hiper-relációs tudásgráfok és a
hipergráfos RAG ad ábrázolást. A minősítők (qualifiers) javítják a linkpredikciót
[StarE2020], a HyperGraphRAG pedig az n-áris tényeket hiperélekként tárolja [HyperGraphRAG2025].
A tárolás kérdése tehát elvben megoldott: ismert, hogyan lehet egy értéket a mértékegységével és a
feltételeivel együtt egy gráfban rögzíteni. A nehézség a kiolvasás: a PDF a feltételt gyakran csak
az elrendezésével fejezi ki, például egy táblázat fejlécével, egy lábjegyzettel vagy azzal, hogy
egy érték egy diagram melyik tartományába esik, és ezt kell helyesen felismerni. Hogy a mi
adatlapgráfunk hogyan tárolja a feltételeket, azt a 4. fejezet mutatja be.

## Kérdés-válaszolás P&ID-ken

### Visszakeresés a rajz gráfján

A legközelebbi előzmény a ChatP&ID [Alimin2026]: DEXPI-rajzokat pyDEXPI-vel Neo4j-gráffá alakít,
és egy iteratív ágens négy visszakeresési eszköz közül választ. A négy eszköz négy különböző
választ ad arra, hogyan jut el a gráf releváns része a modellhez. A ContextRAG az egész (sűrített)
gráfot szövegként a promptba teszi, keresés nélkül. A VectorRAG a kérdéshez jelentés szerint
leghasonlóbb csúcsok leírását adja, beágyazásvektorok koszinusz-hasonlósága alapján. A PathRAG egy
így talált kiinduló csúcsból lépésenként bejárja a szomszédokat. A CypherRAG-ban a modell a
kérdést Cypher-lekérdezéssé fordítja, az adatbázis lefuttatja, és az eredmény kerül a promptba.
Egyetlen lapon, 19 kérdésen a ContextRAG adta a legjobb eredményt; a szerzők szerint viszont ez a
módszer többlapos rajzoknál nem skálázódik. Egy korábbi munka ugyanettől a csoporttól a
sűrített gráfot GraphML-ként, visszakeresés nélkül adja a modellnek, egy folyamatábrán, három
kérdésen értékelve [Alimin2025]. A legnagyobb közölt P&ID-kérdéskészlet a PIDQA-é: 500 szintetikus
rajzlapon 64 000 programmal előállított kérdés-válasz pár, négy kategóriában (egyszerű és térbeli
számlálás, térbeli kapcsolat, értékalapú kérdés). A rajzból képfelismeréssel tulajdonsággráf
készül Neo4j-ben, a kérdést pedig egy LLM fordítja Cypher-lekérdezéssé; minden kérdés egyetlen
lapra vonatkozik, lapokon vagy dokumentumokon átívelő kérdés nincs benne [Gupta2025].

Raszteres rajzokon a Gadekar és társai által javasolt módszer előbb visszanyeri a folyamatgráfot,
majd a látás-nyelvi modell a topológiai kérdésekre csak hét, tényt visszaadó gráfoperátoron
keresztül válaszolhat [Gadekar2026]; a TopoPID-VQA kérdésein ez a megkötés jelentősen javítja a
pontos egyezést, de egylapos, szintetikus rajzokon. A szoftveres előzmények között egy nyílt
LangGraph-ágens hét általános gráfeszközzel kérdez DEXPI-fájlokon, kérdésenként egy fájlon
[PidGraphAgent2026], egy ipari esettanulmány pedig olyan Neo4j-tudásgráfot ír le, amely
helyreállítja a lapok közötti kapcsolatokat, és fölötte egy ágens előre definiált
gráflekérdező eszközökkel és szabad Cypherrel válaszol, kiértékelés közlése nélkül
[Kochanski2026].

### A rajzok gráffá alakítása

A rajzok digitalizálását mi nem végezzük el, de a kérdés-válaszolás bemenete ennek a kimenete.
Egy transzformeres módszer a szimbólumokat és a kapcsolataikat együtt jósolja, és ehhez kiadta a
PID2Graph adatkészletet, amelynek gráfjai tisztán geometriaiak, címkék és lapok közötti
megoldókulcs nélkül [Sturmer2024], [PID2Graph2025]. Ipari rajzokból automatikus
tudásgráf-építést [Lopomo2026], a pyDEXPI-gráfon szabályalapú javítást [SchulzeBalhorn2025], és
mesterséges rajzgenerálást [Hirtreiter2022] is javasoltak. A képfelismerés töredezett
vonalszakaszait folytonos kapcsolati gráffá egyesítő módszer [Prusty2025] és a digitalizálást
tagkinyerésként és topológia-következtetésként, két lépésben, multimodális nyelvi modellel
megoldó megközelítés [Zhu2026a] is a rajz gráfját állítja elő, amelyre a kérdés-válaszolás épül. Valódi, többlapos, nyilvános
rajzsorozatból kevés van; az OPEN100 sorozat 12 lapja ezek közé tartozik [OPEN100].

### Üzemi méret

A fenti munkák közös vonása, hogy egy-egy rajzlapot vizsgálnak, és a rajzon kívüli
dokumentumokat (adatlapokat) nem kapcsolják be. Kiszely Benedek egyéni munkája (plantgraph) a
rajzi kérdés-válaszolást üzemi méretben vizsgálja, véletlenszerűen generált, többlapos szintetikus
üzemeken (a generátor véletlenszám-generátorának kezdőértéke, a seed, meghatározza az üzemet: ugyanaz
a seed mindig ugyanazt az üzemet adja), mert
nyilvános, a lapok közötti kapcsolatok megoldókulcsával ellátott többlapos rajzkészlet nincs. A
kérdéseket és a referenciaválaszokat program állítja elő a generátor megoldókulcsként szolgáló
üzemgráfjából, és a válaszokat is program pontozza (ugyanezt a pontozót használjuk mi is, 3.
fejezet); a pontosság a helyesen megválaszolt kérdések aránya. A generátornak két változata van:
egy egyszerűbb, első változat, és egy valósághűbb, későbbi változat, amelynek üzemeiben oszlopok,
reaktorok, biztonsági szelepek és a berendezések között sok jelöletlen idom is van. Az alábbiakban
minden számnál megadjuk, melyik változat üzemein mérték.

**A gráf nélküli alapmódszer.** A ContextRAG a teljes rajzot szövegként a promptba teszi. Az
egyszerűbb generátor üzemein a pontossága 1-ről 30 lapra 0,824-ről 0,658-ra csökkent, miközben a
kaszkádé 0,941-ről 0,947-re változott. A valósághűbb generátor üzemein, egy 1, 3 és 11 lapos
rajzokon végzett mérés-sorozatban a kaszkád pontossága 0,957 / 0,885 / 0,909, a ContextRAG-é
0,686 / 0,654 / 0,614 volt. A ContextRAG költségét a forrás a kaszkád költségéhez viszonyítva
közli: kérdésenként az egyszerűbb üzemeken 1 lapon 1,8-szer, 30 lapon 41,5-ször, a valósághűbb
üzemeken 1 lapon 3,79-szer, 11 lapon 21,57-szer annyiba kerül, mint a kaszkád. A szövegként leírt
rajz egy bizonyos méret fölött már nem fér el a modell promptjában: az egyszerűbb generátor
üzemein ez körülbelül 143, a valósághűbbén körülbelül 62 lap; a két szám tehát a két
generátorváltozathoz tartozik.

**A kaszkád 100 és 1000 lapos üzemen.** Az egyszerűbb generátor üzemein a kaszkád a lezárt
teszten 100 lapos üzemen 0,937, 1000 lapos üzemen 0,917 pontosságot ért el. A lezárt teszt 460
kérdése olyan üzemekre vonatkozott, amelyeket a fejlesztés során egyszer sem használtak: a
generátor új seedekkel állította elő őket, a kérdéseket és a referenciaválaszokat pedig program
készítette ezeknek az üzemeknek a megoldókulcsából, így a rendszer ezeket a rajzokat korábban nem
láthatta. A valósághűbb generátor üzemein az egyszerűbb üzemekre fejlesztett rendszer gyengébb,
ezért Benedek ezekre az üzemekre külön hangolt és befagyasztott egy kaszkádot; ezt használjuk mi
is (5. fejezet). Két, a hangolás során nem használt üzemen (kb. 100 és kb. 1000 lap, egyenként 163
kérdés) a hangolt kaszkád 154, illetve 156, a hangolás előtti 145, illetve 144 helyes választ adott.
A lezárt teszten (üzemenként 440 kérdés) a hangolt kaszkád kb. 100 lapon 401 (0,911), kb. 1000
lapon 392 (0,891) helyes választ adott. A −0,020-es különbség nem szignifikáns (a 95%-os
konfidenciaintervallum −0,059 és +0,018 között van, tehát a nullát is tartalmazza), vagyis a
tízszer nagyobb üzemen a pontosság nem romlott mérhetően. A kérdésenkénti költség 0,00137, illetve
0,00148 USD volt, a medián késleltetés 7,1, illetve 7,5 s; a medián késleltetés a kérdésenkénti
válaszidő tipikus értéke (a kérdések felére ennél gyorsabban, felére lassabban érkezett válasz).

**Új kérdéstípusok.** Benedek a rendszert olyan kérdéstípusokon is megmérte, amelyeket a
hangolás során nem használt (100 kérdés). Ezeken a hangolt kaszkád pontossága kb. 100 lapon 0,770,
kb. 1000 lapon 0,740 volt. Az elmaradás szinte teljesen a lefelé eső elzáró
szelepeket kereső kérdésekből jön: ezek közül a 20-ból mindkét méretnél csak 2 volt helyes.

Ezeket a számokat jelen munka nem méri újra; a 6. fejezetben a gráf nélküli módszer
skálázódásának hátteréül szolgálnak.

## Kérdés-válaszolás műszaki dokumentumokon

Gyártási dokumentumokon a Document GraphRAG a dokumentum saját szerkezetéből és egy könnyű,
automatikusan épített példánygráfból épít tudásgráfot [Knollmeyer2025]; a szerzők elismerik, hogy
szakterületen az automatikus tudásgráf-építés pontatlan, ezért ma is főleg kézi munka. Ipari
tudásbázison a Golden-Retriever a visszakeresés előtt egy reflexiós lépésben azonosítja és
tisztázza a szakzsargont és a rövidítéseket [GoldenRetriever2024]. A műszaki dokumentumokba
ágyazott táblázatokat és szerkezetet a visszakeresésben külön kezelő, strukturált adatokat
figyelembe vevő RAG-irány [StructRAG2025] azt jelzi, hogy az adatlapi táblázatok a sima
szövegdarabolástól eltérő kezelést igényelnek. Mérnöki
rajzokat és kézikönyveket feldolgozó látás-nyelvi modellek egy friss benchmarkon megtalálják a
tételeket, de gyakran pontatlanul írják le őket, és a szövegátfedésen alapuló metrikák alulmérik
a képességüket; a szerzők ezért keresztbírálós LLM-értékelést használnak [Kumar2026]. Ezért a
szabad szöveges válaszokat mi is bírálóval pontozzuk (3. fejezet).

Szabó Zsombor egyéni munkája (plantdocs) egyetlen eszköz adatlapjából épít ISO 15926 / QUDT
szerinti tudásgráfot, amelyben a feltételek és a kereszthivatkozások külön elemek maradnak. Két lekérdezési
módszert hasonlít össze: A1 (RDF + SPARQL) és A2 (Neo4j + Cypher, vektoros kereséssel). A
plantdocs végső mérésén (a Rosemount 3051 adatlap 200 befagyasztott kérdésén, vak
bírálóval) az A1 141, az A2 172 kérdésre adott helyes választ. Ebben a munkában az A2 az adatlapoldal alapja.

## GraphRAG és visszakeresési stratégiák

### Mikor segít a gráf?

A gráfalapú RAG nem mindig jobb a szövegalapúnál. Egy benchmark szöveges korpuszon méretfüggő
keresztezést mutatott ki a sima RAG és egy gráfalapú módszer között: kis korpuszon a sima RAG nyer,
és a gráf előnye a korpusz méretével jelenik meg [Xiang2025]. A ChatP&ID egylapos eredménye
és Benedek üzemi méretű mérései ugyanezt a mintát mutatják a rajzokon; kis üzemen (például a mi
négylapos prototípus-üzemünkön) ezért a gráf nélküli módszer erős ellenfél.

Ha több visszakeresési stratégia áll rendelkezésre, kérdésenként lehet közöttük választani. A
GraphRAG-Router megerősítéses tanulással tanított útválasztója kérdésenként választ GraphRAG-módszer
és nyelvi modell között, és ezzel csökkenti a nagy modell hívásainak számát [Fan2026]. A mi M2
routerünk ennek egyszerű, tanítás nélküli változata: egy nyelvi modell dönti el lépésenként,
melyik meglévő rendszert hívja.

### Gráfeszközöket hívó ágensek

A tudásgráf-kérdés-válaszolás bevett mintája az ágens, amely lépésenként eszközöket hív a gráfon,
és az eredményekből állítja össze a választ. A KBQA-Agent hét tudásbázis-eszközt ad (relációk,
szomszédok, attribútumok, legnagyobb és legkisebb érték, metszet, darabszám); minden lépés
eredménye nevet kap, így egy későbbi lépés név szerint visszautalhat rá, és azon dolgozhat tovább
(például előbb a szomszédokat kéri le, majd ezek közül választja ki a legnagyobb értékűt)
[KBQAAgent2024]. Hasonló mintát követ a KG-Agent
[KGAgent2024] és a Graph-CoT [GraphCoT2024]. A skála másik végén a szabad
Cypher áll: a Neo4j MCP-szervere mindössze sémalekérdező, olvasó és író Cypher-eszközt ad, a
lekérdezést a modell írja [MCPNeo4j].

Benedek ágense a KBQA-Agent családjába tartozik: hat általános, egymással komponálható üzemi
primitívet hív, az eredményeket hivatkozással adja tovább; a mi
`datasheet_fact` primitívünk ezt a készletet bővíti (5. fejezet).

### Kaszkád és önjelzés

A kaszkád (lépcsős módszer) a kérdést előbb a legolcsóbb módszernek adja, és csak akkor viszi
tovább, ha az olcsó válasz gyanús. A gyanú forrása önjelzés: olyan jel, amelyet a lépcső maga ad
a válaszáról, a helyes válasz ismerete nélkül, például a hibát dobó vagy üres lekérdezés. Az ilyen
szabály nem illeszt paramétert a mért adatra, ezért kevésbé hajlamos a túlillesztésre, mint a
kérdéstípus szerinti útválasztás. Benedek kaszkádja is
ilyen szabállyal dönt; az 5. fejezetben részletezzük.

## Összevetés

Az alábbi táblázat azt foglalja össze, hogy a kapcsolódó munkák a probléma mely részeit fedik le;
a kiértékelés méretét a forrás szerint adjuk meg.

Táblázat: A kapcsolódó munkák összevetése
| Munka | Rajz | Adatlap | Több lap | Gráf | Kiértékelés mérete |
|---|---|---|---|---|---|
| ChatP&ID [Alimin2026] | igen (DEXPI) | nem | nem, egy lap | Neo4j, tulajdonsággráf | 19 kérdés |
| Talking like P&IDs [Alimin2025] | igen (DEXPI) | nem | nem | sűrített gráf a promptban | 3 kérdés, egy folyamatábra |
| PIDQA [Gupta2025] | igen (szintetikus, raszteres) | nem | nem, kérdésenként egy lap | Neo4j, tulajdonsággráf, Text2Cypher | 64 000 kérdés, 500 lap |
| Gadekar és társai [Gadekar2026] | igen (raszteres) | nem | nem | visszanyert folyamatgráf, 7 operátor | 3000 kérdés, szintetikus lapok |
| pid-graph-agent [PidGraphAgent2026] | igen (DEXPI) | nem | nem, kérdésenként egy fájl | gráfeszközös ágens | 15 + 37 saját kérdés |
| Everllence-esettanulmány [Kochanski2026] | igen | nem | igen | Neo4j, ágens | nem közöl |
| Lopomo és társai [Lopomo2026] | igen (126 rajz) | nem | nincs adat | automatikusan épített tudásgráf | gráfépítés, nem kérdés-válaszolás |
| Document GraphRAG [Knollmeyer2025] | nem | gyártási dokumentumok | – | dokumentumszerkezet és példánygráf | nincs adat |
| Enginuity [Kumar2026] | mérnöki rajzok | kézikönyvek, alkatrésztáblák | – | nincs | 6940 oldal |
| plantgraph (Kiszely Benedek) | igen (szintetikus) | nem | igen, kb. 100 és 1000 lap | Neo4j, üzemi réteg | 460 kérdés a lezárt teszten |
| plantdocs (Szabó Zsombor) | nem | igen, egy eszköz | – | ISO 15926 / QUDT, RDF és Neo4j | 200 kérdés |
| Jelen munka | igen (30 és 50 lapos fejlesztési, 100 és 1000 lapos tesztüzem) | igen, 7 adatlap | igen | összevont Neo4j-gráf | üzemenként 60 kérdés + 12 (e) kérdés |

A rajzoldali munkák szinte mind egylaposak, és egyikük sem kapcsolja be az eszközök adatlapjait;
az egyetlen többlapos ipari példa kiértékelést nem közöl. A dokumentumoldali munkák pedig nem
használják a rajz topológiáját.

## A hiányzó lépés

A két egyéni munka ugyanannak az üzemi dokumentációnak két oldalát dolgozza fel. A rajzon
látszik, hogy mi mivel áll kapcsolatban, az adatlapon, hogy egy eszköz mire képes. Egy mérnöki
kérdés gyakran mindkettőt igényli („mekkora a maximális nyomás azon a szelepen, amely a P-101
nyomóoldalát elzárja?”). Az általunk áttekintett irodalomban nem találtunk olyan munkát, amely a
rajzi gráfot és az eszközönkénti adatlapgráfokat egy lekérdezhető modellben kötné össze, és ezt
mérné. Ez a dolgozat tárgya.
