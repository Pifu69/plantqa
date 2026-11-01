# Háttér és kapcsolódó munkák

Mielőtt a két rendszer összekötésére rátérnénk, áttekintjük, mit kell tudni a két
dokumentumfajtáról, milyen szabványok írják le őket gépileg értelmezhető formában, és mit ért el
eddig a szakirodalom a rajzokon és a műszaki dokumentumokon végzett kérdés-válaszolásban. A
fejezet végén egy táblázatban vetjük össze a kapcsolódó munkákat, és megmutatjuk, melyik lépés
hiányzik.

## P&ID-k és gyártói adatlapok

### A P&ID mint dokumentum

A csővezeték- és műszerezési rajz (P&ID) az üzem központi tervdokumentuma: megmutatja, mely
berendezések, szelepek és műszerek vannak az üzemben, és hogyan kapcsolódnak egymáshoz
[Toghraei2019], [Christensen2020].

A rajzi elemeket a tag azonosítja (például P-101, FT-202). A tag betűi az elem fajtáját és
szerepét jelölik. A műszereknél az első betű a mért változó (F áramlás, P nyomás, L szint,
T hőmérséklet), a további betűk a funkció (például T távadó, IC szabályozó), és a betűk a
hurokszámmal együtt adnak egyedi azonosítót [AIChE2010a]. Az FT-202 például így olvasható: F = a
mért változó az áramlás, T = a műszer távadó, 202 = a szabályozókör (hurok) száma; ugyanennek a
körnek a szabályozója FIC-202. A csővezetékek azonosítója, a vezetékszám szokás szerint névleges
átmérőből, közegkódból, sorszámból, csőosztályból és szigetelésből áll [AIChE2010b]. A
példaüzemeink tag-jei ugyanezt a betűrendszert követik, de a hurokszám helyett az egység és a
sorszám áll bennük: a P-1-3 az 1. egység harmadik szivattyúja, az FT-2-2 a 2. egység második
szabályozókörének áramlástávadója.

Egy valódi üzem rajza sok lapra tagolódik. A laphatáron átmenő vezetéket lapközi csatlakozó
(off-page connector) folytatja: a lap szélén álló, feliratozott jel, amely megnevezi a másik
lapot, és amelyhez a másik lapon egy párja tartozik. A rajzi szabályok szerint a többlapos rajzok
vezetékvégei kölcsönösen hivatkoznak egymásra [ISO10628-1], és a rajzok közötti hivatkozó jelek
jól strukturált rajzszámot hordoznak, amely akár reguláris kifejezésekkel is összeköthető
[Mani2020].

A laphatár két különböző kapcsolatot vághat el, és ezek elmulasztása más-más hibát okoz. Ha egy
csövet vág el, két csatlakozó jelzi, hogy a vezeték a másik lapon folytatódik; ha a gráf építője
nem köti össze őket, az út megszakad, és ez egy egyszerű ellenőrzéssel észrevehető, mert a
csatlakozó párja nélkül marad. Ha viszont egy elemet vág el, ugyanaz a berendezés több lapon is
megjelenik, az egyiken teljes adataival, a többin csak a tag-jével. Ha ezeket az előfordulásokat
a gráf építője nem vonja össze, ugyanaz a berendezés két külön csúcsként kerül a gráfba, mindkét
csúcsnak vannak kapcsolatai, és a gráf épnek látszik. Egy, a berendezésről szóló kérdés (például
„mi táplálja ezt a hőcserélőt?”) azonban csak az egyik csúcs kapcsolatait látja, így a válasz
hiányos lesz, és ezt semmi nem jelzi.

### A DEXPI és a pyDEXPI

A rajzok digitális cseréjének szabványa a DEXPI, amely egy UML információs modell saját
XML-formátummal [DEXPI2025]. Érdemes három szintet megkülönböztetni: a rajzi szabvány (például az
ISO 10628) azt mondja meg, hogyan néz ki egy szimbólum; az információs modell azt, milyen
osztályok és attribútumok vannak; az ontológia pedig ugyanezt formális logikával és globális
azonosítókkal írja le. A DEXPI információs modell, ontológiaformája nincs, de az osztályai az
ISO 15926 szabvány referenciakönyvtárából származnak, így jelentésük rögzített [DEXPI2025]. Egy
DEXPI-modell egyetlen rajzot ír le; azt, hogy két lapon lévő elem ugyanaz, nem modellezi.

A DEXPI szemantikus változata épülőben van: a TotalEnergies a DEXPI ontológiai alapokra helyezésén
dolgozik [DEXPI2026news], a POSC Caesar egy kézikönyve pedig a DEXPI tulajdonságmodelljét igazítja
egy ipari ontológiához, egyelőre egyetlen kézzel írt példán [ArrowheadHandbook]; az OPC UA ipari
kommunikációs szabvány felé is van leképezés [OPC30250]. Ezért ebben a dolgozatban nem építünk
P&ID-ontológiát, hanem a kapcsolódó munkákhoz hasonlóan a DEXPI osztályneveit használjuk a rajzi
elemek típusaként. A DEXPI Python-megvalósítása a pyDEXPI, amely a rajzot gráffá is tudja alakítani
[pyDEXPI]; a ChatP&ID és elődje is ennek osztályneveit teszi a gráfcsúcsokra [Alimin2026],
[Alimin2025], és a plantgraph generátora is pyDEXPI-modellt épít, ezért a példaüzemek elemei is
ezeket az osztályneveket viselik (például CentrifugalPump, CheckValve).

### A gyártói adatlap

A rajz csak a kapcsolatokat mutatja; az egyes eszközök műszaki jellemzőit (nyomás- és
hőmérséklethatár, anyag, méret, rendelhető opciók) a gyártói adatlapok tartalmazzák. Egy adatlap
néhány oldalastól több mint száz oldalasig terjedő PDF, táblázatokkal, lábjegyzetekkel,
feltételekhez kötött értékekkel és diagramokkal.

Az adatlapi tény ritkán egyetlen szám. Egy szabályozószelep adatlapján egy hőmérsékleti határ
csak egy adott testanyagra és csatlakozóméret-tartományra érvényes, egy lábjegyzet tovább
szűkíti, és ugyanaz az érték két mértékegységben is ki van nyomtatva. Ha egy rendszer ebből csak
a számot és az egységet őrzi meg, a válasza nem hiányos, hanem hibás lehet. A plantdocs végső
mérésén éppen a feltételes kérdéseken volt nagy a két lekérdezési módszer különbsége: a 31
feltételes kérdésből az A1 21-re, az A2 28-ra, a 17 több feltételt kombináló kérdésből 7-re,
illetve 15-re adott helyes választ.

### Szabványok az adatlapi tények ábrázolására

Az adatlapi tények gépileg értelmezhető leírására több, egymásra épülő szabvány létezik. Az
alapfogalmakat (fizikai tárgy, rész és egész, információ, érték és mértékegység) az IDO
(Industrial Data Ontology) adja; ez OWL 2 nyelven írt ontológia, korábban ISO/TR 15926-14 volt, ma
ISO 23726-3 néven szabványosítják [IDO]. A konkrét berendezés-, cső- és műszerosztályokat és
tulajdonságaikat a POSC Caesar szervezet referenciakönyvtára (PCA RDL) sorolja fel [PCARDL]. A
CFIHOS azt írja le, milyen adatokat kell átadni egy üzem átadásakor (tag-ek, berendezésosztályok
jellemzői, dokumentumadatok) [CFIHOS], a QUDT pedig a mértékegységeket és a mennyiségfajtákat
[QUDT]. Más szókészletek (OntoCAPE [OntoCAPE], SOSA/SSN [SOSASSN2017], IOF [IOF], schema.org
[SchemaOrg]) erre a célra nem alkalmasak: vagy régóta nem frissülnek, vagy nem írják le a
folyamatüzemi berendezéseket. A plantdocs ezért az ISO 15926 vonalat választotta, és ugyanerre
épül egy friss munka is, amely a szelepek tervezési szabványait IDO-alapú ontológiává alakítja
[Gjerver2025]. Mivel a DEXPI osztályai is az ISO 15926-ból származnak, a rajzi és az adatlapi
oldal ugyanarra a szemantikai alapra épül.

### Tulajdonsággráf és RDF

A tudásgráfok két elterjedt formája az RDF és a tulajdonsággráf. Az RDF-ben minden állítás egy
alany–állítmány–tárgy hármas, az azonosítók globálisak, és az élnek nincs saját tulajdonsága. A
tulajdonsággráfban (legismertebb megvalósítása a Neo4j adatbázis, amelynek lekérdezőnyelve a
Cypher) a csúcsoknak és az éleknek is lehetnek tulajdonságaik, az azonosítók pedig helyiek. A
ChatP&ID szerzői az attribútumokban gazdag mérnöki adat miatt a tulajdonsággráfot választották
[Alimin2026], és a plantgraph is Neo4j-re épül. A plantdocs adatlapgráfja RDF-ben készül (mert az
IDO is RDF-alapú ontológia), de egy bővítménnyel (neosemantics) Neo4j-be is betölthető; ez a híd
teszi lehetővé, hogy a két réteg egy adatbázisba kerüljön.

### Feltételes tények

Az adatlapi tények jelentős része több szereplős: egy érték egy alanyról, egy tulajdonságról és
több feltételről egyszerre szól. Az ilyen tények egyszerű hármasokra bontása elveszíti a
feltételt [HyperRAG2026]. Erre a hiper-relációs tudásgráfok és a hipergráfos RAG ad ábrázolást: a
tényekhez fűzött minősítők javítják a hiányzó kapcsolatok előrejelzését [StarE2020], a
HyperGraphRAG pedig a több szereplős tényeket hiperélekként tárolja [HyperGraphRAG2025]. A tárolás
kérdése tehát elvben megoldott. A nehézség a kiolvasás: a PDF a feltételt gyakran csak az
elrendezésével fejezi ki, például egy táblázat fejlécével, egy lábjegyzettel vagy azzal, hogy egy
érték egy diagram melyik tartományába esik. Hogy a mi adatlapgráfunk hogyan tárolja a
feltételeket, azt a 4. fejezet mutatja be.

## Kérdés-válaszolás P&ID-ken

### Visszakeresés a rajz gráfján

A legközelebbi előzmény a ChatP&ID [Alimin2026]: DEXPI-rajzokat alakít Neo4j-gráffá, és egy
ágens négy visszakeresési módszer közül választ. A ContextRAG az egész (sűrített) gráfot
szövegként a promptba teszi, keresés nélkül. A VectorRAG a kérdéshez jelentés szerint
leghasonlóbb csúcsok leírását adja. A PathRAG egy így talált csúcsból lépésenként bejárja a
szomszédokat. A CypherRAG-ban a modell a kérdést Cypher-lekérdezéssé fordítja, az adatbázis
lefuttatja, és az eredmény kerül a promptba. Egyetlen lapon, 19 kérdésen a ContextRAG adta a
legjobb eredményt; a szerzők szerint viszont ez a módszer többlapos rajzoknál nem skálázódik. Egy
korábbi munka ugyanettől a csoporttól a sűrített gráfot visszakeresés nélkül adja a modellnek,
egy folyamatábrán, három kérdésen értékelve [Alimin2025]. A legnagyobb közölt P&ID-kérdéskészlet a
PIDQA-é: 500 szintetikus rajzlapon 64 000 programmal előállított kérdés-válasz pár; a rajzból
képfelismeréssel Neo4j-gráf készül, a kérdést egy nyelvi modell fordítja Cypher-lekérdezéssé, és
minden kérdés egyetlen lapra vonatkozik [Gupta2025].

Raszteres rajzokon Gadekar és társai előbb visszanyerik a folyamatgráfot, majd a látás-nyelvi
modell a topológiai kérdésekre csak hét, tényt visszaadó gráfműveleten keresztül válaszolhat
[Gadekar2026]; ez a megkötés jelentősen javítja a pontosságot, de egylapos, szintetikus rajzokon.
Egy nyílt forráskódú ágens hét általános gráfeszközzel kérdez DEXPI-fájlokon, kérdésenként egy
fájlon [PidGraphAgent2026], egy ipari esettanulmány pedig olyan tudásgráfot ír le, amely
helyreállítja a lapok közötti kapcsolatokat, de kiértékelést nem közöl [Kochanski2026].

### A rajzok gráffá alakítása

A rajzok digitalizálását mi nem végezzük el, de a kérdés-válaszolás bemenete ennek a kimenete. Egy
transzformeres módszer a szimbólumokat és a kapcsolataikat együtt ismeri fel, és ehhez kiadta a
PID2Graph adatkészletet, amelynek gráfjai címkék és lapok közötti megoldókulcs nélküliek
[Sturmer2024], [PID2Graph2025]. Javasoltak automatikus tudásgráf-építést ipari rajzokból
[Lopomo2026], szabályalapú javítást a rajz gráfján [SchulzeBalhorn2025], mesterséges
rajzgenerálást [Hirtreiter2022], a töredezett vonalszakaszok folytonos gráffá egyesítését
[Prusty2025] és multimodális nyelvi modellel végzett, kétlépéses digitalizálást [Zhu2026a] is.
Valódi, többlapos, nyilvános rajzsorozatból kevés van; az OPEN100 sorozat 12 lapja ezek közé
tartozik [OPEN100].

### Üzemi méretű kérdés-válaszolás: a plantgraph

A fenti munkák egy-egy rajzlapot vizsgálnak, és a rajzon kívüli dokumentumokat nem kapcsolják be.
A plantgraph a rajzi kérdés-válaszolást üzemi méretben vizsgálja. Mivel nincs nyilvános, a lapok
közötti kapcsolatok megoldókulcsával ellátott többlapos rajzkészlet, szintetikus üzemeket
generál: egy véletlenszám-generátor dönt az üzem felépítéséről, és ennek kezdőértéke, a seed,
egyértelműen meghatározza az üzemet (ugyanaz a seed mindig ugyanazt az üzemet adja). A kérdéseket
és a referenciaválaszokat program számolja ki az ismert üzemgráfból, és a válaszokat is program
pontozza; a pontosság a helyes válaszok aránya. A generátornak két változata van: egy egyszerűbb
és egy valósághűbb, amelynek üzemeiben oszlopok, reaktorok, biztonsági szelepek és a berendezések
között sok jelöletlen idom is van.

A plantgraph mérései két tanulsággal szolgálnak ehhez a dolgozathoz. Az első, hogy a teljes rajz
promptba tétele (a ContextRAG) nem skálázódik. Az egyszerűbb generátor üzemein ennek pontossága 1
lapról 30 lapra 0,824-ről 0,658-ra csökkent, miközben a kaszkádé 0,941-ről 0,947-re változott, és
kérdésenként 1 lapon 1,8-szer, 30 lapon 41,5-ször annyiba került, mint a kaszkád. A szövegként
leírt rajz egy bizonyos méret fölött el sem fér a modell promptjában; ez a határ az egyszerűbb
generátor üzemein körülbelül 143, a valósághűbbén körülbelül 62 lap. A második tanulság, hogy a
kaszkád nagy üzemen is működik. A valósághűbb generátorra hangolt és befagyasztott kaszkád a
hangolás során nem használt üzemeken kb. 100 lapon 440 kérdésből 401-re (0,911), kb. 1000 lapon
392-re (0,891) adott helyes választ. A −0,020-es különbség nem szignifikáns: a 95%-os
konfidenciaintervallum, vagyis az a tartomány, amelyben a valódi különbség nagy valószínűséggel
van, −0,059 és +0,018 között van, tehát a nullát is tartalmazza. A kérdésenkénti költség 0,00137,
illetve 0,00148 USD volt. Ezt a hangolt kaszkádot használjuk mi is (5. fejezet); a számokat nem
mérjük újra, a 6. fejezetben háttérként szolgálnak.

## Kérdés-válaszolás műszaki dokumentumokon

Gyártási dokumentumokon a Document GraphRAG a dokumentum saját szerkezetéből és egy automatikusan
épített gráfból dolgozik [Knollmeyer2025]; a szerzők elismerik, hogy szakterületen az automatikus
tudásgráf-építés pontatlan, ezért ma is főleg kézi munka. Ipari tudásbázison a Golden-Retriever a
visszakeresés előtt azonosítja és tisztázza a szakzsargont és a rövidítéseket
[GoldenRetriever2024]. A táblázatokat és a szerkezetet külön kezelő RAG-módszerek [StructRAG2025]
azt jelzik, hogy az adatlapi táblázatok a sima szövegdarabolástól eltérő kezelést igényelnek.
Mérnöki rajzokat és kézikönyveket feldolgozó látás-nyelvi modellek egy friss mérésen megtalálják a
tételeket, de gyakran pontatlanul írják le őket, és a szövegátfedésen alapuló metrikák alulmérik a
képességüket, ezért a szerzők nyelvi modellel bíráltatják a válaszokat [Kumar2026]. A szabad
szöveges válaszokat mi is bírálóval pontozzuk (3. fejezet).

A plantdocs egyetlen eszköz adatlapjából épít ISO 15926 és QUDT szerinti tudásgráfot, amelyben a
feltételek és a kereszthivatkozások külön elemek maradnak. Két lekérdezési módszert hasonlított
össze: az A1 a gráf RDF-formáját kérdezi, az A2 a Neo4j-be töltött gráfot, vektoros kereséssel
kiegészítve. A végső mérésen (a Rosemount 3051 távadó adatlapjának 200 befagyasztott kérdésén, vak
bírálóval) az A1 141, az A2 172 kérdésre adott helyes választ, ezért ebben a munkában az A2 az
adatlapoldal alapja.

## GraphRAG és visszakeresési stratégiák

A gráfalapú visszakeresés nem mindig jobb a szövegalapúnál. Egy szöveges korpuszon végzett mérés
szerint kis korpuszon a sima RAG nyer, és a gráf előnye a korpusz méretével jelenik meg
[Xiang2025]. A ChatP&ID egylapos eredménye és a plantgraph üzemi méretű mérései ugyanezt a mintát
mutatják a rajzokon, ezért kis üzemen a gráf nélküli módszer erős ellenfél.

Ha több visszakeresési stratégia áll rendelkezésre, kérdésenként lehet közöttük választani. A
GraphRAG-Router megerősítéses tanulással tanított irányítója kérdésenként választ a módszerek és a
modellek között [Fan2026]; a mi M2 irányítónk ennek egyszerű, tanítás nélküli változata, amelyben
egy nyelvi modell dönti el lépésenként, melyik meglévő rendszert hívja. A tudásgráfon végzett
kérdés-válaszolás bevett mintája az ágens, amely lépésenként eszközöket hív a gráfon, és az
eredményekből állítja össze a választ. A KBQA-Agent hét tudásbázis-eszközt ad, és minden lépés
eredménye nevet kap, így egy későbbi lépés név szerint visszautalhat rá [KBQAAgent2024]; hasonló
mintát követ a KG-Agent [KGAgent2024] és a Graph-CoT [GraphCoT2024]. A skála másik végén a szabad
lekérdezés áll: a Neo4j modellekhez készült szervere csak sémalekérdező, olvasó és író
Cypher-eszközt ad, a lekérdezést a modell írja [MCPNeo4j]. A plantgraph ágense a KBQA-Agent
családjába tartozik, a kaszkád pedig a kettőt kombinálja: a kérdést előbb a legolcsóbb lépcsőnek,
egyetlen lekérdezésnek adja, és csak akkor viszi tovább az ágenshez, ha a válasz gyanús. A gyanú
forrása önjelzés, vagyis olyan jel, amelyet a lépcső maga ad a válaszáról a helyes válasz
ismerete nélkül, például a hibát dobó vagy üres lekérdezés. Az ilyen szabály nem illeszt
paramétert a mért adatra, ezért kevésbé hajlamos a túlillesztésre.

## Összevetés

Az alábbi táblázat azt foglalja össze, hogy a kapcsolódó munkák a probléma mely részeit fedik le;
a kiértékelés méretét a forrás szerint adjuk meg.

Táblázat: A kapcsolódó munkák összevetése
| Munka | Rajz | Adatlap | Több lap | Gráf | Kiértékelés mérete |
|---|---|---|---|---|---|
| ChatP&ID [Alimin2026] | igen (DEXPI) | nem | nem, egy lap | Neo4j | 19 kérdés |
| Talking like P&IDs [Alimin2025] | igen (DEXPI) | nem | nem | sűrített gráf a promptban | 3 kérdés, egy folyamatábra |
| PIDQA [Gupta2025] | igen (szintetikus, raszteres) | nem | nem, kérdésenként egy lap | Neo4j, Cypher | 64 000 kérdés, 500 lap |
| Gadekar és társai [Gadekar2026] | igen (raszteres) | nem | nem | visszanyert folyamatgráf, 7 művelet | 3000 kérdés, szintetikus lapok |
| pid-graph-agent [PidGraphAgent2026] | igen (DEXPI) | nem | nem, kérdésenként egy fájl | gráfeszközös ágens | 15 + 37 saját kérdés |
| Everllence-esettanulmány [Kochanski2026] | igen | nem | igen | Neo4j, ágens | nem közöl |
| Lopomo és társai [Lopomo2026] | igen (126 rajz) | nem | nincs adat | automatikusan épített tudásgráf | gráfépítés, nem kérdés-válaszolás |
| Document GraphRAG [Knollmeyer2025] | nem | gyártási dokumentumok | – | dokumentumszerkezet és példánygráf | nincs adat |
| Enginuity [Kumar2026] | mérnöki rajzok | kézikönyvek, alkatrésztáblák | – | nincs | 6940 oldal |
| plantgraph | igen (szintetikus) | nem | igen, kb. 100 és 1000 lap | Neo4j, üzemi réteg | 460 kérdés a lezárt teszten |
| plantdocs | nem | igen, egy eszköz | – | ISO 15926 / QUDT, RDF és Neo4j | 200 kérdés |
| Jelen munka | igen (4–1000 lapos szintetikus üzemek) | igen, 7 adatlap | igen | összevont Neo4j-gráf | üzemenként 60 + 12 kérdés |

A rajzoldali munkák szinte mind egylaposak, és egyikük sem kapcsolja be az eszközök adatlapjait;
az egyetlen többlapos ipari példa kiértékelést nem közöl. A dokumentumoldali munkák pedig nem
használják a rajz topológiáját. Egy mérnöki kérdés gyakran mindkettőt igényli, az általunk
áttekintett irodalomban azonban nem találtunk olyan munkát, amely a rajzi gráfot és az
eszközönkénti adatlapgráfokat egy lekérdezhető modellben kötné össze, és ezt mérné. A következő
fejezetekben ezt a hiányzó lépést tesszük meg, kezdve azokkal az adatokkal, amelyeken mérünk.
