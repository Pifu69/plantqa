// A dolgozat összeállítása: dolgozat/src/*.md (egyszerű markdown) -> dolgozat/dolgozat.docx.
// Támogatott: # / ## / ### címsor, bekezdés, "- " és "1. " lista, | táblázat | (előtte
// "Táblázat: felirat" sor), ![felirat](kép.png), ```kódblokk```, **félkövér**, *dőlt*, `kód`.
// Az ábrák és táblázatok számozása automatikus ("3. ábra:", "2. táblázat:").
// Futtatás: node dolgozat/build/build.js
const fs = require("fs");
let listInstance = 0;
const path = require("path");
const {
  AlignmentType, Document, Footer, HeadingLevel, ImageRun, LevelFormat, Packer,
  PageBreak, PageNumber, Paragraph, ShadingType, Tab, Table, TableCell, TableOfContents, TableRow,
  TextRun, WidthType,
} = require("docx");

const ROOT = path.resolve(__dirname, "..", "..");
const SRC = path.join(ROOT, "dolgozat", "src");
const OUT = path.join(ROOT, "dolgozat", "dolgozat.docx");
const FONT = "Cambria";
const BODY_PT = 11;
const TEXT_WIDTH = 8503; // A4, bal 3,5 cm / jobb 2,5 cm margó (VIK-sablon): 11906 - 1985 - 1418 DXA

let figureNo = 0;
let tableNo = 0;
let chapterNo = 0;
let sectionNo = 0;
const UNNUMBERED = ["Irodalomjegyzék", "Függelék"];

function numbered(level, text) {
  // fejezet- és alfejezetszám (a VIK-sablon szokása); az irodalom és a függelék számozatlan
  if (level === 1) {
    if (UNNUMBERED.includes(text)) { chapterNo = -1; return text; }
    chapterNo += 1; sectionNo = 0; return `${chapterNo}. ${text}`;
  }
  if (level === 2 && chapterNo > 0) { sectionNo += 1; return `${chapterNo}.${sectionNo} ${text}`; }
  return text;
}

// Hivatkozások: a szövegben [KULCS] vagy [K1, K2] (egymás után vesszővel is: [K1], [K2]);
// a kimenetben felső indexes sorszám az Irodalomjegyzék (08-irodalom.md) sorrendje szerint.
const BIB = new Map(); // kulcs -> sorszám
const UNKNOWN_KEYS = new Set();
// Kulcsnak csak betűvel kezdődő, szóköz nélküli azonosító számít (így a [0,133; 0,400]
// intervallum és a [szöveg](link) markdown-hivatkozás nem cserélődik).
const KEY = String.raw`[A-Za-z][A-Za-z0-9\-]*`;
const CITE_GROUP = String.raw`\[(?:${KEY})(?:\s*,\s*(?:${KEY}))*\](?!\()`;
const CITE_RE = new RegExp(String.raw`\s?${CITE_GROUP}(?:\s*,\s*${CITE_GROUP})*`, "g");

function loadBib() {
  const md = fs.readFileSync(path.join(SRC, "08-irodalom.md"), "utf8").replace(/\r/g, "");
  for (const line of md.split("\n")) {
    const m = line.match(/^- \[([^\]]+)\] /);
    if (m) BIB.set(m[1], BIB.size + 1);
  }
}

function citeRuns(text, base) {
  // egy kódjelölés nélküli szövegrész futásai, a hivatkozásokat felső indexre cserélve
  const out = [];
  let last = 0;
  for (const m of text.matchAll(CITE_RE)) {
    const keys = [...m[0].matchAll(/[^\s\[\],]+/g)].map((k) => k[0]);
    if (!keys.every((k) => BIB.has(k))) { keys.filter((k) => !BIB.has(k)).forEach((k) => UNKNOWN_KEYS.add(k)); continue; }
    if (m.index > last) out.push(new TextRun({ text: text.slice(last, m.index), ...base }));
    const nums = [...new Set(keys.map((k) => BIB.get(k)))].sort((a, b) => a - b);
    out.push(new TextRun({ text: nums.join(","), superScript: true, ...base }));
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push(new TextRun({ text: text.slice(last), ...base }));
  return out;
}

function runs(text, base = {}) {
  // **félkövér**, *dőlt*, `kód` beágyazott jelölés futásokra bontva
  const out = [];
  const re = /(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g;
  let last = 0;
  for (const m of text.matchAll(re)) {
    if (m.index > last) out.push(...citeRuns(text.slice(last, m.index), base));
    const t = m[0];
    if (t.startsWith("**")) out.push(...citeRuns(t.slice(2, -2), { bold: true, ...base }));
    else if (t.startsWith("`")) out.push(new TextRun({ text: t.slice(1, -1), font: "Consolas", size: 19, ...base }));
    else out.push(...citeRuns(t.slice(1, -1), { italics: true, ...base }));
    last = m.index + t.length;
  }
  if (last < text.length) out.push(...citeRuns(text.slice(last), base));
  return out;
}

function para(text, opts = {}) {
  return new Paragraph({ children: runs(text), spacing: { after: 120, line: 300 },
    alignment: AlignmentType.JUSTIFIED, ...opts });
}

function caption(text) {
  return new Paragraph({ children: runs(text, { size: 19 }), alignment: AlignmentType.CENTER,
    spacing: { before: 60, after: 200 } });
}

function image(file, label) {
  const full = path.resolve(SRC, file);
  const data = fs.readFileSync(full);
  const w = data.readUInt32BE(16), h = data.readUInt32BE(20); // PNG IHDR
  const width = 600, height = Math.round((600 * h) / w);
  figureNo += 1;
  return [
    new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120 },
      children: [new ImageRun({ type: "png", data, transformation: { width, height } })] }),
    caption(`${figureNo}. ábra: ${label}`),
  ];
}

function cell(text, header, width) {
  return new TableCell({
    width: { size: width, type: WidthType.DXA },
    shading: header ? { type: ShadingType.CLEAR, color: "auto", fill: "DCE6F0" } : undefined,
    margins: { top: 40, bottom: 40, left: 80, right: 80 },
    children: [new Paragraph({ children: runs(text, { size: 18, bold: header }) })],
  });
}

function table(lines, label) {
  const rows = lines.filter((l) => !/^\|\s*-/.test(l)).map((l) =>
    l.trim().replace(/^\||\|$/g, "").split("|").map((c) => c.trim()));
  const cols = rows[0].length;
  const width = Math.floor(TEXT_WIDTH / cols);
  tableNo += 1;
  const t = new Table({
    width: { size: width * cols, type: WidthType.DXA },
    columnWidths: Array(cols).fill(width),
    rows: rows.map((r, i) => new TableRow({ tableHeader: i === 0,
      children: r.map((c) => cell(c, i === 0, width)) })),
  });
  return [caption(`${tableNo}. táblázat: ${label}`), t, new Paragraph({ spacing: { after: 120 } })];
}

function heading(level, text, breakBefore = false) {
  return new Paragraph({ heading: level, pageBreakBefore: breakBefore, children: [new TextRun(text)] });
}

function codeBlock(lines, start) {
  const out = [];
  let i = start + 1;
  while (i < lines.length && !lines[i].startsWith("```")) {
    out.push(new Paragraph({ spacing: { after: 0 },
      shading: { type: ShadingType.CLEAR, color: "auto", fill: "F2F2F2" },
      children: [new TextRun({ text: lines[i] || " ", font: "Consolas", size: 17 })] }));
    i += 1;
  }
  out.push(new Paragraph({ spacing: { after: 120 } }));
  return [out, i + 1];
}

const BLOCK_START = /^(#|- |\d+\. |\||!\[|```|Táblázat: )/;

function chapter(md) {
  const out = [];
  const lines = md.replace(/\r/g, "").split("\n");
  let i = 0, pendingTable = "", first = true, prevNumbered = false;
  while (i < lines.length) {
    const line = lines[i];
    if (line.startsWith("# ")) { out.push(heading(HeadingLevel.HEADING_1, numbered(1, line.slice(2)), true)); first = false; i += 1; continue; }
    if (line.startsWith("## ")) { out.push(heading(HeadingLevel.HEADING_2, numbered(2, line.slice(3)))); i += 1; continue; }
    if (line.startsWith("### ")) { out.push(heading(HeadingLevel.HEADING_3, line.slice(4))); i += 1; continue; }
    if (line.startsWith("Táblázat: ")) { pendingTable = line.slice(10); i += 1; continue; }
    if (line.startsWith("|")) {
      const block = [];
      while (i < lines.length && lines[i].startsWith("|")) block.push(lines[i++]);
      out.push(...table(block, pendingTable)); pendingTable = ""; continue;
    }
    const img = line.match(/^!\[(.*)\]\((.*)\)\s*$/);
    if (img) { out.push(...image(img[2], img[1])); i += 1; continue; }
    if (line.startsWith("```")) { const [code, next] = codeBlock(lines, i); out.push(...code); i = next; continue; }
    const bib = line.match(/^- \[([^\]]+)\] (.*)$/);
    if (bib && BIB.has(bib[1])) {
      // irodalomjegyzéki tétel: [n] sorszámmal, függő behúzással
      out.push(new Paragraph({ children: [new TextRun({ children: [`[${BIB.get(bib[1])}]`, new Tab()] }), ...runs(bib[2])],
        spacing: { after: 60 }, indent: { left: 560, hanging: 560 }, tabStops: [{ type: "left", position: 560 }] }));
      prevNumbered = false; i += 1; continue;
    }
    if (/^(- |\d+\. )/.test(line)) {
      // Listaelem: a behúzott folytatósorok ugyanahhoz az elemhez tartoznak.
      let text = line.replace(/^(- |\d+\. )/, "");
      let j = i + 1;
      while (j < lines.length && /^\s{2,}\S/.test(lines[j])) text += " " + lines[j++].trim();
      const numberedItem = /^\d+\. /.test(line);
      // Minden új számozott lista 1-től indul: külön számozási példányt kap.
      if (numberedItem && !prevNumbered) listInstance += 1;
      const ref = numberedItem ? { reference: "numbers", level: 0, instance: listInstance } : { reference: "bullets", level: 0 };
      out.push(new Paragraph({ numbering: ref, children: runs(text), spacing: { after: 60 } }));
      prevNumbered = numberedItem; i = j; continue;
    }
    prevNumbered = false;
    if (!line.trim()) { i += 1; continue; }
    const parts = [line];
    while (i + 1 < lines.length && lines[i + 1].trim() && !BLOCK_START.test(lines[i + 1])) parts.push(lines[++i]);
    out.push(para(parts.join(" "))); i += 1;
  }
  return out;
}

function centered(text, size, opts = {}) {
  return new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 160 },
    children: [new TextRun({ text, size, ...opts })] });
}

function titlePage(meta) {
  return [
    centered("Budapesti Műszaki és Gazdaságtudományi Egyetem", 26, { bold: true }),
    centered("Villamosmérnöki és Informatikai Kar", 24),
    centered(meta.department, 22),
    new Paragraph({ spacing: { before: 2400 } }),
    centered(meta.title, 36, { bold: true }),
    centered(meta.subtitle, 24, { italics: true }),
    new Paragraph({ spacing: { before: 1600 } }),
    centered("Tudományos Diákköri Konferencia dolgozat", 22),
    centered(`Szerzők: ${meta.authors.join(", ")}`, 22),
    centered(`Témavezető: ${meta.supervisor}`, 22),
    new Paragraph({ spacing: { before: 2400 } }),
    centered(meta.date, 22),
    new Paragraph({ children: [new PageBreak()] }),
  ];
}

function abstractPage(title, file) {
  const blocks = fs.readFileSync(path.join(SRC, file), "utf8").trim().split(/\n\s*\n/);
  return [heading(HeadingLevel.HEADING_1, title, true), ...blocks.map((p) => para(p.replace(/\n/g, " ")))];
}

function styles() {
  const h = (id, size, color, before, after, level) => ({ id, name: id.replace("Heading", "Heading "),
    basedOn: "Normal", next: "Normal", quickFormat: true, run: { size, bold: true, color },
    paragraph: { spacing: { before, after }, outlineLevel: level } });
  return {
    default: { document: { run: { font: FONT, size: BODY_PT * 2 } } },
    paragraphStyles: [h("Heading1", 32, "1F3A5F", 240, 240, 0), h("Heading2", 26, "1F3A5F", 240, 120, 1),
      h("Heading3", 23, "000000", 180, 100, 2)],
  };
}

function numbering() {
  const level = (format, text) => [{ level: 0, format, text, alignment: AlignmentType.LEFT,
    style: { paragraph: { indent: { left: 540, hanging: 300 } } } }];
  return { config: [{ reference: "bullets", levels: level(LevelFormat.BULLET, "•") },
    { reference: "numbers", levels: level(LevelFormat.DECIMAL, "%1.") }] };
}

function main() {
  const meta = JSON.parse(fs.readFileSync(path.join(SRC, "meta.json"), "utf8"));
  loadBib();
  const chapters = fs.readdirSync(SRC).filter((f) => /^\d\d-.*\.md$/.test(f)).sort();
  const body = chapters.flatMap((f) => chapter(fs.readFileSync(path.join(SRC, f), "utf8")));
  const footer = new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER,
    children: [new TextRun({ children: [PageNumber.CURRENT], size: 18 })] })] });
  const doc = new Document({
    creator: meta.authors.join(", "), title: meta.title, styles: styles(), numbering: numbering(),
    sections: [{
      properties: { page: { margin: { top: 1418, bottom: 1418, left: 1985, right: 1418 } } },
      footers: { default: footer },
      children: [
        ...titlePage(meta),
        ...abstractPage("Kivonat", "kivonat.md"),
        ...abstractPage("Abstract", "abstract.md"),
        heading(HeadingLevel.HEADING_1, "Tartalomjegyzék", true),
        new TableOfContents("Tartalomjegyzék", { hyperlink: true, headingStyleRange: "1-3" }),
        ...body,
      ],
    }],
  });
  Packer.toBuffer(doc).then((buf) => {
    fs.writeFileSync(OUT, buf);
    console.log(`written ${OUT}: ${figureNo} figures, ${tableNo} tables, ${BIB.size} references`);
    if (UNKNOWN_KEYS.size) console.log(`ismeretlen hivatkozási kulcsok: ${[...UNKNOWN_KEYS].join(", ")}`);
  });
}

main();
