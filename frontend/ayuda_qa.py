import tkinter as tk
from tkinter import ttk


HELP_SECTIONS = [
    {
        "title": "1. Logueo y perfiles",
        "keywords": ["login", "logueo", "perfil", "usuario", "contraseña", "ingreso"],
        "steps": [
            "Abra XTRAVON ONE y espere la pantalla de carga.",
            "Seleccione el perfil correcto: Supervisor, Operador patio, Cliente o Chofer.",
            "En produccion, use credenciales asignadas por roles y permisos.",
            "Valide que el menu corresponda al rol antes de iniciar una operacion.",
        ],
        "notes": [
            "Operador patio solo debe usar Lector QR Patio y SOF.",
            "Chofer solo debe ver su QR activo y viajes propios.",
            "Supervisor tiene acceso operativo completo segun permisos.",
        ],
    },
    {
        "title": "2. Apertura de buque",
        "keywords": ["abrir buque", "apertura", "operacion", "productos", "bodega", "stowage"],
        "steps": [
            "Ingrese a Operaciones Buque.",
            "Digite nombre del buque y seleccione fecha de inicio.",
            "Agregue productos con el boton +.",
            "Ingrese capacidad por bodega en MT.",
            "Si una bodega esta partida, agregue particiones por producto o cliente.",
            "Revise la silueta del buque y presione Abrir operacion.",
            "Confirme que la operacion quede en estado ABIERTA.",
        ],
        "notes": [
            "El stowage plan debe coincidir con bodegas, productos y capacidades reales.",
            "Puede haber mas de una operacion abierta si el negocio lo requiere.",
        ],
    },
    {
        "title": "3. Cuotas por cliente",
        "keywords": ["cuotas", "cliente", "empresa", "producto", "mt", "kg", "lb"],
        "steps": [
            "Seleccione la operacion activa.",
            "Ingrese cliente, cuota y unidad.",
            "Use + para agregar N lineas de clientes.",
            "Use - para quitar lineas incorrectas.",
            "Presione Crear cuotas y luego Cargar cuotas activas para validar.",
        ],
        "notes": [
            "Las cuotas controlan descargado, pendiente y sobrecuota.",
            "Las cuotas son por operacion, cliente y producto.",
        ],
    },
    {
        "title": "4. Carga inicial de guias y choferes",
        "keywords": ["boletas", "template", "excel", "guias", "qr", "chofer", "placa"],
        "steps": [
            "Ingrese a Carga de Boletas.",
            "Presione Buscar operacion activa.",
            "Abra el template y complete guia, empresa, buque, fecha, producto, chofer, placa, bodega y embarque si aplica.",
            "Guarde el Excel y presione Cargar Excel.",
            "Use Cargar Tabla para consultar registros.",
            "La carga inicial queda aprobada automaticamente porque pertenece al arranque controlado.",
        ],
        "notes": [
            "La entrega y asignacion de QR se gestiona desde Despacho de Viajes.",
            "Las guias extraordinarias posteriores deben pasar por Aprobaciones.",
        ],
    },
    {
        "title": "5. Aprobaciones extraordinarias",
        "keywords": ["aprobaciones", "aprobar", "rechazar", "pending", "pendientes", "extraordinarias"],
        "steps": [
            "Use Aprobaciones solo para guias extraordinarias no incluidas en la carga inicial.",
            "Abra template, complete guias y cargue Excel.",
            "Presione Ver datos cargados para mostrar PENDING.",
            "Marque registros o seleccione todo.",
            "Aplique Aprobar o Rechazar y agregue comentario si corresponde.",
            "Al aprobar, se genera QR y pass hatch.",
        ],
        "notes": [
            "PENDING significa pendiente de revision.",
            "Rechazos deben conservar comentario de auditoria.",
        ],
    },
    {
        "title": "6. Despacho de Viajes",
        "keywords": ["despacho", "viajes", "asignar", "reasignar", "whatsapp", "correo", "solicitud"],
        "steps": [
            "Ingrese a Despacho de Viajes y busque operacion activa.",
            "Revise solicitudes, guias asignadas, primer escaneo, segundo escaneo, tercer escaneo, completadas y bloqueos.",
            "Seleccione chofer, placa, cliente y producto.",
            "Confirme asignacion manualmente.",
            "El sistema habilita QR y puede enviarlo por app, WhatsApp o correo si esta configurado.",
            "Si un chofer no continua, sus guias pendientes quedan para reasignacion manual.",
        ],
        "notes": [
            "El ERP propone, despacho confirma.",
            "No debe existir autoasignacion ciega.",
        ],
    },
    {
        "title": "7. Lector QR Patio",
        "keywords": ["lector", "qr", "patio", "primer escaneo", "segundo escaneo", "tercer escaneo", "marchamos"],
        "steps": [
            "Operador patio abre Lector QR Patio.",
            "Primer escaneo: ficha y peso vacio.",
            "Segundo escaneo: numero de tolva.",
            "Tercer escaneo: peso lleno y marchamos.",
            "Use + para agregar marchamos y - para eliminar uno incorrecto.",
            "Si no hay señal, la app guarda local y sincroniza cuando vuelve la conexion.",
        ],
        "notes": [
            "El QR completado no debe permitir nuevos escaneos.",
            "QR invalido debe generar alerta visible y trazabilidad.",
        ],
    },
    {
        "title": "8. SOF - Statement of Facts",
        "keywords": ["sof", "statement", "evento", "demora", "clima", "bodega", "offline"],
        "steps": [
            "Ingrese a SOF.",
            "La operacion abierta debe cargarse por defecto.",
            "Seleccione fecha, hora desde y hora hasta.",
            "Seleccione categoria, subcategoria y bodega si aplica.",
            "Escriba el evento y guarde.",
            "Si esta offline, el SOF queda en memoria y se sincroniza luego.",
        ],
        "notes": [
            "SOF es evidencia operacional.",
            "Indique causa, duracion, bodega y efecto.",
        ],
    },
    {
        "title": "9. Centro Ejecutivo e Informes",
        "keywords": ["centro ejecutivo", "dashboard", "kpi", "graficos", "informes", "pdf", "excel"],
        "steps": [
            "Ingrese a Centro Ejecutivo.",
            "Busque operacion y cargue filtros.",
            "Filtre por empresa, guia, producto, chofer o placa.",
            "Presione Generar datos.",
            "Revise KPIs, silueta del buque, cuotas vs descargado, tendencia y alertas.",
            "En Informes seleccione operacion, tipo de reporte y formato de descarga.",
        ],
        "notes": [
            "Los datos no cargan solos para evitar lag.",
            "Cada reporte debe responder a una necesidad distinta.",
        ],
    },
    {
        "title": "10. Liquidaciones Choferes",
        "keywords": [
            "liquidaciones",
            "liquidacion",
            "choferes",
            "chofer",
            "viajes",
            "mt",
            "descargado",
            "empresa",
            "producto",
            "placa",
            "guia",
            "exportar",
            "pago",
        ],
        "steps": [
            "Ingrese a Liquidaciones Choferes.",
            "Presione Buscar operacion para cargar operaciones y filtros disponibles.",
            "Seleccione la operacion que desea liquidar.",
            "Filtre por empresa, producto, chofer, placa, guia o rango de fechas si aplica.",
            "Presione Generar liquidacion.",
            "Revise KPIs: guias asignadas, completadas, pendientes, MT descargadas, duracion total, promedio de viaje, choferes y empresas.",
            "Revise graficos de MT por chofer, MT por empresa y MT por producto.",
            "Use la tabla Detalle de liquidacion para auditar guia por guia.",
            "Use filtros tipo Excel dentro de la tabla para seleccionar varios valores o escribir texto de busqueda.",
            "Exporte a Excel o PDF segun el cierre requerido por administracion.",
        ],
        "notes": [
            "MT descargadas debe calcularse como peso lleno menos peso vacio, sumado por guia completada.",
            "La liquidacion debe filtrarse por operacion_id para no mezclar buques.",
            "Sirve para pago, productividad, auditoria y conciliacion por chofer, empresa y producto.",
            "No reemplaza Despacho de Viajes ni Centro Ejecutivo; es un modulo de cierre administrativo.",
        ],
    },
    {
        "title": "11. P.O.R.T.I.A",
        "keywords": ["portia", "ia", "voz", "clima", "calado", "riesgos", "buque"],
        "steps": [
            "Diga Oye Portia, Hola Portia o Portia estas ahi.",
            "Espere confirmacion de voz.",
            "Haga una pregunta corta y clara.",
            "Para detener diga Es todo Portia, Desconectate Portia o Silencio Portia.",
            "Use la pantalla P.O.R.T.I.A para analisis mas completo.",
        ],
        "notes": [
            "Para clima usa criterio de pronostico.",
            "Para riesgos usa lenguaje prudente como aparentemente.",
        ],
    },
]


FAQ_ITEMS = [
    {
        "question": "Como abro una operacion de buque?",
        "answer": [
            "Entre a Operaciones Buque.",
            "Complete buque, fecha, productos, bodegas y particiones si aplica.",
            "Revise la silueta y presione Abrir operacion.",
        ],
        "keywords": ["abrir", "operacion", "buque", "bodega", "stowage"],
    },
    {
        "question": "Cuando uso Aprobaciones?",
        "answer": [
            "Solo para guias extraordinarias cargadas despues de la carga inicial.",
            "La carga inicial de una operacion queda aprobada automaticamente.",
            "Las extraordinarias quedan PENDING hasta aprobar o rechazar.",
        ],
        "keywords": ["aprobaciones", "pending", "extraordinaria", "aprobar", "rechazar"],
    },
    {
        "question": "Como funciona el QR del chofer?",
        "answer": [
            "El chofer ve solo un QR activo por ciclo.",
            "Cuando completa los escaneos, el QR se archiva.",
            "Si tiene otra guia asignada, se le pregunta si continua antes de mostrar el siguiente QR.",
        ],
        "keywords": ["qr", "chofer", "viaje", "ciclo", "continuar"],
    },
    {
        "question": "Que hago si no hay conexion en patio?",
        "answer": [
            "El operador puede seguir escaneando desde handheld.",
            "La lectura queda guardada en memoria local.",
            "Cuando vuelve internet, la app sincroniza automaticamente.",
        ],
        "keywords": ["offline", "conexion", "sin internet", "handheld", "sincronizar"],
    },
    {
        "question": "Como registro un SOF?",
        "answer": [
            "Entre a SOF.",
            "La operacion abierta se carga por defecto.",
            "Complete fecha, hora desde/hasta, categoria, subcategoria y evento.",
            "Guarde. Si esta offline en app, se sincroniza luego.",
        ],
        "keywords": ["sof", "evento", "demora", "statement", "facts"],
    },
    {
        "question": "Como uso Centro Ejecutivo?",
        "answer": [
            "Busque la operacion.",
            "Cargue filtros si necesita filtrar por empresa, guia, producto, chofer o placa.",
            "Presione Generar datos para construir KPIs y graficos.",
        ],
        "keywords": ["centro", "ejecutivo", "dashboard", "kpi", "graficos", "filtros"],
    },
    {
        "question": "Como genero una liquidacion de chofer?",
        "answer": [
            "Entre a Liquidaciones Choferes.",
            "Presione Buscar operacion y seleccione el buque correcto.",
            "Filtre por empresa, producto, chofer, placa, guia o fechas.",
            "Presione Generar liquidacion y revise KPIs, graficos y detalle guia por guia.",
            "Exporte a Excel o PDF cuando el resultado este validado.",
        ],
        "keywords": ["liquidacion", "liquidaciones", "chofer", "choferes", "viajes", "pago", "mt"],
    },
]


def install_ayuda_qa_screen(app_class):
    app_class.show_ayuda_qa = show_ayuda_qa
    app_class.ayuda_buscar = ayuda_buscar
    app_class.ayuda_render = ayuda_render
    app_class.ayuda_render_indice = ayuda_render_indice
    app_class.ayuda_render_faq = ayuda_render_faq
    app_class.ayuda_render_tema = ayuda_render_tema
    app_class.ayuda_render_flujo = ayuda_render_flujo
    app_class.ayuda_aplicar_selector = ayuda_aplicar_selector
    app_class.ayuda_dibujar_visual = ayuda_dibujar_visual


def normalize(text):
    return str(text or "").lower().strip()


def buscar_secciones(query):
    query = normalize(query)
    if not query:
        return HELP_SECTIONS
    tokens = [token for token in query.split() if token]
    scored = []
    for section in HELP_SECTIONS:
        haystack = normalize(" ".join([
            section["title"],
            " ".join(section["keywords"]),
            " ".join(section["steps"]),
            " ".join(section["notes"]),
        ]))
        score = sum(1 for token in tokens if token in haystack)
        if score:
            scored.append((score, section))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [section for _score, section in scored]


def buscar_faq(query):
    query = normalize(query)
    if not query:
        return FAQ_ITEMS
    tokens = [token for token in query.split() if token]
    scored = []
    for item in FAQ_ITEMS:
        haystack = normalize(" ".join([
            item["question"],
            " ".join(item["answer"]),
            " ".join(item["keywords"]),
        ]))
        score = sum(1 for token in tokens if token in haystack)
        if score:
            scored.append((score, item))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [item for _score, item in scored]


def show_ayuda_qa(self):
    self.clear_content()
    self.highlight_sidebar_button("Ayuda / Q&A")
    self.ayuda_query_var = tk.StringVar()
    self.ayuda_topic_var = tk.StringVar(value=HELP_SECTIONS[0]["title"])
    self.ayuda_view_var = tk.StringVar(value="Guia paso a paso")
    self.ayuda_result_text = None
    self.ayuda_visual_canvas = None
    self.ayuda_visual_mode = "indice"

    self.create_page_title(
        self.content,
        "Ayuda / Q&A",
        "Manual operativo paso a paso. Responde desde la guia de uso, no desde P.O.R.T.I.A.",
    )

    wrapper = tk.Frame(self.content, bg=self.colors["bg_main"])
    wrapper.pack(fill="both", expand=True, padx=25, pady=(0, 20))

    panel = tk.Frame(wrapper, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    panel.pack(fill="x", pady=(0, 10))
    tk.Label(
        panel,
        text="Centro de ayuda operativo",
        font=("Segoe UI", 13, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors["text_dark"],
    ).pack(anchor="w", padx=14, pady=(12, 6))

    selector = tk.Frame(panel, bg=self.colors["bg_card"])
    selector.pack(fill="x", padx=14, pady=(0, 10))
    selector.grid_columnconfigure(0, weight=2)
    selector.grid_columnconfigure(1, weight=1)
    selector.grid_columnconfigure(2, weight=2)

    tk.Label(
        selector,
        text="Tema",
        font=("Segoe UI", 9, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors["text_dark"],
    ).grid(row=0, column=0, sticky="w", padx=(0, 8))
    tk.Label(
        selector,
        text="Vista",
        font=("Segoe UI", 9, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors["text_dark"],
    ).grid(row=0, column=1, sticky="w", padx=(0, 8))
    tk.Label(
        selector,
        text="Pregunta rapida",
        font=("Segoe UI", 9, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors["text_dark"],
    ).grid(row=0, column=2, sticky="w", padx=(0, 8))

    topic_combo = ttk.Combobox(
        selector,
        textvariable=self.ayuda_topic_var,
        values=[section["title"] for section in HELP_SECTIONS],
        state="readonly",
    )
    topic_combo.grid(row=1, column=0, sticky="ew", padx=(0, 8))
    topic_combo.bind("<<ComboboxSelected>>", lambda _event: self.ayuda_aplicar_selector())

    view_combo = ttk.Combobox(
        selector,
        textvariable=self.ayuda_view_var,
        values=["Guia paso a paso", "FAQ del tema", "Flujo visual", "Manual completo"],
        state="readonly",
        width=18,
    )
    view_combo.grid(row=1, column=1, sticky="ew", padx=(0, 8))
    view_combo.bind("<<ComboboxSelected>>", lambda _event: self.ayuda_aplicar_selector())

    entry = ttk.Entry(selector, textvariable=self.ayuda_query_var)
    entry.grid(row=1, column=2, sticky="ew", padx=(0, 8))
    entry.bind("<Return>", lambda _event: self.ayuda_buscar())

    actions = tk.Frame(panel, bg=self.colors["bg_card"])
    actions.pack(fill="x", padx=14, pady=(0, 12))
    ttk.Button(actions, text="Buscar en ayuda", style="Olive.TButton", command=self.ayuda_buscar).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Ver indice ejecutivo", style="Gray.TButton", command=self.ayuda_render_indice).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="FAQ general", style="Gray.TButton", command=self.ayuda_render_faq).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Limpiar", style="Gray.TButton", command=lambda: [self.ayuda_query_var.set(""), self.ayuda_render_indice()]).pack(side="left")

    content_panel = tk.Frame(wrapper, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    content_panel.pack(fill="both", expand=True)

    visual_panel = tk.Frame(content_panel, bg=self.colors["bg_card"])
    visual_panel.pack(fill="x", padx=14, pady=(14, 0))
    self.ayuda_visual_canvas = tk.Canvas(
        visual_panel,
        height=120,
        bg=self.colors["bg_card"],
        highlightthickness=0,
    )
    self.ayuda_visual_canvas.pack(fill="x", expand=True)
    self.ayuda_visual_canvas.bind("<Configure>", lambda _event: self.ayuda_dibujar_visual())

    text_frame = tk.Frame(content_panel, bg=self.colors["bg_card"])
    text_frame.pack(fill="both", expand=True, padx=14, pady=14)

    self.ayuda_result_text = tk.Text(
        text_frame,
        wrap="word",
        font=("Segoe UI", 10),
        bg=self.colors["bg_main"],
        fg=self.colors["text_dark"],
        insertbackground=self.colors["accent"],
        selectbackground=self.colors["accent"],
        selectforeground=self.colors["text_light"],
        relief="flat",
    )
    y = ttk.Scrollbar(text_frame, orient="vertical", command=self.ayuda_result_text.yview)
    self.ayuda_result_text.configure(yscrollcommand=y.set)
    self.ayuda_result_text.pack(side="left", fill="both", expand=True)
    y.pack(side="right", fill="y")

    self.ayuda_render_indice()


def ayuda_buscar(self):
    query = self.ayuda_query_var.get().strip()
    matches = buscar_secciones(query)
    faq_matches = buscar_faq(query)
    if not matches:
        self.ayuda_result_text.delete("1.0", "end")
        self.ayuda_result_text.insert(
            "1.0",
            "No encontre ese punto exacto.\n\n"
            "Pruebe con palabras como apertura, cuotas, QR, SOF, despacho, aprobaciones, informes, liquidaciones, handheld, chofer o PORTIA.",
        )
        return
    self.ayuda_render(matches[:3] if query else matches, faq_matches[:3] if query else None)


def ayuda_aplicar_selector(self):
    selected = next(
        (section for section in HELP_SECTIONS if section["title"] == self.ayuda_topic_var.get()),
        HELP_SECTIONS[0],
    )
    view = self.ayuda_view_var.get()
    if view == "FAQ del tema":
        related = buscar_faq(" ".join(selected["keywords"]))
        self.ayuda_visual_mode = "faq"
        self.ayuda_render([selected], related[:4])
    elif view == "Flujo visual":
        self.ayuda_render_flujo(selected)
    elif view == "Manual completo":
        self.ayuda_visual_mode = "manual"
        self.ayuda_render(HELP_SECTIONS)
    else:
        self.ayuda_render_tema(selected)


def ayuda_render_indice(self):
    if self.ayuda_result_text is None:
        return
    self.ayuda_visual_mode = "indice"
    lines = [
        "XTRAVON ONE | Indice ejecutivo de ayuda",
        "",
        "Use el selector de Tema para navegar sin llenar la pantalla de botones.",
        "Use Vista para cambiar entre guia paso a paso, FAQ del tema, flujo visual o manual completo.",
        "",
        "Temas disponibles:",
    ]
    for section in HELP_SECTIONS:
        lines.append(f"- {section['title']}: {', '.join(section['keywords'][:4])}")
    lines.extend([
        "",
        "Preguntas frecuentes:",
    ])
    for item in FAQ_ITEMS:
        lines.append(f"- {item['question']}")
    self.ayuda_result_text.delete("1.0", "end")
    self.ayuda_result_text.insert("1.0", "\n".join(lines))
    self.ayuda_dibujar_visual()


def ayuda_render_faq(self):
    if self.ayuda_result_text is None:
        return
    self.ayuda_visual_mode = "faq"
    lines = ["XTRAVON ONE | Preguntas frecuentes", ""]
    for item in FAQ_ITEMS:
        lines.append(item["question"])
        lines.append("-" * len(item["question"]))
        for idx, answer in enumerate(item["answer"], start=1):
            lines.append(f"{idx}. {answer}")
        lines.append("")
    self.ayuda_result_text.delete("1.0", "end")
    self.ayuda_result_text.insert("1.0", "\n".join(lines))
    self.ayuda_dibujar_visual()


def ayuda_render_tema(self, section):
    if hasattr(self, "ayuda_topic_var"):
        self.ayuda_topic_var.set(section["title"])
    self.ayuda_visual_mode = "tema"
    self.ayuda_render([section])


def ayuda_render_flujo(self, section):
    if self.ayuda_result_text is None:
        return
    if hasattr(self, "ayuda_topic_var"):
        self.ayuda_topic_var.set(section["title"])
    self.ayuda_visual_mode = "flujo"
    lines = [
        f"XTRAVON ONE | Flujo visual: {section['title'].split('. ', 1)[-1]}",
        "",
        "La parte superior resume el proceso en tarjetas secuenciales.",
        "Use esta vista para explicar rapidamente que ocurre antes, durante y despues de cada modulo.",
        "",
        "Secuencia operativa:",
    ]
    for idx, step in enumerate(section["steps"], start=1):
        lines.append(f"{idx}. {step}")
    lines.extend(["", "Puntos de control:"])
    for note in section["notes"]:
        lines.append(f"- {note}")
    self.ayuda_result_text.delete("1.0", "end")
    self.ayuda_result_text.insert("1.0", "\n".join(lines))
    self.ayuda_dibujar_visual()


def ayuda_render(self, sections, faq_sections=None):
    if self.ayuda_result_text is None:
        return
    if getattr(self, "ayuda_visual_mode", None) not in ("faq", "manual"):
        self.ayuda_visual_mode = "tema"
    lines = [
        "XTRAVON ONE | Manual operativo",
        "",
        "Esta ayuda responde con pasos del manual. No consulta IA ni internet.",
        "",
    ]
    for section in sections:
        lines.append(section["title"])
        lines.append("-" * len(section["title"]))
        lines.append("Pasos:")
        for idx, step in enumerate(section["steps"], start=1):
            lines.append(f"{idx}. {step}")
        lines.append("")
        lines.append("Validaciones:")
        for note in section["notes"]:
            lines.append(f"- {note}")
        lines.append("")
    if faq_sections:
        lines.append("Preguntas frecuentes relacionadas")
        lines.append("---------------------------------")
        for item in faq_sections:
            lines.append(item["question"])
            for idx, answer in enumerate(item["answer"], start=1):
                lines.append(f"{idx}. {answer}")
            lines.append("")
    self.ayuda_result_text.delete("1.0", "end")
    self.ayuda_result_text.insert("1.0", "\n".join(lines))
    self.ayuda_dibujar_visual()


def ayuda_dibujar_visual(self):
    canvas = getattr(self, "ayuda_visual_canvas", None)
    if canvas is None:
        return
    canvas.delete("all")
    width = max(canvas.winfo_width(), 900)
    height = max(canvas.winfo_height(), 120)
    bg = self.colors["bg_card"]
    accent = self.colors["accent"]
    info = self.colors.get("info", "#7C8DA6")
    success = self.colors.get("success", "#7A9E7E")
    warning = self.colors.get("warning", "#C97B63")
    text = self.colors["text_dark"]
    card = self.colors["bg_main"]

    mode = getattr(self, "ayuda_visual_mode", "tema")
    if mode == "indice":
        blocks = [
            ("1", "Ingreso", "Rol y acceso"),
            ("2", "Operacion", "Buque, bodegas, cuotas"),
            ("3", "Guias", "Carga, despacho y QR"),
            ("4", "Campo", "Escaneos, SOF y offline"),
            ("5", "Control", "KPIs, informes, liquidaciones y PORTIA"),
        ]
        colors = [accent, info, success, warning, self.colors.get("danger", "#B15C4A")]
        canvas.create_rectangle(0, 0, width, height, fill=bg, outline="")
        canvas.create_text(12, 12, text="Mapa ejecutivo del sistema", anchor="nw", fill=text, font=("Segoe UI", 10, "bold"))
        usable_w = max(width - 40, 500)
        box_w = max(min((usable_w - ((len(blocks) - 1) * 20)) / len(blocks), 215), 130)
        x = 20
        y = 44
        for idx, (num, title, subtitle) in enumerate(blocks):
            fill = colors[idx % len(colors)]
            canvas.create_rectangle(x, y, x + box_w, y + 54, fill=card, outline=fill, width=2)
            canvas.create_text(x + 12, y + 10, text=f"{num}. {title}", anchor="nw", fill=text, font=("Segoe UI", 9, "bold"))
            canvas.create_text(x + 12, y + 30, text=subtitle, anchor="nw", fill=text, font=("Segoe UI", 8), width=box_w - 20)
            if idx < len(blocks) - 1:
                canvas.create_line(x + box_w + 3, y + 27, x + box_w + 17, y + 27, fill=fill, width=2, arrow="last")
            x += box_w + 20
        return

    if mode == "faq":
        canvas.create_rectangle(0, 0, width, height, fill=bg, outline="")
        canvas.create_text(12, 12, text="FAQ operativo: pregunta -> accion -> validacion", anchor="nw", fill=text, font=("Segoe UI", 10, "bold"))
        blocks = [("Pregunta", "Identifique la duda"), ("Accion", "Siga los pasos"), ("Validacion", "Confirme el resultado")]
        colors = [accent, info, success]
        usable_w = max(width - 40, 450)
        box_w = max(min((usable_w - 48) / 3, 250), 150)
        x = 20
        y = 46
        for idx, (title, subtitle) in enumerate(blocks):
            fill = colors[idx]
            canvas.create_rectangle(x, y, x + box_w, y + 48, fill=card, outline=fill, width=2)
            canvas.create_text(x + 12, y + 9, text=title, anchor="nw", fill=text, font=("Segoe UI", 9, "bold"))
            canvas.create_text(x + 12, y + 28, text=subtitle, anchor="nw", fill=text, font=("Segoe UI", 8))
            if idx < len(blocks) - 1:
                canvas.create_line(x + box_w + 5, y + 24, x + box_w + 19, y + 24, fill=fill, width=2, arrow="last")
            x += box_w + 24
        return

    selected_title = getattr(self, "ayuda_topic_var", tk.StringVar(value=HELP_SECTIONS[0]["title"])).get()
    selected = next((section for section in HELP_SECTIONS if section["title"] == selected_title), HELP_SECTIONS[0])
    steps = selected["steps"][:4]
    if not steps:
        return

    canvas.create_rectangle(0, 0, width, height, fill=bg, outline="")
    canvas.create_text(
        12,
        12,
        text=f"Flujo visual: {selected['title'].split('. ', 1)[-1]}",
        anchor="nw",
        fill=text,
        font=("Segoe UI", 10, "bold"),
    )

    colors = [accent, info, success, warning]
    usable_w = max(width - 40, 400)
    box_w = max(min((usable_w - ((len(steps) - 1) * 24)) / len(steps), 245), 150)
    x = 20
    y = 42
    for idx, step in enumerate(steps, start=1):
        fill = colors[(idx - 1) % len(colors)]
        canvas.create_rectangle(x, y, x + box_w, y + 58, fill=card, outline=fill, width=2)
        canvas.create_oval(x + 10, y + 12, x + 36, y + 38, fill=fill, outline="")
        canvas.create_text(x + 23, y + 25, text=str(idx), fill="#FFFFFF", font=("Segoe UI", 9, "bold"))
        canvas.create_text(
            x + 46,
            y + 12,
            text=step[:58] + ("..." if len(step) > 58 else ""),
            anchor="nw",
            fill=text,
            font=("Segoe UI", 8, "bold"),
            width=max(box_w - 54, 80),
        )
        if idx < len(steps):
            canvas.create_line(x + box_w + 4, y + 29, x + box_w + 20, y + 29, fill=fill, width=2, arrow="last")
        x += box_w + 24
