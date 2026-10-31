// Az előadás második fele (a build.js hívja): (e) eredmény, hibaelemzés, összefoglalás,
// köszönet, tartalék diák. A számok a runs/<EXP>/summary.csv és pairs.csv fájlokból jönnek.
const fs = require("fs");
const path = require("path");
const B = require("./build.js");
const { pres, content, title, body, image, csv, all, pct, hu, MODEL, METHOD, ROOT, OUT, NAVY, WHITE, LIGHT, INK, MUTED } = B;

const COMPLEX = path.join(ROOT, "runs", "EXP-030", "summary.csv");
const complexAll = fs.existsSync(COMPLEX) ? csv(COMPLEX).filter((r) => r.family === "all") : [];
const accOf = (m, mo) => (all.find((r) => r.method === m && r.model === mo) || {}).accuracy;
const corrOf = (m, mo) => (all.find((r) => r.method === m && r.model === mo) || {}).correct;
const pairOf = (mo, a, b) => B.pairs.find((p) => p.model === mo && p.a === a && p.b === b) || {};

function complexSlide() {
  const labels = complexAll.map((r) => `${r.method} ${r.model === "glm" ? "GLM" : "Luna"}`);
  const values = complexAll.map((r) => Number(r.correct));
  const partial = complexAll.map((r) => Number(r.partial));
  const notes = complexAll.map((r) => `${r.method} ${MODEL[r.model]}: ${r.correct} helyes a ${r.n}-ből`).join("; ");
  const s = content(`Külön mérést végeztünk 12 olyan kérdésen, amelyekhez a rajzon egy utat vagy elemhalmazt kell bejárni, és két-három adatlapot kell összevetni. Ezeket a végső teszt után, változatlan módszerekkel futtattuk. Eredmény: ${notes}.`);
  title(s, "Több adatlapos kérdések (12 db) — EXP-030");
  if (values.length) {
    s.addChart(pres.charts.BAR, [{ name: "helyes", labels, values }, { name: "részben helyes", labels, values: partial }], { x: 0.4, y: 1.0, w: 5.6, h: 4.0, barDir: "col",
      barGrouping: "stacked", chartColors: [NAVY, "9FB6D0"], showValue: true, dataLabelPosition: "ctr", dataLabelFormatCode: "0",
      dataLabelFontSize: 10, dataLabelColor: WHITE, valAxisMinVal: 0, valAxisMaxVal: 12, showLegend: true, legendPos: "b", legendFontSize: 10, legendFontFace: "+mn-lt",
      catAxisLabelFontSize: 10, valAxisLabelFontSize: 9, catAxisLabelColor: MUTED, valAxisLabelColor: MUTED,
      valGridLine: { color: "E4E3DF", size: 0.5 }, catGridLine: { style: "none" }, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt" });
  }
  body(s, ["Út + szélsőérték, halmaz + felsorolás, két lépés + összevetés", "Referencia programmal: gold gráf + PDF-ből gyűjtött tények",
    "4 kérdésnél a helyes válasz: a rajzból nem dönthető el"], { x: 6.2, y: 1.2, w: 3.4, h: 3.6, fontSize: 14 });
}

function errorSlide() {
  const s = content("Három jellemző hibát láttunk. Az M1 egyetlen lekérdezéssel talál egy releváns adatpontot, a kaszkád elfogadja a nem üres eredményt, és kimarad egy feltétel vagy második érték. A router a rajzeszköznek szabad szöveges kérdést ad, ezért ott a válasz alakja elcsúszhat, például szelepet ad szabályozókör helyett. A baseline a visszakeresett darabok közül néha nem kapja meg a szükséges táblázatot. Hallucinációt egyik módszer sem produkált a teszten.");
  title(s, "Hibaelemzés");
  const cards = [["M1", "Egy szűk lekérdezés, hiányos sor elfogadva: a feltétel vagy a második érték kimarad"],
    ["M2", "A rajzeszköz szabad szöveges kérdést kap: a válasz alakja elcsúszhat (szelep a kör helyett)"],
    ["M3", "A 12 visszakeresett darab nem mindig hozza a szükséges adatlap-táblázatot"]];
  cards.forEach(([m, t], i) => {
    const x = 0.5 + i * 3.1;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.3, w: 2.85, h: 3.2, fill: { color: LIGHT }, line: { color: LIGHT }, rectRadius: 0.08 });
    s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: 1.5, w: 0.7, h: 0.7, fill: { color: METHOD[m] }, line: { color: METHOD[m] } });
    s.addText(m, { x: x + 0.2, y: 1.5, w: 0.7, h: 0.7, fontSize: 14, bold: true, color: WHITE, align: "center", isTextBox: true });
    s.addText(t, { x: x + 0.2, y: 2.4, w: 2.45, h: 1.9, fontSize: 14, color: INK, valign: "top", isTextBox: true });
  });
}

function summarySlide() {
  const d1 = pairOf("glm", "M1", "M2"), d3 = pairOf("glm", "M1", "M3");
  const s = content(`Összefoglalva: az összevont gráfon a vegyes kérdések megválaszolhatók, de a router pontosabb volt. GLM-mel az M2 ${corrOf("M2", "glm")}, az M3 ${corrOf("M3", "glm")}, az M1 ${corrOf("M1", "glm")} helyes választ adott a 40-ből; az M1 elmaradása mindkettőtől szignifikáns. Az M1 a legdrágább, az M3 a legolcsóbb, de ez a kis rajzon igaz. A különbség az adatlapi és vegyes kérdéseken jön ki, és egyik módszer sem hallucinált.`);
  title(s, "Összefoglalás");
  const rows = [["RQ1", `Router (M2) a legjobb: GLM-mel ${pct(accOf("M2", "glm"))}, M1 ${pct(accOf("M1", "glm"))} (M1−M2 ${hu(d1.diff, 3)} [${hu(d1.ci_low, 3)}; ${hu(d1.ci_high, 3)}], M1−M3 ${hu(d3.diff, 3)})`],
    ["RQ2", "M1 a legdrágább; M2 GLM-mel kb. fele, Lunával 0,4-szerese; M3 a legolcsóbb (a kis rajzon)"],
    ["RQ3", "Rajz- és „nincs benne” kérdés: mind erős; adatlapi és vegyes kérdésen nyílik szét"]];
  rows.forEach(([k, t], i) => {
    s.addShape(pres.shapes.OVAL, { x: 0.6, y: 1.25 + i * 1.2, w: 0.8, h: 0.8, fill: { color: NAVY }, line: { color: NAVY } });
    s.addText(k, { x: 0.6, y: 1.25 + i * 1.2, w: 0.8, h: 0.8, fontSize: 14, bold: true, color: WHITE, align: "center", isTextBox: true });
    s.addText(t, { x: 1.65, y: 1.25 + i * 1.2, w: 7.9, h: 0.8, fontSize: 15, color: INK, valign: "middle", isTextBox: true });
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
  const s = content("Tartalék: a teljes eredménymátrix a végső teszten.");
  title(s, `Tartalék: teljes eredmény (${B.TEST})`);
  const rows = [["Módszer", "Modell", "Helyes", "Részben", "Rossz", "Halluc.", "Pontosság [95% CI]"]];
  all.forEach((r) => rows.push([r.method, MODEL[r.model], r.correct, r.partial, r.wrong, r.hallucinated, `${hu(r.accuracy, 3)} [${hu(r.ci_low, 3)}–${hu(r.ci_high, 3)}]`]));
  s.addTable(rows.map((r, i) => r.map((t) => ({ text: String(t), options: { bold: i === 0, fill: { color: i === 0 ? LIGHT : WHITE }, fontSize: 12, color: INK } }))),
    { x: 0.5, y: 1.1, w: 9, colW: [1.0, 1.8, 0.9, 0.9, 0.9, 0.9, 2.6], border: { type: "solid", color: "D5DDE6", pt: 0.75 } });
}

function backupLimits() {
  const s = content("Tartalék: a korlátok. Egyetlen kis szintetikus üzem; modellkészítésű referenciák és modell-bíráló; családonként tíz tesztkérdés; a POSC Caesar régi végpontja nem volt elérhető; a kaszkádot Benedek a v2 üzemekre hangolta, mi a v1-et használtuk.");
  title(s, "Tartalék: korlátok");
  body(s, ["Egy kis szintetikus üzem (26 tag, 4 lap)", "Modellkészítésű referencia, vak modell-bíráló (nem ember)",
    "Családonként 10 tesztkérdés: széles intervallumok", "POSC Caesar régi SPARQL-végpontja nem volt elérhető",
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
