# Demó és esettanulmány

A mért számok azt mutatják meg, milyen gyakran helyes egy módszer, azt nem, hogyan jut el a
válaszig. Ebben a fejezetben bemutatjuk a webes demót (a dolgozat ötödik hozzájárulását), majd
két képernyőképen végigkövetünk két kérdést; a próba további négy kérdését a Függelék F
mutatja be. A képek a demó próbáján készültek: hat
kérdést tettünk fel a futó demón, az (a), (a), (b), (c), (d) és (e) családból, az M1, M2 és M3
módszerrel, GLM-mel; mind a hat kérdésre érdemi válasz jött. A próba nem pontossági mérés, a
válaszokat nem pontoztuk.

## A demó felépítése

A demó egy helyi webalkalmazás: egy webszerver és egyetlen
weboldal. A szerver ugyanazokat a módszerobjektumokat építi fel, amelyeket a mérés használ (az
első kérdésnél, utána újrahasznosítja őket), így a demó válaszai pontosan azon az úton születnek,
amelyet az 5. fejezetben leírtunk. A korábban feltett kérdésekre a demó a már eltárolt válaszokkal
is tud felelni, új, fizetős modellhívás nélkül.

Az oldal két részre oszlik.

- **Bal oldal: a dokumentum.** Alapállapotban a P&ID látszik, a generátor rajzexportjából: a fejléc
  megnevezi a korpuszt (a plantgraph 6-os seedű üzeme), és lapváltó gombokkal a négy lap
  között lehet lépkedni; a teljes rajz PDF-ben is megnyitható. Ha a felhasználó egy válasz
  adatlapi forrásoldalára kattint, a bal oldalon az adatlap adott oldala jelenik meg képként, a
  fejlécben a dokumentum azonosítójával és oldalszámával, valamint egy hivatkozással, amely a PDF-et
  ennél az oldalnál nyitja meg.
- **Jobb oldal: a kérdés és a válasz.** Egy szövegmezőbe kerül a kérdés; alatta választható a
  módszer (M1, M2 vagy M3, egy rövid leírással), a modell (`z-ai/glm-5.3-flash` vagy
  `openai/gpt-6-luna`) és a válaszalak (az 5. fejezetben felsorolt alakok közül). Az alapértelmezés
  az M2 GLM-mel, mert ez a párosítás volt a legjobb a kis üzem tesztjén (31 helyes a
  40-ből; ezt az oldal ki is írja) és a 100 lapos tesztüzemen is (51 helyes a 60-ból). A
  demó a kis üzemen fut, mert annak négy lapja a képernyőn jól áttekinthető.

A válasz alatt a demó megmutatja a válasz nyomait: a módszert, a modellt, a kimenetelt, a
késleltetést, a tokenszámot, a költséget és a gyorsítótárból jött hívások számát. Ezután
következik az útvonal címkék sorozataként (az M1-nél a tierek és az adatlapi primitívhívások, az
M2-nél a router eszközhívásai, az M3-nál a kontextus fajtája), az adatlapi forrásoldalak
kattintható oldalszámként, és egy lenyitható blokkban a lefutott lekérdezések. Végül a dev halmaz
kérdései szerepelnek példaként, családonként csoportosítva. A teszthalmaz kérdései nincsenek a
példák között.

A képernyőképeket egy program készítette: minden kérdést előbb az API-n tett fel, majd fej
nélküli böngészővel lefényképezte az oldalt. Ezért a képeken látható késleltetés a gyorsítótárból
kiszolgált válaszé; a valódi késleltetést a 6. fejezet adja.

## Két kérdés végigkövetve

A Függelék F két kérdést lépésenként végigkövet a demóban: egy összetett kérdést, amelynél a router
előbb a rajzeszközt, majd a távadó adatlapját kérdezi, és egy megválaszolhatatlan kérdést, amelynél
a „nincs benne” válasz mellett a demó azt is megmutatja, mit tartalmaz az adatlap.

## Tanulságok

A demó azt mutatja meg, amit a pontossági számok nem: az útvonal és a lekérdezések láthatók, így
egy rossz válasz gyorsan felismerhető, és a forrásoldal egy kattintással a rajz helyén jelenik meg.

A demó korlátai: egy új kérdés élő LLM-hívásokba kerül, és másodpercekig tart (a gyorsítótár
csak az ismétlést teszi ingyenessé); a demó egyetlen üzemet ismer, mert egy másik üzemhez a teljes
összevont betöltést újra kellene futtatni; és angol nyelvű, mint a kérdéssor és a két
forrásrendszer promptjai.
