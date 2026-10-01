from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image as RLImage,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
OUT = ROOT / "Entregables"
OUT.mkdir(exist_ok=True)
IMG_DIR = OUT / "lss_mbb_assets"
IMG_DIR.mkdir(exist_ok=True)

PDF_PATH = OUT / "XTRAVON_ONE_Estudio_LSS_Master_Black_Belt.pdf"

NAVY = "#081324"
ATLANTIC = "#0B1E3A"
CYAN = "#00E5FF"
COMMAND = "#0066FF"
MINT = "#2BD4A7"
AMBER = "#FFB21F"
RISK = "#FF4F7A"
WHITE = "#F5F7FA"
STEEL = "#C7CDD6"
INK = "#111827"
MUTED = "#4B5563"
LINE = "#D9E2EC"
LIGHT = "#F8FAFC"


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/aptos.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    bold_candidates = [
        "C:/Windows/Fonts/aptosbd.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]
    for path in (bold_candidates if bold else candidates):
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def make_cover() -> Path:
    path = IMG_DIR / "lss_cover.png"
    w, h = 1800, 1050
    img = Image.new("RGB", (w, h), NAVY)
    draw = ImageDraw.Draw(img)

    for x in range(0, w, 78):
        draw.line((x, 0, x - 280, h), fill="#0C223B", width=1)
    for y in range(0, h, 76):
        draw.line((0, y, w, y), fill="#0C223B", width=1)

    logo_path = ASSETS / "xtravon_splash.png"
    if not logo_path.exists():
        logo_path = ASSETS / "XTRAVON_seal_round_transparent.png"
    logo = Image.open(logo_path).convert("RGBA")
    logo.thumbnail((590, 470))
    img.paste(logo, (85, 85), logo)

    draw.text((720, 105), "XTRAVON ONE", font=font(74, True), fill=WHITE)
    draw.text((724, 196), "ESTUDIO LSS MASTER BLACK BELT", font=font(43, True), fill=CYAN)
    draw.text((724, 260), "Analisis DMAIC, CTQ, desperdicios, riesgos, control operacional y mejora continua", font=font(25), fill=STEEL)

    bullets = [
        "Control de flujo end-to-end por buque, guia, chofer, cliente y bodega",
        "Reduccion de defectos documentales, reprocesos y riesgo de perdida",
        "Modelo de control con indicadores, alertas y trazabilidad auditable",
        "Hoja de ruta para pilotaje, estabilizacion y escalamiento regional",
    ]
    y = 385
    for item in bullets:
        draw.ellipse((730, y + 8, 750, y + 28), fill=CYAN)
        draw.text((770, y), item, font=font(27, True), fill=WHITE)
        y += 68

    cards = [
        ("DEFINE", "Problema, VOC, CTQ"),
        ("MEASURE", "Baselines y defectos"),
        ("ANALYZE", "Causas y modos de falla"),
        ("IMPROVE", "Flujo digital y controles"),
        ("CONTROL", "KPIs, auditoria y SOP"),
    ]
    x0, y0 = 120, 790
    for i, (title, desc) in enumerate(cards):
        x = x0 + i * 325
        draw.rounded_rectangle((x, y0, x + 280, y0 + 110), radius=18, fill=ATLANTIC, outline=CYAN, width=3)
        draw.text((x + 22, y0 + 22), title, font=font(27, True), fill=CYAN)
        draw.text((x + 22, y0 + 65), desc, font=font(18), fill=STEEL)

    draw.text((100, 980), f"QORA SYSTEMS - MSL | Fecha: {datetime.now().strftime('%d/%m/%Y')}", font=font(20, True), fill=STEEL)
    img.save(path)
    return path


def make_dmaic_timeline() -> Path:
    path = IMG_DIR / "dmaic_timeline.png"
    w, h = 1500, 540
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.text((45, 30), "Roadmap DMAIC para XTRAVON ONE", font=font(42, True), fill=INK)
    draw.text((45, 82), "De control inicial a sistema operacional robusto, medible y escalable.", font=font(23), fill=MUTED)
    phases = [
        ("DEFINE", "Alcance por buque\nVOC / CTQ\nRoles"),
        ("MEASURE", "Baseline viajes\nErrores doc.\nTiempos puerto"),
        ("ANALYZE", "Causas raiz\nRiesgo QR\nCuotas vs real"),
        ("IMPROVE", "Despacho digital\nOffline handheld\nSOF estandar"),
        ("CONTROL", "KPIs diarios\nAuditoria\nControl plan"),
    ]
    x0, y0 = 85, 180
    for i, (title, desc) in enumerate(phases):
        x = x0 + i * 280
        color = [CYAN, COMMAND, MINT, AMBER, RISK][i]
        draw.rounded_rectangle((x, y0, x + 230, y0 + 210), radius=18, fill=ATLANTIC, outline=color, width=4)
        draw.rectangle((x, y0, x + 230, y0 + 18), fill=color)
        draw.text((x + 25, y0 + 38), title, font=font(27, True), fill=WHITE)
        yy = y0 + 86
        for line in desc.split("\n"):
            draw.text((x + 25, yy), line, font=font(20), fill=STEEL)
            yy += 32
        if i < len(phases) - 1:
            draw.line((x + 236, y0 + 105, x + 270, y0 + 105), fill=CYAN, width=4)
            draw.polygon([(x + 270, y0 + 105), (x + 255, y0 + 95), (x + 255, y0 + 115)], fill=CYAN)
    img.save(path)
    return path


def make_value_stream() -> Path:
    path = IMG_DIR / "value_stream.png"
    w, h = 1700, 760
    img = Image.new("RGB", (w, h), NAVY)
    draw = ImageDraw.Draw(img)
    draw.text((55, 35), "Value Stream operativo: graneles / QR / despacho", font=font(44, True), fill=WHITE)
    draw.text((55, 92), "Lectura MBB: separar flujo esencial, puntos de defecto y controles automatizados.", font=font(24), fill=STEEL)
    steps = [
        ("1", "Apertura\nbuque", "Plan, bodegas,\nproductos"),
        ("2", "Cuotas\ncliente", "CTQ: cuota,\nproducto, bodega"),
        ("3", "Carga\nguias", "Datos chofer,\nplaca, cliente"),
        ("4", "Despacho\nQR", "Asignacion\ncontrolada"),
        ("5", "Patio\nescaneos", "Ingreso, tolva,\nsalida"),
        ("6", "SOF / eventos", "Demoras,\nclima, riesgo"),
        ("7", "Cierre\nreporte", "Dif., cuotas,\nalertas"),
    ]
    x0, y0 = 55, 210
    for i, (num, title, desc) in enumerate(steps):
        x = x0 + i * 235
        draw.rounded_rectangle((x, y0, x + 190, y0 + 170), radius=16, fill=ATLANTIC, outline=CYAN, width=3)
        draw.ellipse((x + 16, y0 + 18, x + 58, y0 + 60), fill=MINT)
        draw.text((x + 30, y0 + 25), num, font=font(20, True), fill=NAVY)
        draw.text((x + 72, y0 + 22), title, font=font(24, True), fill=WHITE)
        yy = y0 + 92
        for line in desc.split("\n"):
            draw.text((x + 22, yy), line, font=font(18), fill=STEEL)
            yy += 26
        if i < len(steps) - 1:
            draw.line((x + 195, y0 + 85, x + 225, y0 + 85), fill=MINT, width=4)
            draw.polygon([(x + 225, y0 + 85), (x + 210, y0 + 75), (x + 210, y0 + 95)], fill=MINT)

    wastes = [
        ("Espera", "Camiones sin QR / sin asignacion"),
        ("Reproceso", "Guias corregidas manualmente"),
        ("Defecto", "Cliente, placa o peso mal digitado"),
        ("Movimiento", "Papel, llamadas y WhatsApps fuera de control"),
        ("Sobreproceso", "QR creados sin despacho confirmado"),
    ]
    draw.rounded_rectangle((75, 475, 1625, 690), radius=20, outline=AMBER, width=3, fill="#07101F")
    draw.text((105, 500), "Desperdicios Lean detectados y controlables", font=font(27, True), fill=AMBER)
    x = 105
    for title, desc in wastes:
        draw.rounded_rectangle((x, 555, x + 280, 655), radius=12, fill=ATLANTIC, outline=AMBER, width=2)
        draw.text((x + 16, 573), title, font=font(20, True), fill=WHITE)
        draw.text((x + 16, 607), desc, font=font(15), fill=STEEL)
        x += 300
    img.save(path)
    return path


def make_fmea_chart() -> Path:
    path = IMG_DIR / "fmea_chart.png"
    w, h = 1500, 660
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.text((55, 40), "FMEA operacional: RPN antes vs controlado", font=font(40, True), fill=INK)
    draw.text((55, 90), "Los valores son estimativos para priorizacion inicial; deben calibrarse con datos reales del piloto.", font=font(22), fill=MUTED)
    modes = [
        ("QR falso", 280, 80),
        ("Guia duplicada", 210, 70),
        ("Sobrecuota", 240, 95),
        ("Peso fuera rango", 180, 85),
        ("Sin senal patio", 220, 105),
        ("Error documental", 260, 90),
    ]
    left, top = 330, 170
    maxv = 300
    for i, (label, before, after) in enumerate(modes):
        y = top + i * 70
        draw.text((55, y + 10), label, font=font(22, True), fill=INK)
        draw.rounded_rectangle((left, y, left + 900, y + 28), radius=8, fill="#E5E7EB")
        draw.rounded_rectangle((left, y, left + int(900 * before / maxv), y + 28), radius=8, fill=RISK)
        draw.rounded_rectangle((left, y + 32, left + int(900 * after / maxv), y + 58), radius=8, fill=MINT)
        draw.text((left + int(900 * before / maxv) + 10, y - 1), str(before), font=font(18, True), fill=RISK)
        draw.text((left + int(900 * after / maxv) + 10, y + 31), str(after), font=font(18, True), fill=MINT)
    draw.rectangle((1110, 95, 1140, 120), fill=RISK)
    draw.text((1150, 94), "RPN antes", font=font(19, True), fill=INK)
    draw.rectangle((1280, 95, 1310, 120), fill=MINT)
    draw.text((1320, 94), "RPN controlado", font=font(19, True), fill=INK)
    img.save(path)
    return path


def make_control_dashboard() -> Path:
    path = IMG_DIR / "control_dashboard.png"
    w, h = 1500, 720
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)
    draw.text((55, 40), "Control Plan: tablero LSS recomendado", font=font(40, True), fill=INK)
    cards = [
        ("FTQ documental", ">= 99.50%", "Defectos / guia"),
        ("Tiempo ciclo camion", "P50 / P90", "Ingreso a salida"),
        ("Sobrecuota", "0 eventos", "Cliente/producto/buque"),
        ("QR invalido", "0 criticos", "Seguridad"),
        ("Sync offline", "< 15 min", "Recuperacion senal"),
        ("SOF cierre", "100%", "Eventos auditados"),
    ]
    x0, y0 = 65, 125
    for i, (title, target, desc) in enumerate(cards):
        x = x0 + (i % 3) * 465
        y = y0 + (i // 3) * 190
        color = [CYAN, COMMAND, MINT, AMBER, RISK, CYAN][i]
        draw.rounded_rectangle((x, y, x + 410, y + 145), radius=16, fill=ATLANTIC, outline=color, width=4)
        draw.rectangle((x, y, x + 410, y + 14), fill=color)
        draw.text((x + 24, y + 34), title, font=font(27, True), fill=WHITE)
        draw.text((x + 24, y + 78), target, font=font(32, True), fill=color)
        draw.text((x + 24, y + 118), desc, font=font(18), fill=STEEL)
    draw.rounded_rectangle((65, 535, 1430, 660), radius=18, fill=LIGHT, outline=LINE)
    draw.text((95, 562), "Regla MBB:", font=font(25, True), fill=INK)
    draw.text((250, 562), "todo indicador debe tener dueno, frecuencia, fuente de datos, limite de control y accion de reaccion.", font=font(24), fill=MUTED)
    draw.text((95, 608), "Sin plan de reaccion, un KPI es decoracion. Con plan de reaccion, el ERP se vuelve sistema de control.", font=font(23, True), fill=INK)
    img.save(path)
    return path


def p(text, style):
    return Paragraph(text, style)


def make_table(data, widths, font_size=7.5, header=True):
    wrapped = []
    for row in data:
        wrapped.append([Paragraph(str(cell), ParagraphStyle("cell", fontName="Helvetica", fontSize=font_size, leading=font_size + 2, textColor=colors.HexColor(INK))) for cell in row])
    t = Table(wrapped, colWidths=widths, repeatRows=1 if header else 0)
    ts = [
        ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor(LINE)),
        ("INNERGRID", (0, 0), (-1, -1), 0.35, colors.HexColor(LINE)),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        ts.extend([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(NAVY)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ])
    for r in range(1 if header else 0, len(data)):
        ts.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#FFFFFF" if r % 2 else "#F8FAFC")))
    t.setStyle(TableStyle(ts))
    return t


def build_pdf():
    cover = make_cover()
    dmaic = make_dmaic_timeline()
    vsm = make_value_stream()
    fmea = make_fmea_chart()
    control = make_control_dashboard()
    flowchart = OUT / "XTRAVON_ONE_Flowchart_End_to_End_ES.jpg"

    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=letter,
        rightMargin=0.55 * inch,
        leftMargin=0.55 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.5 * inch,
        title="XTRAVON ONE - Estudio LSS Master Black Belt",
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TitleX", fontName="Helvetica-Bold", fontSize=23, leading=27, textColor=colors.HexColor(NAVY), spaceAfter=8))
    styles.add(ParagraphStyle("H1X", fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=colors.HexColor(NAVY), spaceBefore=8, spaceAfter=5))
    styles.add(ParagraphStyle("BodyX", fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor(INK), spaceAfter=5))
    styles.add(ParagraphStyle("SmallX", fontName="Helvetica", fontSize=7.5, leading=10, textColor=colors.HexColor(MUTED), spaceAfter=4))
    styles.add(ParagraphStyle("CenterX", fontName="Helvetica-Bold", fontSize=10, leading=12, alignment=TA_CENTER, textColor=colors.HexColor(NAVY)))

    story = []
    story.append(RLImage(str(cover), width=7.35 * inch, height=4.28 * inch))
    story.append(Spacer(1, 0.16 * inch))
    story.append(p("Dictamen Master Black Belt", styles["H1X"]))
    story.append(p(
        "XTRAVON ONE no debe evaluarse como un software aislado, sino como un sistema de control de proceso para operaciones portuarias de graneles. "
        "El objetivo LSS es reducir variacion, defectos, espera, reproceso y perdida de trazabilidad desde apertura del buque hasta cierre e informe.",
        styles["BodyX"],
    ))
    story.append(PageBreak())

    story.append(p("1. Resumen Ejecutivo LSS", styles["TitleX"]))
    story.append(p(
        "Desde la mirada de un LSS Master Black Belt, el sistema resuelve un problema operacional de alto costo: operaciones con datos dispersos, papel, baja visibilidad, "
        "riesgo de robo/error documental y poca capacidad para medir la descarga real contra cuotas, bodegas y tiempos. La oportunidad no es solo digitalizar: es convertir "
        "la operacion en un flujo medible, controlado y auditable.",
        styles["BodyX"],
    ))
    story.append(make_table([
        ["Elemento", "Lectura MBB", "Implicacion"],
        ["Y del proceso", "Descarga correcta, segura y trazable por buque/cliente/producto/bodega.", "Debe medirse diariamente, no al cierre."],
        ["Defecto critico", "Guia incorrecta, QR no valido, sobrecuota, peso anomalo, salida sin ingreso.", "Requiere alarma y bloqueo operativo."],
        ["Unidad de flujo", "Guia/viaje/camion.", "Permite calcular ciclo, capacidad, promedio y variacion."],
        ["Cliente del proceso", "Cliente importador, despacho, patio, gerencia, auditoria.", "Cada uno tiene CTQ distinto."],
        ["Condicion de exito", "Menos reproceso, menos tiempos muertos, trazabilidad completa y cierre rapido.", "El ERP debe actuar como control plan."],
    ], [1.35 * inch, 3.4 * inch, 2.5 * inch]))
    story.append(RLImage(str(dmaic), width=7.2 * inch, height=2.6 * inch))
    story.append(PageBreak())

    story.append(p("2. SIPOC y CTQ", styles["TitleX"]))
    story.append(p("El SIPOC evidencia que los principales riesgos nacen antes del patio: mala apertura, cuota mal definida, plantilla mal cargada o guia sin asignacion correcta.", styles["BodyX"]))
    story.append(make_table([
        ["S", "I", "P", "O", "C"],
        ["Cliente/importador, naviera, terminal, despacho, patio", "Stowage plan, cuotas, choferes, placas, guias, productos", "Apertura, carga, despacho, escaneo, cierre", "QR valido, viaje trazado, tonelaje descargado, SOF, informe", "Gerencia, cliente, auditoria, aseguradora"],
    ], [1.35 * inch, 1.55 * inch, 1.55 * inch, 1.55 * inch, 1.25 * inch], font_size=7.2))
    story.append(Spacer(1, 0.1 * inch))
    story.append(make_table([
        ["CTQ", "Medicion", "Meta sugerida", "Reaccion si falla"],
        ["Exactitud documental", "Guias sin correccion / total guias", ">= 99.5%", "Bloquear lote y abrir causa raiz."],
        ["QR seguro", "QR invalido / lecturas", "0 criticos", "Issue log automatico + bloqueo de placa/guia."],
        ["Ciclo camion", "Minutos ingreso-salida P50/P90", "Por baseline del puerto", "Investigar SOF/demora si excede limite."],
        ["Cuota vs descargado", "MT descargado vs cuota cliente", "0 sobrecuota", "Bloqueo preventivo de nuevos QR."],
        ["Offline sync", "Eventos sincronizados / eventos offline", "100%", "Reintento y alerta si > 15 min sin sincronizar."],
        ["Cierre operativo", "Operacion con reporte completo", "100%", "No archivar sin validacion de diferencias."],
    ], [1.55 * inch, 2.15 * inch, 1.35 * inch, 2.2 * inch]))
    story.append(PageBreak())

    story.append(p("3. Value Stream y desperdicios Lean", styles["TitleX"]))
    story.append(RLImage(str(vsm), width=7.25 * inch, height=3.25 * inch))
    story.append(Spacer(1, 0.1 * inch))
    story.append(make_table([
        ["Desperdicio", "Manifestacion en puerto", "Control XTRAVON"],
        ["Espera", "Camion esperando guia, QR o autorizacion.", "Despacho de viajes, QR activo por asignacion, solicitudes visibles."],
        ["Defecto", "Guia duplicada, placa incorrecta, peso fuera de rango.", "Validaciones, alarmas y issue log automatico."],
        ["Reproceso", "Correcciones manuales y llamadas posteriores.", "Aprobaciones, reasignacion, auditoria y versionado."],
        ["Movimiento", "Papel, busqueda de documentos, traslados innecesarios.", "Template, QR, app chofer y handheld."],
        ["Sobreproduccion", "QR generados sin necesidad real.", "Despacho confirma ciclo y continuidad."],
    ], [1.35 * inch, 3.0 * inch, 2.9 * inch]))
    story.append(PageBreak())

    story.append(p("4. Analisis de causa raiz", styles["TitleX"]))
    story.append(p(
        "El sistema ataca varias causas raiz clasicas: ausencia de fuente unica de verdad, baja segregacion de roles, poca visibilidad en tiempo real, falta de cierre documental y controles reactivos. "
        "La mejora clave es que cada guia sea tratada como unidad transaccional controlada.",
        styles["BodyX"],
    ))
    story.append(make_table([
        ["Problema", "Causa probable", "Control actual", "Brecha restante"],
        ["Robo o uso indebido de QR", "QR visible o compartible fuera del flujo.", "Pass hatch, firma, despacho y QR activo.", "Reforzar binding por dispositivo/chofer y auditoria de geolocalizacion."],
        ["Sobrecuota", "No se descuenta en tiempo real.", "Centro ejecutivo y cuotas vs descargado.", "Bloqueo automatico fino por cliente/producto/bodega."],
        ["Error de peso", "Captura manual o fuera de tolerancia.", "Peso vacio/lleno y alertas.", "Definir limites de control por producto/vehiculo."],
        ["Demoras no explicadas", "SOF tardio o incompleto.", "SOF offline y categorias.", "Analisis de Pareto mensual por causa/dueno."],
        ["Caida de red", "Operador depende de backend online.", "Cache offline + sync.", "Prueba de estres en handheld real."],
    ], [1.4 * inch, 2.0 * inch, 2.05 * inch, 1.8 * inch]))
    story.append(RLImage(str(fmea), width=7.2 * inch, height=3.1 * inch))
    story.append(PageBreak())

    story.append(p("5. FMEA y priorizacion", styles["TitleX"]))
    story.append(p("La tabla FMEA inicial debe usarse como instrumento vivo. La recomendacion MBB es recalcular RPN semanalmente durante el piloto con datos reales.", styles["BodyX"]))
    story.append(make_table([
        ["Modo de falla", "Severidad", "Ocurrencia", "Deteccion", "RPN inicial", "Accion recomendada"],
        ["QR falso o compartido", "10", "4", "7", "280", "Firma por dispositivo, QR activo y bloqueo por estado."],
        ["Guia duplicada", "8", "5", "5", "200", "Constraint DB + alerta en carga Excel."],
        ["Sobrecuota cliente", "9", "4", "6", "216", "Bloqueo preventivo al alcanzar cuota."],
        ["Peso fuera de rango", "7", "5", "5", "175", "Limites por producto/camion y excepcion aprobada."],
        ["Offline no sincroniza", "8", "4", "6", "192", "Cola local, reintento 15s, alerta y dashboard sync."],
        ["SOF incompleto", "6", "6", "5", "180", "Campos obligatorios por categoria y cierre controlado."],
    ], [1.45 * inch, 0.65 * inch, 0.75 * inch, 0.65 * inch, 0.75 * inch, 3.0 * inch], font_size=7.1))
    story.append(PageBreak())

    story.append(p("6. Control Plan recomendado", styles["TitleX"]))
    story.append(RLImage(str(control), width=7.2 * inch, height=3.45 * inch))
    story.append(make_table([
        ["Indicador", "Fuente", "Frecuencia", "Dueno", "Accion de reaccion"],
        ["FTQ documental", "Carga boletas / aprobaciones", "Diario", "Supervisor", "Retener lote y corregir causa raiz."],
        ["Ciclo camion P90", "Lecturas QR", "Turno", "Patio", "Abrir SOF si excede limite."],
        ["Pendiente por bodega", "Centro ejecutivo", "Turno", "Gerencia", "Ajustar despacho/producto."],
        ["Eventos offline pendientes", "Handheld sync", "15 min", "TI/Patio", "Reintento y verificacion de senal."],
        ["Sobrecuota", "Cuotas vs descargado", "Tiempo real", "Despacho", "Bloquear nuevos QR del cliente/producto."],
        ["QR invalido", "Scanner", "Tiempo real", "Patio", "Alerta roja + SOF + bloqueo."],
    ], [1.35 * inch, 1.55 * inch, 0.8 * inch, 0.8 * inch, 2.75 * inch], font_size=7.2))
    story.append(PageBreak())

    story.append(p("7. Evaluacion del sistema por modulo", styles["TitleX"]))
    modules = [
        ["Operaciones Buque", "Esencial", "Define alcance, productos, bodegas y cuotas.", "Agregar versionado de stowage plan y cambios aprobados."],
        ["Carga Boletas", "Esencial", "Crea base transaccional de guias.", "Validacion mas fuerte de duplicados, formato y operacion activa."],
        ["Despacho Viajes", "Esencial", "Controla QR activo y continuidad.", "Hacer Pareto de reasignaciones y causas."],
        ["Lector QR Patio", "Esencial", "Captura estados y pesos.", "Prueba offline en campo y limites estadisticos por peso."],
        ["SOF", "Esencial/soporte", "Documenta causas de variacion.", "Catalogo estandar y Pareto automatico."],
        ["Centro Ejecutivo", "Complementario fuerte", "Visibilidad y decisiones.", "Agregar control charts P50/P90 y SPC."],
        ["Informes", "Complementario", "Cierre, evidencia y reclamos.", "Versionar reportes y aprobacion final."],
        ["PORTIA", "Complementario", "Asistente operacional.", "Respuestas mas cortas, cache y modo control room."],
        ["Q&A", "Complementario", "Reduce curva de aprendizaje.", "Vincular manual a pantalla actual."],
    ]
    story.append(make_table([["Modulo", "Rol LSS", "Valor", "Mejora MBB"]] + modules, [1.35 * inch, 1.15 * inch, 2.25 * inch, 2.5 * inch], font_size=7.2))
    story.append(PageBreak())

    story.append(p("8. Beneficio economico potencial", styles["TitleX"]))
    story.append(p(
        "Sin datos reales de baseline, el estudio no debe prometer ahorro exacto. Aun asi, se puede estimar el potencial por categorias de perdida: demoras, reprocesos, reclamos, diferencias de peso, sobrecuotas y robo/uso indebido.",
        styles["BodyX"],
    ))
    story.append(make_table([
        ["Categoria", "Driver de ahorro", "Formula sugerida"],
        ["Demoras", "Horas evitadas por mejor despacho/SOF", "Horas reducidas x costo hora puerto/camion"],
        ["Errores documentales", "Guias corregidas evitadas", "Defectos evitados x costo reproceso"],
        ["Diferencias de carga", "MT recuperadas o justificadas", "MT x valor producto o reclamo"],
        ["Sobrecuota", "MT bloqueadas antes de salida", "MT no autorizadas x valor/penalidad"],
        ["Reclamos", "Evidencia oportuna para aseguradora", "Monto recuperado - costo documental"],
        ["Productividad", "Mas viajes efectivos por turno", "Viajes adicionales x margen operativo"],
    ], [1.6 * inch, 2.55 * inch, 3.1 * inch]))
    story.append(Spacer(1, 0.12 * inch))
    story.append(p("<b>Recomendacion MBB:</b> durante el primer buque piloto, capturar baseline manual vs digital para calcular COPQ real (Cost of Poor Quality).", styles["BodyX"]))
    story.append(PageBreak())

    story.append(p("9. Roadmap de madurez", styles["TitleX"]))
    roadmap = [
        ["0-30 dias", "Estabilizar flujo esencial", "UAT handheld, cargas iniciales, despacho, QR, SOF offline, cierre."],
        ["31-60 dias", "Control estadistico", "Pareto SOF, limites de peso, ciclo camion, alertas por bodega/producto."],
        ["61-90 dias", "Estandarizacion comercial", "Manual, SOP, roles, reportes ejecutivos, checklist deployment."],
        ["90+ dias", "Escalamiento regional", "Multi pais, multi puerto, portal cliente, integraciones correo/WhatsApp/ERP."],
    ]
    story.append(make_table([["Horizonte", "Objetivo", "Entregable"]] + roadmap, [1.2 * inch, 2.0 * inch, 4.05 * inch]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(p("10. Dictamen final Master Black Belt", styles["H1X"]))
    story.append(p(
        "XTRAVON ONE tiene potencial de convertirse en un sistema de control operacional tipo SAP especializado para graneles si mantiene el foco en el flujo esencial: buque, guias, cuotas, despacho, QR, patio, SOF y cierre. "
        "La recomendacion MBB es no agregar complejidad sin medicion. Cada nueva pantalla debe reducir un defecto, tiempo de ciclo, riesgo o reproceso medible. El sistema debe evolucionar desde digitalizacion hacia control estadistico y prevencion.",
        styles["BodyX"],
    ))

    def footer(canvas, doc_obj):
        canvas.saveState()
        canvas.setFillColor(colors.HexColor(NAVY))
        canvas.rect(0, 0, letter[0], 0.34 * inch, stroke=0, fill=1)
        canvas.setFillColor(colors.white)
        canvas.setFont("Helvetica", 7.5)
        canvas.drawString(0.55 * inch, 0.13 * inch, "QORA SYSTEMS - XTRAVON ONE | Estudio LSS Master Black Belt")
        canvas.drawRightString(letter[0] - 0.55 * inch, 0.13 * inch, f"Pagina {doc_obj.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return PDF_PATH


if __name__ == "__main__":
    print(build_pdf())
