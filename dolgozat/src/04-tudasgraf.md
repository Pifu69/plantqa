# Az összevont tudásgráf

A két egyéni munka két külön gráfot épít: a rajzból egy üzemi réteget (Benedek), az adatlapokból
eszközönként egy-egy adatlapgráfot (plantdocs). Az összevonás célja, hogy egyetlen adatbázisban
egyetlen lekérdezés mindkettőt elérje. Ebben a fejezetben előbb röviden összefoglaljuk a két
forrásfolyamatot és az általuk épített réteget, utána a két réteg közötti kapcsolatot és a
betöltés mérését. A két folyamat kódját nem módosítottuk; részletes leírásuk, amely a két
egyéni munka terveiből és kódjából származik, a Függelék D-ben található.

## A rajzoldali réteg

Benedek rendszerében a generátor egy teljes üzemet épít, a lapokra bontó (splitter) lapokra
vágja, a feloldó (resolver) a lapokból megoldókulcs nélkül visszaépíti az üzemet, végül a betöltő
Neo4j-be tölti (részletesen: Függelék D). A generátor minden véletlen döntést egyetlen seedelt véletlenszám-generátoron át
hoz meg, ezért ugyanaz a seed ugyanazt az üzemet adja; a kimenet valódi pyDEXPI-modell elágazó
topológiával, a berendezésekhez tartozó szabályozókörökkel és a szokásos tagbetűkkel. A
példaüzemek a generátor egyszerűbb, első változatával készültek, mert a valósághűbb, későbbi
változat berendezésosztályai nem szűkíthetők az adatlappal rendelkező osztályokra. A bontó minden elvágott
élre lapközi csatlakozópárt illeszt, a megoldókulcsot pedig külön fájlba írja, amely a vizsgált
adatbázisba nem kerül be. A feloldó csak a lapokat látja: a csatlakozókat a feliratuk kölcsönös
hivatkozása alapján párosítja, a több lapon felrajzolt elemeket a (tag, osztály) kulcs szerint
vonja össze, és nem találgat. Mivel a bontást a rendszer maga végzi, a feloldó eredménye a
megoldókulcshoz mérhető. A példaüzem 4 lapja között 4 lapközi csatlakozópár van; a
rajzexportban mind a 8 lapközi jel összekötött, a visszaépítési ellenőrzés pedig
hibátlan volt.

### Az üzemi réteg és a vonalnézet

Benedek döntése szerint az adatbázisban két réteg lehet: a rajz szerinti
előfordulásréteg (rajzolt szimbólumok, lapközi csonkok, azonossági élek) a nyomon követésre, és az
összevont üzemi réteg, a tulajdonképpeni tudásgráf, amely kizárólag a feloldó kimenetéből épül.
Az üzemi rétegben egy laphatár átlépése egyetlen él, az előfordulásrétegben több lépéses minta.

A generált üzemet Benedek betöltője tölti a Neo4j-adatbázisba. Minden rajzi elem pontosan egy
csúcs lesz, akkor is, ha több lapon is szerepel. A csúcs több szinten is hordozza az elem
típusát: egy centrifugálszivattyú egyben szivattyú és berendezés is, így egy lekérdezés bármelyik
szinten rákereshet. Az elemek közötti csöveket az áramlás irányába mutató kapcsolatok írják le
(`send_to`); ha egy ilyen kapcsolat átlépi a laphatárt, ezt a kapcsolat jelölése is rögzíti. A
jelvezetékeknek, a mérésnek (melyik távadó melyik elemet méri) és a beavatkozásnak (melyik
szabályozó melyik szelepet működteti) külön kapcsolattípusa van. Végül minden elem kapcsolatban
áll azzal a lappal, amelyen szerepel, és azzal az egységgel, amelyhez tartozik.

Erre épül a vonalnézet. Ez egy rövidítő kapcsolat (`line_to`), amely két berendezést vagy szelepet
közvetlenül köt össze, és átugorja a köztük lévő kisebb csőidomokat. Így az olyan kérdés, mint „mi
a szivattyú utáni következő szelep?”, egyetlen lépésben megválaszolható; az átugrott elemeket a
rövidítő kapcsolat megjegyzi. A csövenkénti kapcsolatok is megmaradnak, így a részletes nézet sem
vész el. A vonalnézetet Benedek a generátor valósághűbb változatának üzemeihez vezette be, ahol
sok jelöletlen idom áll az elemek között; a mi üzemeinkben ilyen idom nincs, de a kaszkád
promptjai és lekérdezési szabályai erre a nézetre készültek, ezért ezt használjuk. A kis
prototípus-üzem üzemi rétege 36 csúcsból és 116 kapcsolatból áll.

## Az adatlapoldali réteg

A plantdocs egy gyártói adatlap PDF-jéből tíz számozott lépésben jut el az ontológia szerinti
RDF-gráfig:

1. elrendezés-elemzés az Azure Document Intelligence szolgáltatással (bekezdések, táblázatok, ábrák);
2. rekordok: egy nyelvi modell a táblázatokból paraméter–érték–egység rekordokat ír, a
   táblázatbeli útvonallal;
3. ábrák: kivágás, osztályozás és a rajzokon lévő jelek feloldása;
4. diagramok leolvasása;
5. ellenőrzés: minden rekord számának megkeresése a PDF szövegében;
6. célformátum: a rekordokból ontológiafüggetlen tények és feltételek;
7. lábjegyzetek: az ábrákhoz tartozó lábjegyzetek bekötése;
8. forrásleírások: minden forrásról (táblázatról, ábráról, szövegrészről) rövid leírás;
9. szókészlet-illesztés: a tulajdonságokhoz és feltételekhez szabványos fogalmak rendelése;
10. RDF: a gráf előállítása.

A lépések felváltva programok és nyelvi modellek; minden nyelvimodell-lépés kimenete csak akkor
mehet tovább, ha átmegy egy programmal ellenőrzött formai és tartalmi feltételrendszeren. Az
általunk feldolgozott négy adatlapon minden nyelvimodell-kimenet elsőre átment ezen az
ellenőrzésen.

A célformátumban egy rekord egy tény, nem egy nyomtatott cella; a feltételek elsőrendű elemek,
a nyomtatott forma megmarad, és minden visszakövethető a PDF-oldalig. Az RDF-modell a plantdocs
ontológiai döntése szerint az ISO 15926 vonalat követi: az IDO a felső ontológia, a
POSC Caesar könyvtára az eszköz- és referenciaszótár, a mértékegység QUDT, saját, kézzel írt
szókészlet pedig nem lehet. Egy mennyiségi tény mennyiségi adatpont (Quantity Datum), a
feltételek együttese egy esetcsúcs (Case), amelyre a tény és minden egyes feltétel mutat, a forrás
szakaszcsúcs (Section Datum), a lábjegyzet külön adatpont (részletesen: Függelék D).

### Az adatlapréteg a Neo4j-ben

Egy adatlapgráf a plantdocs RDF-kimenete, amelyet a neosemantics (n10s) bővítmény tölt be:
minden csúcs `:Resource {uri}`, az RDF-típusok további címkék (például a mennyiségi adatpont
címkéje `plm__PCA_100029511`), a szabványos azonosítók rövidített előtagos neveket kapnak. Az
eszköz gyökércsúcsának URI-ja `urn:plantdocs:<doc>:device`. Az adatpontok az eszközre vagy egy
alkatrészére mutatnak, a feltételeket esetcsúcs, a lábjegyzeteket külön adatpont, a forrást
(táblázat, ábra, szakasz) forrásszakasz-csúcs hordozza oldalszámmal. Ez a szerkezet őrzi meg,
hogy egy érték milyen feltétel mellett és melyik oldalon érvényes. A hét eszközgráf együtt
27 615 csúcsból és 103 366 kapcsolatból áll; a közös szókészlet-csúcsok (egységek, osztályok,
szabványos attribútumok) száma 221.

![Az összevont gráf csúcsai rétegenként és adatlaponként.](../../figures/graph_layers.png)

## Az összekötés

A két réteget egy kapcsolat köti össze: `(:PlantItem {tag})-[:DESCRIBED_BY]->(eszköz)`. A
kapcsolatot a program által előállított tag → adatlap tábla alapján töltjük be; a 26 tagelt
elemből 24-nek van adatlapja, ennyi `DESCRIBED_BY` él jön létre. Több tag
mutathat ugyanarra az eszközgráfra: a nyolc szivattyú ugyanazt a Gorman-Rupp adatlapot kapja,
mert ugyanaz a típus. A névütközést az URI-k dokumentumonkénti előtagja zárja ki; emellett
minden adatlapcsúcs `document_id` tulajdonságot kap, amellyel a lekérdezés egy dokumentumra
szűkíthető. A közös szókészlet-csúcsok (például egy mértékegység) az eszközök között közösek.

Egy összetett kérdés így egyetlen bejárásként fogalmazható meg: a rajzi rétegben megkeressük a
kérdéses elemet (például a P-1-1 utáni első szelepet a `line_to` mentén), a `DESCRIBED_BY`
kapcsolaton átlépünk az adatlapjára, és ott a megfelelő adatpontot olvassuk ki a feltételével és
az oldalszámával. Az alábbi minta az összevont gráf egy részletét mutatja Cypher-jelöléssel: egy
szivattyút, a rajzi szomszédját, az adatlapja gyökércsúcsát és egy adatpontot a környezetével.

```
// rajzi réteg (Benedek, vonalnézet)
(p:PlantItem:CentrifugalPump {tag: 'P-1-3'})-[:line_to]->(v:PlantItem:Valve)
(p)-[:is_drawn_on]->(:Sheet)

// az összekötés
(p)-[:DESCRIBED_BY]->(dev:Resource:lis__PhysicalObject)

// adatlapi réteg (plantdocs, egy adatpont a környezetével)
(d:plm__PCA_100029511)-[:plm__PCA_100029516]->(dev)                 // alany: az eszköz vagy egy alkatrésze
(d)-[:plm__PCA_100029520]->(c:plm__PCA_100029524)                   // eset: a feltételek együttese
(cond:plm__PCA_100029508)-[:plm__PCA_100029520]->(c)                // egy feltétel ugyanabban az esetben
(d)-[:plm__PCA_100029525]->(s:plm__PCA_100029513)                   // forrásszakasz, oldalszámmal
(d)-[:plm__PCA_100029514]->(f:plm__PCA_100029505)                   // lábjegyzet
(d)-[:lis__datumUOM]->(u:Resource)                                  // mértékegység, QUDT-megfeleltetéssel
```

Az összekötés módját több alternatívával szemben választottuk. A legegyszerűbb az lett volna, ha
az adatlapi tényeket tulajdonságként a rajzi csúcsra másoljuk; ez azonban éppen a feltételeket,
a lábjegyzeteket és az oldalszámot veszítené el, amelyekért a plantdocs gráfja készült. Két
külön adatbázis között egy lekérdezés nem járhat át (és a helyi Neo4j Community kiadás csak egy
felhasználói adatbázist enged); az egész gráf RDF-ben pedig Benedek Neo4j-re írt kaszkádjának
módosítását igényelte volna. A
tagalapú él a legkisebb beavatkozás: egyik réteg szerkezete sem változik, és a kapcsolat a
gyakorlatot követi, ahol a tag köti össze a rajzot a többi dokumentummal. Ára, hogy a tag →
adatlap táblát elő kell állítani; nálunk ezt program végzi a generátor kimenetéből (3. fejezet),
valódi üzemben ez az eszközlista vagy az átadási adatbázis dolga volna.

## Betöltés

A betöltés egy paranccsal újrafuttatható. Sorrendje: az
adatbázis törlése és a neosemantics beállítása, az eszközgráfok betöltése és névtérbe sorolása,
az üzemi réteg betöltése Benedek betöltőjével (amely csak a saját korpuszát törli), a
`DESCRIBED_BY` élek, végül a plantdocs A2 vektoros kereséséhez szükséges beágyazások. A teljes
betöltés 243,2 s; ennek nagy része (222,4 s) a 14 489 beágyazás előállítása, tárolása és indexelése, az üzemi
réteg 3,6 s alatt töltődik be. A helyi Neo4j Community kiadás csak egy felhasználói
adatbázist enged, ezért a betöltő minden futáskor az egész adatbázist újraépíti.

Két illesztési pontra külön figyelni kellett. Benedek tárellenőrzése összeveti az adatbázis
kapcsolatszámait a betöltési tervvel, és eltérésnél nem indítja el a kaszkádot; ezért a kaszkád egy
leszármazott nézeten át olvas, amely a `DESCRIBED_BY` kapcsolatot nem számolja a rajzi
korpuszhoz. A másik pont a plantdocs: az alkalmazása dokumentumonként törli és
újratölti az adatbázist, ami az összevont gráfot tönkretenné. Ezért az A2-t nem az alkalmazáson
át hívjuk, hanem közvetlenül a lekérdező függvényét, egy dokumentumra szűkítő lekérdezés-futtatóval
(5. fejezet).
