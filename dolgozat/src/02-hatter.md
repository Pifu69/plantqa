# Háttér és kapcsolódó munkák

## P&ID-k és gyártói adatlapok

A csővezeték- és műszerezési rajz (P&ID) az üzem központi tervdokumentuma: megmutatja, mely
berendezések, szelepek és műszerek vannak az üzemben, és hogyan kapcsolódnak egymáshoz
[Toghraei2019], [Christensen2020]. Egy valódi üzem rajza sok lapra tagolódik; a laphatáron
átmenő vezetéket lapközi csatlakozó (off-page connector) folytatja egy másik lapon. A rajzi
elemeket a tag azonosítja (pl. P-101, FT-202); a tag betűi az elem fajtáját jelölik. A rajz
digitális cseréjének szabványa a DEXPI, amely az ISO 15926-4 referenciakönyvtárára épülő UML
információs modell XML-szerializációval [DEXPI2025]; Python-megvalósítása a pyDEXPI [pyDEXPI].

A rajz csak a kapcsolatokat mutatja; az egyes eszközök műszaki jellemzőit (nyomás- és
hőmérséklethatár, anyag, méret, opciók) a gyártói adatlapok tartalmazzák. Egy adatlap tipikusan
több tíz oldalas PDF, táblázatokkal, lábjegyzetekkel, feltételekhez kötött értékekkel és
diagramokkal. Az adatlapi tények szemantikus ábrázolására az ISO 15926 utódjaként szabványosított
Industrial Data Ontology (IDO) [IDO], a POSC Caesar referenciakönyvtára [PCARDL], a CFIHOS
attribútumkészlete [CFIHOS] és a mértékegységekre a QUDT [QUDT] áll rendelkezésre.

## Kérdés-válaszolás P&ID-ken

A legközelebbi előzmény a ChatP&ID [Alimin2026]: DEXPI-rajzokat pyDEXPI-vel Neo4j-gráffá alakít,
és egy ágens négy visszakeresési eszköz (ContextRAG, VectorRAG, PathRAG, CypherRAG) közül
választ. Egyetlen lapon, 19 kérdésen a teljes gráfot a promptba tevő ContextRAG adta a legjobb
eredményt. Egy korábbi munka ugyanettől a csoporttól a sűrített gráfot GraphML-ként, visszakeresés
nélkül adja a modellnek [Alimin2025]. Raszteres rajzokon a Gadekar és társai által javasolt
módszer a visszanyert folyamatgráfra korlátozza a látás-nyelvi modell válaszait, hét tényt
visszaadó gráfoperátoron keresztül [Gadekar2026]. A rajzok gráffá alakítása maga is aktív terület:
transzformeres digitalizálás és a PID2Graph adatkészlet [Sturmer2024], [PID2Graph2025], ipari
rajzokból automatikus tudásgráf-építés [Lopomo2026], szabályalapú javítás gráfon
[SchulzeBalhorn2025] és mesterséges rajzgenerálás [Hirtreiter2022]. Valódi, többlapos, nyilvános
rajzsorozatból kevés van; az OPEN100 sorozat 12 lapja ezek közé tartozik [OPEN100].

Közös vonásuk, hogy egy-egy rajzlapot vizsgálnak, és a rajzon kívüli dokumentumokat (adatlapokat)
nem kapcsolják be. Kiszely Benedek egyéni munkája a P&ID-QA-t üzemi méretben vizsgálja: seedelt,
többlapos szintetikus üzemeken, ahol a lapokra bontás a megoldókulcs. Az ott mért kaszkád a
README szerint a lezárt teszten 100 lapos üzemen 0,937, 1000 lapos üzemen 0,917 pontosságot ért
el, és a ContextRAG pontossága és költsége a lapszámmal romlott (Kiszely, plantgraph README és
`_results.md`). Ezek a számok háttérként szerepelnek; jelen munka nem méri őket újra.

## Kérdés-válaszolás műszaki dokumentumokon

Gyártási dokumentumokon a Document GraphRAG a dokumentum saját szerkezetéből és egy könnyű
példánygráfból épít tudásgráfot [Knollmeyer2025]; ipari tudásbázison a Golden-Retriever a
szakzsargon tisztázásával javítja a visszakeresést [GoldenRetriever2024]. Mérnöki rajzokat és
kézikönyveket feldolgozó látás-nyelvi modellek egy friss benchmarkon megtalálják a tételeket, de
gyakran pontatlanul írják le őket [Kumar2026]. Az adatlapi tények jelentős része feltételhez
kötött (egy hőmérséklethatár csak egy anyagra érvényes), és az ilyen n-áris tények bináris
hármasokra bontása elveszíti a feltételt; erre a hiper-relációs tudásgráfok és a hipergráfos RAG
ad ábrázolást [StarE2020], [HyperGraphRAG2025], [HyperRAG2026].

Szabó Zsombor egyéni munkája (plantdocs) egyetlen eszköz adatlapjából épít ISO 15926 / QUDT
szerinti tudásgráfot, amelyben a feltételek és a kereszthivatkozások külön elemek maradnak.
Két lekérdezési módszert hasonlít össze: A1 (RDF + SPARQL) és A2 (Neo4j + Cypher, vektoros
kereséssel). A plantdocs végső mérésén (EXP-0041, a Rosemount 3051 adatlap 200 befagyasztott
kérdésén, GLM-mel, vak bírálóval) az A1 141, az A2 172 kérdésre adott helyes választ (a plantdocs
`_results.md` szerint). Ebben a munkában az A2 az adatlapoldal alapja.

## GraphRAG és visszakeresési stratégiák

A gráfalapú RAG nem mindig jobb a szövegalapúnál: egy benchmark szerint kis korpuszon a sima RAG
nyer, és a gráf előnye a korpusz méretével jelenik meg [Xiang2025]. Kérdésenkénti útválasztással a
GraphRAG-módszerek között a nagy modell hívásai csökkenthetők [Fan2026]. A gráfeszközöket hívó
ágensek (KBQA-Agent, KG-Agent, Graph-CoT) a tudásgráf-kérdés-válaszolás bevett mintái
[KBQAAgent2024], [KGAgent2024], [GraphCoT2024]; Benedek ágense és a mi új primitívünk ebbe a
családba tartozik.

## A hiányzó lépés

A két egyéni munka ugyanannak az üzemi dokumentációnak két oldalát dolgozza fel. A rajzon
látszik, hogy mi mivel áll kapcsolatban, az adatlapon, hogy egy eszköz mire képes. Egy mérnöki
kérdés gyakran mindkettőt igényli („mekkora a maximális nyomás azon a szelepen, amely a P-101
nyomóoldalát elzárja?”). Nem találtunk olyan munkát a két repó irodalmi jegyzeteiben, amely a
rajzi gráfot és az eszközönkénti adatlapgráfokat egy lekérdezhető modellben kötné össze, és ezt
mérné. Ez a dolgozat tárgya.
