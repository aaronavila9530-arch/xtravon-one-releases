
const fs = require("fs");
const path = require("path");

function loadPptxGen() {
  const roots = [
    process.env.NODE_PATH,
    path.join(__dirname, "node_modules"),
  ].filter(Boolean);

  for (const root of roots) {
    try {
      return require(path.join(root, "pptxgenjs"));
    } catch (_err) {}
  }
  return require("pptxgenjs");
}

const pptxgen = loadPptxGen();
const pptx = new pptxgen();
pptx.layout = "LAYOUT_WIDE";
pptx.author = "MSL / ERP GRAIN CONTROL";
pptx.company = "MSL";
pptx.subject = "Presentacion comercial ERP GRAIN CONTROL";
pptx.title = "ERP GRAIN CONTROL - Presentacion Comercial";
pptx.lang = "es-CR";
pptx.theme = {
  headFontFace: "Aptos Display",
  bodyFontFace: "Aptos",
  lang: "es-CR",
};
pptx.margin = 0;

const OUT = path.join(__dirname, "Entregables", "ERP_GRAIN_CONTROL_Presentacion_Comercial.pptx");
const SPLASH = path.join(__dirname, "assets", "splash_grain_control.png");

const C = {
  bg: "D6D3C9",
  sidebar: "5F6654",
  topbar: "B7B7A4",
  card: "F2F1EC",
  accent: "6B705C",
  accent2: "A5A58D",
  text: "2F2F2F",
  muted: "5A5A5A",
  border: "9A9A8A",
  warn: "C97B63",
  ok: "7A9E7E",
  info: "7C8DA6",
  danger: "B15C4A",
  white: "FFFFFF",
};

const W = 13.333;
const H = 7.5;

function slide(title, subtitle) {
  const s = pptx.addSlide();
  s.background = { color: C.bg };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: W, h: H, fill: { color: C.bg }, line: { color: C.bg } });
  s.addText(title, {
    x: 0.42, y: 0.30, w: 7.7, h: 0.45,
    fontFace: "Aptos Display", fontSize: 24, bold: true, color: C.text, margin: 0,
    breakLine: false, fit: "shrink"
  });
  if (subtitle) {
    s.addText(subtitle, {
      x: 0.43, y: 0.84, w: 11.9, h: 0.30,
      fontSize: 9.5, color: C.muted, margin: 0, breakLine: false, fit: "shrink"
    });
  }
  s.addShape(pptx.ShapeType.line, { x: 0.42, y: 1.20, w: 12.45, h: 0, line: { color: C.border, width: 1 } });
  return s;
}

function footer(s, n) {
  s.addText("ERP GRAIN CONTROL | Inteligencia logística y riesgo operativo", {
    x: 0.42, y: 7.17, w: 7.4, h: 0.16, fontSize: 6.8, color: C.muted, margin: 0
  });
  s.addText(String(n).padStart(2, "0"), {
    x: 12.25, y: 7.12, w: 0.55, h: 0.20, fontSize: 7.5, color: C.muted, align: "right", margin: 0
  });
}

function box(s, x, y, w, h, opts = {}) {
  s.addShape(pptx.ShapeType.roundRect, {
    x, y, w, h,
    rectRadius: 0.04,
    fill: { color: opts.fill || C.card, transparency: opts.transparency || 0 },
    line: { color: opts.line || C.border, width: opts.width || 1 },
    shadow: opts.shadow ? { type: "outer", color: "888888", opacity: 0.12, blur: 1, angle: 45, distance: 1 } : undefined,
  });
  if (opts.bar) {
    s.addShape(pptx.ShapeType.rect, { x, y, w, h: 0.07, fill: { color: opts.bar }, line: { color: opts.bar } });
  }
}

function label(s, txt, x, y, w, h, opts = {}) {
  s.addText(txt, {
    x, y, w, h,
    fontSize: opts.size || 9,
    bold: opts.bold || false,
    color: opts.color || C.text,
    margin: opts.margin ?? 0.03,
    breakLine: false,
    fit: "shrink",
    align: opts.align || "left",
    valign: opts.valign || "mid",
  });
}

function body(s, txt, x, y, w, h, opts = {}) {
  s.addText(txt, {
    x, y, w, h,
    fontSize: opts.size || 10,
    color: opts.color || C.text,
    margin: opts.margin ?? 0.05,
    breakLine: true,
    fit: "shrink",
    valign: "top",
    bold: opts.bold || false,
    bullet: opts.bullet || undefined,
    breakLine: opts.breakLine ?? true,
  });
}

function metric(s, title, value, x, y, w, h, color = C.accent, caption = "") {
  box(s, x, y, w, h, { fill: C.card, bar: color });
  label(s, title, x + 0.18, y + 0.22, w - 0.36, 0.22, { size: 8.4, bold: true, color: C.muted });
  label(s, value, x + 0.18, y + 0.56, w - 0.36, 0.42, { size: 20, bold: true });
  if (caption) label(s, caption, x + 0.18, y + 1.08, w - 0.36, 0.22, { size: 7.2, color: C.muted });
}

function bulletList(s, items, x, y, w, h, size = 9.4) {
  const lines = items.map(v => ({ text: v, options: { bullet: { type: "ul" }, hanging: 3 } }));
  s.addText(lines, { x, y, w, h, fontSize: size, color: C.text, margin: 0.04, breakLine: true, fit: "shrink" });
}

function barChart(s, title, items, x, y, w, h, maxValue, color = C.accent) {
  box(s, x, y, w, h, { fill: C.card, line: C.border });
  label(s, title, x + 0.16, y + 0.12, w - 0.3, 0.25, { size: 10, bold: true });
  const left = x + 1.55, top = y + 0.55, barH = 0.18, gap = 0.17;
  const usable = w - 2.0;
  items.forEach((it, idx) => {
    const yy = top + idx * (barH + gap);
    label(s, it[0], x + 0.18, yy - 0.02, 1.22, 0.18, { size: 7.2, color: C.muted });
    s.addShape(pptx.ShapeType.rect, { x: left, y: yy, w: usable, h: barH, fill: { color: "E7E5DD" }, line: { color: "E7E5DD" } });
    s.addShape(pptx.ShapeType.rect, { x: left, y: yy, w: Math.max(0.03, usable * it[1] / maxValue), h: barH, fill: { color }, line: { color } });
    label(s, Number(it[1]).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 }), left + usable + 0.08, yy - 0.02, 0.58, 0.18, { size: 6.8, color: C.text });
  });
}

function lineChart(s, title, values, x, y, w, h, color = C.info) {
  box(s, x, y, w, h, { fill: C.card, line: C.border });
  label(s, title, x + 0.16, y + 0.12, w - 0.32, 0.25, { size: 10, bold: true });
  const gx = x + 0.45, gy = y + 0.55, gw = w - 0.75, gh = h - 0.90;
  s.addShape(pptx.ShapeType.line, { x: gx, y: gy + gh, w: gw, h: 0, line: { color: C.border, width: 1 } });
  s.addShape(pptx.ShapeType.line, { x: gx, y: gy, w: 0, h: gh, line: { color: C.border, width: 1 } });
  const max = Math.max(...values.map(v => v[1]));
  let prev = null;
  values.forEach((v, i) => {
    const px = gx + (gw * i / (values.length - 1));
    const py = gy + gh - (gh * v[1] / max);
    if (prev) s.addShape(pptx.ShapeType.line, { x: prev[0], y: prev[1], w: px - prev[0], h: py - prev[1], line: { color, width: 2.2 } });
    s.addShape(pptx.ShapeType.ellipse, { x: px - 0.045, y: py - 0.045, w: 0.09, h: 0.09, fill: { color: C.accent }, line: { color: C.accent } });
    prev = [px, py];
  });
  label(s, values[0][0], gx, gy + gh + 0.08, 0.7, 0.16, { size: 6.5, color: C.muted });
  label(s, values[values.length - 1][0], gx + gw - 0.7, gy + gh + 0.08, 0.7, 0.16, { size: 6.5, color: C.muted, align: "right" });
}

function donutLegend(s, title, items, x, y, w, h) {
  box(s, x, y, w, h, { fill: C.card, line: C.border });
  label(s, title, x + 0.16, y + 0.12, w - 0.3, 0.25, { size: 10, bold: true });
  const total = items.reduce((a, b) => a + b[1], 0);
  const cx = x + 0.76, cy = y + 1.00;
  const colors = [C.accent, C.ok, C.warn, C.info, C.danger];
  let start = 0;
  items.forEach((it, i) => {
    const pct = it[1] / total;
    // A PowerPoint-native pie approximation with stacked partial circles.
    s.addShape(pptx.ShapeType.arc, {
      x: cx - 0.43, y: cy - 0.43, w: 0.86, h: 0.86,
      adjustPoint: start,
      line: { color: colors[i % colors.length], width: 9 },
      rotate: start * 360,
    });
    start += pct;
  });
  s.addShape(pptx.ShapeType.ellipse, { x: cx - 0.25, y: cy - 0.25, w: 0.50, h: 0.50, fill: { color: C.card }, line: { color: C.card } });
  label(s, "100%", cx - 0.18, cy - 0.07, 0.36, 0.14, { size: 7, bold: true, align: "center" });
  items.forEach((it, i) => {
    const yy = y + 0.55 + i * 0.28;
    s.addShape(pptx.ShapeType.rect, { x: x + 1.40, y: yy + 0.04, w: 0.10, h: 0.10, fill: { color: colors[i % colors.length] }, line: { color: colors[i % colors.length] } });
    label(s, `${it[0]}: ${it[1].toFixed(2)}%`, x + 1.56, yy, w - 1.72, 0.18, { size: 7.6, color: C.text });
  });
}

function ship(s, x, y, w, h, title, holds, mode = "full") {
  box(s, x, y, w, h, { fill: C.card, line: C.border });
  label(s, title, x + 0.17, y + 0.12, w - 0.34, 0.25, { size: 10, bold: true });
  const sx = x + 0.38, sy = y + 0.68, sw = w - 0.76, sh = h - 1.05;
  s.addShape(pptx.ShapeType.pentagon, {
    x: sx, y: sy + sh * 0.22, w: sw, h: sh * 0.56,
    fill: { color: "DFE4D8" },
    line: { color: C.accent, width: 1.6 },
  });
  const holdW = sw * 0.145;
  holds.forEach((v, i) => {
    const hx = sx + sw * 0.08 + i * (holdW + sw * 0.035);
    const hy = sy + sh * 0.38;
    s.addShape(pptx.ShapeType.rect, { x: hx, y: hy, w: holdW, h: sh * 0.24, fill: { color: "FFFFFF", transparency: 5 }, line: { color: C.border, width: 0.8 } });
    const fillH = sh * 0.24 * (mode === "emptying" ? v / 100 : 1);
    const fy = hy + sh * 0.24 - fillH;
    s.addShape(pptx.ShapeType.rect, { x: hx + 0.02, y: fy, w: holdW - 0.04, h: Math.max(0.02, fillH), fill: { color: mode === "emptying" ? C.warn : C.ok }, line: { color: mode === "emptying" ? C.warn : C.ok } });
    label(s, `B${i + 1}`, hx, hy - 0.18, holdW, 0.13, { size: 6.5, bold: true, align: "center" });
    label(s, `${v.toFixed(2)}%`, hx, hy + sh * 0.27, holdW, 0.13, { size: 5.9, align: "center", color: C.muted });
  });
}

function uiWindow(s, x, y, w, h, title) {
  box(s, x, y, w, h, { fill: C.card, line: C.border, shadow: true });
  s.addShape(pptx.ShapeType.rect, { x, y, w, h: 0.36, fill: { color: C.topbar }, line: { color: C.topbar } });
  label(s, title, x + 0.20, y + 0.08, w - 0.4, 0.18, { size: 8.5, bold: true });
}

function tableMock(s, x, y, w, h, headers, rows) {
  box(s, x, y, w, h, { fill: "FFFFFF", line: C.border });
  const rh = 0.28;
  s.addShape(pptx.ShapeType.rect, { x, y, w, h: rh, fill: { color: C.accent }, line: { color: C.accent } });
  const cw = w / headers.length;
  headers.forEach((hd, i) => label(s, hd, x + i * cw + 0.04, y + 0.06, cw - 0.08, 0.13, { size: 6.8, bold: true, color: C.white, align: "center" }));
  rows.forEach((r, ri) => {
    const yy = y + rh + ri * rh;
    if (ri % 2 === 1) s.addShape(pptx.ShapeType.rect, { x, y: yy, w, h: rh, fill: { color: "F3F2ED" }, line: { color: "F3F2ED" } });
    r.forEach((cell, ci) => label(s, String(cell), x + ci * cw + 0.04, yy + 0.06, cw - 0.08, 0.13, { size: 6.3, color: C.text, align: "center" }));
  });
}

function callout(s, title, text, x, y, w, h, color = C.accent) {
  box(s, x, y, w, h, { fill: C.card, line: C.border, bar: color });
  label(s, title, x + 0.15, y + 0.18, w - 0.3, 0.22, { size: 9.6, bold: true });
  body(s, text, x + 0.15, y + 0.52, w - 0.3, h - 0.65, { size: 8.2, color: C.muted });
}

let n = 1;

// 1 cover
{
  const s = pptx.addSlide();
  s.background = { color: C.bg };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: W, h: H, fill: { color: C.bg }, line: { color: C.bg } });
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: 4.35, h: H, fill: { color: C.sidebar }, line: { color: C.sidebar } });
  if (fs.existsSync(SPLASH)) {
    s.addImage({ path: SPLASH, x: 0.45, y: 0.45, w: 3.45, h: 2.45, transparency: 3 });
  }
  label(s, "ERP GRAIN CONTROL", 4.85, 1.10, 7.8, 0.55, { size: 30, bold: true });
  body(s, "Transformamos operaciones logísticas en decisiones estratégicas mediante inteligencia operativa, recuperación de pérdidas y gestión de riesgo en tiempo real.", 4.88, 1.84, 7.4, 0.78, { size: 15, color: C.text });
  box(s, 4.88, 3.12, 7.45, 1.10, { fill: C.card, line: C.border, bar: C.accent });
  body(s, "Somos su solución integral para la optimización estratégica de la cadena logística de sus importaciones.", 5.10, 3.38, 7.0, 0.46, { size: 13, bold: true });
  label(s, "Plataforma regional para operaciones portuarias, graneles, cuotas, QR, SOF, reportes e IA marítima.", 5.10, 3.93, 7.0, 0.18, { size: 8.8, color: C.muted });
  label(s, "“Lo que no se mide en campo, no se controla… y lo que no se controla, se pierde.”", 4.90, 5.05, 7.4, 0.35, { size: 13, bold: true, color: C.accent });
  label(s, "Presentación comercial | MSL", 4.90, 6.80, 3.2, 0.18, { size: 8, color: C.muted });
}

// 2
{
  const s = slide("El problema operativo", "El costo real no está solo en la descarga: está en lo que no se ve, no se mide o no se aprueba a tiempo.");
  callout(s, "Robo y riesgo en campo", "Camiones, guías y rutas sin validación digital elevan exposición operativa y reputacional.", 0.55, 1.55, 3.85, 1.35, C.danger);
  callout(s, "Errores documentales", "Papel, lápiz y transcripción manual crean diferencias de peso, clientes, placas y tiempos.", 4.75, 1.55, 3.85, 1.35, C.warn);
  callout(s, "Cuotas sin control vivo", "La operación puede seguir liberando viajes aunque el cliente ya haya cumplido su cuota.", 8.95, 1.55, 3.85, 1.35, C.info);
  box(s, 0.55, 3.35, 12.25, 2.55, { fill: C.card, line: C.border });
  label(s, "Cambio propuesto", 0.85, 3.62, 2.3, 0.25, { size: 13, bold: true });
  bulletList(s, [
    "De registro manual a trazabilidad QR con escaneos controlados por etapa.",
    "De cierre reactivo a alertas en tiempo real: sobrecuota, guía duplicada, salida sin ingreso, peso fuera de rango.",
    "De reportes tardíos a centro ejecutivo con KPI, bodega, cliente, producto, SOF y productividad.",
    "De información dispersa a una sola fuente de verdad por buque, operación y cliente."
  ], 0.90, 4.05, 6.05, 1.55, 11);
  ship(s, 7.35, 3.73, 4.95, 1.65, "Operación controlada por bodega", [100, 100, 100, 100, 100], "full");
  footer(s, n++);
}

// 3
{
  const s = slide("Qué es ERP GRAIN CONTROL", "Una plataforma operativa y ejecutiva para controlar graneles desde la apertura del buque hasta el informe final.");
  const items = [
    ["01", "Apertura de operación", "Buque, fecha, productos, bodegas, cuotas por cliente y reglas operativas."],
    ["02", "Control en campo", "QR, aprobación, escaneos, pesos, marchamos, evidencia y excepciones."],
    ["03", "Inteligencia ejecutiva", "KPIs, alertas, descarga por bodega, cuotas vs descargado e IA marítima."],
    ["04", "Reportería comercial", "PDF, Excel, CSV y Word por buque, cliente, producto, bodega o fecha."]
  ];
  items.forEach((it, i) => {
    const x = 0.55 + (i % 2) * 6.2;
    const y = 1.55 + Math.floor(i / 2) * 2.15;
    box(s, x, y, 5.85, 1.65, { fill: C.card, line: C.border, bar: [C.accent, C.ok, C.info, C.warn][i] });
    label(s, it[0], x + 0.22, y + 0.34, 0.62, 0.35, { size: 18, bold: true, color: [C.accent, C.ok, C.info, C.warn][i] });
    label(s, it[1], x + 1.0, y + 0.25, 4.55, 0.25, { size: 13, bold: true });
    body(s, it[2], x + 1.0, y + 0.67, 4.55, 0.55, { size: 9.2, color: C.muted });
  });
  label(s, "Resultado: menos pérdida, menos disputa, más velocidad de decisión y mejor defensa documental ante reclamos.", 0.62, 6.35, 11.9, 0.25, { size: 13, bold: true, color: C.accent, align: "center" });
  footer(s, n++);
}

// 4
{
  const s = slide("Oferta de servicio", "MSL combina plataforma, monitoreo, auditoría operativa y rediseño de procesos.");
  box(s, 0.55, 1.45, 5.9, 4.85, { fill: C.card, line: C.border, bar: C.accent });
  label(s, "Ofrecemos", 0.82, 1.77, 2.0, 0.35, { size: 17, bold: true });
  bulletList(s, [
    "Monitoreo continuo de operaciones logísticas y portuarias",
    "Sistema automatizado de gestión de operaciones",
    "Auditoría completa de procesos",
    "Rediseño de procesos",
    "Reducción de costos logísticos",
    "Planificación portuaria",
    "Alertas de riesgo: demoras y pérdidas",
    "Reportes mensuales y en tiempo real",
    "Análisis de performance portuario",
    "Gestión de reclamos ante aseguradoras",
  ], 0.90, 2.25, 5.25, 3.45, 8.2);
  box(s, 6.85, 1.45, 5.95, 2.05, { fill: C.card, line: C.border, bar: C.info });
  label(s, "Evolución regional", 7.12, 1.77, 3.8, 0.3, { size: 16, bold: true });
  body(s, "Tras 20 años en el mercado Latinoamericano, MSL ha evolucionado para convertirse en una plataforma regional de inteligencia logística y riesgo en comercio internacional.", 7.12, 2.20, 5.35, 0.82, { size: 11.2 });
  box(s, 6.85, 3.85, 5.95, 2.45, { fill: C.card, line: C.border, bar: C.ok });
  label(s, "Objetivo comercial", 7.12, 4.18, 3.8, 0.3, { size: 16, bold: true });
  body(s, "Entregar a la gerencia una visión completa de lo descargado, pendiente de descarga, riesgos, diferencias, reclamos y productividad, con evidencia suficiente para actuar y cobrar.", 7.12, 4.60, 5.35, 0.95, { size: 11.2 });
  footer(s, n++);
}

// 5 architecture
{
  const s = slide("Arquitectura funcional", "Cada módulo se conecta a una operación de buque para evitar mezclar datos históricos y operación activa.");
  const mods = [
    ["Operaciones de Buque", "Apertura, cierre, bodegas, productos y cuotas"],
    ["Aprobaciones", "Carga pendiente, aprobación, rechazo y comentario"],
    ["Carga de Boletas", "Template, QR, tabla, exportaciones y detalle"],
    ["SOF", "Eventos, demoras, bodegas, subcategorías y evidencia"],
    ["Centro Ejecutivo", "KPIs, alertas, gráficos, bodega y reportes"],
    ["Maritime IA", "Análisis, riesgos, tiempo estimado y chat operativo"],
  ];
  mods.forEach((m, i) => {
    const x = 0.68 + (i % 3) * 4.15;
    const y = 1.55 + Math.floor(i / 3) * 2.05;
    box(s, x, y, 3.72, 1.38, { fill: C.card, line: C.border, bar: [C.accent, C.ok, C.info, C.warn, C.danger, C.accent2][i] });
    label(s, m[0], x + 0.20, y + 0.24, 3.30, 0.25, { size: 11.5, bold: true });
    body(s, m[1], x + 0.20, y + 0.63, 3.30, 0.42, { size: 8.2, color: C.muted });
  });
  s.addShape(pptx.ShapeType.line, { x: 2.4, y: 4.95, w: 8.55, h: 0, line: { color: C.accent, width: 2, beginArrowType: "none", endArrowType: "triangle" } });
  label(s, "Base de datos por operación: no mezcla buques, clientes, cuotas ni historia operativa.", 1.22, 5.28, 10.9, 0.33, { size: 13, bold: true, align: "center", color: C.accent });
  footer(s, n++);
}

// 6 Centro Ejecutivo
{
  const s = slide("Centro Ejecutivo", "La vista gerencial une dashboard, control por bodega, cuotas vs descargado, alertas e informes.");
  metric(s, "Viajes", "413.00", 0.55, 1.45, 2.45, 1.20, C.accent);
  metric(s, "Peso descargado", "21,953.35", 3.25, 1.45, 2.45, 1.20, C.info, "MT");
  metric(s, "Pendiente de descarga", "31,058.23", 5.95, 1.45, 2.65, 1.20, C.warn, "MT");
  metric(s, "Avance", "41.42%", 8.85, 1.45, 2.20, 1.20, C.ok);
  metric(s, "Alertas", "7.00", 11.30, 1.45, 1.50, 1.20, C.danger);
  ship(s, 0.55, 3.00, 5.95, 2.10, "Silueta del buque: descarga por bodega", [74.10, 58.80, 43.25, 35.55, 18.40], "emptying");
  barChart(s, "Cuotas vs descargado", [["Nordgrain", 82], ["Baltic Mills", 61], ["Helvetia", 43], ["Aurum", 27]], 6.78, 3.00, 2.95, 2.10, 100, C.ok);
  lineChart(s, "Productividad diaria", [["D1", 12], ["D2", 18], ["D3", 15], ["D4", 23], ["D5", 28], ["D6", 31]], 9.95, 3.00, 2.85, 2.10, C.info);
  callout(s, "Lectura ejecutiva", "El usuario filtra por operación, empresa, bodega, cliente, producto y fecha. Los datos se generan solo al presionar el botón, reduciendo carga innecesaria del backend.", 0.55, 5.45, 12.25, 0.92, C.accent);
  footer(s, n++);
}

// 7 Operaciones de Buque
{
  const s = slide("Operaciones de Buque", "Apertura controlada: buque, fecha, productos, bodegas y cuotas sin mezclar operaciones.");
  uiWindow(s, 0.55, 1.45, 5.85, 4.95, "Nueva operación");
  label(s, "Buque", 0.85, 2.02, 1.0, 0.16, { size: 7.5, bold: true });
  box(s, 0.85, 2.22, 2.25, 0.25, { fill: "FFFFFF", line: C.border });
  label(s, "MV NUEVA TECH", 0.91, 2.27, 2.0, 0.11, { size: 6.8 });
  label(s, "Fecha inicio", 3.35, 2.02, 1.2, 0.16, { size: 7.5, bold: true });
  box(s, 3.35, 2.22, 2.15, 0.25, { fill: "FFFFFF", line: C.border });
  label(s, "4 de Mayo de 2026", 3.41, 2.27, 1.9, 0.11, { size: 6.8 });
  label(s, "Productos", 0.85, 2.74, 1.0, 0.16, { size: 7.5, bold: true });
  ["Maíz", "DDGS", "Frijol de Soya"].forEach((p, i) => { box(s, 0.85, 2.98 + i * 0.35, 4.65, 0.25, { fill: "FFFFFF", line: C.border }); label(s, p, 0.93, 3.03 + i * 0.35, 2.0, 0.11, { size: 6.8 }); });
  ship(s, 0.85, 4.08, 4.75, 1.45, "Bodegas declaradas", [100, 100, 100, 100, 100], "full");
  uiWindow(s, 6.70, 1.45, 6.10, 4.95, "Cuotas por cliente");
  tableMock(s, 7.05, 2.05, 5.42, 2.05, ["Cliente", "Cuota MT", "Unidad"], [
    ["Nordgrain GmbH", "8,000.00", "MT"],
    ["Baltic Mills", "7,500.00", "MT"],
    ["Helvetia Foods", "6,250.00", "MT"],
    ["Aurum Feed", "5,800.00", "MT"],
  ]);
  callout(s, "Control esperado", "Las cuotas se asignan a una operación específica. El sistema puede impedir QR si el cliente ya cumplió la cuota asignada.", 7.05, 4.58, 5.42, 0.94, C.warn);
  footer(s, n++);
}

// 8 QR and approvals
{
  const s = slide("Aprobaciones, boletas y QR", "El flujo evita cargar datos sobre una operación incorrecta y deja auditoría de cada acción.");
  uiWindow(s, 0.55, 1.45, 5.95, 4.90, "Aprobaciones");
  tableMock(s, 0.90, 2.00, 5.25, 2.10, ["Guía", "Cliente", "Producto", "Estado"], [
    ["07356", "Nordgrain", "Maíz", "PENDING"],
    ["07357", "Baltic", "DDGS", "PENDING"],
    ["07358", "Aurum", "Soya", "RECHAZADA"],
  ]);
  callout(s, "Supervisión", "Marcar todo, seleccionar guías, aprobar, rechazar y comentar. Cada acción queda asociada a usuario y estado.", 0.90, 4.55, 5.25, 0.82, C.accent);
  uiWindow(s, 6.88, 1.45, 5.92, 4.90, "Control QR");
  metric(s, "Escaneo 1", "Ingreso", 7.25, 2.02, 1.55, 0.95, C.info);
  metric(s, "Escaneo 2", "Tolva", 8.98, 2.02, 1.55, 0.95, C.warn);
  metric(s, "Escaneo 3", "Salida", 10.70, 2.02, 1.55, 0.95, C.ok);
  bulletList(s, [
    "QR sin pass hash visible para evitar falsificación.",
    "Código de verificación protegido en backend.",
    "Alertas por QR inválido, guía completa o cuota cumplida.",
    "Issue/SOF automático cuando ocurre excepción."
  ], 7.25, 3.35, 5.0, 1.25, 8.8);
  footer(s, n++);
}

// 9 SOF
{
  const s = slide("SOF: Statement of Facts", "Registro estructurado de eventos, demoras, causas, bodegas y trazabilidad del barco.");
  metric(s, "Eventos", "34.00", 0.55, 1.45, 2.4, 1.05, C.accent);
  metric(s, "Horas demora", "18.75", 3.15, 1.45, 2.4, 1.05, C.warn);
  metric(s, "Bodega crítica", "B3", 5.75, 1.45, 2.4, 1.05, C.danger);
  metric(s, "Impacto estimado", "4.20%", 8.35, 1.45, 2.4, 1.05, C.info);
  donutLegend(s, "Categorías de demora", [["Grúa", 32], ["Clima", 24], ["Camiones", 18], ["Bodega", 16], ["Otros", 10]], 0.55, 2.95, 3.95, 2.25);
  barChart(s, "Demoras por bodega", [["B1", 3.2], ["B2", 4.8], ["B3", 7.6], ["B4", 2.1], ["B5", 1.0]], 4.80, 2.95, 3.95, 2.25, 8, C.warn);
  tableMock(s, 9.05, 2.95, 3.75, 2.25, ["Fecha", "Hora", "Evento"], [
    ["04 May", "08:40", "Fallo grúa"],
    ["04 May", "11:15", "Apertura bodega"],
    ["05 May", "15:30", "Clima"],
    ["05 May", "18:20", "Camiones"],
  ]);
  callout(s, "Valor", "El SOF deja de ser una bitácora plana y se convierte en evidencia cuantificable para reclamos, productividad y negociación.", 0.55, 5.65, 12.25, 0.62, C.accent);
  footer(s, n++);
}

// 10 Reports
{
  const s = slide("Informes descargables", "Cada tipo de informe tiene estructura propia: no todos responden a la misma pregunta.");
  const reports = [
    ["Resumen ejecutivo por buque", "KPIs, tendencias, bodega, productividad, alertas y lectura gerencial."],
    ["SOF", "Duraciones, categorías, subcategorías, bodega afectada, timeline y evidencia."],
    ["Cuotas vs descargado", "Cliente, producto, cuota, descargado, pendiente de descarga, avance y sobrecuota."],
    ["Descarga por bodega", "Capacidad inicial, descargado, pendiente, porcentaje y ritmo por bodega."],
    ["Alertas operativas", "Incidentes, severidad, fecha, recurrencia, impacto y estado de resolución."],
    ["Productividad por camión", "Tiempo ingreso-salida, pesos, viajes, outliers y ranking operativo."],
  ];
  reports.forEach((r, i) => {
    const x = 0.55 + (i % 2) * 6.18;
    const y = 1.48 + Math.floor(i / 2) * 1.57;
    callout(s, r[0], r[1], x, y, 5.78, 1.18, [C.accent, C.info, C.ok, C.warn, C.danger, C.accent2][i]);
  });
  label(s, "Formatos: PDF, Excel, CSV y Word con gráficos, tarjetas KPI y tablas según el tipo de reporte.", 0.62, 6.43, 12.0, 0.22, { size: 12.5, bold: true, color: C.accent, align: "center" });
  footer(s, n++);
}

// 11 Maritime IA
{
  const s = slide("Maritime IA", "Asistente ejecutivo para convertir datos operativos en diagnóstico, riesgo y recomendación.");
  uiWindow(s, 0.55, 1.45, 12.25, 4.85, "Maritime IA");
  box(s, 0.95, 2.05, 3.25, 0.42, { fill: "FFFFFF", line: C.border });
  label(s, "1 | MV NUEVA TECH | ABIERTA", 1.08, 2.17, 2.65, 0.11, { size: 7.2 });
  box(s, 4.45, 2.05, 2.35, 0.42, { fill: "FFFFFF", line: C.border });
  label(s, "Tiempo estimado", 4.58, 2.17, 1.70, 0.11, { size: 7.2 });
  box(s, 7.05, 2.05, 1.65, 0.42, { fill: C.accent, line: C.accent });
  label(s, "Generar análisis", 7.20, 2.18, 1.25, 0.11, { size: 7.2, bold: true, color: C.white, align: "center" });
  callout(s, "Preguntas que responde", "¿Cuánto falta para terminar? ¿Qué cliente va atrasado? ¿Qué bodega requiere atención? ¿Qué riesgo operativo existe hoy? ¿Qué demoras explican la pérdida de productividad?", 0.95, 2.95, 5.55, 1.50, C.info);
  callout(s, "Salida esperada", "Resumen ejecutivo, hallazgos, riesgos priorizados, recomendación accionable, tiempo estimado y soporte con datos de la operación.", 6.82, 2.95, 5.55, 1.50, C.ok);
  label(s, "La IA no sustituye el control operativo: acelera lectura, priorización y preparación de decisiones.", 1.05, 5.35, 11.1, 0.24, { size: 12.5, bold: true, color: C.accent, align: "center" });
  footer(s, n++);
}

// 12 Mobile
{
  const s = slide("App móvil y HandHeld", "La operación de campo se mueve al dispositivo: QR, roles, aprobaciones, cliente y evidencia.");
  box(s, 0.70, 1.45, 3.05, 4.90, { fill: "FFFFFF", line: C.border, shadow: true });
  s.addShape(pptx.ShapeType.roundRect, { x: 0.95, y: 1.75, w: 2.55, h: 4.30, rectRadius: 0.1, fill: { color: "F5F4EF" }, line: { color: C.text, width: 1.2 } });
  label(s, "ERP GRAIN CONTROL", 1.15, 2.05, 2.1, 0.20, { size: 8.5, bold: true, align: "center" });
  ["Dashboard", "QR", "SOF", "Informes", "Maritime IA"].forEach((v, i) => {
    box(s, 1.18, 2.55 + i * 0.55, 2.1, 0.32, { fill: i === 1 ? C.accent : "FFFFFF", line: C.border });
    label(s, v, 1.30, 2.64 + i * 0.55, 1.8, 0.09, { size: 6.7, bold: i === 1, color: i === 1 ? C.white : C.text, align: "center" });
  });
  const cap = [
    ["Supervisor", "Aprueba, rechaza, consulta KPIs y reportes."],
    ["Operador de patio", "Solo lector QR y captura operativa autorizada."],
    ["Cliente", "Visualiza cuotas, descargado, pendiente e informes."],
    ["HandHeld", "Renting recomendado para operación robusta en campo."],
  ];
  cap.forEach((c, i) => callout(s, c[0], c[1], 4.20 + (i % 2) * 4.25, 1.65 + Math.floor(i / 2) * 2.05, 3.75, 1.35, [C.accent, C.info, C.ok, C.warn][i]));
  footer(s, n++);
}

// 13 Pricing
{
  const s = slide("Modelo comercial", "Fee mensual claro, servidores y licencias incluidos por MSL.");
  metric(s, "1 país", "USD 5,000.00", 0.75, 1.60, 3.65, 1.45, C.accent, "mensuales + renting HandHeld + IVA");
  metric(s, "6 países", "USD 1,500.00", 4.82, 1.60, 3.65, 1.45, C.ok, "por país + renting HandHeld + IVA");
  metric(s, "Infraestructura", "Incluida", 8.88, 1.60, 3.65, 1.45, C.info, "servidores y licencias sin adicional");
  box(s, 0.75, 3.65, 11.78, 1.72, { fill: C.card, line: C.border, bar: C.warn });
  label(s, "Notas comerciales", 1.05, 3.95, 2.5, 0.25, { size: 14, bold: true });
  bulletList(s, [
    "El costo puede variar según nuevos requerimientos, integraciones, volumen operativo, automatizaciones especiales o alcance regional.",
    "El fee mensual cubre plataforma, evolución del sistema, soporte funcional y disponibilidad de la solución.",
    "HandHeld se cotiza como renting según cantidad de dispositivos, país y condiciones de operación."
  ], 1.08, 4.38, 10.90, 0.64, 9);
  label(s, "Propuesta diseñada para escalar sin comprar servidores ni licencias adicionales.", 0.82, 6.08, 11.55, 0.25, { size: 13, bold: true, color: C.accent, align: "center" });
  footer(s, n++);
}

// 14 Roadmap
{
  const s = slide("Evolución recomendada", "La plataforma puede crecer hacia rentabilidad, reclamos, portal cliente y analítica avanzada.");
  const road = [
    ["Fase 1", "Control operativo", "Buques, cuotas, QR, aprobaciones, SOF e informes."],
    ["Fase 2", "Riesgo y reclamos", "Alertas de pérdida, demoras, evidencia y expediente asegurador."],
    ["Fase 3", "Finanzas", "Costo por tonelada, margen, productividad diaria y diferencias."],
    ["Fase 4", "Portal cliente", "Cuotas, descargado, pendiente e informes por cliente."],
  ];
  road.forEach((r, i) => {
    const x = 0.85 + i * 3.10;
    box(s, x, 1.75, 2.62, 3.25, { fill: C.card, line: C.border, bar: [C.accent, C.info, C.warn, C.ok][i] });
    label(s, r[0], x + 0.2, 2.05, 2.2, 0.22, { size: 11, bold: true, color: [C.accent, C.info, C.warn, C.ok][i] });
    label(s, r[1], x + 0.2, 2.42, 2.2, 0.30, { size: 13, bold: true });
    body(s, r[2], x + 0.2, 2.95, 2.18, 0.90, { size: 8.4, color: C.muted });
    if (i < 3) s.addShape(pptx.ShapeType.line, { x: x + 2.65, y: 3.35, w: 0.40, h: 0, line: { color: C.accent, width: 1.5, endArrowType: "triangle" } });
  });
  label(s, "La inversión inicial se convierte en una plataforma de inteligencia logística regional, no en una herramienta aislada.", 0.80, 5.88, 11.75, 0.30, { size: 13, bold: true, color: C.accent, align: "center" });
  footer(s, n++);
}

// 15 Closing
{
  const s = pptx.addSlide();
  s.background = { color: C.sidebar };
  s.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: W, h: H, fill: { color: C.sidebar }, line: { color: C.sidebar } });
  label(s, "ERP GRAIN CONTROL", 0.75, 0.80, 7.5, 0.48, { size: 28, bold: true, color: C.white });
  body(s, "Una plataforma para medir el campo, controlar la operación y convertir cada buque en una decisión estratégica.", 0.78, 1.65, 7.2, 0.70, { size: 17, color: C.white });
  box(s, 0.78, 3.05, 6.80, 1.25, { fill: C.card, line: C.card });
  body(s, "“Lo que no se mide en campo, no se controla… y lo que no se controla, se pierde.”", 1.05, 3.42, 6.25, 0.40, { size: 16, bold: true, color: C.accent });
  ship(s, 8.15, 1.25, 4.30, 3.10, "De granel a control ejecutivo", [100, 82, 61, 43, 24], "emptying");
  label(s, "MSL | Plataforma regional de inteligencia logística y riesgo en comercio internacional", 0.80, 6.75, 7.4, 0.18, { size: 8.5, color: "E6E6E6" });
}

pptx.writeFile({ fileName: OUT });
