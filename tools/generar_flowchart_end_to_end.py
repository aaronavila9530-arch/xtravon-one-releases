from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "Entregables"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 4200, 2500

COLORS = {
    "deep": "#081324",
    "atlantic": "#0B1E3A",
    "panel": "#0D2238",
    "panel2": "#102A44",
    "line": "#1D4462",
    "cyan": "#00E5FF",
    "ice": "#6FFBFF",
    "blue": "#0066FF",
    "green": "#21D6A2",
    "amber": "#FFB020",
    "red": "#FF4F73",
    "white": "#F5F7FA",
    "silver": "#C7CDD6",
    "muted": "#8FA7BE",
    "black": "#02070D",
}


def rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))


def f(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


FONT_TITLE = f(72, True)
FONT_SUB = f(34, False)
FONT_PHASE = f(33, True)
FONT_LANE = f(28, True)
FONT_CARD_TITLE = f(27, True)
FONT_CARD = f(22, False)
FONT_SMALL = f(18, False)
FONT_TAG = f(22, True)


def text_size(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


def wrap_lines(draw, text, font, max_width):
    lines = []
    for raw in str(text).split("\n"):
        raw = raw.strip()
        if not raw:
            lines.append("")
            continue
        words = raw.split()
        current = ""
        for word in words:
            trial = f"{current} {word}".strip()
            if text_size(draw, trial, font)[0] <= max_width or not current:
                current = trial
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
    return lines


def draw_wrapped(draw, xy, text, font, fill, max_width, line_gap=6):
    x, y = xy
    for line in wrap_lines(draw, text, font, max_width):
        draw.text((x, y), line, font=font, fill=fill)
        y += font.size + line_gap
    return y


def arrow(draw, start, end, color, width=6):
    draw.line([start, end], fill=color, width=width)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = max((dx * dx + dy * dy) ** 0.5, 1)
    ux, uy = dx / length, dy / length
    px, py = -uy, ux
    s = 22
    p1 = (end[0] - ux * s + px * s * 0.55, end[1] - uy * s + py * s * 0.55)
    p2 = (end[0] - ux * s - px * s * 0.55, end[1] - uy * s - py * s * 0.55)
    draw.polygon([end, p1, p2], fill=color)


def elbow_arrow(draw, points, color, width=6):
    if len(points) < 2:
        return
    for start, end in zip(points, points[1:-1]):
        draw.line([start, end], fill=color, width=width)
    arrow(draw, points[-2], points[-1], color, width)


def dashed_line(draw, start, end, color, width=4, dash=18, gap=12):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    dist = max((dx * dx + dy * dy) ** 0.5, 1)
    steps = int(dist // (dash + gap)) + 1
    for i in range(steps):
        a = i * (dash + gap) / dist
        b = min((i * (dash + gap) + dash) / dist, 1)
        draw.line([(x1 + dx * a, y1 + dy * a), (x1 + dx * b, y1 + dy * b)], fill=color, width=width)


def card(draw, box, title, body, kind="essential", step=None):
    x0, y0, x1, y1 = box
    fill = rgb(COLORS["panel"])
    outline = rgb(COLORS["cyan"] if kind == "essential" else COLORS["amber"])
    accent = rgb(COLORS["green"] if kind == "essential" else COLORS["amber"])
    draw.rounded_rectangle(box, radius=18, fill=fill, outline=outline, width=4)
    draw.rounded_rectangle([x0, y0, x1, y0 + 14], radius=8, fill=accent)
    if step:
        draw.ellipse([x0 + 18, y0 + 24, x0 + 62, y0 + 68], fill=accent)
        draw.text((x0 + 40, y0 + 33), str(step), font=FONT_TAG, fill=rgb(COLORS["black"]), anchor="ma")
        tx = x0 + 76
    else:
        tx = x0 + 22
    draw_wrapped(draw, (tx, y0 + 26), title, FONT_CARD_TITLE, rgb(COLORS["white"]), x1 - tx - 18, line_gap=4)
    draw_wrapped(draw, (x0 + 24, y0 + 88), body, FONT_CARD, rgb(COLORS["silver"]), x1 - x0 - 48, line_gap=5)


def pill(draw, box, text, fill, color_text="#02070D"):
    draw.rounded_rectangle(box, radius=20, fill=rgb(fill))
    draw.text(((box[0] + box[2]) / 2, box[1] + 11), text, font=FONT_TAG, fill=rgb(color_text), anchor="ma")


def main():
    img = Image.new("RGB", (W, H), rgb(COLORS["deep"]))
    draw = ImageDraw.Draw(img)

    # Subtle grid
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, H)], fill=(9, 28, 47), width=1)
    for y in range(0, H, 80):
        draw.line([(0, y), (W, y)], fill=(9, 28, 47), width=1)

    draw.rectangle([0, 0, W, 250], fill=rgb(COLORS["atlantic"]))
    draw.text((90, 54), "XTRAVON ONE | GRAIN CONTROL", font=FONT_TITLE, fill=rgb(COLORS["white"]))
    draw.text((92, 140), "Flowchart END TO END - Actividades esenciales vs complementarias por rol", font=FONT_SUB, fill=rgb(COLORS["ice"]))
    pill(draw, [3150, 62, 3560, 116], "ESENCIAL", COLORS["green"])
    pill(draw, [3150, 135, 3560, 189], "COMPLEMENTARIO", COLORS["amber"])
    draw.text((3635, 70), "Si se elimina, el flujo operativo se rompe.", font=FONT_SMALL, fill=rgb(COLORS["silver"]))
    draw.text((3635, 143), "Agrega visibilidad, analitica o soporte; no detiene la operacion.", font=FONT_SMALL, fill=rgb(COLORS["silver"]))

    left = 80
    top = 320
    lane_w = 520
    lane_gap = 20
    lane_h = 1450
    lanes = [
        ("Supervisor Operacion", "Configura, abre buque, valida carga inicial y cierre."),
        ("Despacho", "Asigna guias, confirma continuidad y reasigna pendientes."),
        ("Operador Patio", "Escanea QR, registra pesos, tolva, marchamos y SOF."),
        ("Chofer", "Recibe QR vigente, ejecuta viaje y confirma continuidad."),
        ("Gerente / Cliente", "Consulta resultados, informes, riesgos y performance."),
        ("Sistema / Backend", "Valida seguridad, estados, auditoria, offline y sincronizacion."),
    ]
    for i, (name, desc) in enumerate(lanes):
        x0 = left + i * (lane_w + lane_gap)
        draw.rounded_rectangle([x0, top, x0 + lane_w, top + lane_h], radius=24, fill=rgb(COLORS["atlantic"]), outline=rgb(COLORS["line"]), width=3)
        draw.rectangle([x0, top, x0 + lane_w, top + 82], fill=rgb(COLORS["panel2"]))
        draw.text((x0 + 24, top + 18), name, font=FONT_LANE, fill=rgb(COLORS["white"]))
        draw_wrapped(draw, (x0 + 24, top + 52), desc, FONT_SMALL, rgb(COLORS["muted"]), lane_w - 48, line_gap=4)

    # Phase labels
    phases = [
        (310, "1. Preparacion"),
        (560, "2. Apertura y plan"),
        (820, "3. Carga y aprobacion"),
        (1085, "4. Despacho y QR"),
        (1350, "5. Patio / escaneos"),
        (1610, "6. Cierre / archivo"),
    ]
    for y, label in phases:
        draw.text((W - 740, y - 32), label, font=FONT_PHASE, fill=rgb(COLORS["ice"]))
        dashed_line(draw, (70, y), (W - 80, y), rgb(COLORS["line"]), width=2, dash=22, gap=18)

    x = [left + i * (lane_w + lane_gap) for i in range(6)]

    # Essential cards in swimlanes
    card(draw, [x[5] + 28, 420, x[5] + lane_w - 28, 590],
         "Roles, permisos y seguridad",
         "Crear usuarios, permisos, perfil supervisor/patio/chofer/cliente. Definir QR_SECRET, pass hatch y auditoria.",
         "essential", 1)

    card(draw, [x[0] + 28, 560, x[0] + lane_w - 28, 745],
         "Abrir operacion de buque",
         "Nombre del buque, fecha inicio, productos, bodegas, particiones, stowage plan y estado ABIERTA.",
         "essential", 2)
    card(draw, [x[0] + 28, 770, x[0] + lane_w - 28, 945],
         "Crear cuotas por cliente",
         "Asignar cliente, producto, cuota y unidad. Validar que el total coincida con la operacion y bodegas.",
         "essential", 3)

    card(draw, [x[0] + 28, 990, x[0] + lane_w - 28, 1215],
         "Carga inicial de boletas",
         "Abrir template, llenar guia/cliente/producto/chofer/placa/bodega, cargar Excel. Estas guias quedan aprobadas de inicio.",
         "essential", 4)
    card(draw, [x[5] + 28, 990, x[5] + lane_w - 28, 1215],
         "Validacion de carga",
         "Ligar cada guia a operacion correcta. Generar hash interno. Evitar mezcla entre buques abiertos.",
         "essential", 5)

    card(draw, [x[1] + 28, 1085, x[1] + lane_w - 28, 1310],
         "Despacho asigna guia",
         "Seleccionar chofer, placa, cliente y producto. El sistema toma guia disponible/asignada correcta y habilita QR vigente.",
         "essential", 6)
    card(draw, [x[3] + 28, 1085, x[3] + lane_w - 28, 1310],
         "Chofer recibe QR",
         "App muestra solo QR vigente, cliente, producto, viajes asignados/pendientes y peso acumulado. No muestra pass hatch.",
         "essential", 7)

    card(draw, [x[2] + 28, 1350, x[2] + lane_w - 28, 1585],
         "Primer escaneo - ingreso",
         "Leer QR con SE4710 o camara. Registrar ficha y peso vacio. Guia pasa a EN_PUERTO.",
         "essential", 8)
    card(draw, [x[2] + 28, 1605, x[2] + lane_w - 28, 1815],
         "Segundo y tercer escaneo",
         "Segundo: numero de tolva. Tercero: peso lleno y marchamos N. Guia queda COMPLETA y QR bloqueado.",
         "essential", 9)
    card(draw, [x[5] + 28, 1385, x[5] + lane_w - 28, 1645],
         "Offline y sincronizacion",
         "Si no hay red, handheld guarda local. Reintenta cada ciclo al recuperar conexion. Evita detener operacion.",
         "essential", 10)

    card(draw, [x[1] + 28, 1500, x[1] + lane_w - 28, 1735],
         "Continuidad o reasignacion",
         "Tras completar ciclo, chofer confirma si continua. Si no continua, guias pendientes pasan a despacho para reasignacion manual.",
         "essential", 11)
    card(draw, [x[0] + 28, 1500, x[0] + lane_w - 28, 1735],
         "Cierre operativo",
         "Validar cuotas, SOF, diferencias, guias completas, bodegas descargadas y autorizaciones. Cerrar o archivar operacion.",
         "essential", 12)

    # SOF essential but cross-lane
    card(draw, [x[2] + 28, 1010, x[2] + lane_w - 28, 1260],
         "SOF operativo",
         "Registrar evento, hora desde/hasta, bodega, categoria y descripcion. Puede guardarse offline y sincronizar.",
         "essential", 13)

    # Complementary section
    comp_y0 = 1845
    draw.rounded_rectangle([80, comp_y0, W - 80, H - 110], radius=28, fill=rgb(COLORS["panel"]), outline=rgb(COLORS["amber"]), width=4)
    draw.text((120, comp_y0 + 35), "ACTIVIDADES COMPLEMENTARIAS - agregan control, analitica y soporte sin detener la operacion base", font=FONT_PHASE, fill=rgb(COLORS["amber"]))

    comp_cards = [
        ("Centro Ejecutivo", "KPIs, silueta del buque, avance por bodega, cuota vs descargado, viajes restantes, alertas y tendencias."),
        ("Informes", "PDF, Excel, Word o CSV por buque, cliente, producto, bodega, SOF, productividad y diferencias documentales."),
        ("Liquidaciones Choferes", "Resumen administrativo por chofer, empresa y producto: viajes, MT descargadas, duracion, detalle y exportacion."),
        ("P.O.R.T.I.A", "Asistente para clima, riesgos, AIS, calados, SOF, duracion estimada y consultas operativas."),
        ("Ayuda / Q&A", "Manual operativo interno: pasos, FAQ, flujo visual y guia completa para usuarios nuevos."),
        ("Historial de Buques", "Consulta de operaciones cerradas, comparativo historico, cuotas y performance por operacion."),
        ("Cliente / Gerencia", "Visibilidad controlada de cuotas, descargado, pendientes, reportes y riesgos ejecutivos."),
    ]
    cx, cy = 120, comp_y0 + 110
    cw, ch = 560, 170
    for i, (title, body) in enumerate(comp_cards):
        col = i % 4
        row = i // 4
        bx = cx + col * (cw + 48)
        by = cy + row * (ch + 52)
        card(draw, [bx, by, bx + cw, by + ch], title, body, "complementary", None)

    # Arrows essential flow. Routed with elbow connectors to reduce visual crossings.
    green = rgb(COLORS["green"])
    cyan = rgb(COLORS["cyan"])
    guide = rgb("#1FA6A2")
    # Step 1 is a prerequisite for the whole flow. Make the connection visible,
    # but keep it in an upper empty corridor so it does not compete with the main flow.
    elbow_arrow(draw, [(x[5] + 28, 505), (x[0] + 492, 505), (x[0] + 492, 560)], guide, width=4)
    elbow_arrow(draw, [(x[0] + 260, 745), (x[0] + 260, 770)], green)
    elbow_arrow(draw, [(x[0] + 260, 945), (x[0] + 260, 990)], green)
    # 4 -> 5: initial load must be validated by backend first.
    elbow_arrow(draw, [(x[0] + 492, 1045), (x[0] + 492, 955), (x[5] + 28, 955), (x[5] + 28, 1085)], green)
    # 5 -> 6: after backend validation, dispatch receives assignable guides.
    elbow_arrow(draw, [(x[5] + 28, 1180), (x[5] + 28, 1315), (x[1] + 260, 1315), (x[1] + 260, 1310)], green)
    # 6 -> 7: dispatch confirms the guide and the driver receives one active QR.
    elbow_arrow(draw, [(x[1] + 492, 1195), (x[3] + 28, 1195)], green)
    # Driver -> first scan through a clean lower corridor.
    elbow_arrow(draw, [(x[3] + 260, 1310), (x[3] + 260, 1335), (x[2] + 260, 1335), (x[2] + 260, 1350)], green)
    elbow_arrow(draw, [(x[2] + 260, 1585), (x[2] + 260, 1605)], green)
    # Offline/sync supports the scan stages.
    dashed_line(draw, (x[2] + 492, 1470), (x[5] + 28, 1470), guide, width=3, dash=18, gap=14)
    dashed_line(draw, (x[5] + 28, 1470), (x[5] + 28, 1515), guide, width=3, dash=18, gap=14)
    # Completed cycle -> continuity -> close. Keep this in the lower corridor.
    elbow_arrow(draw, [(x[2] + 28, 1715), (x[1] + 492, 1715)], green)
    elbow_arrow(draw, [(x[1] + 28, 1620), (x[0] + 492, 1620)], green)

    # Complementary dotted connections
    muted_amber = rgb("#8A6B1F")
    dashed_line(draw, (x[0] + 300, 1735), (420, comp_y0 + 110), muted_amber, width=3, dash=16, gap=18)
    dashed_line(draw, (x[2] + 300, 1260), (1500, comp_y0 + 110), muted_amber, width=3, dash=16, gap=18)
    dashed_line(draw, (x[5] + 300, 1645), (2580, comp_y0 + 110), muted_amber, width=3, dash=16, gap=18)

    # Footer legend
    draw.text((90, H - 70), "Lectura: las tarjetas verdes/cyan son esenciales; las ambar son complementarias. El flujo base debe poder operar incluso si analitica, informes o IA se desactivan temporalmente.", font=FONT_SMALL, fill=rgb(COLORS["silver"]))
    draw.text((W - 850, H - 70), "QORA SYSTEMS - XTRAVON ONE | End-to-end operational control", font=FONT_SMALL, fill=rgb(COLORS["ice"]))

    jpg_path = OUT / "XTRAVON_ONE_Flowchart_End_to_End_ES.jpg"
    img.save(jpg_path, "JPEG", quality=95, subsampling=0)
    print(jpg_path)


if __name__ == "__main__":
    main()
