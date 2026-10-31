// Az előadás összeállítása: node eloadas/build/build.js -> eloadas/eloadas.pptx
// Minden szám és diagram futáskor az eredményfájlokból jön (runs/<EXP>/summary.csv, pairs.csv,
// data/plant/load_report.json, figures/plan.json); az ábrák a figures/ mappából és a demó
// képernyőképei a figures/demo/ mappából. A szöveg a dolgozattal egyező forrásokra épül.
// A 10. diától a build_rest.js folytatja.
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
const TEST = plan.test;
const summary = csv(path.join(ROOT, "runs", TEST, "summary.csv"));
const pairs = csv(path.join(ROOT, "runs", TEST, "pairs.csv"));
const load = JSON.parse(fs.readFileSync(path.join(ROOT, "data", "plant", "load_report.json"), "utf8"));
const all = summary.filter((r) => r.family === "all");
const best = [...all].sort((a, b) => b.accuracy - a.accuracy || a.cost_usd - b.cost_usd)[0];
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
  s.addNotes("Jó napot kívánunk. Szabó Zsombor és Kiszely Benedek vagyunk. A dolgozatunk két egyéni munkát köt össze: egy P&ID-rajzokból épített üzemi gráfot és gyártói adatlapokból épített eszközgráfokat, és azt méri, hogyan lehet a kettőn együtt kérdezni.");
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
  const s = content("Három kérdést tettünk fel. Először: megválaszolhatók-e az ilyen kérdések egyetlen összevont gráfon, és ez hogyan viszonyul egy routerhez, illetve egy gráf nélküli baseline-hoz. Másodszor: mennyibe kerül ez tokenben, pénzben és időben. Harmadszor: melyik kérdéstípuson segít a gráf, és hol hibáznak a módszerek.");
  title(s, "Kutatási kérdések");
  const rq = [["RQ1", "Egy összevont gráf (M1) vs. router (M2) vs. gráf nélküli baseline (M3): pontosság"],
    ["RQ2", "Költség: token, USD, késleltetés, két modellel"], ["RQ3", "Mely kérdéscsaládokon segít a gráf, és milyen hibák jellemzők?"]];
  rq.forEach(([k, t], i) => {
    s.addShape(pres.shapes.OVAL, { x: 0.6, y: 1.25 + i * 1.2, w: 0.8, h: 0.8, fill: { color: NAVY }, line: { color: NAVY } });
    s.addText(k, { x: 0.6, y: 1.25 + i * 1.2, w: 0.8, h: 0.8, fontSize: 14, bold: true, color: WHITE, align: "center", isTextBox: true });
    s.addText(t, { x: 1.65, y: 1.25 + i * 1.2, w: 7.8, h: 0.8, fontSize: 17, color: INK, valign: "middle", isTextBox: true });
  });
}

function graphSlide() {
  const c = load.counts;
  const s = content(`A példaüzemet Benedek generátora állította elő, seedelve: négy lap, 26 tagelt elem. Minden tagelt fizikai elemhez tartozik gyártói adatlap, hét különböző adatlap. Az összevont gráfban az üzemi réteg ${c.plant_nodes} csúcs, a hét adatlapgráf együtt ${c.device_nodes} csúcs, és a kettőt ${c.described_by} DESCRIBED_BY él köti össze a tag alapján.`);
  title(s, "Egy adatbázis, két réteg");
  stat(s, 0.5, String(c.plant_nodes), "üzemi csúcs (4 lap, 26 tag)");
  stat(s, 2.8, c.device_nodes.toLocaleString("hu-HU"), "adatlapcsúcs (7 adatlap)");
  stat(s, 5.1, String(c.described_by), "DESCRIBED_BY él (tag → adatlap)");
  stat(s, 7.4, `${Math.round(load.seconds.total)} s`, "teljes betöltés egy paranccsal");
  s.addText("(:PlantItem {tag:'P-1-3'}) -[:DESCRIBED_BY]-> (eszköz) <-[alany]- (adatpont: érték, feltétel, oldal)", { x: 0.5, y: 3.0, w: 9, h: 0.5, fontSize: 13, fontFace: "Consolas", color: NAVY, isTextBox: true });
  body(s, ["Rajz: Benedek generátora és betöltője (változtatás nélkül)", "Adatlap: plantdocs ISO 15926 / QUDT gráf, Opus-feldolgozás"], { x: 0.5, y: 3.6, w: 9, h: 1.3 });
  s.addText(`Forrás: ${plan.load}`, { x: 6.5, y: 5.0, w: 3.2, h: 0.25, fontSize: 9, color: MUTED, align: "right", isTextBox: true });
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
  const s = content("A kérdéssor 60 kérdésből áll, négy családban: csak rajz, csak adatlap tagen át, összetett, és megválaszolhatatlan. Húsz kérdés a fejlesztéshez kellett, negyvenet befagyasztottunk és csak a végén futtattuk. Ahol lehetett, programmal pontoztunk, a többit vak bíráló értékelte, aki nem látta, melyik módszer válaszolt.");
  title(s, "Kiértékelés: 60 kérdés, négy család");
  const rows = [["Család", "Példa", "Referencia"],
    ["(a) rajz", "Which instruments measure E-2-1?", "Benedek generátora"],
    ["(b) adatlap", "Regarding P-1-3: max casing pressure?", "plantdocs gold párok"],
    ["(c) összetett", "Consider the transmitter that measures E-2-1. …", "programmal (a)+(b)"],
    ["(d) nincs benne", "Regarding PV-2-1: how to take the bonnet off safely?", "„Not in the documents”"]];
  s.addTable(rows.map((r, i) => r.map((t) => ({ text: t, options: { bold: i === 0, fill: { color: i === 0 ? LIGHT : WHITE }, fontSize: 12, color: INK } }))),
    { x: 0.5, y: 1.1, w: 9, colW: [1.7, 4.6, 2.7], border: { type: "solid", color: "D5DDE6", pt: 0.75 } });
  body(s, ["Dev 20 kérdés (iterációk), teszt 40 (befagyasztva, sha256)", "Programos pontozás + vak bíráló (plantdocs EXP-0029 prompt)"], { x: 0.5, y: 3.75, w: 9, h: 1.2 });
}

function chartAxes() {
  return { catAxisLabelColor: MUTED, valAxisLabelColor: MUTED, valGridLine: { color: "E4E3DF", size: 0.5 },
    catGridLine: { style: "none" }, catAxisLabelFontFace: "+mn-lt", valAxisLabelFontFace: "+mn-lt" };
}

function resultSlide() {
  const fams = ["a", "b", "c", "d", "all"];
  const keys = all.map((r) => [r.method, r.model]);
  const find = (m, mo, f) => summary.find((r) => r.method === m && r.model === mo && r.family === f) || {};
  const data = keys.map(([m, mo]) => ({ name: `${m} · ${MODEL[mo]}`, labels: fams.map((f) => FAMILY[f]),
    values: fams.map((f) => Number(find(m, mo, f).accuracy || 0)) }));
  const s = content(`A befagyasztott teszten a legjobb párosítás a(z) ${best.method} volt ${MODEL[best.model]} modellel, ${pct(best.accuracy)} pontossággal. Az ábra családonként mutatja a hat párosítást; a halványabb oszlopok a GPT-6 Luna.`);
  title(s, `Végső teszt (40 kérdés) — ${TEST}`);
  s.addChart(pres.charts.BAR, data, { x: 0.4, y: 1.0, w: 9.2, h: 4.1, barDir: "col", barGrouping: "clustered",
    chartColors: keys.map(([m, mo]) => (mo === "glm" ? METHOD[m] : METHOD_LIGHT[m])),
    valAxisMinVal: 0, valAxisMaxVal: 1, valAxisLabelFormatCode: "0%", showLegend: true, legendPos: "b", legendFontSize: 10,
    legendFontFace: "+mn-lt", catAxisLabelFontSize: 11, valAxisLabelFontSize: 10, ...chartAxes() });
}

function costSlide() {
  const labels = all.map((r) => `${r.method} ${r.model === "glm" ? "GLM" : "Luna"}`);
  const cost = all.map((r) => Number(r.cost_usd) / Number(r.n));
  const lat = all.map((r) => Number(r.latency_median_s));
  const s = content("Bal oldalon a kérdésenkénti költség, jobb oldalon a medián válaszidő. A költség a szolgáltató által jelentett ár, a cache-ből érkező hívásnál is az eredeti hívásé. Két külön diagram, mert a két mennyiség skálája eltér.");
  title(s, "Költség és késleltetés");
  const opts = (t, fmt) => ({ barDir: "col", showTitle: true, title: t, titleFontSize: 12, titleColor: INK, showLegend: false,
    chartColors: all.map((r) => (r.model === "glm" ? METHOD[r.method] : METHOD_LIGHT[r.method])), showValue: true,
    dataLabelPosition: "outEnd", dataLabelFormatCode: fmt, dataLabelFontSize: 9, dataLabelColor: INK,
    catAxisLabelFontSize: 9, valAxisLabelFontSize: 9, ...chartAxes() });
  s.addChart(pres.charts.BAR, [{ name: "USD / kérdés", labels, values: cost }], { x: 0.4, y: 1.0, w: 4.5, h: 4.0, ...opts("Költség / kérdés (USD)", "0.0000") });
  s.addChart(pres.charts.BAR, [{ name: "s", labels, values: lat }], { x: 5.1, y: 1.0, w: 4.5, h: 4.0, ...opts("Medián késleltetés (s)", "0.0") });
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
  MODEL, FAMILY, METHOD, TEST, OUT, NAVY, WHITE, LIGHT, INK, MUTED };
require("./build_rest.js");
