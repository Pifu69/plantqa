// Az előadás összeállítása: node eloadas/build/build.js -> eloadas/eloadas.pptx
// Minden szám és diagram futáskor az eredményfájlokból jön (runs/<EXP>/summary.csv, pairs.csv,
// data/plant/load_report.json, figures/plan.json); az ábrák a figures/ mappából és a demó
// képernyőképei a figures/demo/ mappából. A szöveg a dolgozattal egyező forrásokra épül.
// A 10. diától a build_rest.js folytatja. A közös mérés a két nagy üzemen (figures/plan.json „large”).
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const ROOT = path.resolve(__dirname, "..", "..");
const FIG = path.join(ROOT, "figures");
const OUT = path.join(ROOT, "eloadas", "eloadas.pptx");
const NAVY = "1F3A5F", INK = "1D2733", MUTED = "52514E", LIGHT = "EEF2F6", WHITE = "FFFFFF";
const METHOD = { M1: "2A78D6", M2: "EB6834", M3: "1BAF7A" };
const METHOD_LIGHT = { M1: "8DB6EA", M2: "F4A988", M3: "86D7B9" };
const MODEL = { glm: "GLM-5.3 Flash", luna: "GPT-6 Luna" };
const FAMILY = { a: "(a) rajz", b: "(b) adatlap", c: "(c) összetett", d: "(d) nincs benne", all: "összesen" };

function csv(file) {
  const [head, ...lines] = fs.readFileSync(file, "utf8").trim().split(/\r?\n/);
  const keys = head.split(",");
  return lines.map((l) => Object.fromEntries(l.split(",").map((v, i) => [keys[i], v])));
}

const plan = JSON.parse(fs.readFileSync(path.join(FIG, "plan.json"), "utf8"));
// A közös mérés a két nagy üzemen (plan.large); a kis üzem (plan.test) a fejlesztés terepe.
const LARGE = plan.large.map((item) => {
  const rows = csv(path.join(ROOT, "runs", item.exp, "summary.csv")).filter((r) => r.split === "dev+test");
  const plant = item.name === "pqb" ? "plant-pqb" : "plant-pqc";
  return { ...item, rows, all: rows.filter((r) => r.family === "all"),
    pairs: csv(path.join(ROOT, "runs", item.exp, "pairs.csv")),
    load: JSON.parse(fs.readFileSync(path.join(ROOT, "data", plant, "load_report.json"), "utf8")),
    tags: JSON.parse(fs.readFileSync(path.join(ROOT, "data", plant, "tags.json"), "utf8")).length };
});
const TEST = LARGE.map((l) => l.exp).join(", ");
const summary = LARGE[0].rows;
const pairs = LARGE[0].pairs;
const all = LARGE[0].all;
const best = [...all].sort((a, b) => b.accuracy - a.accuracy || a.cost_usd - b.cost_usd)[0];
const KEYS = [["M1", "glm"], ["M2", "glm"], ["M3", "glm"], ["M1", "luna"], ["M2", "luna"], ["M3", "luna"]];
const rowOf = (l, m, mo, f = "all") => l.rows.find((r) => r.method === m && r.model === mo && r.family === f) || {};
const pct = (x) => `${Math.round(Number(x) * 100)}%`;
const hu = (x, d = 2) => Number(x).toFixed(d).replace(".", ",");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
pres.author = "Szabó Zsombor István, Kiszely Benedek";
pres.title = "Tudásgráf-építés műszaki rajzokból és adatlapokból";
pres.theme = { headFontFace: "Cambria", bodyFontFace: "Calibri" };

pres.defineSlideMaster({
  title: "CONTENT", background: { color: WHITE },
  objects: [{ text: { text: "TDK 2026 · plantqa", options: { x: 0.4, y: 5.3, w: 4, h: 0.25, fontSize: 9, color: MUTED } } }],
  slideNumber: { x: 9.2, y: 5.3, w: 0.5, h: 0.25, fontSize: 9, color: MUTED },
});
pres.defineSlideMaster({ title: "DARK", background: { color: NAVY } });

function title(slide, text) {
  slide.addText(text, { x: 0.4, y: 0.25, w: 9.2, h: 0.7, fontFace: "Cambria", fontSize: 28, bold: true, color: NAVY, isTextBox: true, margin: 0 });
}

function body(slide, items, box) {
  slide.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1 } })),
    { fontSize: 15, color: INK, paraSpaceAfter: 8, valign: "top", isTextBox: true, ...box });
}

function image(slide, file, box) {
  const full = path.join(FIG, file);
  if (fs.existsSync(full)) slide.addImage({ path: full, ...box, sizing: { type: "contain", w: box.w, h: box.h } });
}

function stat(slide, x, value, label) {
  slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 1.25, w: 2.1, h: 1.35, fill: { color: LIGHT }, line: { color: LIGHT }, rectRadius: 0.08 });
  slide.addText(value, { x, y: 1.32, w: 2.1, h: 0.75, fontSize: 30, bold: true, color: NAVY, align: "center", isTextBox: true, fontFace: "Cambria" });
  slide.addText(label, { x: x + 0.1, y: 2.02, w: 1.9, h: 0.5, fontSize: 11, color: MUTED, align: "center", isTextBox: true });
}

function content(notes) {
  const s = pres.addSlide({ masterName: "CONTENT" });
  s.addNotes(notes);
  return s;
}

function titleSlide() {
  const s = pres.addSlide({ masterName: "DARK" });
  s.addText("Tudásgráf-építés műszaki rajzokból és adatlapokból skálázható Q&A rendszerhez", { x: 0.6, y: 1.2, w: 8.8, h: 1.6, fontFace: "Cambria", fontSize: 32, bold: true, color: WHITE, isTextBox: true });
  s.addText("Szabó Zsombor István · Kiszely Benedek", { x: 0.6, y: 3.1, w: 8.8, h: 0.4, fontSize: 18, color: WHITE, isTextBox: true });
  s.addText("Témavezető: [TÉMAVEZETŐ] · BME VIK TMIT · TDK 2026", { x: 0.6, y: 3.55, w: 8.8, h: 0.4, fontSize: 14, color: "CADCFC", isTextBox: true });
  s.addNotes("Jó napot kívánunk. Szabó Zsombor és Kiszely Benedek vagyunk. A munkánk két részből áll: Benedek a rajzokból épít az egész üzemet leíró tudásgráfot, én a gyártói adatlapokból eszközönként. A dolgozatban a kettőt összekötjük, és megmérjük, hogyan lehet a kettőn együtt kérdezni egyre nagyobb üzemeken.");
}

function motivation() {
  const s = content("Egy mérnöki kérdés gyakran két dokumentumot is érint. Ha azt kérdezzük, mekkora a megengedett nyomás azon a szelepen, amely egy szivattyú nyomóoldalát elzárja, akkor előbb a rajzon meg kell találni a szelepet, esetleg egy másik lapon, aztán az adatlapján a megfelelő feltételhez tartozó értéket. Ma ezt kézzel végzik.");
  title(s, "Egy kérdés, két dokumentum");
  image(s, "pid_sheet0.png", { x: 0.4, y: 1.05, w: 5.6, h: 3.9 });
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 6.25, y: 1.15, w: 3.4, h: 3.7, fill: { color: LIGHT }, line: { color: LIGHT }, rectRadius: 0.08 });
  s.addText([
    { text: "„Mekkora a megengedett nyomás azon a szelepen, amely a P-101 nyomóoldalát elzárja?”", options: { italic: true, breakLine: true } },
    { text: " ", options: { breakLine: true } },
    { text: "1. rajz: melyik szelep? (lapközi csatlakozón át)", options: { breakLine: true } },
    { text: "2. tag → adatlap", options: { breakLine: true } },
    { text: "3. adatlap: érték + feltétel + oldal" },
  ], { x: 6.4, y: 1.3, w: 3.1, h: 3.4, fontSize: 14, color: INK, valign: "top", isTextBox: true });
}

function questions() {
  const s = content("Három kérdést tettünk fel. Először: megválaszolhatók-e az ilyen kérdések egyetlen összevont gráfon, és ez hogyan viszonyul egy irányítóhoz, illetve egy gráf nélküli alapmódszerhez. Másodszor: hogyan változik a pontosság és a költség, ha nő az üzem, a módszerek változtatása nélkül. Harmadszor: melyik kérdéstípuson segít a gráf, és hol hibáznak a módszerek.");
  title(s, "Kutatási kérdések");
  const rq = [["RQ1", "Egy összevont gráf (M1) vs. router (M2) vs. gráf nélküli baseline (M3): pontosság"],
    ["RQ2", "Skálázódás: pontosság és költség 27 és 98 lapos üzemen, változatlan módszerekkel"], ["RQ3", "Mely kérdéscsaládokon segít a gráf, és milyen hibák jellemzők?"]];
  rq.forEach(([k, t], i) => {
    s.addShape(pres.shapes.OVAL, { x: 0.6, y: 1.25 + i * 1.2, w: 0.8, h: 0.8, fill: { color: NAVY }, line: { color: NAVY } });
    s.addText(k, { x: 0.6, y: 1.25 + i * 1.2, w: 0.8, h: 0.8, fontSize: 14, bold: true, color: WHITE, align: "center", isTextBox: true });
    s.addText(t, { x: 1.65, y: 1.25 + i * 1.2, w: 7.8, h: 0.8, fontSize: 17, color: INK, valign: "middle", isTextBox: true });
  });
}

function graphSlide() {
  const [b, c] = LARGE;
  const s = content(`Három üzemet generáltunk Benedek generátorával: egy négylaposat a fejlesztéshez, és két nagyot a méréshez, ${b.tags} és ${c.tags} tagelt elemmel. Mindegyikhez ugyanaz a hét gyártói adatlap tartozik, a hozzárendelést program végzi. A nagyobbik üzemen ${c.load.counts.described_by} DESCRIBED_BY él köti össze a rajz elemeit az adatlapgráfokkal.`);
  title(s, "Egy adatbázis, két réteg, három üzem");
  stat(s, 0.5, "4 · 27 · 98", "lap (fejlesztés · mérés · mérés)");
  stat(s, 2.8, `${b.tags} · ${c.tags}`, "tagelt elem a két nagy üzemen");
  stat(s, 5.1, c.load.counts.device_nodes.toLocaleString("hu-HU"), "adatlapcsúcs (7 adatlap)");
  stat(s, 7.4, String(c.load.counts.described_by), "DESCRIBED_BY él (98 lap)");
  s.addText("(:PlantItem {tag:'P-1-3'}) -[:DESCRIBED_BY]-> (eszköz) <-[alany]- (adatpont: érték, feltétel, oldal)", { x: 0.5, y: 3.0, w: 9, h: 0.5, fontSize: 13, fontFace: "Consolas", color: NAVY, isTextBox: true });
  body(s, ["Rajz: Benedek generátora és betöltője (változtatás nélkül)", "Adatlap: plantdocs ISO 15926 / QUDT gráf, tag szerint összekötve"], { x: 0.5, y: 3.6, w: 9, h: 1.3 });
  s.addText("Forrás: EXP-053, EXP-066", { x: 6.5, y: 5.0, w: 3.2, h: 0.25, fontSize: 9, color: MUTED, align: "right", isTextBox: true });
}

function methodsSlide() {
  const s = content("Három módszert hasonlítottunk össze. Az M1 Benedek kaszkádja az összevont gráfon: a Cypher-szint mindkét réteg sémáját látja, az ágens pedig új primitívet kapott, amely egy tag adatlapjából kér le tényt. Az M2 egy router, amely a két meglévő rendszert külön hívja. Az M3 gráf nélküli: az egész rajz és a kérdéshez visszakeresett adatlapszöveg egy promptban.");
  title(s, "Három módszer");
  image(s, "methods_overview.png", { x: 0.4, y: 1.0, w: 9.2, h: 3.9 });
}

function demoSlide() {
  const s = content("A demó a plantdocs alkalmazás mintájára készült: bal oldalon a rajz, jobb oldalon a kérdés, a választott módszer és modell. A válasz alatt látszik az útvonal, a lekérdezés és az adatlapi forrásoldal, amelyre kattintva megnyílik a PDF adott oldala.");
  title(s, "A demó");
  const dir = path.join(FIG, "demo");
  const shots = fs.existsSync(dir) ? fs.readdirSync(dir).filter((f) => f.endsWith(".png")).sort() : [];
  if (shots[0]) image(s, path.join("demo", shots[0]), { x: 0.4, y: 1.0, w: 9.2, h: 4.1 });
}

function evalSlide() {
  const s = content("Üzemenként 60 kérdés, négy családban: csak rajz, csak adatlap tagen át, összetett, és megválaszolhatatlan, plusz 12 több adatlapot összevető kérdés. A módszereket a kis üzemen fejlesztettük és befagyasztottuk; a két nagy üzemen semmit nem változtattunk, ott minden kérdés teszt. Ahol lehetett, programmal pontoztunk, a többit vak bíráló értékelte.");
  title(s, "Kiértékelés: üzemenként 60 kérdés");
  const rows = [["Család", "Példa", "Referencia"],
    ["(a) rajz", "Which instruments measure E-2-1?", "Benedek generátora"],
    ["(b) adatlap", "Regarding P-1-3: max casing pressure?", "plantdocs gold párok"],
    ["(c) összetett", "Consider the transmitter that measures E-2-1. …", "programmal (a)+(b)"],
    ["(d) nincs benne", "Regarding PV-2-1: how to take the bonnet off safely?", "„Not in the documents”"]];
  s.addTable(rows.map((r, i) => r.map((t) => ({ text: t, options: { bold: i === 0, fill: { color: i === 0 ? LIGHT : WHITE }, fontSize: 12, color: INK } }))),
    { x: 0.5, y: 1.1, w: 9, colW: [1.7, 4.6, 2.7], border: { type: "solid", color: "D5DDE6", pt: 0.75 } });
  body(s, ["Fejlesztés a 4 lapos üzemen, mérés a 27 és 98 lapos üzemen (befagyasztott módszerek)", "Programos pontozás + vak bíráló (plantdocs EXP-0029 prompt)"], { x: 0.5, y: 3.75, w: 9, h: 1.2 });
}

function chartAxes() {
  return { catAxisLabelColor: MUTED, valAxisLabelColor: MUTED, valGridLine: { color: "E4E3DF", size: 0.5 },
    catGridLine: { style: "none" }, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt" };
}

function resultSlide() {
  const labels = KEYS.map(([m, mo]) => `${m} ${mo === "glm" ? "GLM" : "Luna"}`);
  const data = LARGE.map((l) => ({ name: l.label, labels, values: KEYS.map(([m, mo]) => Number(rowOf(l, m, mo).accuracy || 0)) }));
  const [b, c] = LARGE;
  const s = content(`Mindkét nagy üzemen az irányító volt a legjobb a GLM modellel: ${rowOf(b, "M2", "glm").correct}, illetve ${rowOf(c, "M2", "glm").correct} helyes válasz a 60-ból. A gráfos módszerek pontossága a két méret között kevéssé változott, a gráf nélküli módszeré modellenként ellentétes irányba mozdult.`);
  title(s, `Pontosság a két nagy üzemen — ${TEST}`);
  s.addChart(pres.charts.BAR, data, { x: 0.4, y: 1.0, w: 9.2, h: 4.1, barDir: "col", barGrouping: "clustered",
    chartColors: ["9FB6D0", NAVY], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0%", dataLabelFontSize: 9,
    dataLabelColor: INK, valAxisMinVal: 0, valAxisMaxVal: 1, valAxisLabelFormatCode: "0%", showLegend: true, legendPos: "b",
    legendFontSize: 10, legendFontFace: "+mn-lt", catAxisLabelFontSize: 11, valAxisLabelFontSize: 10, ...chartAxes() });
}

function costSlide() {
  const labels = KEYS.map(([m, mo]) => `${m} ${mo === "glm" ? "GLM" : "Luna"}`);
  const data = LARGE.map((l) => ({ name: l.label, labels,
    values: KEYS.map(([m, mo]) => { const r = rowOf(l, m, mo); return Number(r.cost_usd) / Number(r.n); }) }));
  const [b, c] = LARGE;
  const m3 = (l) => Number(rowOf(l, "M3", "luna").cost_usd) / Number(rowOf(l, "M3", "luna").n);
  const s = content(`A kérdésenkénti költség. A gráfos módszereké a két méret között nem nő, mert a modellhez csak a lekérdezés eredménye jut el. A gráf nélküli módszer viszont az egész rajzot viszi magával: Lunával ${hu(m3(b), 5)}-ról ${hu(m3(c), 5)} dollárra nőtt a költsége kérdésenként.`);
  title(s, "Költség / kérdés: a gráf nélküli módszer drágul");
  s.addChart(pres.charts.BAR, data, { x: 0.4, y: 1.0, w: 9.2, h: 4.1, barDir: "col", barGrouping: "clustered",
    chartColors: ["9FB6D0", NAVY], showValue: true, dataLabelPosition: "outEnd", dataLabelFormatCode: "0.000", dataLabelFontSize: 9,
    dataLabelColor: INK, showLegend: true, legendPos: "b", legendFontSize: 10, legendFontFace: "+mn-lt",
    catAxisLabelFontSize: 11, valAxisLabelFontSize: 10, valAxisLabelFormatCode: "0.000", ...chartAxes() });
}

titleSlide();
motivation();
questions();
graphSlide();
methodsSlide();
demoSlide();
evalSlide();
resultSlide();
costSlide();

module.exports = { pres, content, title, body, image, csv, summary, pairs, all, best, pct, hu, plan, ROOT, FIG,
  MODEL, FAMILY, METHOD, TEST, OUT, NAVY, WHITE, LIGHT, INK, MUTED, LARGE, KEYS, rowOf };
require("./build_rest.js");
