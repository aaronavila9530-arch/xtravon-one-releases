import tkinter as tk
from tkinter import messagebox, ttk


def install_gestion_profesional_screen(app_class):
    app_class.show_gestion_profesional = show_gestion_profesional
    app_class.api_get_gestion_resumen = api_get_gestion_resumen
    app_class.api_get_matriz_cumplimiento = api_get_matriz_cumplimiento
    app_class.api_get_gestion_reclamos = api_get_gestion_reclamos
    app_class.api_crear_gestion_reclamo = api_crear_gestion_reclamo
    app_class.api_actualizar_gestion_reclamo = api_actualizar_gestion_reclamo
    app_class.api_get_gestion_auditoria = api_get_gestion_auditoria
    app_class.api_get_portal_cliente = api_get_portal_cliente
    app_class.api_get_evidencias = api_get_evidencias
    app_class.api_crear_evidencia = api_crear_evidencia
    app_class.api_actualizar_evidencia = api_actualizar_evidencia
    app_class.gestion_cargar_operaciones = gestion_cargar_operaciones
    app_class.gestion_buscar_resumen = gestion_buscar_resumen
    app_class.gestion_evaluar_cumplimiento = gestion_evaluar_cumplimiento
    app_class.gestion_cargar_reclamos = gestion_cargar_reclamos
    app_class.gestion_guardar_reclamo = gestion_guardar_reclamo
    app_class.gestion_editar_reclamo = gestion_editar_reclamo
    app_class.gestion_cargar_auditoria = gestion_cargar_auditoria
    app_class.gestion_cargar_portal_cliente = gestion_cargar_portal_cliente
    app_class.gestion_cargar_evidencias = gestion_cargar_evidencias
    app_class.gestion_guardar_evidencia = gestion_guardar_evidencia
    app_class.gestion_editar_evidencia = gestion_editar_evidencia
    app_class.gestion_limpiar_evidencia = gestion_limpiar_evidencia
    app_class.api_get_alertas_reglas = api_get_alertas_reglas
    app_class.api_crear_alerta_regla = api_crear_alerta_regla
    app_class.api_evaluar_alertas = api_evaluar_alertas
    app_class.api_get_acciones = api_get_acciones
    app_class.api_crear_accion = api_crear_accion
    app_class.api_get_decisiones = api_get_decisiones
    app_class.api_crear_decision = api_crear_decision
    app_class.api_get_notificaciones = api_get_notificaciones
    app_class.api_crear_notificacion = api_crear_notificacion
    app_class.api_marcar_notificacion_enviada = api_marcar_notificacion_enviada
    app_class.gestion_cargar_reglas_alerta = gestion_cargar_reglas_alerta
    app_class.gestion_evaluar_alertas = gestion_evaluar_alertas
    app_class.gestion_cargar_acciones = gestion_cargar_acciones
    app_class.gestion_crear_accion_desde_alerta = gestion_crear_accion_desde_alerta
    app_class.gestion_guardar_regla_alerta = gestion_guardar_regla_alerta
    app_class.gestion_cargar_decisiones = gestion_cargar_decisiones
    app_class.gestion_guardar_decision = gestion_guardar_decision
    app_class.gestion_cargar_notificaciones = gestion_cargar_notificaciones
    app_class.gestion_guardar_notificacion = gestion_guardar_notificacion
    app_class.gestion_marcar_notificacion_enviada = gestion_marcar_notificacion_enviada
    app_class.gestion_operacion_id = gestion_operacion_id
    app_class.gestion_render_kpis = gestion_render_kpis
    app_class.gestion_limpiar_reclamo = gestion_limpiar_reclamo


def show_gestion_profesional(self):
    previous_ops_cache = list(getattr(self, "gestion_ops_cache", []) or [])
    previous_operacion = ""
    previous_operacion_id = getattr(self, "gestion_last_operacion_id", None)
    if hasattr(self, "gestion_operacion_var"):
        try:
            previous_operacion = self.gestion_operacion_var.get().strip()
        except Exception:
            previous_operacion = ""

    self.clear_content()
    self.highlight_sidebar_button("Gestion Ejecutiva")

    self.gestion_ops_cache = previous_ops_cache
    self.gestion_reclamos_cache = []
    self.gestion_editando_reclamo_id = None
    self.gestion_editando_evidencia_id = None
    self.gestion_last_operacion_id = previous_operacion_id
    self.gestion_operacion_var = tk.StringVar(value=previous_operacion)
    self.gestion_cliente_var = tk.StringVar()
    self.gestion_estado_var = tk.StringVar(value="Listo. Use los botones para consultar datos del backend.")
    self.gestion_cumplimiento_estado_var = tk.StringVar(value="Matriz sin evaluar.")
    self.gestion_cumplimiento_recomendacion_var = tk.StringVar(value="Seleccione una operacion y presione Evaluar cumplimiento.")
    self.gestion_reclamo_tipo_var = tk.StringVar(value="OPERATIVO")
    self.gestion_reclamo_severidad_var = tk.StringVar(value="MEDIA")
    self.gestion_reclamo_estado_var = tk.StringVar(value="ABIERTO")
    self.gestion_reclamo_titulo_var = tk.StringVar()
    self.gestion_reclamo_cliente_var = tk.StringVar()
    self.gestion_reclamo_monto_var = tk.StringVar(value="0.00")
    self.gestion_reclamo_responsable_var = tk.StringVar()
    self.gestion_regla_nombre_var = tk.StringVar()
    self.gestion_regla_tipo_var = tk.StringVar(value="SOBRECUOTA")
    self.gestion_regla_severidad_var = tk.StringVar(value="ALTA")
    self.gestion_regla_umbral_var = tk.StringVar(value="100.00")
    self.gestion_accion_responsable_var = tk.StringVar()
    self.gestion_decision_titulo_var = tk.StringVar()
    self.gestion_decision_tipo_var = tk.StringVar(value="OPERATIVA")
    self.gestion_decision_responsable_var = tk.StringVar()
    self.gestion_notificacion_destino_var = tk.StringVar()
    self.gestion_notificacion_asunto_var = tk.StringVar()
    self.gestion_notificacion_canal_var = tk.StringVar(value="INTERNO")
    self.gestion_notificacion_prioridad_var = tk.StringVar(value="MEDIA")
    self.gestion_evidencia_tipo_var = tk.StringVar(value="DOCUMENTO")
    self.gestion_evidencia_estado_var = tk.StringVar(value="PENDIENTE")
    self.gestion_evidencia_titulo_var = tk.StringVar()
    self.gestion_evidencia_referencia_var = tk.StringVar()
    self.gestion_evidencia_url_var = tk.StringVar()
    self.gestion_evidencia_fecha_var = tk.StringVar()

    self.create_page_title(
        self.content,
        "Gestion Ejecutiva",
        "Reclamos, auditoria, portal cliente, evidencias e impacto operativo bajo demanda.",
    )

    actions = tk.Frame(self.content, bg=self.colors["bg_main"])
    actions.pack(fill="x", padx=25, pady=(0, 10))
    ttk.Button(actions, text="Buscar operaciones", style="Olive.TButton", command=self.gestion_cargar_operaciones).pack(side="left", padx=(0, 8))
    self.gestion_operacion_combo = ttk.Combobox(actions, textvariable=self.gestion_operacion_var, values=[], state="readonly", width=42)
    self.gestion_operacion_combo.pack(side="left", padx=(0, 8))
    if self.gestion_ops_cache:
        values = [
            f"{op.get('id')} | {op.get('nombre_buque')} | {op.get('fecha_inicio')} | {op.get('estado')}"
            for op in self.gestion_ops_cache
        ]
        self.gestion_operacion_combo["values"] = values
        if previous_operacion in values:
            self.gestion_operacion_var.set(previous_operacion)
        elif previous_operacion_id:
            match = next((item for item in values if item.startswith(f"{previous_operacion_id} |")), "")
            self.gestion_operacion_var.set(match)
    ttk.Button(actions, text="Buscar resumen", style="Gray.TButton", command=self.gestion_buscar_resumen).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Evaluar cumplimiento", style="Olive.TButton", command=self.gestion_evaluar_cumplimiento).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Cargar reclamos", style="Gray.TButton", command=self.gestion_cargar_reclamos).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Cargar auditoria", style="Gray.TButton", command=self.gestion_cargar_auditoria).pack(side="left", padx=(0, 8))

    status = tk.Frame(self.content, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    status.pack(fill="x", padx=25, pady=(0, 10))
    tk.Label(status, textvariable=self.gestion_estado_var, bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x", padx=14, pady=8)

    host = tk.Frame(self.content, bg=self.colors["bg_main"])
    host.pack(fill="both", expand=True, padx=25, pady=(0, 20))
    canvas = tk.Canvas(host, bg=self.colors["bg_main"], highlightthickness=0)
    scroll_y = ttk.Scrollbar(host, orient="vertical", command=canvas.yview)
    scroll_x = ttk.Scrollbar(host, orient="horizontal", command=canvas.xview)
    body = tk.Frame(canvas, bg=self.colors["bg_main"])
    window_id = canvas.create_window((0, 0), window=body, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    self.bind_scroll_canvas(canvas, body, window_id, min_width=1080)
    canvas.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    host.grid_rowconfigure(0, weight=1)
    host.grid_columnconfigure(0, weight=1)

    self.gestion_kpis_frame = tk.Frame(body, bg=self.colors["bg_main"])
    self.gestion_kpis_frame.pack(fill="x", pady=(0, 12))
    self.gestion_render_kpis({})

    cumplimiento_panel = tk.Frame(body, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    cumplimiento_panel.pack(fill="both", expand=True, pady=(0, 12))
    tk.Label(cumplimiento_panel, text="Matriz de cumplimiento para cierre", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 4))
    tk.Label(cumplimiento_panel, textvariable=self.gestion_cumplimiento_estado_var, bg=self.colors["bg_card"], fg=self.colors["danger"], font=("Segoe UI", 11, "bold"), anchor="w").pack(fill="x", padx=14, pady=(0, 2))
    tk.Label(cumplimiento_panel, textvariable=self.gestion_cumplimiento_recomendacion_var, bg=self.colors["bg_card"], fg="#5A5A5A", font=("Segoe UI", 10), anchor="w").pack(fill="x", padx=14, pady=(0, 8))
    cumplimiento_table = tk.Frame(cumplimiento_panel, bg=self.colors["bg_card"])
    cumplimiento_table.pack(fill="both", expand=True, padx=14, pady=(0, 14))
    ccols = ("criterio", "estado", "detalle", "impacto")
    self.gestion_cumplimiento_tree = ttk.Treeview(cumplimiento_table, columns=ccols, show="headings", height=8)
    for col, text, width in [
        ("criterio", "Criterio", 170), ("estado", "Estado", 100),
        ("detalle", "Detalle", 520), ("impacto", "Impacto / accion", 520),
    ]:
        self.gestion_cumplimiento_tree.heading(col, text=text)
        self.gestion_cumplimiento_tree.column(col, width=width, anchor="center")
    cy = ttk.Scrollbar(cumplimiento_table, orient="vertical", command=self.gestion_cumplimiento_tree.yview)
    cx = ttk.Scrollbar(cumplimiento_table, orient="horizontal", command=self.gestion_cumplimiento_tree.xview)
    self.gestion_cumplimiento_tree.configure(yscrollcommand=cy.set, xscrollcommand=cx.set)
    self.gestion_cumplimiento_tree.grid(row=0, column=0, sticky="nsew")
    cy.grid(row=0, column=1, sticky="ns")
    cx.grid(row=1, column=0, sticky="ew")
    cumplimiento_table.grid_rowconfigure(0, weight=1)
    cumplimiento_table.grid_columnconfigure(0, weight=1)

    top = tk.Frame(body, bg=self.colors["bg_main"])
    top.pack(fill="both", expand=True, pady=(0, 12))

    reclamo_panel = tk.Frame(top, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    reclamo_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))
    tk.Label(reclamo_panel, text="Reclamos / Claims", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 6))

    form = tk.Frame(reclamo_panel, bg=self.colors["bg_card"])
    form.pack(fill="x", padx=14, pady=(0, 8))
    fields = [
        ("Cliente", self.gestion_reclamo_cliente_var, None),
        ("Tipo", self.gestion_reclamo_tipo_var, ["OPERATIVO", "DOCUMENTAL", "PESO", "CUOTA", "SEGURIDAD", "DEMORA", "OTROS"]),
        ("Severidad", self.gestion_reclamo_severidad_var, ["BAJA", "MEDIA", "ALTA", "CRITICA"]),
        ("Estado", self.gestion_reclamo_estado_var, ["ABIERTO", "EN_REVISION", "CERRADO", "DESCARTADO"]),
    ]
    for idx, (label, var, values) in enumerate(fields):
        box = tk.Frame(form, bg=self.colors["bg_card"])
        box.grid(row=0, column=idx, sticky="ew", padx=4)
        tk.Label(box, text=label, bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        if values:
            ttk.Combobox(box, textvariable=var, values=values, state="readonly").pack(fill="x")
        else:
            ttk.Entry(box, textvariable=var).pack(fill="x")
        form.grid_columnconfigure(idx, weight=1)

    form2 = tk.Frame(reclamo_panel, bg=self.colors["bg_card"])
    form2.pack(fill="x", padx=14, pady=(0, 8))
    for idx, (label, var) in enumerate([
        ("Titulo", self.gestion_reclamo_titulo_var),
        ("Monto estimado USD", self.gestion_reclamo_monto_var),
        ("Responsable", self.gestion_reclamo_responsable_var),
    ]):
        box = tk.Frame(form2, bg=self.colors["bg_card"])
        box.grid(row=0, column=idx, sticky="ew", padx=4)
        tk.Label(box, text=label, bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ttk.Entry(box, textvariable=var).pack(fill="x")
        form2.grid_columnconfigure(idx, weight=1)

    tk.Label(reclamo_panel, text="Descripcion", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=18)
    self.gestion_reclamo_descripcion = tk.Text(reclamo_panel, height=3, wrap="word", font=("Segoe UI", 9))
    self.gestion_reclamo_descripcion.pack(fill="x", padx=18, pady=(0, 8))

    buttons = tk.Frame(reclamo_panel, bg=self.colors["bg_card"])
    buttons.pack(fill="x", padx=14, pady=(0, 8))
    ttk.Button(buttons, text="Crear / Guardar reclamo", style="Olive.TButton", command=self.gestion_guardar_reclamo).pack(side="left", padx=(0, 8))
    ttk.Button(buttons, text="Editar seleccionado", style="Gray.TButton", command=self.gestion_editar_reclamo).pack(side="left", padx=(0, 8))
    ttk.Button(buttons, text="Limpiar", style="Gray.TButton", command=self.gestion_limpiar_reclamo).pack(side="left")

    table_frame = tk.Frame(reclamo_panel, bg=self.colors["bg_card"])
    table_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))
    cols = ("id", "cliente", "tipo", "sev", "estado", "titulo", "monto")
    self.gestion_reclamos_tree = ttk.Treeview(table_frame, columns=cols, show="headings", height=10)
    for col, text, width in [
        ("id", "ID", 55), ("cliente", "Cliente", 150), ("tipo", "Tipo", 110),
        ("sev", "Sev.", 80), ("estado", "Estado", 110), ("titulo", "Titulo", 260), ("monto", "Monto", 100),
    ]:
        self.gestion_reclamos_tree.heading(col, text=text)
        self.gestion_reclamos_tree.column(col, width=width, anchor="center")
    y = ttk.Scrollbar(table_frame, orient="vertical", command=self.gestion_reclamos_tree.yview)
    x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.gestion_reclamos_tree.xview)
    self.gestion_reclamos_tree.configure(yscrollcommand=y.set, xscrollcommand=x.set)
    self.gestion_reclamos_tree.grid(row=0, column=0, sticky="nsew")
    y.grid(row=0, column=1, sticky="ns")
    x.grid(row=1, column=0, sticky="ew")
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    portal_panel = tk.Frame(top, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1, width=420)
    portal_panel.pack(side="right", fill="both")
    portal_panel.pack_propagate(False)
    tk.Label(portal_panel, text="Portal cliente", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 6))
    filter_row = tk.Frame(portal_panel, bg=self.colors["bg_card"])
    filter_row.pack(fill="x", padx=14, pady=(0, 8))
    ttk.Entry(filter_row, textvariable=self.gestion_cliente_var).pack(side="left", fill="x", expand=True, padx=(0, 8))
    ttk.Button(filter_row, text="Buscar", style="Olive.TButton", command=self.gestion_cargar_portal_cliente).pack(side="left")
    portal_table = tk.Frame(portal_panel, bg=self.colors["bg_card"])
    portal_table.pack(fill="both", expand=True, padx=14, pady=(0, 14))
    pcols = ("cliente", "producto", "cuota", "desc", "pend", "avance")
    self.gestion_portal_tree = ttk.Treeview(portal_table, columns=pcols, show="headings", height=15)
    for col, text, width in [
        ("cliente", "Cliente", 130), ("producto", "Producto", 120), ("cuota", "Cuota MT", 90),
        ("desc", "Desc. MT", 90), ("pend", "Pend. MT", 90), ("avance", "Avance", 80),
    ]:
        self.gestion_portal_tree.heading(col, text=text)
        self.gestion_portal_tree.column(col, width=width, anchor="center")
    py = ttk.Scrollbar(portal_table, orient="vertical", command=self.gestion_portal_tree.yview)
    px = ttk.Scrollbar(portal_table, orient="horizontal", command=self.gestion_portal_tree.xview)
    self.gestion_portal_tree.configure(yscrollcommand=py.set, xscrollcommand=px.set)
    self.gestion_portal_tree.grid(row=0, column=0, sticky="nsew")
    py.grid(row=0, column=1, sticky="ns")
    px.grid(row=1, column=0, sticky="ew")
    portal_table.grid_rowconfigure(0, weight=1)
    portal_table.grid_columnconfigure(0, weight=1)

    evidencias_panel = tk.Frame(body, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    evidencias_panel.pack(fill="both", expand=True, pady=(0, 12))
    tk.Label(evidencias_panel, text="Centro de evidencias operativas", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 6))
    ev_form = tk.Frame(evidencias_panel, bg=self.colors["bg_card"])
    ev_form.pack(fill="x", padx=14, pady=(0, 8))
    for idx, (label, var, values) in enumerate([
        ("Tipo", self.gestion_evidencia_tipo_var, ["DOCUMENTO", "FOTO", "FIRMA", "MARCHAMO", "PESO", "SOF", "RECLAMO", "OTRO"]),
        ("Estado", self.gestion_evidencia_estado_var, ["PENDIENTE", "VALIDADA", "RECHAZADA", "OBSERVADA"]),
        ("Titulo", self.gestion_evidencia_titulo_var, None),
        ("Fecha YYYY-MM-DD", self.gestion_evidencia_fecha_var, None),
    ]):
        box = tk.Frame(ev_form, bg=self.colors["bg_card"])
        box.grid(row=0, column=idx, sticky="ew", padx=4)
        tk.Label(box, text=label, bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        if values:
            ttk.Combobox(box, textvariable=var, values=values, state="readonly").pack(fill="x")
        else:
            ttk.Entry(box, textvariable=var).pack(fill="x")
        ev_form.grid_columnconfigure(idx, weight=1)

    ev_form2 = tk.Frame(evidencias_panel, bg=self.colors["bg_card"])
    ev_form2.pack(fill="x", padx=14, pady=(0, 8))
    for idx, (label, var) in enumerate([
        ("Referencia / Guia / Marchamo", self.gestion_evidencia_referencia_var),
        ("Ruta local o URL", self.gestion_evidencia_url_var),
    ]):
        box = tk.Frame(ev_form2, bg=self.colors["bg_card"])
        box.grid(row=0, column=idx, sticky="ew", padx=4)
        tk.Label(box, text=label, bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        ttk.Entry(box, textvariable=var).pack(fill="x")
        ev_form2.grid_columnconfigure(idx, weight=1)

    tk.Label(evidencias_panel, text="Comentario / observacion", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=18)
    self.gestion_evidencia_comentario = tk.Text(evidencias_panel, height=3, wrap="word", font=("Segoe UI", 9))
    self.gestion_evidencia_comentario.pack(fill="x", padx=18, pady=(0, 8))
    ev_buttons = tk.Frame(evidencias_panel, bg=self.colors["bg_card"])
    ev_buttons.pack(fill="x", padx=14, pady=(0, 8))
    ttk.Button(ev_buttons, text="Crear / Guardar evidencia", style="Olive.TButton", command=self.gestion_guardar_evidencia).pack(side="left", padx=(0, 8))
    ttk.Button(ev_buttons, text="Editar seleccionada", style="Gray.TButton", command=self.gestion_editar_evidencia).pack(side="left", padx=(0, 8))
    ttk.Button(ev_buttons, text="Cargar evidencias", style="Gray.TButton", command=self.gestion_cargar_evidencias).pack(side="left", padx=(0, 8))
    ttk.Button(ev_buttons, text="Limpiar", style="Gray.TButton", command=self.gestion_limpiar_evidencia).pack(side="left")

    ev_table = tk.Frame(evidencias_panel, bg=self.colors["bg_card"])
    ev_table.pack(fill="both", expand=True, padx=14, pady=(0, 14))
    ev_cols = ("id", "tipo", "estado", "titulo", "referencia", "url", "fecha")
    self.gestion_evidencias_tree = ttk.Treeview(ev_table, columns=ev_cols, show="headings", height=8)
    for col, text, width in [
        ("id", "ID", 55), ("tipo", "Tipo", 110), ("estado", "Estado", 110),
        ("titulo", "Titulo", 260), ("referencia", "Referencia", 160),
        ("url", "Ruta / URL", 360), ("fecha", "Fecha", 120),
    ]:
        self.gestion_evidencias_tree.heading(col, text=text)
        self.gestion_evidencias_tree.column(col, width=width, anchor="center")
    ev_y = ttk.Scrollbar(ev_table, orient="vertical", command=self.gestion_evidencias_tree.yview)
    ev_x = ttk.Scrollbar(ev_table, orient="horizontal", command=self.gestion_evidencias_tree.xview)
    self.gestion_evidencias_tree.configure(yscrollcommand=ev_y.set, xscrollcommand=ev_x.set)
    self.gestion_evidencias_tree.grid(row=0, column=0, sticky="nsew")
    ev_y.grid(row=0, column=1, sticky="ns")
    ev_x.grid(row=1, column=0, sticky="ew")
    ev_table.grid_rowconfigure(0, weight=1)
    ev_table.grid_columnconfigure(0, weight=1)

    audit_panel = tk.Frame(body, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    audit_panel.pack(fill="both", expand=True)
    tk.Label(audit_panel, text="Auditoria de cambios recientes", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 6))
    audit_frame = tk.Frame(audit_panel, bg=self.colors["bg_card"])
    audit_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))
    acols = ("id", "tabla", "accion", "registro", "usuario", "fecha", "resumen")
    self.gestion_auditoria_tree = ttk.Treeview(audit_frame, columns=acols, show="headings", height=9)
    for col, text, width in [
        ("id", "ID", 60), ("tabla", "Tabla", 190), ("accion", "Accion", 90),
        ("registro", "Registro", 90), ("usuario", "Usuario", 130), ("fecha", "Fecha", 150), ("resumen", "Resumen", 520),
    ]:
        self.gestion_auditoria_tree.heading(col, text=text)
        self.gestion_auditoria_tree.column(col, width=width, anchor="center")
    ay = ttk.Scrollbar(audit_frame, orient="vertical", command=self.gestion_auditoria_tree.yview)
    ax = ttk.Scrollbar(audit_frame, orient="horizontal", command=self.gestion_auditoria_tree.xview)
    self.gestion_auditoria_tree.configure(yscrollcommand=ay.set, xscrollcommand=ax.set)
    self.gestion_auditoria_tree.grid(row=0, column=0, sticky="nsew")
    ay.grid(row=0, column=1, sticky="ns")
    ax.grid(row=1, column=0, sticky="ew")
    audit_frame.grid_rowconfigure(0, weight=1)
    audit_frame.grid_columnconfigure(0, weight=1)

    risk_panel = tk.Frame(body, bg=self.colors["bg_main"])
    risk_panel.pack(fill="both", expand=True, pady=(12, 0))

    reglas_panel = tk.Frame(risk_panel, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    reglas_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))
    tk.Label(reglas_panel, text="Motor de alertas configurables", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 6))
    regla_form = tk.Frame(reglas_panel, bg=self.colors["bg_card"])
    regla_form.pack(fill="x", padx=14, pady=(0, 8))
    for idx, (label, var, values) in enumerate([
        ("Nombre", self.gestion_regla_nombre_var, None),
        ("Tipo", self.gestion_regla_tipo_var, ["SOBRECUOTA", "DURACION_CAMION", "PESO_FUERA_RANGO", "QR_BLOQUEADO"]),
        ("Severidad", self.gestion_regla_severidad_var, ["BAJA", "MEDIA", "ALTA", "CRITICA"]),
        ("Umbral", self.gestion_regla_umbral_var, None),
    ]):
        box = tk.Frame(regla_form, bg=self.colors["bg_card"])
        box.grid(row=0, column=idx, sticky="ew", padx=4)
        tk.Label(box, text=label, bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        if values:
            ttk.Combobox(box, textvariable=var, values=values, state="readonly").pack(fill="x")
        else:
            ttk.Entry(box, textvariable=var).pack(fill="x")
        regla_form.grid_columnconfigure(idx, weight=1)
    regla_buttons = tk.Frame(reglas_panel, bg=self.colors["bg_card"])
    regla_buttons.pack(fill="x", padx=14, pady=(0, 8))
    ttk.Button(regla_buttons, text="Cargar reglas", style="Gray.TButton", command=self.gestion_cargar_reglas_alerta).pack(side="left", padx=(0, 8))
    ttk.Button(regla_buttons, text="Crear regla", style="Olive.TButton", command=self.gestion_guardar_regla_alerta).pack(side="left", padx=(0, 8))
    ttk.Button(regla_buttons, text="Evaluar alertas", style="Olive.TButton", command=self.gestion_evaluar_alertas).pack(side="left")
    reglas_table = tk.Frame(reglas_panel, bg=self.colors["bg_card"])
    reglas_table.pack(fill="both", expand=True, padx=14, pady=(0, 14))
    self.gestion_reglas_tree = ttk.Treeview(reglas_table, columns=("id", "nombre", "tipo", "sev", "umbral", "activo"), show="headings", height=8)
    for col, text, width in [
        ("id", "ID", 55), ("nombre", "Nombre", 190), ("tipo", "Tipo", 150),
        ("sev", "Sev.", 80), ("umbral", "Umbral", 90), ("activo", "Activo", 70),
    ]:
        self.gestion_reglas_tree.heading(col, text=text)
        self.gestion_reglas_tree.column(col, width=width, anchor="center")
    ry = ttk.Scrollbar(reglas_table, orient="vertical", command=self.gestion_reglas_tree.yview)
    rx = ttk.Scrollbar(reglas_table, orient="horizontal", command=self.gestion_reglas_tree.xview)
    self.gestion_reglas_tree.configure(yscrollcommand=ry.set, xscrollcommand=rx.set)
    self.gestion_reglas_tree.grid(row=0, column=0, sticky="nsew")
    ry.grid(row=0, column=1, sticky="ns")
    rx.grid(row=1, column=0, sticky="ew")
    reglas_table.grid_rowconfigure(0, weight=1)
    reglas_table.grid_columnconfigure(0, weight=1)

    acciones_panel = tk.Frame(risk_panel, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    acciones_panel.pack(side="right", fill="both", expand=True)
    tk.Label(acciones_panel, text="Alertas evaluadas y plan de accion", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 6))
    accion_row = tk.Frame(acciones_panel, bg=self.colors["bg_card"])
    accion_row.pack(fill="x", padx=14, pady=(0, 8))
    tk.Label(accion_row, text="Responsable", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(side="left")
    ttk.Entry(accion_row, textvariable=self.gestion_accion_responsable_var, width=24).pack(side="left", padx=(8, 12))
    ttk.Button(accion_row, text="Crear accion desde alerta", style="Olive.TButton", command=self.gestion_crear_accion_desde_alerta).pack(side="left", padx=(0, 8))
    ttk.Button(accion_row, text="Cargar acciones", style="Gray.TButton", command=self.gestion_cargar_acciones).pack(side="left")
    alerta_frame = tk.Frame(acciones_panel, bg=self.colors["bg_card"])
    alerta_frame.pack(fill="both", expand=True, padx=14, pady=(0, 8))
    self.gestion_alertas_tree = ttk.Treeview(alerta_frame, columns=("tipo", "sev", "titulo", "mensaje", "valor"), show="headings", height=6)
    for col, text, width in [
        ("tipo", "Tipo", 130), ("sev", "Sev.", 80), ("titulo", "Titulo", 190),
        ("mensaje", "Mensaje", 360), ("valor", "Valor", 80),
    ]:
        self.gestion_alertas_tree.heading(col, text=text)
        self.gestion_alertas_tree.column(col, width=width, anchor="center")
    self.gestion_alertas_tree.pack(fill="both", expand=True)
    acciones_frame = tk.Frame(acciones_panel, bg=self.colors["bg_card"])
    acciones_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))
    self.gestion_acciones_tree = ttk.Treeview(acciones_frame, columns=("id", "prio", "estado", "titulo", "resp", "limite"), show="headings", height=6)
    for col, text, width in [
        ("id", "ID", 55), ("prio", "Prioridad", 90), ("estado", "Estado", 100),
        ("titulo", "Titulo", 260), ("resp", "Responsable", 130), ("limite", "Limite", 100),
    ]:
        self.gestion_acciones_tree.heading(col, text=text)
        self.gestion_acciones_tree.column(col, width=width, anchor="center")
    self.gestion_acciones_tree.pack(fill="both", expand=True)

    gov_panel = tk.Frame(body, bg=self.colors["bg_main"])
    gov_panel.pack(fill="both", expand=True, pady=(12, 0))

    decisiones_panel = tk.Frame(gov_panel, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    decisiones_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))
    tk.Label(decisiones_panel, text="Bitacora de decisiones", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 6))
    decision_form = tk.Frame(decisiones_panel, bg=self.colors["bg_card"])
    decision_form.pack(fill="x", padx=14, pady=(0, 8))
    for idx, (label, var, values) in enumerate([
        ("Titulo", self.gestion_decision_titulo_var, None),
        ("Tipo", self.gestion_decision_tipo_var, ["OPERATIVA", "COMERCIAL", "RIESGO", "RECLAMO", "CLIENTE"]),
        ("Responsable", self.gestion_decision_responsable_var, None),
    ]):
        box = tk.Frame(decision_form, bg=self.colors["bg_card"])
        box.grid(row=0, column=idx, sticky="ew", padx=4)
        tk.Label(box, text=label, bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        if values:
            ttk.Combobox(box, textvariable=var, values=values, state="readonly").pack(fill="x")
        else:
            ttk.Entry(box, textvariable=var).pack(fill="x")
        decision_form.grid_columnconfigure(idx, weight=1)
    tk.Label(decisiones_panel, text="Decision / impacto", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=18)
    self.gestion_decision_text = tk.Text(decisiones_panel, height=3, wrap="word", font=("Segoe UI", 9))
    self.gestion_decision_text.pack(fill="x", padx=18, pady=(0, 8))
    decision_buttons = tk.Frame(decisiones_panel, bg=self.colors["bg_card"])
    decision_buttons.pack(fill="x", padx=14, pady=(0, 8))
    ttk.Button(decision_buttons, text="Crear decision", style="Olive.TButton", command=self.gestion_guardar_decision).pack(side="left", padx=(0, 8))
    ttk.Button(decision_buttons, text="Cargar decisiones", style="Gray.TButton", command=self.gestion_cargar_decisiones).pack(side="left")
    decision_table = tk.Frame(decisiones_panel, bg=self.colors["bg_card"])
    decision_table.pack(fill="both", expand=True, padx=14, pady=(0, 14))
    self.gestion_decisiones_tree = ttk.Treeview(decision_table, columns=("id", "tipo", "titulo", "resp", "estado", "fecha"), show="headings", height=8)
    for col, text, width in [
        ("id", "ID", 55), ("tipo", "Tipo", 100), ("titulo", "Titulo", 260),
        ("resp", "Responsable", 130), ("estado", "Estado", 90), ("fecha", "Fecha", 140),
    ]:
        self.gestion_decisiones_tree.heading(col, text=text)
        self.gestion_decisiones_tree.column(col, width=width, anchor="center")
    self.gestion_decisiones_tree.pack(fill="both", expand=True)

    notificaciones_panel = tk.Frame(gov_panel, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    notificaciones_panel.pack(side="right", fill="both", expand=True)
    tk.Label(notificaciones_panel, text="Notificaciones internas", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 6))
    notif_form = tk.Frame(notificaciones_panel, bg=self.colors["bg_card"])
    notif_form.pack(fill="x", padx=14, pady=(0, 8))
    for idx, (label, var, values) in enumerate([
        ("Canal", self.gestion_notificacion_canal_var, ["INTERNO", "EMAIL", "WHATSAPP", "REUNION"]),
        ("Destino", self.gestion_notificacion_destino_var, None),
        ("Prioridad", self.gestion_notificacion_prioridad_var, ["BAJA", "MEDIA", "ALTA", "CRITICA"]),
    ]):
        box = tk.Frame(notif_form, bg=self.colors["bg_card"])
        box.grid(row=0, column=idx, sticky="ew", padx=4)
        tk.Label(box, text=label, bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        if values:
            ttk.Combobox(box, textvariable=var, values=values, state="readonly").pack(fill="x")
        else:
            ttk.Entry(box, textvariable=var).pack(fill="x")
        notif_form.grid_columnconfigure(idx, weight=1)
    asunto_row = tk.Frame(notificaciones_panel, bg=self.colors["bg_card"])
    asunto_row.pack(fill="x", padx=18, pady=(0, 8))
    tk.Label(asunto_row, text="Asunto", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
    ttk.Entry(asunto_row, textvariable=self.gestion_notificacion_asunto_var).pack(fill="x")
    tk.Label(notificaciones_panel, text="Mensaje", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w", padx=18)
    self.gestion_notificacion_text = tk.Text(notificaciones_panel, height=3, wrap="word", font=("Segoe UI", 9))
    self.gestion_notificacion_text.pack(fill="x", padx=18, pady=(0, 8))
    notif_buttons = tk.Frame(notificaciones_panel, bg=self.colors["bg_card"])
    notif_buttons.pack(fill="x", padx=14, pady=(0, 8))
    ttk.Button(notif_buttons, text="Crear notificacion", style="Olive.TButton", command=self.gestion_guardar_notificacion).pack(side="left", padx=(0, 8))
    ttk.Button(notif_buttons, text="Cargar notificaciones", style="Gray.TButton", command=self.gestion_cargar_notificaciones).pack(side="left", padx=(0, 8))
    ttk.Button(notif_buttons, text="Marcar enviada", style="Gray.TButton", command=self.gestion_marcar_notificacion_enviada).pack(side="left")
    notif_table = tk.Frame(notificaciones_panel, bg=self.colors["bg_card"])
    notif_table.pack(fill="both", expand=True, padx=14, pady=(0, 14))
    self.gestion_notificaciones_tree = ttk.Treeview(notif_table, columns=("id", "canal", "destino", "prio", "estado", "asunto"), show="headings", height=8)
    for col, text, width in [
        ("id", "ID", 55), ("canal", "Canal", 90), ("destino", "Destino", 130),
        ("prio", "Prioridad", 90), ("estado", "Estado", 100), ("asunto", "Asunto", 300),
    ]:
        self.gestion_notificaciones_tree.heading(col, text=text)
        self.gestion_notificaciones_tree.column(col, width=width, anchor="center")
    self.gestion_notificaciones_tree.pack(fill="both", expand=True)


def gestion_operacion_id(self):
    value = self.gestion_operacion_var.get().strip()
    if not value:
        return getattr(self, "gestion_last_operacion_id", None)
    try:
        operacion_id = int(value.split("|", 1)[0].strip())
        self.gestion_last_operacion_id = operacion_id
        return operacion_id
    except Exception:
        return getattr(self, "gestion_last_operacion_id", None)


def gestion_render_kpis(self, kpis):
    for widget in self.gestion_kpis_frame.winfo_children():
        widget.destroy()
    rows = [
        [
            ("Guias", kpis.get("guias", 0), self.colors["accent"]),
            ("Avance", f"{self.safe_number(kpis.get('avance_pct')):,.2f}%", self.colors["success"]),
            ("Reclamos abiertos", kpis.get("reclamos_abiertos", 0), self.colors["warning"]),
            ("Impacto estimado", f"${self.safe_number(kpis.get('impacto_estimado_usd')):,.2f}", self.colors["danger"]),
        ],
        [
            ("Acciones abiertas", kpis.get("acciones_abiertas", 0), self.colors["warning"]),
            ("Acciones criticas", kpis.get("acciones_criticas", 0), self.colors["danger"]),
            ("Decisiones", kpis.get("decisiones", 0), self.colors["accent"]),
            ("Evidencias", kpis.get("evidencias", 0), self.colors["success"]),
            ("Notif. pendientes", kpis.get("notificaciones_pendientes", 0), self.colors["info"]),
        ],
    ]
    for row_items in rows:
        row_frame = tk.Frame(self.gestion_kpis_frame, bg=self.colors["bg_main"])
        row_frame.pack(fill="x", pady=(0, 10))
        for title, value, color in row_items:
            self.create_card(row_frame, title, value, color)


def api_get_gestion_resumen(self, operacion_id=None):
    import requests
    params = {}
    if operacion_id:
        params["operacion_id"] = operacion_id
    respuesta = requests.get(f"{self.api_base}/gestion-profesional/resumen", params=params, timeout=90)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_get_matriz_cumplimiento(self, operacion_id):
    import requests
    respuesta = requests.get(
        f"{self.api_base}/gestion-profesional/cumplimiento",
        params={"operacion_id": operacion_id},
        timeout=90,
    )
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_get_gestion_reclamos(self, operacion_id=None):
    import requests
    params = {}
    if operacion_id:
        params["operacion_id"] = operacion_id
    respuesta = requests.get(f"{self.api_base}/gestion-profesional/reclamos", params=params, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_crear_gestion_reclamo(self, payload):
    import requests
    respuesta = requests.post(f"{self.api_base}/gestion-profesional/reclamos", json=payload, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_actualizar_gestion_reclamo(self, reclamo_id, payload):
    import requests
    respuesta = requests.put(f"{self.api_base}/gestion-profesional/reclamos/{reclamo_id}", json=payload, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_get_gestion_auditoria(self):
    import requests
    respuesta = requests.get(f"{self.api_base}/gestion-profesional/auditoria", timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_get_portal_cliente(self, operacion_id, cliente=None):
    import requests
    params = {"operacion_id": operacion_id}
    if cliente:
        params["cliente"] = cliente
    respuesta = requests.get(f"{self.api_base}/gestion-profesional/portal-cliente", params=params, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_get_evidencias(self, operacion_id=None, tipo=None, estado=None):
    import requests
    params = {}
    if operacion_id:
        params["operacion_id"] = operacion_id
    if tipo:
        params["tipo"] = tipo
    if estado:
        params["estado"] = estado
    respuesta = requests.get(f"{self.api_base}/gestion-profesional/evidencias", params=params, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_crear_evidencia(self, payload):
    import requests
    respuesta = requests.post(f"{self.api_base}/gestion-profesional/evidencias", json=payload, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_actualizar_evidencia(self, evidencia_id, payload):
    import requests
    respuesta = requests.put(f"{self.api_base}/gestion-profesional/evidencias/{evidencia_id}", json=payload, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_get_alertas_reglas(self):
    import requests
    respuesta = requests.get(f"{self.api_base}/gestion-profesional/alertas/reglas", timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_crear_alerta_regla(self, payload):
    import requests
    respuesta = requests.post(f"{self.api_base}/gestion-profesional/alertas/reglas", json=payload, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_evaluar_alertas(self, operacion_id):
    import requests
    respuesta = requests.get(f"{self.api_base}/gestion-profesional/alertas/evaluar", params={"operacion_id": operacion_id}, timeout=90)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_get_acciones(self, operacion_id=None):
    import requests
    params = {}
    if operacion_id:
        params["operacion_id"] = operacion_id
    respuesta = requests.get(f"{self.api_base}/gestion-profesional/acciones", params=params, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_crear_accion(self, payload):
    import requests
    respuesta = requests.post(f"{self.api_base}/gestion-profesional/acciones", json=payload, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_get_decisiones(self, operacion_id=None):
    import requests
    params = {}
    if operacion_id:
        params["operacion_id"] = operacion_id
    respuesta = requests.get(f"{self.api_base}/gestion-profesional/decisiones", params=params, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_crear_decision(self, payload):
    import requests
    respuesta = requests.post(f"{self.api_base}/gestion-profesional/decisiones", json=payload, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_get_notificaciones(self, operacion_id=None):
    import requests
    params = {}
    if operacion_id:
        params["operacion_id"] = operacion_id
    respuesta = requests.get(f"{self.api_base}/gestion-profesional/notificaciones", params=params, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_crear_notificacion(self, payload):
    import requests
    respuesta = requests.post(f"{self.api_base}/gestion-profesional/notificaciones", json=payload, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_marcar_notificacion_enviada(self, notificacion_id):
    import requests
    respuesta = requests.post(f"{self.api_base}/gestion-profesional/notificaciones/{notificacion_id}/marcar-enviada", timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def gestion_cargar_operaciones(self):
    seleccion_actual = self.gestion_operacion_var.get().strip() if hasattr(self, "gestion_operacion_var") else ""
    id_actual = getattr(self, "gestion_last_operacion_id", None)

    def tarea():
        return self.api_get_operaciones_buque()

    def al_terminar(data):
        self.gestion_ops_cache = data.get("data", []) if isinstance(data, dict) else []
        values = [
            f"{op.get('id')} | {op.get('nombre_buque')} | {op.get('fecha_inicio')} | {op.get('estado')}"
            for op in self.gestion_ops_cache
        ]
        elegido = ""
        if seleccion_actual in values:
            elegido = seleccion_actual
        elif id_actual:
            elegido = next((item for item in values if item.startswith(f"{id_actual} |")), "")
        if not elegido:
            abierto = next((item for item in values if item.endswith("| ABIERTA")), "")
            elegido = abierto or (values[0] if values else "")
        self.gestion_operacion_var.set(elegido)
        if elegido:
            try:
                self.gestion_last_operacion_id = int(elegido.split("|", 1)[0].strip())
            except Exception:
                pass
        self.gestion_operacion_combo["values"] = values
        self.gestion_estado_var.set(f"Operaciones cargadas: {len(values)}.")

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Buscando operaciones...", tarea, al_terminar)


def gestion_buscar_resumen(self):
    operacion_id = self.gestion_operacion_id()
    if not operacion_id:
        messagebox.showwarning("Sin operacion", "Presione Buscar operaciones y seleccione una operacion primero.")
        return

    def tarea():
        return self.api_get_gestion_resumen(operacion_id)

    def al_terminar(data):
        kpis = data.get("kpis", {})
        self.gestion_render_kpis(kpis)
        lectura = data.get("lectura", [])
        self.gestion_estado_var.set("Resumen actualizado. " + (" ".join(lectura[:1]) if lectura else ""))

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Calculando resumen ejecutivo...", tarea, al_terminar)


def gestion_evaluar_cumplimiento(self):
    operacion_id = self.gestion_operacion_id()
    if not operacion_id:
        messagebox.showwarning("Sin operacion", "Seleccione una operacion primero.")
        return

    def tarea():
        return self.api_get_matriz_cumplimiento(operacion_id)

    def al_terminar(data):
        for item in self.gestion_cumplimiento_tree.get_children():
            self.gestion_cumplimiento_tree.delete(item)

        estado = data.get("estado_general", "SIN_DATOS")
        score = self.safe_number(data.get("score"))
        bloqueos = self.safe_int(data.get("bloqueos"))
        riesgos = self.safe_int(data.get("riesgos"))
        descargado = self.safe_number(data.get("descargado_mt"))
        self.gestion_cumplimiento_estado_var.set(
            f"Estado: {estado} | Score: {score:,.2f}/100 | Bloqueos: {bloqueos} | Riesgos: {riesgos} | Descargado: {descargado:,.2f} MT"
        )
        self.gestion_cumplimiento_recomendacion_var.set(data.get("recomendacion", ""))

        for row in data.get("criterios", []):
            self.gestion_cumplimiento_tree.insert(
                "",
                "end",
                values=(
                    row.get("criterio", ""),
                    row.get("estado", ""),
                    row.get("detalle", ""),
                    row.get("impacto", ""),
                ),
            )
        self.gestion_estado_var.set("Matriz de cumplimiento evaluada.")

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Evaluando matriz de cumplimiento...", tarea, al_terminar)


def gestion_cargar_reclamos(self):
    operacion_id = self.gestion_operacion_id()
    if not operacion_id:
        messagebox.showwarning("Sin operacion", "Presione Buscar operaciones y seleccione una operacion primero.")
        return

    def tarea():
        return self.api_get_gestion_reclamos(operacion_id)

    def al_terminar(data):
        self.gestion_reclamos_cache = data.get("data", [])
        for item in self.gestion_reclamos_tree.get_children():
            self.gestion_reclamos_tree.delete(item)
        for rec in self.gestion_reclamos_cache:
            self.gestion_reclamos_tree.insert(
                "",
                "end",
                values=(
                    rec.get("id"),
                    rec.get("cliente", ""),
                    rec.get("tipo", ""),
                    rec.get("severidad", ""),
                    rec.get("estado", ""),
                    rec.get("titulo", ""),
                    f"{self.safe_number(rec.get('monto_estimado')):,.2f}",
                ),
            )
        self.gestion_estado_var.set(f"Reclamos cargados: {len(self.gestion_reclamos_cache)}.")

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Cargando reclamos...", tarea, al_terminar)


def gestion_guardar_reclamo(self):
    titulo = self.gestion_reclamo_titulo_var.get().strip()
    if not titulo:
        messagebox.showwarning("Dato requerido", "Digite un titulo para el reclamo.")
        return
    payload = {
        "operacion_id": self.gestion_operacion_id(),
        "cliente": self.gestion_reclamo_cliente_var.get().strip() or None,
        "tipo": self.gestion_reclamo_tipo_var.get().strip() or "OPERATIVO",
        "severidad": self.gestion_reclamo_severidad_var.get().strip() or "MEDIA",
        "estado": self.gestion_reclamo_estado_var.get().strip() or "ABIERTO",
        "titulo": titulo,
        "descripcion": self.gestion_reclamo_descripcion.get("1.0", "end").strip() or None,
        "monto_estimado": self.safe_number(self.gestion_reclamo_monto_var.get()),
        "responsable": self.gestion_reclamo_responsable_var.get().strip() or None,
        "creado_por": "desktop",
    }

    def tarea():
        if self.gestion_editando_reclamo_id:
            return self.api_actualizar_gestion_reclamo(self.gestion_editando_reclamo_id, payload)
        return self.api_crear_gestion_reclamo(payload)

    def al_terminar(_data):
        self.gestion_limpiar_reclamo()
        self.gestion_cargar_reclamos()

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Guardando reclamo...", tarea, al_terminar)


def gestion_editar_reclamo(self):
    selected = self.gestion_reclamos_tree.selection()
    if not selected:
        messagebox.showwarning("Sin seleccion", "Seleccione un reclamo para editar.")
        return
    reclamo_id = self.safe_int(self.gestion_reclamos_tree.item(selected[0], "values")[0], None)
    reclamo = next((r for r in self.gestion_reclamos_cache if self.safe_int(r.get("id")) == reclamo_id), None)
    if not reclamo:
        messagebox.showwarning("No encontrado", "No se encontro el reclamo en cache. Presione Cargar reclamos.")
        return
    self.gestion_editando_reclamo_id = reclamo_id
    self.gestion_reclamo_cliente_var.set(reclamo.get("cliente") or "")
    self.gestion_reclamo_tipo_var.set(reclamo.get("tipo") or "OPERATIVO")
    self.gestion_reclamo_severidad_var.set(reclamo.get("severidad") or "MEDIA")
    self.gestion_reclamo_estado_var.set(reclamo.get("estado") or "ABIERTO")
    self.gestion_reclamo_titulo_var.set(reclamo.get("titulo") or "")
    self.gestion_reclamo_monto_var.set(f"{self.safe_number(reclamo.get('monto_estimado')):.2f}")
    self.gestion_reclamo_responsable_var.set(reclamo.get("responsable") or "")
    self.gestion_reclamo_descripcion.delete("1.0", "end")
    self.gestion_reclamo_descripcion.insert("1.0", reclamo.get("descripcion") or "")
    self.gestion_estado_var.set(f"Editando reclamo {reclamo_id}. Presione Crear / Guardar reclamo para actualizar.")


def gestion_limpiar_reclamo(self):
    self.gestion_editando_reclamo_id = None
    self.gestion_reclamo_cliente_var.set("")
    self.gestion_reclamo_tipo_var.set("OPERATIVO")
    self.gestion_reclamo_severidad_var.set("MEDIA")
    self.gestion_reclamo_estado_var.set("ABIERTO")
    self.gestion_reclamo_titulo_var.set("")
    self.gestion_reclamo_monto_var.set("0.00")
    self.gestion_reclamo_responsable_var.set("")
    self.gestion_reclamo_descripcion.delete("1.0", "end")


def gestion_cargar_auditoria(self):
    def tarea():
        return self.api_get_gestion_auditoria()

    def al_terminar(data):
        rows = data.get("data", [])
        for item in self.gestion_auditoria_tree.get_children():
            self.gestion_auditoria_tree.delete(item)
        for row in rows:
            self.gestion_auditoria_tree.insert(
                "",
                "end",
                values=(
                    row.get("id", ""),
                    row.get("tabla", ""),
                    row.get("accion", ""),
                    row.get("registro_id", ""),
                    row.get("usuario", ""),
                    row.get("creado_en", ""),
                    row.get("campo_resumen", ""),
                ),
            )
        self.gestion_estado_var.set(f"Auditoria cargada: {len(rows)} eventos.")

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Cargando auditoria...", tarea, al_terminar)


def gestion_cargar_portal_cliente(self):
    operacion_id = self.gestion_operacion_id()
    if not operacion_id:
        messagebox.showwarning("Sin operacion", "Seleccione una operacion primero.")
        return
    cliente = self.gestion_cliente_var.get().strip() or None

    def tarea():
        return self.api_get_portal_cliente(operacion_id, cliente)

    def al_terminar(data):
        rows = data.get("data", [])
        for item in self.gestion_portal_tree.get_children():
            self.gestion_portal_tree.delete(item)
        for row in rows:
            self.gestion_portal_tree.insert(
                "",
                "end",
                values=(
                    row.get("cliente", ""),
                    row.get("producto", ""),
                    f"{self.safe_number(row.get('cuota_mt')):,.2f}",
                    f"{self.safe_number(row.get('descargado_mt')):,.2f}",
                    f"{self.safe_number(row.get('pendiente_mt')):,.2f}",
                    f"{self.safe_number(row.get('avance_pct')):,.2f}%",
                ),
            )
        self.gestion_estado_var.set(f"Portal cliente cargado: {len(rows)} lineas.")

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Cargando portal cliente...", tarea, al_terminar)


def gestion_cargar_evidencias(self):
    operacion_id = self.gestion_operacion_id()
    tipo = self.gestion_evidencia_tipo_var.get().strip()
    estado = self.gestion_evidencia_estado_var.get().strip()

    def tarea():
        return self.api_get_evidencias(operacion_id, tipo or None, estado or None)

    def al_terminar(data):
        rows = data.get("data", [])
        for item in self.gestion_evidencias_tree.get_children():
            self.gestion_evidencias_tree.delete(item)
        for row in rows:
            self.gestion_evidencias_tree.insert(
                "",
                "end",
                values=(
                    row.get("id", ""),
                    row.get("tipo", ""),
                    row.get("estado", ""),
                    row.get("titulo", ""),
                    row.get("referencia", ""),
                    row.get("url_archivo", ""),
                    row.get("fecha_evidencia", "") or row.get("creado_en", ""),
                ),
            )
        self.gestion_estado_var.set(f"Evidencias cargadas: {len(rows)}.")

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Cargando evidencias...", tarea, al_terminar)


def gestion_guardar_evidencia(self):
    titulo = self.gestion_evidencia_titulo_var.get().strip()
    if not titulo:
        messagebox.showwarning("Dato requerido", "Digite un titulo para la evidencia.")
        return

    payload = {
        "operacion_id": self.gestion_operacion_id(),
        "tipo": self.gestion_evidencia_tipo_var.get().strip() or "DOCUMENTO",
        "estado": self.gestion_evidencia_estado_var.get().strip() or "PENDIENTE",
        "titulo": titulo,
        "referencia": self.gestion_evidencia_referencia_var.get().strip() or None,
        "url_archivo": self.gestion_evidencia_url_var.get().strip() or None,
        "comentario": self.gestion_evidencia_comentario.get("1.0", "end").strip() or None,
        "fecha_evidencia": self.gestion_evidencia_fecha_var.get().strip() or None,
        "creado_por": "desktop",
    }
    evidencia_id = self.gestion_editando_evidencia_id

    def tarea():
        if evidencia_id:
            return self.api_actualizar_evidencia(evidencia_id, payload)
        return self.api_crear_evidencia(payload)

    def al_terminar(_data):
        self.gestion_limpiar_evidencia()
        self.gestion_cargar_evidencias()

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Guardando evidencia...", tarea, al_terminar)


def gestion_editar_evidencia(self):
    selected = self.gestion_evidencias_tree.selection()
    if not selected:
        messagebox.showwarning("Sin seleccion", "Seleccione una evidencia.")
        return
    values = self.gestion_evidencias_tree.item(selected[0], "values")
    self.gestion_editando_evidencia_id = self.safe_int(values[0], None)
    self.gestion_evidencia_tipo_var.set(values[1])
    self.gestion_evidencia_estado_var.set(values[2])
    self.gestion_evidencia_titulo_var.set(values[3])
    self.gestion_evidencia_referencia_var.set(values[4])
    self.gestion_evidencia_url_var.set(values[5])
    self.gestion_evidencia_fecha_var.set(str(values[6])[:10] if values[6] else "")
    self.gestion_estado_var.set(f"Editando evidencia ID {values[0]}.")


def gestion_limpiar_evidencia(self):
    self.gestion_editando_evidencia_id = None
    self.gestion_evidencia_tipo_var.set("DOCUMENTO")
    self.gestion_evidencia_estado_var.set("PENDIENTE")
    self.gestion_evidencia_titulo_var.set("")
    self.gestion_evidencia_referencia_var.set("")
    self.gestion_evidencia_url_var.set("")
    self.gestion_evidencia_fecha_var.set("")
    self.gestion_evidencia_comentario.delete("1.0", "end")


def gestion_cargar_reglas_alerta(self):
    def tarea():
        return self.api_get_alertas_reglas()

    def al_terminar(data):
        rows = data.get("data", [])
        for item in self.gestion_reglas_tree.get_children():
            self.gestion_reglas_tree.delete(item)
        for row in rows:
            self.gestion_reglas_tree.insert(
                "",
                "end",
                values=(
                    row.get("id", ""),
                    row.get("nombre", ""),
                    row.get("tipo", ""),
                    row.get("severidad", ""),
                    f"{self.safe_number(row.get('umbral')):,.2f}",
                    "SI" if row.get("activo") else "NO",
                ),
            )
        self.gestion_estado_var.set(f"Reglas de alerta cargadas: {len(rows)}.")

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Cargando reglas de alerta...", tarea, al_terminar)


def gestion_guardar_regla_alerta(self):
    nombre = self.gestion_regla_nombre_var.get().strip()
    if not nombre:
        messagebox.showwarning("Dato requerido", "Digite un nombre para la regla.")
        return
    payload = {
        "nombre": nombre,
        "tipo": self.gestion_regla_tipo_var.get().strip() or "SOBRECUOTA",
        "severidad": self.gestion_regla_severidad_var.get().strip() or "MEDIA",
        "umbral": self.safe_number(self.gestion_regla_umbral_var.get()),
        "activo": True,
        "descripcion": None,
    }

    def tarea():
        return self.api_crear_alerta_regla(payload)

    def al_terminar(_data):
        self.gestion_regla_nombre_var.set("")
        self.gestion_cargar_reglas_alerta()

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Creando regla de alerta...", tarea, al_terminar)


def gestion_evaluar_alertas(self):
    operacion_id = self.gestion_operacion_id()
    if not operacion_id:
        messagebox.showwarning("Sin operacion", "Seleccione una operacion primero.")
        return

    def tarea():
        return self.api_evaluar_alertas(operacion_id)

    def al_terminar(data):
        rows = data.get("data", [])
        for item in self.gestion_alertas_tree.get_children():
            self.gestion_alertas_tree.delete(item)
        for row in rows:
            self.gestion_alertas_tree.insert(
                "",
                "end",
                values=(
                    row.get("tipo", ""),
                    row.get("severidad", ""),
                    row.get("titulo", ""),
                    row.get("mensaje", ""),
                    f"{self.safe_number(row.get('valor')):,.2f}",
                ),
            )
        self.gestion_estado_var.set(f"Alertas evaluadas: {len(rows)}.")

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Evaluando alertas operativas...", tarea, al_terminar)


def gestion_cargar_acciones(self):
    operacion_id = self.gestion_operacion_id()

    def tarea():
        return self.api_get_acciones(operacion_id)

    def al_terminar(data):
        rows = data.get("data", [])
        for item in self.gestion_acciones_tree.get_children():
            self.gestion_acciones_tree.delete(item)
        for row in rows:
            self.gestion_acciones_tree.insert(
                "",
                "end",
                values=(
                    row.get("id", ""),
                    row.get("prioridad", ""),
                    row.get("estado", ""),
                    row.get("titulo", ""),
                    row.get("responsable", ""),
                    row.get("fecha_limite", ""),
                ),
            )
        self.gestion_estado_var.set(f"Acciones cargadas: {len(rows)}.")

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Cargando acciones operativas...", tarea, al_terminar)


def gestion_crear_accion_desde_alerta(self):
    selected = self.gestion_alertas_tree.selection()
    if not selected:
        messagebox.showwarning("Sin alerta", "Seleccione una alerta evaluada para crear una accion.")
        return
    values = self.gestion_alertas_tree.item(selected[0], "values")
    tipo, severidad, titulo, mensaje, _valor = values
    payload = {
        "operacion_id": self.gestion_operacion_id(),
        "alerta_tipo": tipo,
        "titulo": titulo,
        "descripcion": mensaje,
        "responsable": self.gestion_accion_responsable_var.get().strip() or None,
        "prioridad": "CRITICA" if severidad == "CRITICA" else ("ALTA" if severidad == "ALTA" else "MEDIA"),
        "estado": "ABIERTA",
        "creado_por": "desktop",
    }

    def tarea():
        return self.api_crear_accion(payload)

    def al_terminar(_data):
        self.gestion_cargar_acciones()

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Creando accion operativa...", tarea, al_terminar)


def gestion_cargar_decisiones(self):
    operacion_id = self.gestion_operacion_id()

    def tarea():
        return self.api_get_decisiones(operacion_id)

    def al_terminar(data):
        rows = data.get("data", [])
        for item in self.gestion_decisiones_tree.get_children():
            self.gestion_decisiones_tree.delete(item)
        for row in rows:
            self.gestion_decisiones_tree.insert(
                "",
                "end",
                values=(
                    row.get("id", ""),
                    row.get("tipo", ""),
                    row.get("titulo", ""),
                    row.get("responsable", ""),
                    row.get("estado", ""),
                    row.get("creado_en", ""),
                ),
            )
        self.gestion_estado_var.set(f"Decisiones cargadas: {len(rows)}.")

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Cargando decisiones...", tarea, al_terminar)


def gestion_guardar_decision(self):
    titulo = self.gestion_decision_titulo_var.get().strip()
    decision = self.gestion_decision_text.get("1.0", "end").strip()
    if not titulo or not decision:
        messagebox.showwarning("Dato requerido", "Digite titulo y decision.")
        return
    payload = {
        "operacion_id": self.gestion_operacion_id(),
        "tipo": self.gestion_decision_tipo_var.get().strip() or "OPERATIVA",
        "titulo": titulo,
        "decision": decision,
        "impacto": None,
        "responsable": self.gestion_decision_responsable_var.get().strip() or None,
        "estado": "VIGENTE",
        "creado_por": "desktop",
    }

    def tarea():
        return self.api_crear_decision(payload)

    def al_terminar(_data):
        self.gestion_decision_titulo_var.set("")
        self.gestion_decision_responsable_var.set("")
        self.gestion_decision_text.delete("1.0", "end")
        self.gestion_cargar_decisiones()

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Guardando decision...", tarea, al_terminar)


def gestion_cargar_notificaciones(self):
    operacion_id = self.gestion_operacion_id()

    def tarea():
        return self.api_get_notificaciones(operacion_id)

    def al_terminar(data):
        rows = data.get("data", [])
        for item in self.gestion_notificaciones_tree.get_children():
            self.gestion_notificaciones_tree.delete(item)
        for row in rows:
            self.gestion_notificaciones_tree.insert(
                "",
                "end",
                values=(
                    row.get("id", ""),
                    row.get("canal", ""),
                    row.get("destinatario", ""),
                    row.get("prioridad", ""),
                    row.get("estado", ""),
                    row.get("asunto", ""),
                ),
            )
        self.gestion_estado_var.set(f"Notificaciones cargadas: {len(rows)}.")

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Cargando notificaciones...", tarea, al_terminar)


def gestion_guardar_notificacion(self):
    asunto = self.gestion_notificacion_asunto_var.get().strip()
    if not asunto:
        messagebox.showwarning("Dato requerido", "Digite un asunto para la notificacion.")
        return
    payload = {
        "operacion_id": self.gestion_operacion_id(),
        "canal": self.gestion_notificacion_canal_var.get().strip() or "INTERNO",
        "destinatario": self.gestion_notificacion_destino_var.get().strip() or None,
        "asunto": asunto,
        "mensaje": self.gestion_notificacion_text.get("1.0", "end").strip() or None,
        "prioridad": self.gestion_notificacion_prioridad_var.get().strip() or "MEDIA",
        "estado": "PENDIENTE",
        "creado_por": "desktop",
    }

    def tarea():
        return self.api_crear_notificacion(payload)

    def al_terminar(_data):
        self.gestion_notificacion_destino_var.set("")
        self.gestion_notificacion_asunto_var.set("")
        self.gestion_notificacion_text.delete("1.0", "end")
        self.gestion_cargar_notificaciones()

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Creando notificacion...", tarea, al_terminar)


def gestion_marcar_notificacion_enviada(self):
    selected = self.gestion_notificaciones_tree.selection()
    if not selected:
        messagebox.showwarning("Sin seleccion", "Seleccione una notificacion.")
        return
    notificacion_id = self.safe_int(self.gestion_notificaciones_tree.item(selected[0], "values")[0], None)
    if not notificacion_id:
        return

    def tarea():
        return self.api_marcar_notificacion_enviada(notificacion_id)

    def al_terminar(_data):
        self.gestion_cargar_notificaciones()

    self.ejecutar_en_segundo_plano("Gestion Ejecutiva", "Marcando notificacion enviada...", tarea, al_terminar)
