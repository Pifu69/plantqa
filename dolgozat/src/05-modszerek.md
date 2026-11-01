# Kérdés-megválaszolási módszerek

Az összevont gráf önmagában még nem válaszol: kell egy módszer, amely a kérdésből lekérdezést,
abból pedig választ készít. Ebben a fejezetben három ilyen módszert mutatunk be. Az M1 közvetlenül
az összevont gráfot használja, az M2 a két meglévő rendszert külön hívja, és egy irányító köti
össze az eredményüket, az M3 pedig gráf nélküli alapmódszer, amely azt mutatja meg, mennyit ad
hozzá a gráf. A három módszer a két meglévő rendszerre épül, azokat nem módosítja.

Mindhárom módszer ugyanazt kapja: a kérdés szövegét és az elvárt válaszalakot. A válaszalak lehet
szabad szöveg, egy tag vagy tag-ek halmaza, egy rendezett út, igen/nem válasz, darabszám, egy
egység neve vagy egy osztálynév; az alakot egy rögzített mondat írja le, amelyet mindhárom módszer
szó szerint ugyanígy lát. A válasz mindhárom esetben ugyanolyan szerkezetű: maga a válasz és egy
jelző, amely azt mondja meg, hogy a dokumentumok nem tartalmazzák a választ. Mindhárom módszert
két nyelvi modellel mérjük, a GLM-5.3 Flash és a GPT-6 Luna modellel, a rajzoldali rendszerben
rögzített beállításokkal. A fejezetben előbb a közös építőelemeket, majd a három módszert, végül a
fejlesztési üzemeken végzett hangolást írjuk le.

![A három módszer felépítése. Bal: M1 (egy összevont gráf); közép: M2 (irányító a két rendszer fölött); jobb: M3 (gráf nélküli alapmódszer).](../../figures/methods_overview.png)

## Közös építőelemek

### A rajzoldali kaszkád

A kaszkád két szintből áll, és a pontosságot helyezi előtérbe. Az első szinten egy nyelvi modell
egyetlen Cypher-lekérdezést ír a rajzi rétegre. A prompt leírja a gráf szerkezetét (a csúcsok
fajtáit, az éleket és a tulajdonságokat), tartalmaz egy rövid, általános bevezetőt a P&ID-k
olvasásához, és néhány lekérdezési szabályt: korlátlan hosszúságú utat nem szabad keresni, egy
halmazhoz különböző végpontokat kell kérni, egy útvonalhoz a legrövidebb utat, egy elérhetőséghez
pedig a vonalnézet mentén kell vizsgálni, létezik-e út. A lekérdezés csak olvashat, 30 másodperces
időkorláttal és legfeljebb 1000 sorral fut. Ha hibát ad, a modell megkapja az adatbázis
hibaüzenetét, és egyszer újraírhatja; egy program emellett azt is ellenőrzi, hogy a kérdésben
szereplő tag-ek léteznek-e. A kapott sorokból egy közös válaszlépés fogalmazza meg a választ.

A kaszkád akkor fogadja el az első szint válaszát, ha minden önjelzés rendben van: a lépés
válaszolt, érdemben felelt (nem azt mondta, hogy nincs benne), a lekérdezés adott sort, és az
eredmény nem csonka, vagyis nem érte el a sorkorlátot. Egyik jelhez sem kell ismerni a helyes
választ, ezért a szabály a teszten is alkalmazható, és nincs a mért adatra illesztett paramétere.
Ha bármelyik jel hiányzik, a kérdés a második szintre kerül.

A második szinten egy ágens lépésenként, legfeljebb 40 lépésben gráfműveleteket hív. Minden
lépésben egy rögzített formájú utasítást ír (egy művelet hívását a paramétereivel, vagy a munka
befejezését), és a művelet eredményét szövegként kapja vissza. A végén ugyanaz a közös
válaszlépés fogalmaz az összegyűjtött eredményekből, amely az első szint válaszát is írja. A
válaszlépés szabályai szerint egy berendezés- és szeleplistában csak ezek szerepelhetnek, a
kiinduló elem nem kerül a listába, és ha egy kérdezett tag nem létezik, a válasz „nincs benne”.

A kaszkád egyetlen kivételt tesz: a felfelé vagy lefelé eső első szelepet kérdező kérdések rögtön
az ágensnél indulnak. Az ilyen kérdésekre írt lekérdezések ugyanis jellemzően az összes szelepet
kérik az első helyett, és ha gyorsan lefutnak, a kaszkád ezt a rossz, de nem üres eredményt
elfogadná. A lekérdezést író lépés és a válaszlépés alacsony, az ágens magas gondolkodási
szinttel fut.

### Az ágens gráfműveletei

Az ágens hat általános gráfműveletet használhat, amelyek egymással kombinálhatók: a szűrőnek
megfelelő elemek keresését, egy elem szomszédainak lekérdezését, a bejárást egy kiinduló elemtől,
az utat két elem között, egy korábbi eredmény szűkítését és egy korábbi eredmény összesítését. A
műveletek a rajzi réteggel egyező gráfon futnak, ezért az ágens nem látja a laphatárokat, csak az
üzemet. Minden eredmény hivatkozást kap, így egy korábbi lépés eredménye a következő lépés
bemenete lehet: az ágens például előbb megkeresi egy szivattyú szomszédait, majd ezek közül
kiszűri a szelepeket. A tervezési döntés lényege, hogy a műveletek száma a gráf szerkezetéből
következik, nem a kérdéstípusokból: egy új kérdéstípushoz nem új művelet kell, hanem a meglévők új
kombinációja (részletesen: Függelék E).

### Az adatlapoldali A2

Az A2 egy eszköz egy kérdésére a következőképpen válaszol. A modell megkapja az adatlapgráf
szerkezetének leírását, az eszköz gráfjának tartalomjegyzékét és a forrásszakaszok (táblázatok,
ábrák, szövegrészek) katalógusát. Ebből egyetlen, csak olvasó, széles keresésű Cypher-lekérdezést
ír, és legfeljebb három forrásszakaszt választ, amelyeknek minden sora a lekérdezés eredménye mellé
kerül; hibás, üres vagy túl sok sort adó lekérdezésnél egy javítókör következik. Ezzel
párhuzamosan a kérdés jelentéséhez legközelebbi 30 adatpont is előkerül a vektorindexből. A
válaszíró csak a megtalált tényekből fogalmaz: a közvetlen válasz után az értékeket az egységükkel,
a feltételeikkel és oldalhivatkozással adja meg, új tényt, értéket vagy eljárást nem tehet hozzá
(részletesen: Függelék E).

Az A2-t eredetileg egyetlen adatlap gráfjára tervezték, az összevont gráfban viszont hét eszköz
gráfja van egyszerre. Ezért a plantdocs módosítása nélkül három illesztésre volt szükség. A
tartalomjegyzék elé egy sor kerül, amely megnevezi a kérdezett dokumentumot, és előírja, hogy
minden csúcsot a dokumentumazonosító szerint kell szűkíteni. A lekérdezést futtató program csak
olyan lekérdezést enged, amely a dokumentum azonosítóját tartalmazza, és semmilyen írást nem
enged. A vektoros keresés pedig egy nagyobb jelöltkészletből csak a kérdezett dokumentum csúcsait
tartja meg. A másik lehetőség az lett volna, hogy kérdésenként újratöltjük az adatbázist a
kérdezett eszköz gráfjával; ez azonban az összevont gráfot tönkretenné, és értelmetlenné tenné az
egész összevonást.

## M1: egy gráf, egy lekérdezés

Az M1 a kaszkád az összevont gráfon, két kiegészítéssel. Az első, hogy a lekérdezést író lépés a
rajzi réteg mellett az adatlapi réteg leírását is megkapja: az összekötő élt, az A2 gráfleírását
és lekérdezési szabályait, valamint azt, hogy melyik tag melyik dokumentumhoz tartozik. Így
egyetlen lekérdezés követheti a rajzot, és olvashatja az adatlapot; például a P-1-3 szivattyútól
az összekötő élen át eljut az adatlapjához, és ott a kérdés szavaira (például „casing pressure”)
szűrve visszaadja az adatpontok címkéjét, értékét és oldalszámát. A kiegészítés elejét a
Függelék C mutatja.

A második kiegészítés, hogy az ágens egy hetedik műveletet kap, az adatlap-eszközt. Ez egy tag-ből
megkeresi a hozzá tartozó adatlapot, és az A2-vel megválaszoltat róla egy kérdést; az eredmény a
dokumentum azonosítóját, az első forrásoldalakat és az A2 válaszát tartalmazza. Az ágens ezt a
műveletet ugyanúgy látja és hívja, mint a többi hatot. Ha egy tag-hez nincs adatlap, a művelet nem
hibát jelez, hanem szövegesen közli ezt, így az ágens folytathatja a munkát. A művelet leírása arra
kéri az ágenst, hogy a rajzon nem látható tulajdonságokhoz ezt használja, és előbb a rajzon keresse
meg a tag-et.

Az M1 útvonala a lefutott szintekből és az adatlapi hívásokból áll: egy kérdés vagy már az első
szinten lezárul, vagy az ágenshez kerül, amely szükség szerint egy vagy több adatlapot is
megkérdez. A válaszlépés a kaszkád változatlan válaszlépése; az M2-ben és az M3-ban bevezetett
válaszszabályt (lásd alább) ezért az M1 nem kapta meg.

## M2: irányító a két rendszer fölött

Az M2 egy irányító ágens két eszközzel: a rajzeszköz a változatlan kaszkádot kérdezi a rajzról, az
adatlap-eszköz pedig egy tag-hez tartozó eszköz adatlapját az A2-vel. Az irányító minden lépésben
pontosan egy utasítást ír (rajzeszköz-hívás, adatlap-hívás vagy végső válasz a „nincs benne”
jelzővel), a program végrehajtja a hívást, és az eredményt visszaadja. Legfeljebb 16 lépése van, és
ha ez a keret elfogy, egy utolsó hívásban köteles végső választ adni a már összegyűjtött
eredményekből. Ha a kérdés egy elemet a helyével vagy a szerepével nevez meg (például „a P-1-1
utáni szelep”), az irányító előbb a rajzeszköztől kérdezi meg a tag-et, és csak utána az adatlapot.
Alacsony gondolkodási szinttel fut; a rendszerüzenetét a Függelék B közli.

Az M2 és az M3 egy közös válaszszabályt is kap: ha a dokumentumok a kérdésnek csak egy részére
adnak választ, a módszer ezt a részt adja meg, és megnevezi a hiányzó részt; a „nincs benne”
jelzőt csak akkor állítja, ha semmi releváns nincs; tanácsot, eljárást, okot vagy értéket, amelyet
a dokumentumok nem mondanak ki, nem tehet hozzá. A szabály bevezetése után az M2 és az M3
hallucinációi eltűntek (Függelék G).

Az M2-ben mindkét rendszer abban a beállításban fut, amelyre hangolták, és a két rendszer egymásról
nem tud; az összekötést az irányító végzi a kérdés szövegének értelmezésével. Ennek két
következménye van. A rajzeszköz szabad szöveges kérdést kap, a kérdéscsalád megjelölését nem, ezért
a kaszkád az „első szelep” kérdéseket is az első szinten kezdi, és a válasz alakja eltérhet attól,
amit az eredeti kérdés kért; ezt a hibát a 6. fejezetben egy szabályozókörös kérdésen látjuk is.
A másik következmény, hogy egy összetett kérdés legalább két egymás utáni eszközhívást igényel,
amelyek mindegyike maga is több modellhívás, ezért a válaszidő nagyobb.

## M3: gráf nélküli alapmódszer

Az M3-ban nincs gráf. A modell egyetlen promptban megkapja a teljes rajzot szövegként, a ChatP&ID
ContextRAG-módszerének megfelelően, és a hét adatlap PDF-szövegéből a kérdéshez jelentés szerint
legközelebbi 12 részletet, ugyanazzal a beágyazómodellel (Qwen3-Embedding-8B, 512 dimenzió),
amelyet az A2 is használ. A válasz egyetlen hívás, magas gondolkodási szinttel.

A szövegként leírt rajz lapról lapra minden szimbólumot felsorol a tag-jével és az osztályával,
megadja a köztük futó csöveket és jelvezetékeket, és a lapokat a lapközi csatlakozókon át köti
össze. Az M3 modelljének tehát magának kell követnie a csatlakozókat a laphatáron át; az összevont
rajzi réteget nem látja. Az adatlaprészletek a PDF-ek szövegéből készülnek oldalanként, bekezdéshatáron
vágva, és mindegyik hordozza a dokumentum azonosítóját és az oldalszámot. A prompt azt is megadja,
melyik tag-hez melyik adatlap tartozik.

Az alapmódszert szándékosan erősnek választottuk: a négylapos prototípus-üzem rajza elfér a
promptban, és a ChatP&ID mérése szerint egyetlen lapon éppen ez a módszer nyert [Alimin2026]. Ha az
M3 felveszi a versenyt a gráfos módszerekkel, az arra utal, hogy az adott méreten a gráf előnye
legfeljebb a feltételek megőrzésében jelentkezhet.

## Hangolás a fejlesztési üzemeken

Az első prototípust a négylapos üzemen fejlesztettük (Függelék G). A 30 és 50 lapos fejlesztési
üzemen három változtatásra volt szükség; az M3-at nem hangoltuk. Az M2 lépéskerete 6-ról 16-ra
nőtt, és bekerült a kötelező végső válasz, mert a 30 lapos üzemen a 24 több adatlapos válaszból 10
azért maradt üres, mert az irányító elérte a lépéskorlátot. Az M1 lekérdezési szabályai egy újjal
bővültek, mert sok válasza csak részleges volt: az adatlapi tényeket tágan kell szűrni, és minden
értéket a feltételével és az oldalszámával együtt kell visszaadni. Végül a kaszkád kérdésenkénti
időkorlátja 120 másodpercről 240 másodpercre nőtt, mert egy kérdés túllépte a korábbit. A hangolás
után a módszereket befagyasztottuk, és a tesztüzemeken már nem változtattunk rajtuk. A következő fejezet ezeknek a módszereknek a mért eredményét mutatja be.
