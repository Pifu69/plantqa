# Az összevont tudásgráf

A két egyéni munka két külön gráfot épít: a rajzból egy üzemi réteget (Benedek), az adatlapokból
eszközönként egy-egy adatlapgráfot (plantdocs). Az összevonás célja, hogy egyetlen adatbázisban
egyetlen lekérdezés mindkettőt elérje. Ebben a fejezetben a két réteget, a köztük lévő
kapcsolatot és a betöltés mérését mutatjuk be.

## Az üzemi réteg

A generált üzemet Benedek betöltője tölti Neo4j-be, a kaszkád által olvasott `plant_lines`
profillal. Minden rajzi elem egyetlen `(:PlantItem)` csúcs, akárhány lapon szerepel is;
osztálycímkéi a konkrét osztálytól a családig terjednek (például
`:PlantItem:CentrifugalPump:Pump:Equipment`). Az anyagáramot a `send_to` kapcsolat írja le,
csőrészenként; a `line_to` a jelöletlen idomokat átugorva köti a berendezéseket és szelepeket; a
lapot átlépő kapcsolat `crossed_sheets` tulajdonságot kap. A jelutakat a `send_signal_to`, a
mérést a `measured_by`, a beavatkozást a `control` kapcsolat ábrázolja. A példaüzem üzemi rétege
36 csúcsból és 116 kapcsolatból áll (EXP-005).

## Az adatlapréteg

Egy adatlapgráf a plantdocs RDF-kimenete, amelyet a neosemantics (n10s) bővítmény tölt be:
minden csúcs `:Resource {uri}`, az RDF-típusok további címkék (például a mennyiségi adatpont
címkéje `plm__PCA_100029511`). Az eszköz gyökércsúcsának URI-ja `urn:plantdocs:<doc>:device`.
Az adatpontok az eszközre vagy egy alkatrészére mutatnak, a feltételeket esetcsúcs, a
lábjegyzeteket külön adatpont, a forrást (táblázat, ábra, szakasz) forrásszakasz-csúcs hordozza
oldalszámmal. Ez a szerkezet őrzi meg, hogy egy érték milyen feltétel mellett és melyik oldalon
érvényes. A hét eszközgráf együtt 27 615 csúcsból és 103 366 kapcsolatból áll; a közös
szókészlet-csúcsok (egységek, osztályok, szabványos attribútumok) száma 221 (EXP-005).

![Az összevont gráf csúcsai rétegenként és adatlaponként (EXP-005).](../../figures/graph_layers.png)

## Az összekötés

A két réteget egy kapcsolat köti össze: `(:PlantItem {tag})-[:DESCRIBED_BY]->(eszköz)`. A
kapcsolatot a program által előállított tag → adatlap tábla alapján töltjük be; a 26 tagelt
elemből 24-nek van adatlapja, ennyi `DESCRIBED_BY` él jön létre (EXP-002, EXP-005). Több tag
mutathat ugyanarra az eszközgráfra: a nyolc szivattyú ugyanazt a Gorman-Rupp adatlapot kapja,
mert ugyanaz a típus. A névütközést az URI-k dokumentumonkénti előtagja zárja ki; emellett
minden adatlapcsúcs `document_id` tulajdonságot kap, amellyel a lekérdezés egy dokumentumra
szűkíthető. A közös szókészlet-csúcsok (például egy mértékegység) az eszközök között közösek.

Egy összetett kérdés így egyetlen bejárásként fogalmazható meg: a rajzi rétegben megkeressük a
kérdéses elemet (például a P-1-1 utáni első szelepet a `line_to` mentén), a `DESCRIBED_BY`
kapcsolaton átlépünk az adatlapjára, és ott a megfelelő adatpontot olvassuk ki a feltételével és
az oldalszámával.

## Betöltés

A betöltés egy paranccsal újrafuttatható (`python -m plantqa.graph.load`). Sorrendje: az
adatbázis törlése és a neosemantics beállítása, az eszközgráfok betöltése és névtérbe sorolása,
az üzemi réteg betöltése Benedek betöltőjével (amely csak a saját korpuszát törli), a
`DESCRIBED_BY` élek, végül a plantdocs A2 vektoros kereséséhez szükséges beágyazások. A teljes
betöltés 243,2 s; ennek nagy része (222,4 s) a 14 489 beágyazás tárolása és indexelése, az üzemi
réteg 3,6 s alatt töltődik be (EXP-005). A helyi Neo4j Community kiadás csak egy felhasználói
adatbázist enged, ezért a betöltő minden futáskor az egész adatbázist újraépíti.
