# Háttér és kapcsolódó munkák

Ebben a fejezetben összefoglaljuk a dokumentumokat, a szabványokat és a nyelvimodell-alapú
kérdezési módszereket, amelyekre a dolgozat épül, majd egy táblázatban vetjük össze a kapcsolódó
munkákat. Az irodalmat a két forrásrepó irodalmi jegyzeteiből válogattuk; csak olyan forrást
idézünk, amelyet a jegyzet szerint ténylegesen elolvastak.

## P&ID-k és gyártói adatlapok

### A P&ID mint dokumentum

A csővezeték- és műszerezési rajz (P&ID) az üzem központi tervdokumentuma: megmutatja, mely
berendezések, szelepek és műszerek vannak az üzemben, és hogyan kapcsolódnak egymáshoz
[Toghraei2019], [Christensen2020].

A rajzi elemeket a tag azonosítja (pl. P-101, FT-202). A tag betűi az elem fajtáját és szerepét
jelölik, a műszereknél az első betű a mért változót (F áramlás, P nyomás, L szint, T hőmérséklet),
a további betűk a funkciót (például T távadó, IC szabályozó); a betűk a hurokszámmal együtt adnak
egyedi azonosítót [AIChE2010a]. A csővezetékek azonosítója, a vezetékszám szokás szerint
névleges átmérőből, közegkódból, sorszámból, csőosztályból és szigetelésből áll [AIChE2010b]. A
példaüzem tagjei egyszerűsített mintát követnek: a `P-1-3` az 1. egység harmadik szivattyúja, az
`FT-2-2` a 2. egység második szabályozókörének áramlástávadója.

Egy valódi üzem rajza sok lapra tagolódik. A laphatáron átmenő vezetéket lapközi csatlakozó
(off-page connector) folytatja egy másik lapon: a lap szélén álló, feliratozott jel, amely
megnevezi a másik lapot, és amelyhez a másik lapon egy párja tartozik. A rajzi szabályok szerint
a többlapos rajzok vezetékvégei kölcsönösen hivatkoznak egymásra [ISO10628-1], és a rajzok közötti
hivatkozó jelek jól strukturált rajzszámot hordoznak, amely akár reguláris kifejezésekkel is
összeköthető [Mani2020]. A laphatár két különböző kapcsolatot vághat el. Az egyik egy cső: ekkor
két csatlakozó jelzi, hogy a vezeték a másik lapon folytatódik. A másik egy elem: ugyanaz a
berendezés több lapon is megjelenik, egyszer teljes adatokkal, máshol csak a tagjével. Az első
esetben a hiba látható (a gráf szétesik), a másodikban nem: a gráf épnek látszik, de a válaszok
hiányosak.

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
kötött értékekkel és diagramokkal; a példaüzem adatlapjai 2 és 114 oldal közöttiek (EXP-007).

Az adatlapi tény ritkán egyetlen szám. Egy szabályozószelep adatlapján egy hőmérsékleti határ
csak egy adott testanyagra és csatlakozóméret-tartományra érvényes, egy lábjegyzet tovább
szűkíti, és ugyanaz az érték két mértékegységben is ki van nyomtatva. Ha egy rendszer ebből csak
a számot és az egységet őrzi meg, a válasza nem hiányos, hanem hibás lehet. A plantdocs végső
mérésén éppen a feltételes kérdéseken volt nagy a két lekérdezési módszer különbsége: a 31
feltételes kérdésből az A1 21-re, az A2 28-ra, a 17 több feltételt kombináló kérdésből 7-re,
illetve 15-re adott helyes választ (a plantdocs `_results.md` szerint, EXP-0041).

### Szabványok az adatlapi tények ábrázolására

Az adatlapi tények szemantikus ábrázolására több, egymásra épülő szabvány áll rendelkezésre.

- Az **Industrial Data Ontology (IDO)** W3C OWL 2 felső ontológia ipari eszköz- és
  folyamatadatokhoz; korábban ISO/TR 15926-14 volt, ma ISO 23726-3 néven szabványosítják [IDO]. Ez
  adja a nyelvtant: fizikai tárgy, rész–egész viszony, információs tárgy, érték és mértékegység.
- A **POSC Caesar referenciakönyvtára (PCA RDL)** a konkrét berendezés-, cső- és
  műszerosztályok és tulajdonságok gyűjteménye; a régi azonosítói ma is feloldhatók, az új,
  gépileg olvasható forma hitelesítéshez kötött [PCARDL].
- A **CFIHOS** az üzemátadáskor elvárt adatokat írja le (tag- és berendezésosztály-attribútumok,
  dokumentum-metaadatok); referenciaadatai Excelben és CSV-ben érhetők el [CFIHOS].
- A **QUDT** a mértékegységek, mennyiségfajták és dimenziók szemantikus leírása; berendezést és
  topológiát nem modellez [QUDT].

Mérlegelhető, de a célra nem alkalmas szókészlet az OntoCAPE, amely hosszú ideje nem frissül
[OntoCAPE], a berendezést és topológiát nem modellező SOSA/SSN [SOSASSN2017], a folyamatüzemi modul
nélküli IOF [IOF] és a szivattyú- vagy szeleposztályt nem ismerő schema.org [SchemaOrg]. A plantdocs ezért az ISO 15926 vonalat
választotta (4. fejezet); mivel a DEXPI osztálydefiníciói is innen származnak, a rajzi és az
adatlapi oldalnak közös a szemantikai gyökere.

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
[StarE2020], a HyperGraphRAG pedig az n-áris tényeket hiperélekként tárolja [HyperGraphRAG2025]. A plantdocs jegyzetei szerint az ábrázolás tehát elvben megoldott; ami
nehéz, az a dokumentum szerkezetében (táblázatfejlécben, lábjegyzetben, diagramtartományban)
kódolt feltételek kinyerése. A plantdocs a feltételeket a POSC Caesar adatlap-mintájának
esetcsúcsaival ábrázolja; ezt a 4. fejezetben mutatjuk be.

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
kérdésen értékelve [Alimin2025].

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
mesterséges rajzgenerálást [Hirtreiter2022] is javasoltak. Valódi, többlapos, nyilvános
rajzsorozatból kevés van; az OPEN100 sorozat 12 lapja ezek közé tartozik [OPEN100].

### Üzemi méret

A fenti munkák közös vonása, hogy egy-egy rajzlapot vizsgálnak, és a rajzon kívüli
dokumentumokat (adatlapokat) nem kapcsolják be. Kiszely Benedek egyéni munkája a P&ID-QA-t üzemi
méretben vizsgálja: seedelt, többlapos szintetikus üzemeken, ahol a lapokra bontás a
megoldókulcs, mert nyilvános, lapközi megoldókulccsal ellátott többlapos rajzkészlet nincs. Az ott
mért kaszkád a README szerint a lezárt teszten (460 kérdés, a fejlesztés során nem látott
üzemeken) 100 lapos üzemen 0,937, 1000 lapos üzemen 0,917 pontosságot ért el. A ContextRAG
pontossága 1-ről 30 lapra 0,824-ről 0,658-ra csökkent, miközben a kaszkádé 0,941-ről 0,947-re
változott, a ContextRAG relatív költsége a kaszkádéhoz képest 1,8-szorosról 41,5-szeresre nőtt, és a
szerializált rajz körülbelül 143 lap fölött már nem fér el a promptban (Kiszely, plantgraph README).
Ezek a számok háttérként szerepelnek; jelen munka nem méri őket újra, de a 6. fejezetben ezekre
támaszkodunk, amikor a gráf nélküli módszer skálázódásáról beszélünk.

## Kérdés-válaszolás műszaki dokumentumokon

Gyártási dokumentumokon a Document GraphRAG a dokumentum saját szerkezetéből és egy könnyű,
automatikusan épített példánygráfból épít tudásgráfot [Knollmeyer2025]; a szerzők elismerik, hogy
szakterületen az automatikus tudásgráf-építés pontatlan, ezért ma is főleg kézi munka. Ipari
tudásbázison a Golden-Retriever a visszakeresés előtt egy reflexiós lépésben azonosítja és
tisztázza a szakzsargont és a rövidítéseket [GoldenRetriever2024]. Mérnöki
rajzokat és kézikönyveket feldolgozó látás-nyelvi modellek egy friss benchmarkon megtalálják a
tételeket, de gyakran pontatlanul írják le őket, és a szövegátfedésen alapuló metrikák alulmérik
a képességüket; a szerzők ezért keresztbírálós LLM-értékelést használnak [Kumar2026]. Ezért a
szabad szöveges válaszokat mi is bírálóval pontozzuk (3. fejezet).

Szabó Zsombor egyéni munkája (plantdocs) egyetlen eszköz adatlapjából épít ISO 15926 / QUDT
szerinti tudásgráfot, amelyben a feltételek és a kereszthivatkozások külön elemek maradnak. Két lekérdezési
módszert hasonlít össze: A1 (RDF + SPARQL) és A2 (Neo4j + Cypher, vektoros kereséssel). A
plantdocs végső mérésén (EXP-0041, a Rosemount 3051 adatlap 200 befagyasztott kérdésén, GLM-mel,
vak bírálóval) az A1 141, az A2 172 kérdésre adott helyes választ (a plantdocs `_results.md`
szerint). Ebben a munkában az A2 az adatlapoldal alapja.

## GraphRAG és visszakeresési stratégiák

### Mikor segít a gráf?

A gráfalapú RAG nem mindig jobb a szövegalapúnál. Egy benchmark szöveges korpuszon méretfüggő
keresztezést mutatott ki a sima RAG és egy gráfalapú módszer között: kis korpuszon a sima RAG nyer,
és a gráf előnye a korpusz méretével jelenik meg [Xiang2025]. A ChatP&ID egylapos eredménye
és Benedek üzemi méretű mérései ugyanezt a mintát mutatják a rajzokon; a mi négylapos
példaüzemünkön ezért a gráf nélküli módszer erős ellenfél.

Ha több visszakeresési stratégia áll rendelkezésre, kérdésenként lehet közöttük választani. A
GraphRAG-Router megerősítéses tanulással tanított útválasztója kérdésenként választ GraphRAG-módszer
és nyelvi modell között, és ezzel csökkenti a nagy modell hívásainak számát [Fan2026]. A mi M2
routerünk ennek egyszerű, tanítás nélküli változata: egy nyelvi modell dönti el lépésenként,
melyik meglévő rendszert hívja.

### Gráfeszközöket hívó ágensek

A tudásgráf-kérdés-válaszolás bevett mintája az ágens, amely lépésenként eszközöket hív a gráfon,
és az eredményekből állítja össze a választ. A KBQA-Agent hét tudásbázis-eszközt ad (relációk,
szomszédok, attribútumok, legnagyobb és legkisebb érték, metszet, darabszám), amelyek a korábbi
lépések eredményeit megnevező változókon dolgoznak [KBQAAgent2024]. Hasonló mintát követ a KG-Agent
[KGAgent2024] és a Graph-CoT [GraphCoT2024]. A skála másik végén a szabad
Cypher áll: a Neo4j MCP-szervere mindössze sémalekérdező, olvasó és író Cypher-eszközt ad, a
lekérdezést a modell írja [MCPNeo4j].

Benedek ágense a KBQA-Agent családjába tartozik: hat általános, egymással komponálható üzemi
primitívet hív, az eredményeket hivatkozással adja tovább (plantgraph README, ADR-0034); a mi
`datasheet_fact` primitívünk ezt a készletet bővíti (5. fejezet).

### Kaszkád és önjelzés

A kaszkád (lépcsős módszer) a kérdést előbb a legolcsóbb módszernek adja, és csak akkor viszi
tovább, ha az olcsó válasz gyanús. A gyanú forrása önjelzés: olyan jel, amelyet a lépcső maga ad
a válaszáról, a helyes válasz ismerete nélkül, például a hibát dobó vagy üres lekérdezés. Az ilyen
szabály nem illeszt paramétert a mért adatra, ezért kevésbé hajlamos a túlillesztésre, mint a
kérdéstípus szerinti útválasztás (Benedek tanulási jegyzete a kaszkádról). Benedek kaszkádja is
ilyen szabállyal dönt; az 5. fejezetben részletezzük.

## Összevetés

Az alábbi táblázat azt foglalja össze, hogy a kapcsolódó munkák a probléma mely részeit fedik le;
a kiértékelés méretét a forrás jegyzete vagy README-je szerint adjuk meg.

Táblázat: A kapcsolódó munkák összevetése (a két forrásrepó irodalmi jegyzetei, a két forrásrepó README-je és `_results.md`-je, valamint EXP-004 és EXP-009 alapján)
| Munka | Rajz | Adatlap | Több lap | Gráf | Kiértékelés mérete |
|---|---|---|---|---|---|
| ChatP&ID [Alimin2026] | igen (DEXPI) | nem | nem, egy lap | Neo4j, tulajdonsággráf | 19 kérdés |
| Talking like P&IDs [Alimin2025] | igen (DEXPI) | nem | nem | sűrített gráf a promptban | 3 kérdés, egy folyamatábra |
| Gadekar és társai [Gadekar2026] | igen (raszteres) | nem | nem | visszanyert folyamatgráf, 7 operátor | 3000 kérdés, szintetikus lapok |
| pid-graph-agent [PidGraphAgent2026] | igen (DEXPI) | nem | nem, kérdésenként egy fájl | gráfeszközös ágens | 15 + 37 saját kérdés |
| Everllence-esettanulmány [Kochanski2026] | igen | nem | igen | Neo4j, ágens | nem közöl |
| Lopomo és társai [Lopomo2026] | igen (126 rajz) | nem | a jegyzet nem rögzíti | automatikusan épített tudásgráf | gráfépítés, nem kérdés-válaszolás |
| Document GraphRAG [Knollmeyer2025] | nem | gyártási dokumentumok | – | dokumentumszerkezet és példánygráf | a jegyzet nem rögzíti |
| Enginuity [Kumar2026] | mérnöki rajzok | kézikönyvek, alkatrésztáblák | – | nincs | 6940 oldal |
| plantgraph (Kiszely) | igen (szintetikus) | nem | igen, kb. 100 és 1000 lap | Neo4j, üzemi réteg | 460 kérdés a lezárt teszten |
| plantdocs (Szabó) | nem | igen, egy eszköz | – | ISO 15926 / QUDT, RDF és Neo4j | 200 kérdés |
| Jelen munka | igen (4 lap) | igen, 7 adatlap | igen | összevont Neo4j-gráf | 20 dev + 40 teszt kérdés, 12 (e) kérdés |

A rajzoldali munkák szinte mind egylaposak, és egyikük sem kapcsolja be az eszközök adatlapjait;
az egyetlen többlapos ipari példa kiértékelést nem közöl. A dokumentumoldali munkák pedig nem
használják a rajz topológiáját.

## A hiányzó lépés

A két egyéni munka ugyanannak az üzemi dokumentációnak két oldalát dolgozza fel. A rajzon
látszik, hogy mi mivel áll kapcsolatban, az adatlapon, hogy egy eszköz mire képes. Egy mérnöki
kérdés gyakran mindkettőt igényli („mekkora a maximális nyomás azon a szelepen, amely a P-101
nyomóoldalát elzárja?”). Nem találtunk olyan munkát a két repó irodalmi jegyzeteiben, amely a
rajzi gráfot és az eszközönkénti adatlapgráfokat egy lekérdezhető modellben kötné össze, és ezt
mérné. Ez a dolgozat tárgya.
