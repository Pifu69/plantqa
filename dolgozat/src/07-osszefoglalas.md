# Összefoglalás

A dolgozatban két egyéni munkát kötöttünk össze: a P&ID-rajzokból épített üzemi gráfot és a
gyártói adatlapokból épített, eszközönkénti ISO 15926 szerinti gráfokat. A két réteget egyetlen
Neo4j-adatbázisba töltöttük, és a tag-ek alapján összekötöttük. Erre a gráfra három
kérdés-válaszoló módszert építettünk egy négylapos prototípus-üzemen, a közös rendszert egy 30 és
egy 50 lapos fejlesztési üzemen hangoltuk, majd befagyasztva két modellel megmértük egy 100 és egy
1000 lapos, a hangolás során nem használt tesztüzemen, üzemenként 60 kérdésen és 12, több adatlapot
összevető kérdésen.

## Válaszok a kutatási kérdésekre

Az első kérdésre (RQ1) igen a válasz: a rajzokból és az adatlapokból külön épített tudás
összeköthető egyetlen lekérdezhető tudásgráfban, a két forrásrendszer módosítása nélkül. A tag
alapján húzott összekötő él egyik réteg szerkezetén sem változtat, így a rajzi kapcsolatok és az
adatlapi értékek feltételei, lábjegyzetei és forrásoldalai is megmaradnak. Az összevont gráf az
1000 lapos üzemen is felépült: 10 277 rajzi csúcs és 6641 összekötő él jött létre, a betöltés 80,7
másodpercig tartott.

A második kérdésre (RQ2) az a válasz, hogy a mindkét dokumentumfajtát igénylő kérdések nagy része
megválaszolható ezen a gráfon. Az összevont gráfon dolgozó M1 GLM-mel 50 és 43, Lunával 46 és 41
helyes választ adott a 60-ból a 100 és az 1000 lapos tesztüzemen. A két meglévő rendszert külön
hívó irányító (M2) GLM-mel mindkét tesztüzemen a legjobb volt (51 és 48 helyes), de az M1-től való
különbsége nem szignifikáns. A gráf nélküli M3-mal szemben a 100 lapos üzemen GLM-mel az M2, Lunával
az M1 előnye szignifikáns. A rajzi (a) és a megválaszolhatatlan (d) kérdéseken minden módszer erős,
a különbség az adatlapi (b), az összetett (c) és a több adatlapos (e) kérdéseken jön ki. A több
adatlapos kérdések közül a gráf nélküli módszer a 100 lapos üzemen egyiket sem oldotta meg
teljesen, a gráfos módszerek GLM-mel 4–5-öt, az 1000 lapos üzemen 1–3-at. A hibák módszerenként
jellegzetesek: az M1-nél az egyetlen lekérdezésből adódó hiányos válasz, az M2-nél a több
adatlapos kérdéseken a lépéskorlát miatti üres válasz, a gráf nélküli módszernél a téves „nincs
benne” jelzés a leggyakoribb.

A harmadik kérdésre (RQ3) az a válasz, hogy a gráfos módszerek jól skálázódnak, a gráf nélküli
módszer nem. A gráfos módszerek kérdésenkénti költsége a tízszer nagyobb rajzon legfeljebb a
kétszeresére nőtt (az M2 GLM-mel 0,00451 és 0,00866 USD a 100 és az 1000 lapos üzemen), pontosságuk
pedig legfeljebb 7 kérdéssel csökkent (az M2 GLM-mel 51-ről 48-ra, az M1 GLM-mel 50-ről 43-ra, az
M2 Lunával viszont 43-ról 46-ra nőtt). A gráf nélküli M3 költsége a 30 lapos fejlesztési üzem és a
100 lapos tesztüzem között GLM-mel 0,00206-ról 0,00757 USD-re, Lunával 0,00731-ről 0,02501 USD-re
nőtt, az 1000 lapos rajz pedig már nem fér a modellek kontextusába, így ott az M3 nem futtatható.
A gráf tehát nemcsak olcsóbbá, hanem nagy üzemen egyáltalán lehetővé teszi a kérdés-válaszolást;
ez egybevág a plantgraph korábbi méréseivel, amelyek szerint a teljes rajz promptba tétele a
lapszámmal romlik és drágul. A fejlesztési üzemeken végzett hangolás az ott látott üres
válaszokat csökkentette, a tesztüzemek pontosságát mérhetően nem változtatta.

## Korlátok

Az eredmények több korláttal együtt érvényesek. Mind az öt üzem szintetikus (4, 30, 50, 100 és
1000 lap): a plantgraph generátora szabályok szerint állította elő őket (egységek, berendezések,
csővezetékek, szabályozókörök, lapközi csatlakozók), de nem valódi üzemek rajzai, és a hét adatlap
sok tag-et ír le. A generátornak az egyszerűbb változatát használtuk (szivattyúk, hőcserélők,
néhány szeleptípus és szabályozókörök), mert csak abban lehet a berendezésfajtákat azokra
korlátozni, amelyekhez van adatlapunk, míg a kaszkádot a valósághűbb változat üzemeire hangolták.
Az adatlapi kérdések referenciáit egy modell írta a PDF-ből, ember nem ellenőrizte őket; a bíráló is
modell (vak, de nem ember), és ugyanazt a választ két bírálat egyszer eltérően ítélte meg. A több
adatlapos kérdések referenciája óvatos: ha valamelyik elemnek van olyan változata, amelyhez az
adatlap nem ad számot, a „legkisebb” elem nem dönthető el, és a bíráló ilyenkor a konkrét elemet
megnevező választ is rossznak ítéli. Végül a minta kicsi: üzemenként és családonként 15 kérdés,
egyetlen futás, ezért a konfidenciaintervallumok szélesek, és a pontosság üzemenként néhány
kérdéssel ingadozik.

## Továbblépés

A legközvetlenebb javítás az M1 elfogadási szabályának adatlapi kérdésekre szabott változata (például
a feltétel és az oldalszám meglétének ellenőrzése), valamint egy olyan első szint, amely a rajzi
lépés után az adatlapi részt az adatlapoldali rendszerre bízza. Hosszabb távon a mérést valódi
rajzokon, szélesebb adatlapkészlettel és emberileg ellenőrzött referenciákkal kell megismételni.
