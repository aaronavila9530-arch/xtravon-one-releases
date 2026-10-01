from pathlib import Path
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
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
OUT = ROOT / "Entregables"
ASSET_DIR = ROOT / "assets"
MANUAL_ASSETS = OUT / "manual_assets"


PALETTE = {
    "deep": "#081324",
    "atlantic": "#0B1E3A",
    "panel": "#0D2238",
    "line": "#18364F",
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


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def font(size=18, bold=False):
    candidates = [
        "C:/Windows/Fonts/seguisb.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def fit_text(draw, text, box, fnt, fill, anchor="mm", max_lines=2, align="center"):
    x0, y0, x1, y1 = box
    lines = []
    words = str(text).split()
    current = ""
    max_width = x1 - x0 - 12
    for word in words:
        trial = (current + " " + word).strip()
        bbox = draw.textbbox((0, 0), trial, font=fnt)
        if bbox[2] - bbox[0] <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
            if len(lines) >= max_lines:
                break
    if current and len(lines) < max_lines:
        lines.append(current)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
    total_h = len(lines) * (fnt.size + 4)
    y = y0 + ((y1 - y0) - total_h) / 2
    for line in lines:
        if align == "left":
            x = x0 + 10
            a = "la"
        else:
            x = (x0 + x1) / 2
            a = "ma"
        draw.text((x, y), line, font=fnt, fill=fill, anchor=a)
        y += fnt.size + 4


def draw_arrow(draw, start, end, fill, width=4):
    draw.line([start, end], fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 14
    p1 = (end[0] - size * math.cos(angle - math.pi / 6), end[1] - size * math.sin(angle - math.pi / 6))
    p2 = (end[0] - size * math.cos(angle + math.pi / 6), end[1] - size * math.sin(angle + math.pi / 6))
    draw.polygon([end, p1, p2], fill=fill)


def save_img(name, img):
    MANUAL_ASSETS.mkdir(parents=True, exist_ok=True)
    path = MANUAL_ASSETS / name
    img.save(path, "PNG")
    return path


def base_canvas(w=1500, h=850, title=None):
    img = Image.new("RGB", (w, h), hex_to_rgb(PALETTE["deep"]))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, w, 86], fill=hex_to_rgb(PALETTE["atlantic"]))
    if title:
        draw.text((36, 28), title, font=font(34, True), fill=hex_to_rgb(PALETTE["white"]))
        draw.text((36, 64), "XTRAVON ONE | GRAIN CONTROL", font=font(18), fill=hex_to_rgb(PALETTE["ice"]))
    return img, draw


def mock_desktop(lang):
    title = "Centro Ejecutivo - Supervisor" if lang == "ES" else "Executive Center - Supervisor"
    img, d = base_canvas(title=title)
    d.rectangle([28, 110, 1472, 186], fill=hex_to_rgb(PALETTE["panel"]), outline=hex_to_rgb(PALETTE["line"]), width=2)
    labels = ["Buscar operacion", "Generar datos", "Cargar filtros", "Gestion operativa"] if lang == "ES" else ["Find operation", "Generate data", "Load filters", "Operations"]
    x = 50
    for i, label in enumerate(labels):
        color = PALETTE["cyan"] if i in (0, 3) else PALETTE["atlantic"]
        d.rounded_rectangle([x, 126, x + 170, 170], radius=4, fill=hex_to_rgb(color))
        d.text((x + 18, 139), label, font=font(17, True), fill=hex_to_rgb(PALETTE["black"] if color == PALETTE["cyan"] else PALETTE["white"]))
        x += 188
    filters = ["Empresa", "Guia", "Producto", "Chofer", "Placa"] if lang == "ES" else ["Company", "Ticket", "Product", "Driver", "Plate"]
    x = 790
    for f in filters:
        d.text((x, 119), f, font=font(14, True), fill=hex_to_rgb(PALETTE["white"]))
        d.rectangle([x, 142, x + 126, 169], fill=hex_to_rgb(PALETTE["white"]))
        d.polygon([(x + 112, 151), (x + 122, 151), (x + 117, 160)], fill=hex_to_rgb(PALETTE["black"]))
        x += 135

    kpis = [
        ("Guias", "813.00"),
        ("Completas", "279.00"),
        ("Pendientes", "534.00"),
        ("Capacidad MT", "39,000.00"),
        ("Descargado MT", "7,941.77"),
        ("Avance", "20.36%"),
    ] if lang == "ES" else [
        ("Tickets", "813.00"), ("Complete", "279.00"), ("Pending", "534.00"),
        ("Capacity MT", "39,000.00"), ("Discharged MT", "7,941.77"), ("Progress", "20.36%"),
    ]
    x = 34
    for idx, (k, v) in enumerate(kpis):
        d.rectangle([x, 220, x + 218, 335], fill=hex_to_rgb(PALETTE["panel"]), outline=hex_to_rgb(PALETTE["line"]))
        d.rectangle([x, 220, x + 218, 226], fill=hex_to_rgb([PALETTE["cyan"], PALETTE["green"], PALETTE["amber"], PALETTE["blue"], PALETTE["green"], PALETTE["ice"]][idx]))
        d.text((x + 18, 252), k, font=font(18, True), fill=hex_to_rgb(PALETTE["white"]))
        d.text((x + 18, 288), v, font=font(28, True), fill=hex_to_rgb(PALETTE["white"]))
        x += 236

    d.rectangle([34, 370, 1080, 610], fill=hex_to_rgb(PALETTE["panel"]), outline=hex_to_rgb(PALETTE["line"]))
    d.text((58, 392), "Progreso visual por bodega" if lang == "ES" else "Visual progress by hold", font=font(24, True), fill=hex_to_rgb(PALETTE["white"]))
    ship = [(85, 462), (980, 462), (1040, 520), (980, 580), (85, 580)]
    d.line(ship + [ship[0]], fill=hex_to_rgb(PALETTE["cyan"]), width=4)
    holds = [("B5", "83.34%"), ("B4", "83.05%"), ("B3", "81.98%"), ("B2", "76.70%"), ("B1", "75.41%")]
    colors_h = [PALETTE["cyan"], PALETTE["green"], PALETTE["blue"], "#5AAAF5", "#10B9AA"]
    hx = 120
    for (hold, pct), c in zip(holds, colors_h):
        d.rectangle([hx, 485, hx + 150, 560], fill=hex_to_rgb(c))
        d.text((hx + 75, 500), hold, font=font(17, True), fill=hex_to_rgb(PALETTE["black"]), anchor="ma")
        d.text((hx + 75, 528), pct, font=font(17, True), fill=hex_to_rgb(PALETTE["black"]), anchor="ma")
        hx += 170
    d.rectangle([1110, 370, 1472, 610], fill=hex_to_rgb(PALETTE["panel"]), outline=hex_to_rgb(PALETTE["line"]))
    d.text((1132, 394), "Lectura ejecutiva" if lang == "ES" else "Executive reading", font=font(24, True), fill=hex_to_rgb(PALETTE["white"]))
    executive = [
        "Buque: MV ATLANTIC GRAIN" if lang == "ES" else "Vessel: MV ATLANTIC GRAIN",
        "Riesgo: ALTO" if lang == "ES" else "Risk: HIGH",
        "Pendiente: 31,058.23 MT" if lang == "ES" else "Pending: 31,058.23 MT",
        "Plan viajes: faltan 1,115 aprox." if lang == "ES" else "Trip plan: approx. 1,115 remaining",
    ]
    y = 440
    for line in executive:
        d.text((1134, y), line, font=font(18, True), fill=hex_to_rgb(PALETTE["red"]))
        y += 34

    d.rectangle([34, 650, 710, 815], fill=hex_to_rgb(PALETTE["panel"]), outline=hex_to_rgb(PALETTE["line"]))
    d.text((58, 674), "Descargado por cliente (MT)" if lang == "ES" else "Discharged by client (MT)", font=font(22, True), fill=hex_to_rgb(PALETTE["white"]))
    clients = ["AgroCentro", "Molinos Norte", "Baltic Foods", "NordGrain"]
    y = 710
    for i, name in enumerate(clients):
        d.text((58, y), name, font=font(16), fill=hex_to_rgb(PALETTE["white"]))
        d.rectangle([210, y - 4, 210 + 80 + i * 55, y + 16], fill=hex_to_rgb(PALETTE["cyan"]))
        d.text((300 + i * 55, y - 4), f"{750 + i * 82:.2f}", font=font(15, True), fill=hex_to_rgb(PALETTE["white"]))
        y += 28

    d.rectangle([745, 650, 1472, 815], fill=hex_to_rgb(PALETTE["panel"]), outline=hex_to_rgb(PALETTE["line"]))
    d.text((770, 674), "Tendencia diaria descargado (MT)" if lang == "ES" else "Daily discharge trend (MT)", font=font(22, True), fill=hex_to_rgb(PALETTE["white"]))
    pts = [(810, 770), (900, 730), (990, 710), (1080, 735), (1170, 760), (1260, 790), (1350, 780)]
    for a, b in zip(pts, pts[1:]):
        d.line([a, b], fill=hex_to_rgb(PALETTE["cyan"]), width=4)
    for p in pts:
        d.ellipse([p[0] - 6, p[1] - 6, p[0] + 6, p[1] + 6], fill=hex_to_rgb(PALETTE["ice"]))
    return save_img(f"mock_desktop_{lang}.png", img)


def mock_operation(lang):
    title = "Apertura de buque y stowage plan" if lang == "ES" else "Vessel opening and stowage plan"
    img, d = base_canvas(title=title)
    d.rectangle([34, 116, 1466, 330], fill=hex_to_rgb(PALETTE["panel"]), outline=hex_to_rgb(PALETTE["line"]))
    fields = [
        ("Buque", "MV ATLANTIC GRAIN"),
        ("Fecha inicio", "28 de mayo de 2026"),
        ("Producto 1", "Maiz"),
        ("Producto 2", "Frijol de Soya"),
    ] if lang == "ES" else [
        ("Vessel", "MV ATLANTIC GRAIN"),
        ("Start date", "May 28, 2026"),
        ("Product 1", "Corn"),
        ("Product 2", "Soybean meal"),
    ]
    coords = [(70, 160), (760, 160), (70, 240), (760, 240)]
    for (label, value), (x, y) in zip(fields, coords):
        d.text((x, y - 30), label, font=font(17, True), fill=hex_to_rgb(PALETTE["white"]))
        d.rectangle([x, y, x + 610, y + 36], fill=hex_to_rgb(PALETTE["white"]))
        d.text((x + 12, y + 8), value, font=font(17), fill=hex_to_rgb(PALETTE["black"]))

    d.rectangle([34, 360, 1466, 680], fill=hex_to_rgb(PALETTE["panel"]), outline=hex_to_rgb(PALETTE["line"]))
    d.text((60, 390), "Capacidad y particiones por bodega" if lang == "ES" else "Hold capacity and partitions", font=font(24, True), fill=hex_to_rgb(PALETTE["white"]))
    ship = [(80, 455), (1280, 455), (1400, 550), (1280, 645), (80, 645)]
    d.line(ship + [ship[0]], fill=hex_to_rgb(PALETTE["cyan"]), width=4)
    hx = 120
    hold_order = [5, 4, 3, 2, 1]
    for i, h in enumerate(hold_order):
        d.rectangle([hx, 490, hx + 205, 610], outline=hex_to_rgb(PALETTE["cyan"]), width=2)
        if h == 3:
            d.rectangle([hx + 2, 492, hx + 203, 550], fill=hex_to_rgb(PALETTE["blue"]))
            d.rectangle([hx + 2, 552, hx + 203, 608], fill=hex_to_rgb(PALETTE["green"]))
            d.line([hx + 2, 551, hx + 203, 551], fill=hex_to_rgb(PALETTE["white"]), width=3)
            d.text((hx + 102, 506), "B3 / Maiz", font=font(16, True), fill=hex_to_rgb(PALETTE["white"]), anchor="ma")
            d.text((hx + 102, 566), "B3 / DDGS", font=font(16, True), fill=hex_to_rgb(PALETTE["black"]), anchor="ma")
        else:
            d.rectangle([hx + 2, 492, hx + 203, 608], fill=hex_to_rgb([PALETTE["cyan"], PALETTE["green"], "#5AAAF5", PALETTE["amber"], PALETTE["blue"]][i]))
            d.text((hx + 102, 520), f"B{h}", font=font(18, True), fill=hex_to_rgb(PALETTE["black"]), anchor="ma")
            d.text((hx + 102, 552), f"{6000 + i * 800:,.2f} MT", font=font(16, True), fill=hex_to_rgb(PALETTE["black"]), anchor="ma")
        hx += 225
    d.rounded_rectangle([70, 710, 310, 770], radius=5, fill=hex_to_rgb(PALETTE["cyan"]))
    d.text((95, 728), "Abrir operacion" if lang == "ES" else "Open operation", font=font(20, True), fill=hex_to_rgb(PALETTE["black"]))
    d.rounded_rectangle([330, 710, 560, 770], radius=5, fill=hex_to_rgb(PALETTE["atlantic"]))
    d.text((375, 728), "Limpiar" if lang == "ES" else "Clear", font=font(20, True), fill=hex_to_rgb(PALETTE["white"]))
    draw_arrow(d, (555, 620), (805, 620), hex_to_rgb(PALETTE["ice"]), 4)
    d.text((810, 610), "Las particiones separan cliente/producto" if lang == "ES" else "Partitions separate client/product", font=font(18, True), fill=hex_to_rgb(PALETTE["ice"]))
    return save_img(f"mock_operation_{lang}.png", img)


def mock_dispatch(lang):
    title = "Despacho de Viajes" if lang == "ES" else "Trip Dispatch"
    img, d = base_canvas(title=title)
    d.rectangle([34, 112, 1466, 255], fill=hex_to_rgb(PALETTE["panel"]), outline=hex_to_rgb(PALETTE["line"]))
    fields = ["Chofer", "Placa", "Cliente", "Producto"] if lang == "ES" else ["Driver", "Plate", "Client", "Product"]
    x = 65
    for f in fields:
        d.text((x, 135), f, font=font(16, True), fill=hex_to_rgb(PALETTE["white"]))
        d.rectangle([x, 160, x + 285, 194], fill=hex_to_rgb(PALETTE["white"]))
        d.polygon([(x + 268, 174), (x + 280, 174), (x + 274, 184)], fill=hex_to_rgb(PALETTE["black"]))
        x += 350
    d.rounded_rectangle([65, 210, 245, 246], radius=5, fill=hex_to_rgb(PALETTE["cyan"]))
    d.text((83, 219), "Asignar guia" if lang == "ES" else "Assign ticket", font=font(17, True), fill=hex_to_rgb(PALETTE["black"]))
    d.rounded_rectangle([265, 210, 470, 246], radius=5, fill=hex_to_rgb(PALETTE["atlantic"]))
    d.text((285, 219), "Enviar QR" if lang == "ES" else "Send QR", font=font(17, True), fill=hex_to_rgb(PALETTE["white"]))

    cards = [
        ("Solicitudes", "2", PALETTE["red"]),
        ("Asignadas", "120", PALETTE["cyan"]),
        ("Primer escaneo", "65", PALETTE["amber"]),
        ("Segundo escaneo", "42", PALETTE["blue"]),
        ("Tercer escaneo", "30", PALETTE["green"]),
        ("Completadas", "279", PALETTE["ice"]),
    ] if lang == "ES" else [
        ("Requests", "2", PALETTE["red"]), ("Assigned", "120", PALETTE["cyan"]),
        ("First scan", "65", PALETTE["amber"]), ("Second scan", "42", PALETTE["blue"]),
        ("Third scan", "30", PALETTE["green"]), ("Completed", "279", PALETTE["ice"]),
    ]
    x = 34
    for label, value, c in cards:
        d.rectangle([x, 292, x + 220, 400], fill=hex_to_rgb(PALETTE["panel"]), outline=hex_to_rgb(PALETTE["line"]))
        d.rectangle([x, 292, x + 220, 298], fill=hex_to_rgb(c))
        d.text((x + 18, 322), label, font=font(17, True), fill=hex_to_rgb(PALETTE["white"]))
        d.text((x + 18, 354), value, font=font(32, True), fill=hex_to_rgb(PALETTE["white"]))
        x += 238

    panels = [
        ("Solicitudes de nuevo viaje", ["Juan Perez | ABC123 | Maiz", "Luis Rojas | XYZ987 | DDGS"]),
        ("Guias asignadas", ["07764 | AgroCentro | Maiz", "07765 | NordGrain | Soya"]),
        ("En puerto", ["07766 | Peso vacio OK", "07767 | Tolva 3"]),
        ("Completadas recientes", ["07750 | 29.20 MT", "07751 | 28.75 MT"]),
    ] if lang == "ES" else [
        ("New trip requests", ["Juan Perez | ABC123 | Corn", "Luis Rojas | XYZ987 | DDGS"]),
        ("Assigned tickets", ["07764 | AgroCentro | Corn", "07765 | NordGrain | Soy"]),
        ("Inside port", ["07766 | Tare OK", "07767 | Hopper 3"]),
        ("Recently completed", ["07750 | 29.20 MT", "07751 | 28.75 MT"]),
    ]
    positions = [(34, 440), (765, 440), (34, 640), (765, 640)]
    for (heading, rows), (x, y) in zip(panels, positions):
        d.rectangle([x, y, x + 700, y + 165], fill=hex_to_rgb(PALETTE["panel"]), outline=hex_to_rgb(PALETTE["line"]))
        d.text((x + 18, y + 18), heading, font=font(22, True), fill=hex_to_rgb(PALETTE["white"]))
        d.rectangle([x + 18, y + 58, x + 682, y + 90], fill=hex_to_rgb(PALETTE["cyan"]))
        d.text((x + 32, y + 65), "Guia      Cliente      Producto      Estado" if lang == "ES" else "Ticket      Client      Product      Status", font=font(16, True), fill=hex_to_rgb(PALETTE["black"]))
        ry = y + 103
        for row in rows:
            d.text((x + 32, ry), row, font=font(17), fill=hex_to_rgb(PALETTE["white"]))
            ry += 30
    return save_img(f"mock_dispatch_{lang}.png", img)


def mock_handheld(lang):
    title = "Handheld operador de patio" if lang == "ES" else "Yard operator handheld"
    img = Image.new("RGB", (1000, 1100), hex_to_rgb(PALETTE["deep"]))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([245, 40, 755, 1060], radius=55, fill=(12, 16, 23), outline=hex_to_rgb(PALETTE["silver"]), width=6)
    d.rounded_rectangle([285, 95, 715, 1010], radius=25, fill=hex_to_rgb(PALETTE["atlantic"]))
    d.text((315, 125), "XTRAVON ONE", font=font(28, True), fill=hex_to_rgb(PALETTE["white"]))
    d.text((315, 158), "Operador Patio", font=font(20, True), fill=hex_to_rgb(PALETTE["ice"]))
    d.rounded_rectangle([315, 205, 680, 255], radius=10, fill=hex_to_rgb(PALETTE["cyan"]))
    d.text((350, 218), "Lector QR Patio" if lang == "ES" else "Yard QR Reader", font=font(20, True), fill=hex_to_rgb(PALETTE["black"]))
    d.rectangle([315, 290, 680, 500], fill=hex_to_rgb(PALETTE["black"]), outline=hex_to_rgb(PALETTE["cyan"]), width=3)
    d.line([360, 395, 635, 395], fill=hex_to_rgb(PALETTE["cyan"]), width=4)
    d.text((350, 520), "Guia 07765", font=font(26, True), fill=hex_to_rgb(PALETTE["white"]))
    rows = [
        ("Empresa", "AgroCentro"), ("Producto", "Maiz"), ("Chofer", "Juan Perez"),
        ("Escaneo", "Ingreso puerto"), ("Peso vacio", "8,120.00 KG"), ("Ficha", "F-2241")
    ] if lang == "ES" else [
        ("Company", "AgroCentro"), ("Product", "Corn"), ("Driver", "Juan Perez"),
        ("Scan", "Port entry"), ("Tare", "8,120.00 KG"), ("Ticket", "F-2241")
    ]
    y = 565
    for label, val in rows:
        d.text((330, y), label, font=font(17, True), fill=hex_to_rgb(PALETTE["ice"]))
        d.rounded_rectangle([330, y + 25, 665, y + 62], radius=5, fill=hex_to_rgb(PALETTE["white"]))
        d.text((342, y + 34), val, font=font(17), fill=hex_to_rgb(PALETTE["black"]))
        y += 78
    d.rounded_rectangle([330, 920, 665, 978], radius=8, fill=hex_to_rgb(PALETTE["cyan"]))
    d.text((405, 937), "Guardar" if lang == "ES" else "Save", font=font(23, True), fill=hex_to_rgb(PALETTE["black"]))
    draw_arrow(d, (170, 440), (315, 395), hex_to_rgb(PALETTE["ice"]), 5)
    d.text((55, 405), "SE4710 / camara" if lang == "ES" else "SE4710 / camera", font=font(20, True), fill=hex_to_rgb(PALETTE["ice"]))
    return save_img(f"mock_handheld_{lang}.png", img)


def mock_driver(lang):
    title = "Portal Chofer" if lang == "ES" else "Driver portal"
    img = Image.new("RGB", (1000, 1100), hex_to_rgb(PALETTE["deep"]))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([245, 40, 755, 1060], radius=55, fill=(12, 16, 23), outline=hex_to_rgb(PALETTE["silver"]), width=6)
    d.rounded_rectangle([285, 95, 715, 1010], radius=25, fill=hex_to_rgb(PALETTE["atlantic"]))
    d.text((320, 125), "XTRAVON ONE", font=font(27, True), fill=hex_to_rgb(PALETTE["white"]))
    d.text((320, 158), "Portal Chofer" if lang == "ES" else "Driver Portal", font=font(20, True), fill=hex_to_rgb(PALETTE["ice"]))
    d.rectangle([330, 215, 670, 555], fill=hex_to_rgb(PALETTE["white"]))
    # QR-like pattern
    for ix in range(13):
        for iy in range(13):
            if (ix * iy + ix + iy) % 3 == 0 or ix in (1, 2, 10) and iy in (1, 2, 10):
                d.rectangle([350 + ix * 23, 235 + iy * 23, 366 + ix * 23, 251 + iy * 23], fill=hex_to_rgb(PALETTE["black"]))
    d.text((330, 585), "Guia activa 07765" if lang == "ES" else "Active ticket 07765", font=font(25, True), fill=hex_to_rgb(PALETTE["white"]))
    info = [
        ("Empresa", "AgroCentro"),
        ("Producto", "Maiz"),
        ("Chofer", "Aaron Avila"),
        ("Viajes asignados", "5"),
        ("Viajes pendientes", "4"),
        ("Acumulado", "29.20 MT"),
    ] if lang == "ES" else [
        ("Company", "AgroCentro"), ("Product", "Corn"), ("Driver", "Aaron Avila"),
        ("Assigned trips", "5"), ("Pending trips", "4"), ("Accumulated", "29.20 MT"),
    ]
    y = 630
    for label, val in info:
        d.text((330, y), f"{label}: {val}", font=font(20, True), fill=hex_to_rgb(PALETTE["white"]))
        y += 40
    d.rounded_rectangle([330, 900, 665, 958], radius=8, fill=hex_to_rgb(PALETTE["cyan"]))
    d.text((365, 916), "Solicitar viajes" if lang == "ES" else "Request trips", font=font(22, True), fill=hex_to_rgb(PALETTE["black"]))
    return save_img(f"mock_driver_{lang}.png", img)


def mock_sof_reports_portia(lang):
    img, d = base_canvas(title=("SOF, Informes y P.O.R.T.I.A" if lang == "ES" else "SOF, Reports and P.O.R.T.I.A"))
    panels = [
        ("SOF", "Registre hora desde/hasta, bodega, categoria y evento." if lang == "ES" else "Record from/to time, hold, category and event."),
        ("Informes", "Genere PDF, Word, Excel o CSV con graficos y KPIs." if lang == "ES" else "Generate PDF, Word, Excel or CSV with charts and KPIs."),
        ("P.O.R.T.I.A", "Pregunte por riesgos, clima, AIS, calado o duracion." if lang == "ES" else "Ask about risks, weather, AIS, draft or duration."),
    ]
    x = 50
    for idx, (head, body) in enumerate(panels):
        d.rectangle([x, 140, x + 430, 750], fill=hex_to_rgb(PALETTE["panel"]), outline=hex_to_rgb(PALETTE["line"]), width=2)
        d.rectangle([x, 140, x + 430, 148], fill=hex_to_rgb([PALETTE["cyan"], PALETTE["green"], PALETTE["blue"]][idx]))
        d.text((x + 24, 180), head, font=font(34, True), fill=hex_to_rgb(PALETTE["white"]))
        fit_text(d, body, (x + 24, 235, x + 405, 310), font(19, True), hex_to_rgb(PALETTE["silver"]), align="left", max_lines=3)
        if head == "SOF":
            d.rectangle([x + 35, 350, x + 395, 390], fill=hex_to_rgb(PALETTE["white"]))
            d.text((x + 48, 360), "08:00 - 10:30 | Demora | Bodega 2", font=font(16), fill=hex_to_rgb(PALETTE["black"]))
            d.rectangle([x + 35, 420, x + 395, 520], fill=hex_to_rgb(PALETTE["deep"]), outline=hex_to_rgb(PALETTE["cyan"]))
            d.text((x + 48, 440), "Evento: espera por apertura de bodega", font=font(16), fill=hex_to_rgb(PALETTE["white"]))
        elif head == "Informes":
            chart = [(x + 60, 620), (x + 120, 560), (x + 190, 585), (x + 255, 510), (x + 340, 540)]
            for a, b in zip(chart, chart[1:]):
                d.line([a, b], fill=hex_to_rgb(PALETTE["cyan"]), width=5)
            for p in chart:
                d.ellipse([p[0] - 7, p[1] - 7, p[0] + 7, p[1] + 7], fill=hex_to_rgb(PALETTE["ice"]))
            d.rectangle([x + 55, 390, x + 175, 470], fill=hex_to_rgb(PALETTE["cyan"]))
            d.rectangle([x + 205, 350, x + 325, 470], fill=hex_to_rgb(PALETTE["green"]))
        else:
            d.rounded_rectangle([x + 35, 360, x + 395, 520], radius=14, fill=hex_to_rgb(PALETTE["deep"]), outline=hex_to_rgb(PALETTE["cyan"]))
            d.text((x + 55, 390), "Oye Portia...", font=font(22, True), fill=hex_to_rgb(PALETTE["ice"]))
            d.text((x + 55, 440), "Te escucho. Cual es tu consulta?", font=font(18), fill=hex_to_rgb(PALETTE["white"]))
            d.rounded_rectangle([x + 90, 610, x + 340, 675], radius=30, fill=hex_to_rgb(PALETTE["cyan"]))
            d.text((x + 142, 630), "Preguntar", font=font(22, True), fill=hex_to_rgb(PALETTE["black"]))
        x += 470
    return save_img(f"mock_sof_reports_portia_{lang}.png", img)


def make_all_images():
    return {
        "ES": {
            "desktop": mock_desktop("ES"),
            "operation": mock_operation("ES"),
            "dispatch": mock_dispatch("ES"),
            "handheld": mock_handheld("ES"),
            "driver": mock_driver("ES"),
            "sof": mock_sof_reports_portia("ES"),
        },
        "EN": {
            "desktop": mock_desktop("EN"),
            "operation": mock_operation("EN"),
            "dispatch": mock_dispatch("EN"),
            "handheld": mock_handheld("EN"),
            "driver": mock_driver("EN"),
            "sof": mock_sof_reports_portia("EN"),
        },
    }


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "TitleX",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=30,
            leading=34,
            alignment=TA_CENTER,
            textColor=colors.HexColor(PALETTE["white"]),
            spaceAfter=12,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleX",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=12,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor(PALETTE["silver"]),
            spaceAfter=16,
        ),
        "h1": ParagraphStyle(
            "H1X",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=18,
            leading=22,
            textColor=colors.HexColor(PALETTE["atlantic"]),
            spaceBefore=14,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "H2X",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor(PALETTE["blue"]),
            spaceBefore=8,
            spaceAfter=4,
        ),
        "body": ParagraphStyle(
            "BodyX",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.4,
            leading=12.5,
            textColor=colors.HexColor("#1B1F26"),
            spaceAfter=5,
        ),
        "small": ParagraphStyle(
            "SmallX",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=colors.HexColor("#4A5568"),
        ),
        "caption": ParagraphStyle(
            "CaptionX",
            parent=base["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4A5568"),
            spaceAfter=8,
        ),
        "cover_note": ParagraphStyle(
            "CoverNoteX",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            alignment=TA_CENTER,
            textColor=colors.HexColor(PALETTE["ice"]),
        ),
    }


def header_footer(canvas, doc):
    canvas.saveState()
    w, h = letter
    canvas.setFillColor(colors.HexColor(PALETTE["atlantic"]))
    canvas.rect(0, h - 34, w, 34, stroke=0, fill=1)
    canvas.setFillColor(colors.HexColor(PALETTE["white"]))
    canvas.setFont("Helvetica-Bold", 8)
    canvas.drawString(36, h - 22, "XTRAVON ONE | GRAIN CONTROL")
    canvas.setFillColor(colors.HexColor(PALETTE["cyan"]))
    canvas.drawRightString(w - 36, h - 22, "QORA SYSTEMS - MSL Marine Surveyors and Logistics Group")
    canvas.setFillColor(colors.HexColor("#667085"))
    canvas.setFont("Helvetica", 8)
    canvas.drawCentredString(w / 2, 20, f"{doc.page}")
    canvas.restoreState()


def img_flow(path, width=6.9 * inch):
    return [RLImage(str(path), width=width, height=width * 0.56), Spacer(1, 4)]


def bullet_list(items, st):
    return [Paragraph(f"- {item}", st["body"]) for item in items]


ES = {
    "file": "XTRAVON_ONE_Manual_Operativo_ES.pdf",
    "cover_title": "Manual Operativo Detallado",
    "cover_sub": "Guia de uso para supervisores, despacho, operador de patio, choferes y clientes",
    "intro": [
        "XTRAVON ONE | GRAIN CONTROL centraliza la operacion portuaria de granos: apertura de buques, stowage plan, cuotas, guias, QR, escaneos, SOF, despacho de viajes, informes y analitica ejecutiva.",
        "El objetivo del sistema es convertir una operacion historicamente manual en una operacion digital, trazable, medible y auditable, reduciendo errores documentales, diferencias de carga y riesgos operativos.",
    ],
    "toc": "Indice operativo",
    "sections": [
        ("1. Logueo, roles y navegacion inicial", [
            ("Objetivo", ["Ingresar al sistema con el perfil correcto y evitar que un usuario vea funciones que no le corresponden."]),
            ("Paso a paso", [
                "Abra XTRAVON ONE desde el icono de escritorio o desde la app movil.",
                "Espere la pantalla de carga. La barra indica que se estan inicializando componentes locales.",
                "Seleccione el perfil de uso: Supervisor, Operador Patio, Chofer o Cliente.",
                "En produccion, use credenciales personales. Para pruebas puede ingresar con el usuario de demo habilitado.",
                "Valide que el menu muestre solo las pantallas autorizadas para su rol.",
            ]),
            ("Validaciones", [
                "Supervisor: acceso completo a centro ejecutivo, operaciones, despacho, informes, aprobaciones y roles.",
                "Operador Patio: acceso limitado a Lector QR Patio y SOF.",
                "Chofer: acceso a su QR vigente, viajes asignados, viajes pendientes y solicitud de nuevos viajes.",
                "Cliente: acceso a consultas, cuotas, retiros/descargado e informes permitidos.",
            ]),
        ]),
        ("2. Apertura de buque, productos y stowage plan", [
            ("Objetivo", ["Crear una operacion por buque para que todas las guias, cuotas, SOF, QR e informes queden separados por operacion."]),
            ("Paso a paso", [
                "Ingrese a Operaciones Buque.",
                "Digite el nombre del buque tal como se usara en documentos operativos.",
                "Seleccione la fecha de inicio desde el calendario.",
                "Agregue productos con el boton +. Puede registrar varios productos por operacion.",
                "Ingrese capacidad por bodega en MT. La Bodega 1 se representa en la punta del buque y el orden visual sigue hacia popa.",
                "Si una bodega esta partida por producto o cliente, agregue particiones. La suma de particiones debe coincidir con la capacidad de la bodega.",
                "Revise la silueta del buque para confirmar capacidades y particiones.",
                "Presione Abrir operacion. La operacion queda ABIERTA.",
            ]),
            ("Reglas de control", [
                "Una operacion abierta no debe mezclar datos de otra operacion.",
                "Pueden existir dos operaciones abiertas si el negocio lo requiere, pero cada carga debe asociarse explicitamente a su operacion.",
                "No cierre la operacion hasta validar descarga, cuotas, SOF, QR, informes y diferencias.",
            ]),
        ]),
        ("3. Cuotas por cliente", [
            ("Objetivo", ["Controlar cuanto corresponde retirar/descargar por cliente, producto y buque."]),
            ("Paso a paso", [
                "Seleccione la operacion activa o la operacion que desea administrar.",
                "Agregue cliente, cuota y unidad de medida.",
                "Use + para agregar N lineas de clientes y - para eliminar lineas.",
                "Presione Crear cuotas para guardar todas las cuotas de la operacion.",
                "Use Cargar cuotas activas para verificar lo registrado.",
            ]),
            ("Uso ejecutivo", [
                "El Centro Ejecutivo cruza cuota vs descargado real.",
                "El sistema debe alertar sobre sobrecuota, faltante, cliente atrasado y diferencia documental.",
                "Las cuotas tambien sirven para proponer viajes restantes segun el promedio real por camion.",
            ]),
        ]),
        ("4. Carga inicial de boletas y generacion controlada de QR", [
            ("Objetivo", ["Cargar las guias planificadas de inicio y dejarlas asignadas a la operacion correcta."]),
            ("Paso a paso", [
                "Ingrese a Carga de Boletas.",
                "Presione Buscar operacion activa para confirmar la operacion objetivo.",
                "Presione Abrir Template. El archivo Excel se abre para editar con la aplicacion de hojas del equipo.",
                "Complete guia, empresa, buque, fecha, producto, chofer, placa, bodega y embarque si aplica.",
                "Guarde el Excel.",
                "Presione Cargar Excel. La carga inicial queda aprobada automaticamente porque pertenece al plan inicial.",
                "Presione Buscar tabla para consultar y validar los registros cargados.",
            ]),
            ("Reglas", [
                "La carga inicial no debe pasar por Aprobaciones.",
                "El QR se habilita solo para guias asignadas segun despacho y flujo de seguridad.",
                "El pass hatch/hash de verificacion nunca debe mostrarse al chofer.",
            ]),
        ]),
        ("5. Aprobaciones para guias extraordinarias", [
            ("Objetivo", ["Aprobar o rechazar guias adicionales que no estaban en la carga inicial."]),
            ("Paso a paso", [
                "Ingrese a Aprobaciones.",
                "Abra el template extraordinario.",
                "Cargue el Excel extraordinario.",
                "Presione Ver datos cargados.",
                "Filtre por guia, empresa, producto, chofer o placa.",
                "Marque una, varias o todas las guias.",
                "Seleccione la accion: Aprobar, Rechazar, Seleccionar todo o Desmarcar todo.",
                "Agregue comentario si la decision lo requiere.",
            ]),
            ("Reglas", [
                "Solo al aprobar se genera QR y pass hatch.",
                "Las guias rechazadas deben conservar comentario y usuario responsable.",
                "La aprobacion debe quedar auditada para trazabilidad.",
            ]),
        ]),
        ("6. Despacho de Viajes", [
            ("Objetivo", ["Controlar asignacion, continuidad, reasignacion y solicitudes de viaje sin dejar decisiones criticas al chofer."]),
            ("Paso a paso", [
                "Ingrese a Despacho de Viajes.",
                "Busque operacion activa.",
                "Revise los tableros: solicitudes, asignadas, primer escaneo, segundo escaneo, tercer escaneo, completadas, choferes disponibles y bloqueos.",
                "Para asignar, seleccione chofer, placa, empresa y producto. El sistema toma una guia disponible segun la operacion y reglas.",
                "Al confirmar, el QR queda disponible en la app del chofer y opcionalmente se envia por WhatsApp o correo.",
                "Use click derecho o presion prolongada en app para acciones: asignar, reasignar, liberar, cancelar, bloquear o enviar QR.",
            ]),
            ("Reglas", [
                "El ERP puede sugerir, pero despacho confirma.",
                "Si el chofer no continua, sus guias pendientes pasan a pendientes de reasignacion.",
                "La reasignacion se hace manualmente por despacho, no de forma automatica ciega.",
            ]),
        ]),
        ("7. Portal Chofer", [
            ("Objetivo", ["Mostrar al chofer solo lo necesario para operar sin exponer informacion sensible."]),
            ("El chofer ve", [
                "QR vigente del viaje actual.",
                "Empresa, producto y nombre de chofer.",
                "Viajes asignados y viajes pendientes.",
                "Peso acumulado y resumen de viajes.",
            ]),
            ("El chofer no ve", [
                "Pass hatch/hash de verificacion.",
                "Datos internos de auditoria.",
                "Informacion de otros choferes.",
                "Link abierto con toda la informacion de la guia.",
            ]),
            ("Flujo al completar ciclo", [
                "Cuando el tercer escaneo queda completo, el QR se archiva.",
                "La app pregunta si desea continuar con la operacion.",
                "Si responde si, se pide confirmacion y se muestra el siguiente QR asignado.",
                "Si responde no, sus guias pendientes quedan para reasignacion manual en despacho.",
                "Si se queda sin guias, puede presionar Solicitar viajes.",
            ]),
        ]),
        ("8. Lector QR Patio y modo offline", [
            ("Objetivo", ["Registrar los tres puntos de control de cada camion incluso cuando no exista conexion estable."]),
            ("Escaneos", [
                "Primer escaneo: ficha y peso vacio.",
                "Segundo escaneo: numero de tolva.",
                "Tercer escaneo: peso lleno y marchamos.",
                "Marchamos: use + para agregar hasta los marchamos necesarios y - para quitar entradas.",
            ]),
            ("Offline", [
                "El handheld guarda en memoria local si no hay senal.",
                "Cada intento queda en cola con fecha, hora, guia, etapa y datos capturados.",
                "El dispositivo reintenta sincronizar automaticamente cuando vuelve la red.",
                "La operacion no debe detenerse por caida del backend o baja senal.",
            ]),
        ]),
        ("9. SOF - Statement of Facts", [
            ("Objetivo", ["Registrar eventos operativos con hora desde/hasta, bodega, categoria y descripcion."]),
            ("Paso a paso", [
                "Ingrese a SOF.",
                "La operacion activa debe aparecer seleccionada por defecto.",
                "Seleccione guia si el evento aplica a una guia especifica.",
                "Ingrese hora desde y hora hasta.",
                "Seleccione subcategoria.",
                "Escriba el evento con detalle operativo.",
                "Guarde. En handheld/app puede quedar offline y sincronizar luego.",
            ]),
            ("Buenas practicas", [
                "Registrar demoras por grua, maquinaria, clima, bodega, documentacion o seguridad.",
                "Usar descripciones objetivas.",
                "Evitar mezclar eventos de operaciones distintas.",
            ]),
        ]),
        ("10. Centro Ejecutivo", [
            ("Objetivo", ["Analizar avance, riesgo, cuotas, bodegas, tiempos y tendencias por operacion."]),
            ("Paso a paso", [
                "Ingrese a Centro Ejecutivo.",
                "Presione Buscar operacion.",
                "Use filtros dinamicos: empresa, guia, producto, chofer y placa.",
                "Presione Generar datos.",
                "Revise KPIs, silueta de buque, cuota vs descargado, tendencia diaria, duracion por camion y alertas.",
            ]),
            ("Lectura ejecutiva", [
                "El sistema estima viajes restantes segun promedio real por camion.",
                "La bodega se descuenta con peso lleno menos peso vacio.",
                "Los graficos deben ajustarse al filtro seleccionado.",
            ]),
        ]),
        ("11. Informes", [
            ("Objetivo", ["Emitir reportes por buque, cliente, producto, bodega, SOF y alertas."]),
            ("Tipos de informe", [
                "Resumen ejecutivo por buque.",
                "SOF con duraciones por categoria.",
                "Cuotas vs descargado.",
                "Descarga por bodega.",
                "Alertas operativas.",
                "Productividad por camion.",
                "Diferencias documentales.",
            ]),
            ("Formatos", [
                "PDF para presentacion.",
                "Excel para analisis.",
                "Word para reporte editable.",
                "CSV para integraciones.",
            ]),
        ]),
        ("12. P.O.R.T.I.A", [
            ("Objetivo", ["Asistente operativo para responder preguntas sobre la operacion, riesgos, clima, puertos, calados, AIS y tiempos."]),
            ("Activacion", [
                "Diga: Oye Portia, Hola Portia, Portia estas ahi o Hey Portia.",
                "Espere confirmacion de escucha.",
                "Haga una pregunta breve y directa.",
                "Para detener: Es todo Portia, Desconectate Portia o Silencio Portia.",
            ]),
            ("Buenas practicas", [
                "Pregunte una cosa a la vez.",
                "Para clima se responde con lenguaje de pronostico.",
                "Para riesgo se usa lenguaje prudente: aparentemente.",
                "PORTIA no reemplaza validacion de capitania, terminal o autoridad local.",
            ]),
        ]),
        ("13. Roles, permisos y seguridad", [
            ("Objetivo", ["Proteger funciones criticas y asegurar que cada usuario vea solo lo necesario."]),
            ("Controles", [
                "Permisos por rol.",
                "Auditoria de aprobaciones, reasignaciones, escaneos y cierres.",
                "QR valido solo si pertenece a operacion, guia, chofer, placa y estado correcto.",
                "Pass hatch/hash no visible para chofer.",
                "Bloqueo por QR usado, guia completa o cuota cumplida.",
            ]),
        ]),
        ("14. Ayuda / Q&A", [
            ("Objetivo", ["Consultar un manual operativo dentro del ERP sin depender de internet ni IA."]),
            ("Uso", [
                "Seleccione tema.",
                "Seleccione vista: guia, FAQ, flujo visual o manual completo.",
                "Escriba una pregunta corta.",
                "Presione Buscar en ayuda.",
            ]),
        ]),
    ],
}


EN = {
    "file": "XTRAVON_ONE_Operational_Manual_EN.pdf",
    "cover_title": "Detailed Operational Manual",
    "cover_sub": "User guide for supervisors, dispatch, yard operators, drivers and clients",
    "intro": [
        "XTRAVON ONE | GRAIN CONTROL centralizes grain port operations: vessel opening, stowage plan, quotas, tickets, QR controls, scans, SOF, trip dispatch, reports and executive analytics.",
        "The purpose of the system is to turn a historically manual operation into a digital, traceable, measurable and auditable workflow that reduces documentation errors, cargo differences and operational risks.",
    ],
    "toc": "Operational index",
    "sections": [
        ("1. Login, roles and initial navigation", [
            ("Purpose", ["Enter the system with the correct profile and prevent users from accessing functions outside their role."]),
            ("Step by step", [
                "Open XTRAVON ONE from the desktop icon or mobile app.",
                "Wait for the splash/loading screen to complete.",
                "Select the operating profile: Supervisor, Yard Operator, Driver or Client.",
                "In production, use personal credentials. Demo users may be enabled for testing.",
                "Confirm that the visible menu matches the selected role.",
            ]),
            ("Validations", [
                "Supervisor: full access to executive center, operations, dispatch, reports, approvals and roles.",
                "Yard Operator: limited access to Yard QR Reader and SOF.",
                "Driver: access to current QR, assigned trips, pending trips and request trips.",
                "Client: access to authorized quotas, discharge and reports.",
            ]),
        ]),
        ("2. Vessel opening, products and stowage plan", [
            ("Purpose", ["Create a vessel operation so tickets, quotas, SOF, QR and reports stay separated by operation."]),
            ("Step by step", [
                "Open Vessel Operations.",
                "Enter the vessel name exactly as it will be used in operational documents.",
                "Select the start date from the calendar.",
                "Add products with the + button. Multiple products may exist in one operation.",
                "Enter hold capacity in MT. Hold 1 is displayed at the bow and the visual order moves aft.",
                "If a hold is split by product or client, add partitions. Partition totals must match hold capacity.",
                "Review the vessel silhouette to confirm capacity and partitions.",
                "Press Open operation. The operation remains OPEN.",
            ]),
            ("Control rules", [
                "An open operation must not mix records from another operation.",
                "Two operations may be open if the business requires it, but each load must be explicitly linked to its operation.",
                "Do not close the operation until discharge, quotas, SOF, QR, reports and differences are validated.",
            ]),
        ]),
        ("3. Client quotas", [
            ("Purpose", ["Control how much each client must withdraw/discharge by client, product and vessel."]),
            ("Step by step", [
                "Select the active operation or the operation to manage.",
                "Add client, quota and unit of measure.",
                "Use + to add N client rows and - to remove rows.",
                "Press Create quotas to save all quotas for the operation.",
                "Use Load active quotas to verify the saved data.",
            ]),
            ("Executive use", [
                "The Executive Center compares quota vs real discharged amount.",
                "The system should alert overquota, shortfall, delayed client and documentation differences.",
                "Quotas also support trip remaining estimates based on real truck average.",
            ]),
        ]),
        ("4. Initial ticket load and controlled QR generation", [
            ("Purpose", ["Load the planned initial tickets and assign them to the correct operation."]),
            ("Step by step", [
                "Open Ticket Loading.",
                "Press Find active operation to confirm the target operation.",
                "Press Open Template. The Excel file opens for editing.",
                "Complete ticket number, company, vessel, date, product, driver, plate, hold and shipment if applicable.",
                "Save the Excel file.",
                "Press Load Excel. Initial records are approved automatically because they belong to the initial plan.",
                "Press Search table to review the loaded records.",
            ]),
            ("Rules", [
                "Initial loading does not go through Approvals.",
                "QR is enabled only for tickets assigned according to dispatch and security rules.",
                "The pass hatch/verification hash must never be shown to the driver.",
            ]),
        ]),
        ("5. Extraordinary approvals", [
            ("Purpose", ["Approve or reject additional tickets that were not part of the initial load."]),
            ("Step by step", [
                "Open Approvals.",
                "Open the extraordinary template.",
                "Load the extraordinary Excel file.",
                "Press View loaded data.",
                "Filter by ticket, company, product, driver or plate.",
                "Mark one, several or all tickets.",
                "Select action: Approve, Reject, Select all or Clear selection.",
                "Add a comment when the decision requires evidence.",
            ]),
            ("Rules", [
                "QR and pass hatch are generated only after approval.",
                "Rejected records must keep comment and responsible user.",
                "The approval must remain audited for traceability.",
            ]),
        ]),
        ("6. Trip Dispatch", [
            ("Purpose", ["Control assignment, continuity, reassignment and trip requests without leaving critical decisions to the driver."]),
            ("Step by step", [
                "Open Trip Dispatch.",
                "Find active operation.",
                "Review boards: requests, assigned, first scan, second scan, third scan, completed, available drivers and active blocks.",
                "To assign, select driver, plate, company and product. The system takes one ticket according to operation rules.",
                "After confirmation, the QR becomes available in the driver app and may be sent via WhatsApp or email.",
                "Use right click or long press in the app for actions: assign, reassign, release, cancel, block or send QR.",
            ]),
            ("Rules", [
                "The ERP may suggest, but dispatch confirms.",
                "If the driver does not continue, pending tickets go to manual reassignment.",
                "Reassignment is manual and controlled by dispatch, not blind automatic assignment.",
            ]),
        ]),
        ("7. Driver portal", [
            ("Purpose", ["Show drivers only what they need to operate without exposing sensitive information."]),
            ("Driver can see", [
                "Current trip QR.",
                "Company, product and driver name.",
                "Assigned trips and pending trips.",
                "Accumulated weight and trip summary.",
            ]),
            ("Driver cannot see", [
                "Pass hatch/verification hash.",
                "Internal audit data.",
                "Other drivers' information.",
                "An open link with the full ticket data.",
            ]),
            ("Cycle completion flow", [
                "When the third scan is completed, the QR is archived.",
                "The app asks whether the driver wants to continue.",
                "If yes, the decision is confirmed and the next assigned QR is displayed.",
                "If no, pending tickets are sent to dispatch for manual reassignment.",
                "If no tickets remain, the driver may press Request trips.",
            ]),
        ]),
        ("8. Yard QR Reader and offline mode", [
            ("Purpose", ["Record the three truck control points even when connectivity is unstable."]),
            ("Scans", [
                "First scan: yard ticket/ficha and tare weight.",
                "Second scan: hopper number.",
                "Third scan: gross weight and seals.",
                "Seals: use + to add all required seal entries and - to remove entries.",
            ]),
            ("Offline", [
                "The handheld saves locally when there is no signal.",
                "Each attempt is queued with date, time, ticket, stage and captured data.",
                "The device retries synchronization automatically when the network returns.",
                "The operation must not stop because the backend or signal is down.",
            ]),
        ]),
        ("9. SOF - Statement of Facts", [
            ("Purpose", ["Record operational events with from/to time, hold, category and description."]),
            ("Step by step", [
                "Open SOF.",
                "The active operation should be selected by default.",
                "Select ticket if the event applies to a specific ticket.",
                "Enter from time and to time.",
                "Select subcategory.",
                "Write the event with operational detail.",
                "Save. In app/handheld it may remain offline and synchronize later.",
            ]),
            ("Best practices", [
                "Record crane, machinery, weather, hold, documentation or safety delays.",
                "Use objective descriptions.",
                "Do not mix events from different operations.",
            ]),
        ]),
        ("10. Executive Center", [
            ("Purpose", ["Analyze progress, risk, quotas, holds, time and trends by operation."]),
            ("Step by step", [
                "Open Executive Center.",
                "Press Find operation.",
                "Use dynamic filters: company, ticket, product, driver and plate.",
                "Press Generate data.",
                "Review KPIs, vessel silhouette, quota vs discharged, daily trend, truck duration and alerts.",
            ]),
            ("Executive reading", [
                "The system estimates remaining trips using real truck average.",
                "Each hold is discounted using gross weight minus tare weight.",
                "Charts must adjust to the selected filters.",
            ]),
        ]),
        ("11. Reports", [
            ("Purpose", ["Issue reports by vessel, client, product, hold, SOF and alerts."]),
            ("Report types", [
                "Executive vessel summary.",
                "SOF with duration by category.",
                "Quota vs discharged.",
                "Discharge by hold.",
                "Operational alerts.",
                "Truck productivity.",
                "Documentation differences.",
            ]),
            ("Formats", ["PDF for presentation.", "Excel for analysis.", "Word for editable reports.", "CSV for integrations."]),
        ]),
        ("12. P.O.R.T.I.A", [
            ("Purpose", ["Operational assistant for questions about operation, risks, weather, ports, drafts, AIS and times."]),
            ("Activation", [
                "Say: Oye Portia, Hola Portia, Portia estas ahi or Hey Portia.",
                "Wait for the listening confirmation.",
                "Ask one clear question.",
                "To stop: Es todo Portia, Desconectate Portia or Silencio Portia.",
            ]),
            ("Best practices", [
                "Ask one thing at a time.",
                "Weather answers use forecast language.",
                "Risk answers use cautious language: apparently.",
                "PORTIA does not replace validation with port authority, terminal or local authority.",
            ]),
        ]),
        ("13. Roles, permissions and security", [
            ("Purpose", ["Protect critical functions and ensure users see only what they need."]),
            ("Controls", [
                "Role-based permissions.",
                "Audit trail for approvals, reassignments, scans and closures.",
                "QR valid only if operation, ticket, driver, plate and state match.",
                "Pass hatch/hash is not visible to the driver.",
                "Blocking by used QR, complete ticket or fulfilled quota.",
            ]),
        ]),
        ("14. Help / Q&A", [
            ("Purpose", ["Consult an operational manual inside the ERP without internet or AI dependency."]),
            ("Use", [
                "Select topic.",
                "Select view: guide, FAQ, visual flow or full manual.",
                "Write a short question.",
                "Press Search help.",
            ]),
        ]),
    ],
}


def add_toc(story, data, st):
    story.append(Paragraph(data["toc"], st["h1"]))
    rows = []
    for i, (title, _blocks) in enumerate(data["sections"], 1):
        rows.append([str(i), title])
    tbl = Table(rows, colWidths=[0.35 * inch, 6.6 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F3F7FA")),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor(PALETTE["atlantic"])),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#D0D7DE")),
    ]))
    story.append(tbl)
    story.append(PageBreak())


def cover(story, data, st):
    splash = ASSET_DIR / "xtravon_splash.png"
    story.append(Spacer(1, 0.15 * inch))
    if splash.exists():
        story.append(RLImage(str(splash), width=6.9 * inch, height=4.1 * inch))
    story.append(Spacer(1, 0.2 * inch))
    cover_tbl = Table(
        [[Paragraph("XTRAVON ONE | GRAIN CONTROL", st["title"])],
         [Paragraph(data["cover_title"], st["cover_note"])],
         [Paragraph(data["cover_sub"], st["subtitle"])]],
        colWidths=[7.0 * inch],
    )
    cover_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(PALETTE["deep"])),
        ("BOX", (0, 0), (-1, -1), 1.5, colors.HexColor(PALETTE["cyan"])),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(cover_tbl)
    story.append(Spacer(1, 0.25 * inch))
    for p in data["intro"]:
        story.append(Paragraph(p, st["body"]))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("QORA SYSTEMS - Alianza con MSL Marine Surveyors and Logistics Group", st["small"]))
    story.append(PageBreak())


def section(story, title, blocks, st):
    story.append(Paragraph(title, st["h1"]))
    for sub, items in blocks:
        story.append(Paragraph(sub, st["h2"]))
        for item in items:
            story.append(Paragraph(f"- {item}", st["body"]))


def add_visuals(story, paths, lang, st):
    story.append(Paragraph("Vistas y flujos visuales" if lang == "ES" else "Screens and visual workflows", st["h1"]))
    story += img_flow(paths["desktop"])
    story.append(Paragraph("Vista supervisor: Centro Ejecutivo con KPIs, filtros dinamicos, silueta del buque, lectura ejecutiva y graficos." if lang == "ES" else "Supervisor view: Executive Center with KPIs, dynamic filters, vessel silhouette, executive reading and charts.", st["caption"]))
    story += img_flow(paths["operation"])
    story.append(Paragraph("Apertura de buque: productos, capacidades por bodega y particiones visibles para evitar mezcla de carga." if lang == "ES" else "Vessel opening: products, hold capacities and visible partitions to avoid cargo mixing.", st["caption"]))
    story += img_flow(paths["dispatch"])
    story.append(Paragraph("Despacho: tablero por estado del viaje con asignacion confirmada por operador." if lang == "ES" else "Dispatch: trip status board with assignment confirmed by operator.", st["caption"]))
    story.append(PageBreak())
    mobile_tbl = Table(
        [[RLImage(str(paths["handheld"]), width=3.25 * inch, height=3.55 * inch),
          RLImage(str(paths["driver"]), width=3.25 * inch, height=3.55 * inch)]],
        colWidths=[3.45 * inch, 3.45 * inch],
    )
    mobile_tbl.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    story.append(mobile_tbl)
    story.append(Paragraph("Handheld operador de patio y portal del chofer: ambos deben mantener margenes adaptados al dispositivo y operar con la informacion estrictamente necesaria." if lang == "ES" else "Yard handheld and driver portal: both must fit device margins and expose only the information required.", st["caption"]))
    story += img_flow(paths["sof"])
    story.append(Paragraph("SOF, Informes y P.O.R.T.I.A: registros, reportes exportables y asistencia operativa interactiva." if lang == "ES" else "SOF, Reports and P.O.R.T.I.A: event records, exportable reports and interactive operational assistance.", st["caption"]))


def add_section_visual(story, paths, lang, section_number, st):
    visual_map = {
        2: ("operation", "Vista de apertura de buque, bodegas y particiones." if lang == "ES" else "Vessel opening, holds and partitions view."),
        4: ("operation", "La carga inicial queda ligada a la operacion abierta y no pasa por aprobacion extraordinaria." if lang == "ES" else "Initial loading is linked to the open operation and does not go through extraordinary approval."),
        5: ("dispatch", "Las guias extraordinarias requieren aprobacion antes de generar QR." if lang == "ES" else "Extraordinary tickets require approval before QR generation."),
        6: ("dispatch", "Tablero de despacho: solicitudes, asignadas, escaneos, completadas y bloqueos." if lang == "ES" else "Dispatch board: requests, assigned, scans, completed records and blocks."),
        7: ("driver", "Portal chofer: solo QR vigente, empresa, producto, viajes y acumulado." if lang == "ES" else "Driver portal: only current QR, company, product, trips and accumulated weight."),
        8: ("handheld", "Handheld patio: captura operativa y cola offline cuando no hay red." if lang == "ES" else "Yard handheld: operational capture and offline queue when network is unavailable."),
        9: ("sof", "SOF se registra por operacion, hora desde/hasta, bodega, categoria y evento." if lang == "ES" else "SOF is recorded by operation, from/to time, hold, category and event."),
        10: ("desktop", "Centro Ejecutivo consolida KPIs, graficos, avance por bodega y lectura ejecutiva." if lang == "ES" else "Executive Center consolidates KPIs, charts, hold progress and executive reading."),
        11: ("sof", "Informes exportables con graficos, KPIs y analisis segun tipo de reporte." if lang == "ES" else "Exportable reports with charts, KPIs and analysis according to report type."),
        12: ("sof", "P.O.R.T.I.A responde consultas operativas, clima, riesgos, puertos y tiempos." if lang == "ES" else "P.O.R.T.I.A answers operational, weather, risk, port and time questions."),
    }
    if section_number not in visual_map:
        return
    key, caption = visual_map[section_number]
    width = 5.8 * inch if key in ("handheld", "driver") else 6.45 * inch
    story.append(Spacer(1, 4))
    story += img_flow(paths[key], width=width)
    story.append(Paragraph(caption, st["caption"]))


def add_checklists(story, lang, st):
    story.append(PageBreak())
    story.append(Paragraph("Checklists operativos" if lang == "ES" else "Operational checklists", st["h1"]))
    if lang == "ES":
        rows = [
            ["Antes de operar", "Buque abierto, productos correctos, bodegas revisadas, cuotas creadas, usuarios/roles validados."],
            ["Antes de cargar guias", "Operacion correcta seleccionada, template actualizado, chofer y placa completos, bodega y embarque si aplican."],
            ["Antes de despacho", "Guias asignadas, QR habilitado, chofer/placa no bloqueado, cuota y producto disponibles."],
            ["Durante patio", "Primer escaneo con peso vacio/ficha, segundo con tolva, tercero con peso lleno/marchamos."],
            ["Modo offline", "Confirmar que la app muestra pendiente local y sincroniza al recuperar red."],
            ["Cierre", "Cuotas revisadas, SOF completo, informes generados, diferencias documentales resueltas."],
        ]
    else:
        rows = [
            ["Before operation", "Vessel open, products correct, holds reviewed, quotas created, users/roles validated."],
            ["Before ticket load", "Correct operation selected, template updated, driver and plate complete, hold and shipment if applicable."],
            ["Before dispatch", "Tickets assigned, QR enabled, driver/plate not blocked, quota and product available."],
            ["During yard process", "First scan with tare/ficha, second with hopper, third with gross/seals."],
            ["Offline mode", "Confirm the app shows local pending records and syncs when network returns."],
            ["Closing", "Quotas reviewed, SOF complete, reports generated, documentation differences resolved."],
        ]
    tbl = Table([[Paragraph("<b>" + a + "</b>", st["body"]), Paragraph(b, st["body"])] for a, b in rows], colWidths=[1.7 * inch, 5.2 * inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EAFBFF")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#B9C7D4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(tbl)


def build_manual(lang, images):
    data = ES if lang == "ES" else EN
    st = styles()
    output = OUT / data["file"]
    doc = SimpleDocTemplate(
        str(output),
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=48,
        bottomMargin=36,
        title=data["cover_title"],
        author="QORA SYSTEMS",
    )
    story = []
    cover(story, data, st)
    add_toc(story, data, st)
    # Insert visual overview early so the manual feels practical.
    add_visuals(story, images[lang], lang, st)
    story.append(PageBreak())
    for idx, (title, blocks) in enumerate(data["sections"], 1):
        section(story, title, blocks, st)
        add_section_visual(story, images[lang], lang, idx, st)
    add_checklists(story, lang, st)
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    return output


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    images = make_all_images()
    outputs = [build_manual("ES", images), build_manual("EN", images)]
    for out in outputs:
        print(out)


if __name__ == "__main__":
    main()
