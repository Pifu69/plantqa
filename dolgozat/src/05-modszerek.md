# Kérdés-megválaszolási módszerek

Három módszert hasonlítunk össze. Mindhárom a két meglévő rendszerre épül, azokat nem
módosítja: a kódjukat importáljuk, és csak a hiányzó kapcsolatot írjuk meg. A három módszer
ugyanazt a kérdést kapja (szöveg és elvárt válaszalak), és ugyanabban az alakban válaszol:
egy JSON-objektum a válasszal és egy jelzővel arra, hogy a dokumentumok nem tartalmazzák a
választ. Mindhárom módszert mindkét kérdés-válaszoló modellel mérjük: a `z-ai/glm-5.3-flash` és
az `openai/gpt-6-luna` modellel, Benedek rögzített paramétereivel (pinjeivel).

A válaszalak Benedek kérdéstípusait követi: szabad szöveg (`FREE_TEXT`), egy tag vagy taghalmaz
(`TAG`, `TAG_SET`), rendezett út (`TAG_PATH`), igen/nem (`BOOLEAN`), darabszám (`COUNT`), egység
(`UNIT_ID`) és osztálynév (`CLASS_NAME`). A válaszalakot leíró mondatot mindhárom módszer
Benedek kódjából veszi, így a válaszíró modell mindhárom esetben ugyanazt az utasítást látja. A
fejezetben előbb a közös építőelemeket, majd a három módszert és a tervezési döntéseiket
mutatjuk be, végül megfogalmazzuk, mit várunk az egyes módszerektől.

![A három módszer felépítése. Bal: M1 (egy összevont gráf); közép: M2 (router a két rendszer fölött); jobb: M3 (gráf nélküli baseline).](../../figures/methods_overview.png)

## Közös építőelemek

### A rajzoldali kaszkád

Benedek legutóbb mért szabályozott kaszkádja, a `cascade_v4_iso` (a V2T-A rendszer) két szintből
áll. A kaszkádot Benedek a valósághűbb v2 üzemeken hangolta egy külön megjelölt rendszerként
(V2T, ADR-0061), a pontosságot helyezve előtérbe. A hangolás többek között a jelöletlen
idomokat (ehhez készült a 4. fejezetben leírt vonalnézet, mindkét szintre ugyanazzal a
szabállyal), a Cypher-lekérdezések szintaktikai hibáit és a korlátlan útkereséstől lejáró
lekérdezéseket kezelte. A kaszkád két változata közül a `cascade_v4_iso`-t egy előre rögzített szabály
választotta: akkor lép a `cascade_v4` helyébe, ha a hangolókészleten legalább olyan pontos
(`docs/felmeres.md`).

**Első szint: egy Cypher-lekérdezés.** Egy LLM egyetlen Cypher-lekérdezést ír a Neo4j-ben tárolt
üzemi rétegre (`cypher_rag_lines`). A prompt Benedek sémaszövegét (a csúcscímkéket, a
kapcsolatokat és a tulajdonságokat), egy rövid, általános P&ID-olvasási bevezetőt (primer) és
lekérdezési formaszabályokat tartalmaz: korlátlan hosszúságú változó utat nem szabad kötni,
halmazhoz különböző végpontokat kell kérni, útvonalhoz a legrövidebb utat, elérhetőséghez
létezésvizsgálatot a `line_to` mentén. A lekérdezés csak olvashat, 30 s időkorláttal és
legfeljebb 1000 sorral fut. Ha a lekérdezés hibát ad, egy javítókörben a modell megkapja az
adatbázis hibaüzenetét, és újraírhatja. Egy programozott ellenőrzés emellett azt is megnézi, hogy
a kérdésben szereplő tagek léteznek-e. A sorokból a közös válaszlépés fogalmaz.

**Az elfogadási szabály.** A Cypher-szint válaszát a kaszkád akkor fogadja el, ha az önjelzések
mind rendben vannak: a lépés válaszolt, nem tartózkodott („nincs benne” válasz helyett érdemben
felelt), a lekérdezés adott sort, és az eredmény nem csonka (nem érte el a sorkorlátot). Egyik jel
sem igényli a helyes válasz ismeretét, ezért a szabály a teszten is alkalmazható, és nincs
illesztett paramétere. Ha bármelyik jel hiányzik, a kérdés a második szintre kerül.

**Második szint: gráfeszköz-ágens.** Az ágens (`graph_agent_lines`) üzemi primitíveket hív
lépésenként, legfeljebb 40-szer. Minden lépésben egy JSON-akciót ír (egy primitív hívását az
argumentumaival, vagy a befejezést), a primitív eredményét szövegesen kapja vissza, és a
végén az összegyűjtött megfigyelésekből ugyanaz a közös válaszlépés fogalmaz, amely a Cypher-szint
válaszát is írja. A közös válaszlépés szabályai a V2T-ben szigorodtak: egy berendezés- és
szeleplistában csak ezek szerepelhetnek, a kiinduló elem nem kerül a listába, és ha egy kérdezett
tag nem létezik, a válasz „nincs benne”.

**Címke szerinti indítás.** A `cascade_v4_iso` egyetlen kivételt tesz: az „első szelep” típusú
kérdések (a felfelé vagy lefelé eső első szelep, `UPSTREAM_TO_FIRST_VALVE`,
`DOWNSTREAM_TO_FIRST_VALVE`) rögtön az ágensnél indulnak. Ennek oka Benedek elemzése szerint az,
hogy az ilyen kérdésekre írt Cypher-lekérdezések jellemzően az összes felfelé eső szelepet kérik
az első helyett; amíg ezek lejárnak, a kaszkád az ágenshez fordul, ha viszont gyorsan lefutnának,
rossz választ adnának, amelyet a kaszkád elfogadna. Benedek élő kaszkádja a címke szerinti
útválasztást elutasítja, ezért két kaszkádot futtatunk (a teljeset és egy csak-ágenseset), és a
kérdéscsalád címkéje alapján választunk köztük. A Cypher-szint és a válaszlépés alacsony, az
ágens magas gondolkodási szinttel fut (a GLM-hez Benedek alacsony pinjének magas szintű másolatát
használjuk, mert magas GLM-pinje nincs).

A kaszkád elfogadási szabályait, paramétereit és promptjait változatlanul vettük át. A tiereket a
plantqa mérő kliensével raktuk össze Benedek stratégiaépítőjével, mert az ő élő kaszkádja a
tokenhasználatot nem méri; a stratégiák és a promptok ugyanazok.

### Az ágens primitívjei

Benedek ágense hat általános, egymással komponálható primitívet hív (ADR-0034). A primitívek a
feloldó kimenetéből a memóriában épített elemgráfon futnak, amelyben a lapközi csatlakozók és a
többszörösen felrajzolt elemek már össze vannak vonva; ez a gráf a betöltött üzemi réteggel
egyezik. Az ágens tehát nem látja a laphatárokat, csak az üzemet.

Táblázat: Az üzemi primitívek (Benedek ADR-0034-e alapján)
| Primitív | Mit ad vissza |
|---|---|
| `find` | a szűrőnek megfelelő elemek (osztálycímke, osztály, egység, lap, tag, fajta szerint) |
| `neighbours` | egy elem közvetlen szomszédai egy relációcsoport mentén |
| `traverse` | bejárás egy kiinduló elemtől, megállási és szűkítő feltétellel |
| `path` | út két elem között |
| `filter` | egy korábbi eredmény szűkítése a közös szűrőnyelvvel |
| `aggregate` | egy korábbi eredmény csoportosítása vagy összesítése |

A primitívek eredményei hivatkozást (handle) kapnak, így egy korábbi lépés eredménye a következő
bemenete lehet. A szűrőnyelv mind a hat primitívnél ugyanaz, és ugyanazokat a címkeneveket
használja, mint a Cypher-szint sémaszövege; a V2T ezt az elem fajtájával és a vonalnézet
relációcsoportjával bővítette. A tervezési döntés lényege, hogy az eszközök száma a gráfsémából következik, nem a
kérdéstípusokból: a hat primitív a séma szókincsén értelmezett szokásos gráfműveletek
(kiválasztás, kiterjesztés, lezárás, legrövidebb út, szűkítés, csoportosítás), ezért egy új
kérdéstípus egy új kompozíció, nem egy új eszköz. Az egyszerű JSON-akciók minden modellen
ugyanúgy működnek, és a gyorsítótár változtatás nélkül vissza tudja játszani őket.

### Az adatlapoldali A2

A plantdocs A2-módszere egy eszköz egy kérdésére a következő lépésekben válaszol.

1. **Kontextus.** A rendszerüzenet a plantdocs gráfmodelljének leírását (a 4. fejezetben bemutatott
   adatpont-, eset-, szakasz- és lábjegyzetcsúcsokat az előtagos neveikkel), az eszköz gráfjának
   leltárát (az eszköz és alkatrészei, a leggyakoribb adatpontcímkék, a források oldallal) és a forrásszakaszok
   katalógusát tartalmazza; a katalógus soronként egy táblázat, ábra, diagram vagy szövegrész a
   címével, típusával, oldalával, sorainak számával és a 08. lépésben írt leírásával.
2. **Lekérdezésírás.** Egy LLM alacsony gondolkodási szinttel egyetlen csak olvasó
   Cypher-lekérdezést ír, és mellette legfeljebb három forrásszakaszt választ, amelynek a teljes
   tartalmára a válasznak valószínűleg szüksége lesz. A lekérdezési szabályok széles keresést
   kérnek: a kérdés egy szava a címkében, a nyomtatott értékben, az eset címkéjében (a
   feltételekben) vagy egy forrásszakasz címében és leírásában is lehet; a lekérdezésnek mindig
   vissza kell adnia a nyomtatott értéket, a címkét, az esetet, a lábjegyzetet, a forrást és az
   oldalt.
3. **Futtatás és javítás.** Ha a lekérdezés hibát ad, üres, vagy túl sok sort ad vissza, a modell
   egy javítókörben megkapja a problémát („javítsd vagy bővítsd”, illetve „szűkítsd a
   legjellemzőbb szavakra”). Ha a választott szakaszokból jött sor, javítókör nincs; ha a javítás
   üres eredményt ad, az első, nem üres eredmény marad.
4. **Teljes szakaszok.** A kiválasztott szakaszok minden sora a lekérdezés sorai mellé kerül;
   ez azt az esetet fedi le, amikor a táblázat fejlécei nem a kérdés szavait használják.
5. **Vektoros keresés.** A lekérdezésírással párhuzamosan a kérdés beágyazásvektorához
   legközelebbi 30 adatpont kerül elő a gráf vektorindexéből, mindegyik az esetével, a
   lábjegyzetével, az oldalával és a forrásszakaszával. Mivel párhuzamosan fut, a késleltetéshez
   nem ad hozzá.
6. **Válaszírás.** A válaszíró csak a megtalált tényekből fogalmaz: előbb egy-két mondatban a
   közvetlen választ, utána az értékeket az egységükkel és azokkal a feltételekkel, amelyek mellett
   érvényesek, oldalhivatkozással. A kérdést abban az értelemben kell olvasnia, ahogy az adatlap
   használja a szavait; egy szakkifejezést néhány szóval megmagyarázhat, de új tényt, értéket vagy
   eljárást nem tehet hozzá; ha a kérdés egy része nincs a tények között, ezt kimondja. A
   forrásoldalakat a program a felhasznált sorokból gyűjti össze.

Az összevont gráfban több eszköz gráfja van egyszerre, ezért néhány illesztésre volt szükség,
a plantdocs kódjának módosítása nélkül. A leltár elé egy sor kerül, amely közli, hogy a
kérdés melyik dokumentumról szól, és hogy minden csúcsot `document_id` szerint kell szűkíteni. A
lekérdezés-futtató csak olyan lekérdezést enged, amely a dokumentum azonosítóját tartalmazza, és
semmilyen írást nem enged. A vektoros keresés egy nagyobb jelöltkészletből csak a dokumentum
csúcsait tartja meg. A másik lehetőség az lett volna, hogy kérdésenként újratöltjük az
adatbázist a kérdezett eszköz gráfjával, ahogy a plantdocs alkalmazása teszi; ez az összevont
gráfot tönkretenné, és az M1 számára értelmetlenné tenné az egész összevonást.

### Az összevont gráf

Egy Neo4j-adatbázisban van Benedek üzemi rétege és mind a hét eszköz gráfja, a tagen alapuló
`(:PlantItem {tag})-[:DESCRIBED_BY]->(eszköz)` kapcsolattal összekötve, `document_id` szerinti
névterekkel (4. fejezet). A betöltés egy paranccsal újrafuttatható (`python -m plantqa.graph.load`).

## M1 — egy gráf, egy lekérdezés

Az M1 Benedek kaszkádja az összevont gráfon, két kiegészítéssel. A Cypher-szint sémaleírása az
üzemi réteg mellett az adatlapréteget is tartalmazza: a `DESCRIBED_BY` kapcsolatot, a plantdocs
A2-promptjának gráfmodelljét és lekérdezési szabályait, valamint a tagek dokumentumonkénti
listáját. Így egyetlen lekérdezés követheti a rajzot és olvashatja az adatlapot, például:

```
MATCH (p:PlantItem {tag: 'P-1-3'})-[:DESCRIBED_BY]->(dev)
MATCH (d) WHERE d.document_id = dev.document_id AND d:plm__PCA_100029511
  AND toLower(d.plm__PCA_100029521) CONTAINS 'casing pressure'
RETURN d.plm__PCA_100029521 AS label, d.plm__PCA_100029522 AS value, d.schema__pageStart AS page
```

A sémakiegészítés első része az összekötést írja le (a `DESCRIBED_BY` nélküli elemnek, például
egy szabályozófunkciónak nincs adatlapja; minden adatlapcsúcsnak van `document_id` tulajdonsága;
egy tag tényei a fenti mintával érhetők el). Ezt követi a plantdocs A2-promptjának gráfmodell-része
szó szerint, a dokumentumok és tagjeik listája, végül a plantdocs lekérdezési szabályai, amelyek a
második fejlesztési iterációban kerültek be (EXP-011).

Az ágens egy új primitívet kap: a `datasheet_fact(tag, question)` a tagből feloldja az eszközt,
és a plantdocs A2-logikájával kérdezi meg az adatlapját. A primitív Benedek eszközregiszterébe
kerül, ezért az ágens promptjában ugyanúgy jelenik meg, mint a többi primitív. A regisztráció csak
az ágens felépítésének és a kérdés megválaszolásának idejére szól, így Benedek kódja és a többi
futás eszközkészlete nem változik. Az eredmény Benedek eredményosztályainak felületét követi
(szöveges megjelenítés hosszkorláttal), és tartalmazza a dokumentum azonosítóját, a tagot, az
első forrásoldalakat és az A2 válaszát. Ismeretlen vagy adatlap nélküli tagre a primitív nem hibát
dob, hanem szövegesen közli, hogy a taghez nem tartozik adatlap, így az ágens folytathatja a
munkát. Az eszköz leírása arra kéri az ágenst, hogy a rajzon nem látható tulajdonságokhoz ezt
használja, és előbb a rajzon keresse meg a tagot.

Az M1 útvonala a lefutott tierekből és az adatlapi hívásokból áll (például `cypher-v2t`, vagy
`cypher-v2t`, `agent-v2t` és `datasheet_fact:FT-2-2`). A válaszlépés Benedek változatlan
válaszpromptja; az M2-ben és az M3-ban bevezetett válaszszabályt (részválasz, a dokumentumon túli
tanács tilalma) az M1 ezért nem kapta meg, mert az a kaszkád része, amelyet nem módosítunk.

## M2 — router

Az M2 egy ágens két eszközzel: a `drawing(question)` Benedek kaszkádját hívja a rajzra (változtatás
nélkül), a `datasheet(tag, question)` a tagből feloldott eszköz A2-jét. Az ágens minden lépésben
egy JSON-objektumot ír (eszközhívást vagy végső választ), legfeljebb hat eszközhívással. Ha a
kérdés egy elemet a helyével vagy szerepével nevez meg, előbb a rajzeszközt kérdezi meg a tagről,
utána az adatlapot.

**A protokoll.** A rendszerüzenet leírja a két eszközt, felsorolja az adatlappal rendelkező
tageket, megadja a három megengedett JSON-alakot (rajzeszköz-hívás, adatlap-hívás, végső válasz a
„nincs benne” jelzővel) és a válaszalakot. A router minden lépésben pontosan egy JSON-objektumot
ír; a program végrehajtja a hívást, és az eredményt egy új üzenetben („Tool result:”) adja vissza.
Érvénytelen akcióra a router javító üzenetet kap; ha a lépéskeret elfogy, a kérdés
lépéskorlát-eredménnyel zárul. Szolgáltatói hibánál (például
hálózati hibánál) a hívás egyszer újrapróbálkozik, ahogy Benedek kaszkádja is; ha ez is hibás, a
kérdés szolgáltatói hibával zárul, és rossznak számít. A router alacsony gondolkodási szinttel
fut.

**A válaszszabály.** A második fejlesztési iterációtól (EXP-011) az M2 és az M3 egy közös
válaszszabályt kap: ha a dokumentumok a kérdésnek csak egy részére adnak választ, a módszer ezt a
részt adja meg, és megnevezi a hiányzó részt; a „nincs benne” jelzőt csak akkor állítja, ha
semmi releváns nincs; tanácsot, eljárást, okot vagy értéket, amelyet a dokumentumok nem
mondanak ki, nem tehet hozzá. A szabály után a dev halmazon az M2 és az M3 hallucinációi
eltűntek (EXP-011, 6. fejezet).

**Tervezési döntések.** Az M2-ben mindkét rendszer abban a beállításban fut, amelyre a szerzője
hangolta, és a két rendszer egymásról nem tud; az összekötést a router végzi a kérdés szövegének
értelmezésével. Ennek két következménye van. A rajzeszköz szabad szöveges kérdést kap
(`FREE_TEXT`), a kérdéscsalád címkéjét nem, ezért a kaszkád az „első szelep” kérdéseket is a
Cypher-szinten kezdi, és a rajzeszköz válaszának alakja eltérhet attól, amit a kérdés eredetileg
kért (taghalmaz, út); ezt a hibát a 6. fejezetben egy szabályozókörös kérdésen látjuk is. A
másik következmény, hogy az összetett kérdés legalább két egymás utáni eszközhívást igényel,
amelyek mindegyike maga is több LLM-hívás, ezért a késleltetés nagyobb.

## M3 — gráf nélküli baseline

Az M3-ban nincs gráf. A kontextus a teljes rajz Benedek ContextRAG-szerializálásával (ez a
ChatP&ID-módszer: az egész rajz a promptban) és a hét adatlap PDF-szövegéből vektoros
kereséssel kiválasztott 12 legközelebbi darab, ugyanazzal a beágyazómodellel, amelyet a
plantdocs is használ (`qwen/qwen3-embedding-8b`, 512 dimenzió). A válasz egyetlen hívás magas
gondolkodási szinttel, ahogy Benedek ContextRAG-karja is fut.

A szerializált rajz a rajzolt előfordulások gráfja: lapról lapra minden szimbólum egy csúcs a
tagjével és az osztályával, az élek a csövek és a jelek, a lapokat a lapközi csatlakozók kötik
össze. Az M3 modellje tehát maga követi a csatlakozókat a laphatáron át; az összevont üzemi
réteget nem látja. Az adatlap-darabok a PDF-ek szövegrétegéből készülnek oldalanként,
bekezdéshatáron vágva, korlátozott hosszúságú darabokra; minden darab a dokumentum azonosítóját és
az oldalszámot hordozza. A prompt tartalmazza a tag → adatlap táblát is, hogy a modell tudja,
melyik darab melyik elemhez tartozik. Az Azure-kimenet szövegét azért nem használtuk, mert a
plantqa-ban nem minden dokumentumhoz volt meg.

A baseline-t szándékosan erősnek választottuk: a négylapos példaüzem rajza kicsi, így a teljes
rajz elfér a promptban, és a ChatP&ID mérése szerint egyetlen lapon éppen ez a módszer nyert
[Alimin2026]. Az adatlapoldalon a szövegdarabok vektoros keresése a legegyszerűbb, gráf nélküli
visszakeresés; ha az M3 felveszi a versenyt a két gráfos módszerrel, az arra utal, hogy ezen a
méreten a gráf előnye nem a visszakeresésben, hanem legfeljebb a feltételek megőrzésében
jelentkezhet.

## A módszerek várható erősségei és gyengeségei

Az alábbiakban a módszerek felépítéséből következő, minőségi várakozásokat foglaljuk össze; a 6.
fejezet eredményeit ezek fényében érdemes olvasni.

### M1

Az M1 erőssége, hogy egy összetett kérdés elvben egyetlen lekérdezéssel megválaszolható: a
rajzi lépés és az adatlapi tény ugyanabban a mintában szerepel, így nincs szöveges átadás két
rendszer között, és a válasz minden eleme visszakövethető egy csúcsig. Az ágensszint a
`datasheet_fact` primitívvel ugyanazt az A2-logikát éri el, mint az M2, tehát ahol a
Cypher-szint elakad, ott az M1-nek az M2-höz hasonló képességei vannak.

A gyengeségei ugyanebből fakadnak. A Cypher-író modellnek egyszerre két szókincset kell
kezelnie: Benedek olvasható osztálycímkéit és a plantdocs előtagos, számkódos szabványos neveit.
A sémaszöveg ettől hosszú, ami minden kérdés költségét növeli, akkor is, ha a kérdés csak a
rajzról szól. A legnagyobb kockázat az elfogadási szabály: a rajzi kérdéseken a nem üres, nem
csonka eredmény jó jelzés, egy adatlapi kérdésnél viszont egy szűk lekérdezés is adhat nem üres,
de hiányos sort (például egy értéket a feltétele nélkül), amelyet a kaszkád elfogad, és az ágens
nem kap esélyt. Végül a válaszlépés a rajzi kérdésekre készült, és nem tartalmazza az adatlapi
válaszíró szabályait (feltételek kiírása, oldalhivatkozás).

### M2

Az M2 erőssége a modularitás: mindkét rendszer abban a beállításban fut, amelyben a szerzője
mérte, az adatlapi válasz a plantdocs teljes A2-láncán megy át (szakaszválasztás, vektoros
keresés, a feltételeket kiíró válaszíró), és egy új dokumentumtípus egy új eszközzel bővíthető. Az
útvonal átlátható: a naplóból látszik, melyik eszközt milyen kérdéssel hívta a router.

A gyengesége az illesztésben van. A két rendszer szöveggel kommunikál, így a rajzeszköz
válaszának alakja elcsúszhat, és a router félreértheti; az összetett kérdés helyes felbontása is a
routeren múlik. Mivel az eszközhívások egymás után futnak, és mindegyik maga is több LLM-hívás, a
késleltetés a három módszer közül várhatóan itt a legnagyobb.

### M3

Az M3 erőssége az egyszerűség: egyetlen hívás, nincs lekérdezés, amely elromolhat, és nincs
elfogadási szabály, amely rossz választ engedhet át. Egy kis rajzon a teljes gráf elfér a
promptban, és a modell mindent lát; az adatlapi kérdéseknél a kérdés szavaihoz közeli szövegrészek
gyakran éppen a keresett táblázatot tartalmazzák.

A gyengesége a méret és a szerkezet. Benedek mérései szerint a teljes rajz promptba tétele a
lapszámmal romlik és drágul, egy határ fölött pedig nem is fér el (2. fejezet), ezért az M3 előnye
nagyobb üzemen nem várható. Az adatlap-darabok a táblázatokat szövegként, a fejlécektől
elszakítva tartalmazhatják, a feltételek és a lábjegyzetek nem explicitek, és a vektoros keresés
egy több eszközt érintő kérdésnél elhanyagolhatja valamelyik eszköz adatlapját. Az M3 a
forrásoldalakat csak darabszinten tudja megadni.

## Költség és mérés

Minden LLM-hívás egy közös, cache-elt és naplózott rétegen megy át. A cache miatt az ismételt
futás nem fizet újra; minden élő hívás költsége a közös naplóba kerül, és a teljes keret 20 USD
(18 USD felett új mérés nem indul). Kérdésenként mérjük a tokeneket, a szolgáltató által
jelentett költséget (cache-ből érkező válasznál az eredeti hívás árát), a késleltetést és az
útvonalat (melyik szint vagy eszköz kellett a válaszhoz).
