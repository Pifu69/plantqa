// Az előadás második fele (a build.js hívja): (e) eredmény, hibaelemzés, összefoglalás,
// köszönet, tartalék diák. A számok a runs/<EXP>/summary.csv és pairs.csv fájlokból jönnek.
const fs = require("fs");
const path = require("path");
const B = require("./build.js");
const { pres, content, title, body, image, csv, all, pct, hu, MODEL, METHOD, ROOT, OUT, NAVY, WHITE, LIGHT, INK, MUTED, LARGE, KEYS, rowOf } = B;

// Az (e) család a három mérőüzemen (figures/plan.json „complex_scale”).
const COMPLEX = B.plan.complex_scale.map((c) => [c.label, c.exp]).map(([label, exp]) => ({ label, exp,
  rows: csv(path.join(ROOT, "runs", exp, "summary.csv")).filter((r) => r.family === "all") }));
const accOf = (m, mo) => (all.find((r) => r.method === m && r.model === mo) || {}).accuracy;
const corrOf = (m, mo) => (all.find((r) => r.method === m && r.model === mo) || {}).correct;
const pairOf = (mo, a, b) => B.pairs.find((p) => p.model === mo && p.a === a && p.b === b) || {};

function complexSlide() {
  const labels = KEYS.map(([m, mo]) => `${m} ${mo === "glm" ? "GLM" : "Luna"}`);
  const find = (c, m, mo) => c.rows.find((r) => r.method === m && r.model === mo) || {};
  const data = COMPLEX.map((c) => ({ name: c.label, labels, values: KEYS.map(([m, mo]) => Number(find(c, m, mo).correct || 0)) }));
  const notes = COMPLEX.map((c) => `${c.label}: ` + KEYS.filter(([m, mo]) => find(c, m, mo).correct !== undefined).map(([m, mo]) => `${m} ${MODEL[mo]} ${find(c, m, mo).correct}`).join(", ")).join("; ");
  const s = content(`Külön 12 olyan kérdést is feltettünk üzemenként, amelyekhez a rajzon egy utat vagy elemhalmazt kell bejárni, és több adatlapot kell összevetni. A teljesen helyes válaszok száma: ${notes}. A gráf nélküli módszer ezek közül egyet sem oldott meg; az 1000 lapos üzemen nem is futtatható.`);
  title(s, "Több adatlapos kérdések (12 db)");
  s.addChart(pres.charts.BAR, data, { x: 0.4, y: 1.0, w: 5.8, h: 4.0, barDir: "col", barGrouping: "clustered",
    chartColors: ["9FB6D0", NAVY], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0",
    dataLabelFontSize: 10, dataLabelColor: INK, valAxisMinVal: 0, valAxisMaxVal: 12, showLegend: true, legendPos: "b", legendFontSize: 10, legendFontFace: "+mn-lt",
    catAxisLabelFontSize: 10, valAxisLabelFontSize: 9, catAxisLabelColor: MUTED, valAxisLabelColor: MUTED,
    valGridLine: { color: "E4E3DF", size: 0.5 }, catGridLine: { style: "none" }, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt" });
  body(s, ["Teljesen helyes válaszok száma a 12-ből", "Út + szélsőérték, halmaz + felsorolás, két lépés + összevetés",
    "Referencia programmal: a generált üzem pontos leírása + PDF-ből gyűjtött tények"], { x: 6.4, y: 1.2, w: 3.3, h: 3.6, fontSize: 14 });
}

function errorSlide() {
  const s = content("Három jellemző hibát láttunk. Az M1 egyetlen lekérdezéssel talál egy releváns adatpontot, a kaszkád elfogadja a nem üres eredményt, és kimarad egy feltétel vagy második érték. A router a rajzeszköznek szabad szöveges kérdést ad, ezért ott a válasz alakja elcsúszhat, például szelepet ad szabályozókör helyett. A gráf nélküli módszer a nagy rajzon gyakran tévesen azt mondja, hogy a dokumentum nem tartalmazza a választ, és a költsége a rajz méretével nő. A hallucinált válasz ritka volt.");
  title(s, "Hibaelemzés");
  const cards = [["M1", "Egy szűk lekérdezés, hiányos sor elfogadva: a feltétel vagy a második érték kimarad"],
    ["M2", "Szabad szöveges rajzkérdés: a válasz alakja elcsúszhat; hosszú kérdésnél lépéskorlát"],
    ["M3", "Nagy rajzon téves „nincs benne”, és a költség a lapszámmal nő"]];
  cards.forEach(([m, t], i) => {
    const x = 0.5 + i * 3.1;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.3, w: 2.85, h: 3.2, fill: { color: LIGHT }, line: { color: LIGHT }, rectRadius: 0.08 });
    s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: 1.5, w: 0.7, h: 0.7, fill: { color: METHOD[m] }, line: { color: METHOD[m] } });
    s.addText(m, { x: x + 0.2, y: 1.5, w: 0.7, h: 0.7, fontSize: 14, bold: true, color: WHITE, align: "center", isTextBox: true });
    s.addText(t, { x: x + 0.2, y: 2.4, w: 2.45, h: 1.9, fontSize: 14, color: INK, valign: "top", isTextBox: true });
  });
}

function summarySlide() {
  const [c, d] = LARGE;
  const cost = (l, m, mo) => { const r = rowOf(l, m, mo); return Number(r.cost_usd) / Number(r.n); };
  const s = content(`Összefoglalva: a 30 és 50 lapos üzemen hangolt, majd befagyasztott rendszer a soha nem látott 100 és 1000 lapos üzemen is működik. Az irányító GLM-mel ${rowOf(c, "M2", "glm").correct} és ${rowOf(d, "M2", "glm").correct} helyes választ adott a 60-ból. A gráf nélküli módszer 1000 lapnál már nem futtatható.`);
  title(s, "Összefoglalás");
  const rows = [["RQ1", `M2 GLM-mel: ${pct(rowOf(c, "M2", "glm").accuracy)} · ${pct(rowOf(d, "M2", "glm").accuracy)}; M1 GLM-mel: ${pct(rowOf(c, "M1", "glm").accuracy)} · ${pct(rowOf(d, "M1", "glm").accuracy)} (100 · 1000 lap)`],
    ["RQ2", `Gráfos: M2 GLM ${hu(cost(c, "M2", "glm"), 4)} → ${hu(cost(d, "M2", "glm"), 4)} USD/kérdés; gráf nélküli Lunával ${hu(cost(c, "M3", "luna"), 4)} USD (100 lap), 1000 lapon nem fér a kontextusba`],
    ["RQ3", "Rajz- és „nincs benne” kérdés: a gráfos módszerek erősek; adatlapi, összetett és több adatlapos kérdésen nyílik szét"]];
  rows.forEach(([k, t], i) => {
    s.addShape(pres.shapes.OVAL, { x: 0.6, y: 1.25 + i * 1.2, w: 0.8, h: 0.8, fill: { color: NAVY }, line: { color: NAVY } });
    s.addText(k, { x: 0.6, y: 1.25 + i * 1.2, w: 0.8, h: 0.8, fontSize: 14, bold: true, color: WHITE, align: "center", isTextBox: true });
    s.addText(t, { x: 1.65, y: 1.25 + i * 1.2, w: 7.9, h: 0.8, fontSize: 14, color: INK, valign: "middle", isTextBox: true });
  });
}

function thanks() {
  const s = pres.addSlide({ masterName: "DARK" });
  s.addText("Köszönjük a figyelmet!", { x: 0.6, y: 1.8, w: 8.8, h: 1.0, fontFace: "Cambria", fontSize: 36, bold: true, color: WHITE, isTextBox: true });
  s.addText("Kód, mérések, döntések: plantqa (docs/eredmenyek.md, docs/dontesek.md)", { x: 0.6, y: 3.0, w: 8.8, h: 0.5, fontSize: 14, color: "CADCFC", isTextBox: true });
  s.addNotes("Köszönjük a figyelmet, várjuk a kérdéseket.");
}

function backupDev() {
  const s = content("Tartalék: a fejlesztési iterációk a dev halmazon. Az első iterációban a Rosemount-gráf még hiányzott; a második a lekérdezési és válaszszabályokat hozta; a harmadikban bekerült a Rosemount; a negyedikben a befagyasztott módszereket Lunával mértük.");
  title(s, "Tartalék: dev iterációk");
  image(s, "dev_progress.png", { x: 0.4, y: 1.0, w: 9.2, h: 4.1 });
}

function backupTable() {
  const s = content("Tartalék: a teljes eredménymátrix a két tesztüzemen.");
  title(s, "Tartalék: teljes eredmény");
  const rows = [["Módszer", "Modell", "Lap", "Helyes", "Részben", "Rossz", "Halluc.", "Pontosság [95% CI]"]];
  KEYS.forEach(([m, mo]) => LARGE.forEach((l) => { const r = rowOf(l, m, mo); if (r.correct === undefined) return;
    rows.push([m, MODEL[mo], l.label.split(" ")[0], r.correct, r.partial, r.wrong, r.hallucinated, `${hu(r.accuracy, 3)} [${hu(r.ci_low, 3)}–${hu(r.ci_high, 3)}]`]); }));
  s.addTable(rows.map((r, i) => r.map((t) => ({ text: String(t), options: { bold: i === 0, fill: { color: i === 0 ? LIGHT : WHITE }, fontSize: 10, color: INK } }))),
    { x: 0.5, y: 1.0, w: 9, colW: [0.9, 1.6, 0.6, 0.8, 0.9, 0.8, 0.8, 2.6], border: { type: "solid", color: "D5DDE6", pt: 0.75 } });
}

function backupLimits() {
  const s = content("Tartalék: a korlátok. Szintetikus üzemek; modellkészítésű referenciák és modell-bíráló; üzemenként és családonként tizenöt kérdés; a POSC Caesar régi végpontja nem volt elérhető; a kaszkádot Benedek a v2 üzemekre hangolta, mi a v1-et használtuk.");
  title(s, "Tartalék: korlátok");
  body(s, ["Szintetikus üzemek (4, 30, 50, 100 és 1000 lap), hét adatlap", "Modellkészítésű referencia, vak modell-bíráló (nem ember)",
    "Üzemenként és családonként 15 kérdés: széles intervallumok", "POSC Caesar régi SPARQL-végpontja nem volt elérhető",
    "Kaszkád: v2-re hangolva, v1 üzemen futtatva"], { x: 0.5, y: 1.1, w: 9, h: 3.8 });
}

function backupWork() {
  const s = content("Tartalék: munkamegosztás. A rajzoldali rendszer Kiszely Benedek, az adatlapoldali Szabó Zsombor munkája; az összevonást és a mérést közösen készítettük, minden döntés és szám naplózva.");
  title(s, "Tartalék: munkamegosztás");
  body(s, ["Rajz (plantgraph): Kiszely Benedek", "Adatlap (plantdocs): Szabó Zsombor", "Összevonás, kérdéssor, mérés, demó: közösen",
    "Döntések: docs/dontesek.md, számok: docs/eredmenyek.md"], { x: 0.5, y: 1.1, w: 9, h: 3.8 });
}

complexSlide();
errorSlide();
summarySlide();
thanks();
backupDev();
backupTable();
backupLimits();
backupWork();

pres.writeFile({ fileName: OUT }).then((f) => console.log(`written ${f}`));
