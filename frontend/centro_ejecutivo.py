import tkinter as tk
from datetime import date
from tkinter import filedialog, messagebox, simpledialog, ttk


def install_centro_ejecutivo_screen(app_class):
    app_class.show_centro_ejecutivo = show_centro_ejecutivo
    app_class.cargar_centro_ejecutivo = cargar_centro_ejecutivo
    app_class.cargar_operaciones_centro = cargar_operaciones_centro
    app_class.seleccionar_operacion_centro_por_id = seleccionar_operacion_centro_por_id
    app_class.seleccionar_operacion_relevante_centro = seleccionar_operacion_relevante_centro
    app_class.refrescar_operacion_centro_por_seleccion = refrescar_operacion_centro_por_seleccion
    app_class.analizar_operacion_centro = analizar_operacion_centro
    app_class.cargar_filtros_reporte_centro = cargar_filtros_reporte_centro
    app_class.cargar_control_plan_centro = cargar_control_plan_centro
    app_class.cargar_salud_operativa_centro = cargar_salud_operativa_centro
    app_class.cargar_spc_centro = cargar_spc_centro
    app_class.cargar_bloqueos_inteligentes_centro = cargar_bloqueos_inteligentes_centro
    app_class.cargar_excepciones_operativas_centro = cargar_excepciones_operativas_centro
    app_class.cargar_auditoria_senior_centro = cargar_auditoria_senior_centro
    app_class.cargar_cierre_guiado_centro = cargar_cierre_guiado_centro
    app_class.cargar_modo_offline_centro = cargar_modo_offline_centro
    app_class.cargar_productividad_centro = cargar_productividad_centro
    app_class.ejecutar_cierre_guiado_centro = ejecutar_cierre_guiado_centro
    app_class.generar_excepciones_desde_bloqueos_centro = generar_excepciones_desde_bloqueos_centro
    app_class.cerrar_excepcion_centro = cerrar_excepcion_centro
    app_class.render_control_operativo_centro = render_control_operativo_centro
    app_class.render_control_plan_centro = render_control_plan_centro
    app_class.render_salud_operativa_centro = render_salud_operativa_centro
    app_class.render_spc_centro = render_spc_centro
    app_class.render_bloqueos_inteligentes_centro = render_bloqueos_inteligentes_centro
    app_class.render_excepciones_operativas_centro = render_excepciones_operativas_centro
    app_class.render_auditoria_senior_centro = render_auditoria_senior_centro
    app_class.render_cierre_guiado_centro = render_cierre_guiado_centro
    app_class.render_modo_offline_centro = render_modo_offline_centro
    app_class.render_productividad_centro = render_productividad_centro
    app_class.render_kpis_operativos_centro = render_kpis_operativos_centro
    app_class.render_graficos_operativos_centro = render_graficos_operativos_centro
    app_class.crear_tabla_centro = crear_tabla_centro
    app_class.obtener_operacion_centro_seleccionada = obtener_operacion_centro_seleccionada
    app_class.obtener_params_reporte_centro = obtener_params_reporte_centro
    app_class.abrir_selector_fecha_centro = abrir_selector_fecha_centro
    app_class.exportar_centro = exportar_centro
    app_class.dibujar_buque_centro = dibujar_buque_centro
    app_class.actualizar_lectura_centro = actualizar_lectura_centro
    app_class.opciones_centro_desde_boletas = opciones_centro_desde_boletas
    app_class.aplicar_opciones_centro = aplicar_opciones_centro
    app_class.programar_filtrado_centro = programar_filtrado_centro
    app_class.aplicar_filtro_centro_desde_click = aplicar_filtro_centro_desde_click
    app_class.limpiar_filtros_visuales_centro = limpiar_filtros_visuales_centro
    app_class.resetear_filtro_visual_centro_si_fondo = resetear_filtro_visual_centro_si_fondo
    app_class.normalizar_valor_kg_centro = normalizar_valor_kg_centro
    app_class.valor_descargado_visible_centro = valor_descargado_visible_centro
    app_class.normalizar_estado_descarga_visible_centro = normalizar_estado_descarga_visible_centro
    app_class.crear_chart_barras_interactivo_centro = crear_chart_barras_interactivo_centro


def show_centro_ejecutivo(self):
    self.clear_content()
    self.highlight_sidebar_button("Centro Ejecutivo")

    self.centro_operaciones_tree = None
    self.centro_alertas_tree = None
    self.centro_cuotas_tree = None
    self.centro_control_plan_tree = None
    self.centro_salud_operativa_tree = None
    self.centro_spc_tree = None
    self.centro_bloqueos_tree = None
    self.centro_excepciones_tree = None
    self.centro_auditoria_senior_tree = None
    self.centro_cierre_guiado_tree = None
    self.centro_modo_offline_tree = None
    self.centro_productividad_tree = None
    self.centro_cierre_guiado_data = None
    self.centro_modo_offline_data = None
    self.centro_productividad_data = None
    self.centro_ops_cache = []
    self.centro_filtros_precargados = False
    self.centro_empresa_var = tk.StringVar()
    self.centro_bodega_var = tk.StringVar()
    self.centro_guia_var = tk.StringVar()
    self.centro_producto_var = tk.StringVar()
    self.centro_chofer_var = tk.StringVar()
    self.centro_placa_var = tk.StringVar()
    self.centro_estado_filtro_var = tk.StringVar()
    self.centro_etapa_qr_var = tk.StringVar()
    self.centro_fecha_desde_var = tk.StringVar()
    self.centro_fecha_hasta_var = tk.StringVar()
    self.centro_fecha_desde_larga_var = tk.StringVar(value="Desde")
    self.centro_fecha_hasta_larga_var = tk.StringVar(value="Hasta")
    self.centro_exportar_formato_var = tk.StringVar(value="PDF")
    self.centro_estado_var = tk.StringVar(value="Listo. Presione Buscar operacion para consultar el backend.")

    self.create_page_title(
        self.content,
        "Centro Ejecutivo",
        "Control gerencial por buque: bodegas, cuotas, descargado, alertas, KPIs y graficos.",
    )

    actions = tk.Frame(self.content, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    actions.pack(fill="x", padx=25, pady=(0, 10))

    top_actions = tk.Frame(actions, bg=self.colors["bg_card"])
    top_actions.pack(fill="x", padx=12, pady=(10, 6))
    ttk.Button(top_actions, text="Buscar operacion", style="Olive.TButton", command=self.cargar_operaciones_centro).pack(side="left", padx=(0, 8))
    ttk.Button(top_actions, text="Generar datos", style="Gray.TButton", command=self.analizar_operacion_centro).pack(side="left", padx=(0, 8))

    filters = tk.Frame(actions, bg=self.colors["bg_card"])
    filters.pack(fill="x", padx=12, pady=(0, 8))

    filter_specs = [
        ("guia", "Guia", self.centro_guia_var, 14),
        ("chofer", "Chofer", self.centro_chofer_var, 18),
        ("placa", "Placa", self.centro_placa_var, 12),
        ("estado", "Estado", self.centro_estado_filtro_var, 12),
        ("etapa_qr", "Etapa QR", self.centro_etapa_qr_var, 12),
    ]
    self.centro_extra_filter_widgets = {}
    for idx, (key, label, var, width) in enumerate(filter_specs):
        box = tk.Frame(filters, bg=self.colors["bg_card"])
        box.grid(row=idx // 5, column=idx % 5, sticky="ew", padx=5, pady=4)
        tk.Label(box, text=label, bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        combo = ttk.Combobox(box, textvariable=var, values=[""], state="normal", width=width)
        combo.pack(fill="x")
        combo.bind("<<ComboboxSelected>>", lambda _event: self.programar_filtrado_centro())
        combo.bind("<KeyRelease>", lambda _event: self.programar_filtrado_centro(delay=650))
        combo.bind("<Return>", lambda _event: self.programar_filtrado_centro(delay=80))
        combo.bind("<FocusOut>", lambda _event: self.programar_filtrado_centro(delay=250))
        self.centro_extra_filter_widgets[key] = combo

    for col in range(5):
        filters.grid_columnconfigure(col, weight=1)

    export_bar = tk.Frame(actions, bg=self.colors["bg_card"])
    export_bar.pack(fill="x", padx=12, pady=(0, 10))
    ttk.Button(export_bar, textvariable=self.centro_fecha_desde_larga_var, style="Gray.TButton", command=lambda: self.abrir_selector_fecha_centro("desde")).pack(side="left", padx=(0, 8))
    ttk.Button(export_bar, textvariable=self.centro_fecha_hasta_larga_var, style="Gray.TButton", command=lambda: self.abrir_selector_fecha_centro("hasta")).pack(side="left", padx=(0, 8))
    ttk.Combobox(export_bar, textvariable=self.centro_exportar_formato_var, values=["PDF", "Excel", "Word"], state="readonly", width=8).pack(side="left", padx=(0, 8))
    ttk.Button(export_bar, text="Exportar", style="Gray.TButton", command=self.exportar_centro).pack(side="left")

    status = tk.Frame(self.content, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    status.pack(fill="x", padx=25, pady=(0, 10))
    tk.Label(
        status,
        textvariable=self.centro_estado_var,
        font=("Segoe UI", 10, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors["text_dark"],
        anchor="w",
    ).pack(fill="x", padx=14, pady=8)

    host = tk.Frame(self.content, bg=self.colors["bg_main"])
    host.pack(fill="both", expand=True, padx=25, pady=(0, 20))

    canvas = tk.Canvas(host, bg=self.colors["bg_main"], highlightthickness=0)
    scroll_y = ttk.Scrollbar(host, orient="vertical", command=canvas.yview)
    scroll_x = ttk.Scrollbar(host, orient="horizontal", command=canvas.xview)
    body = tk.Frame(canvas, bg=self.colors["bg_main"])
    window_id = canvas.create_window((0, 0), window=body, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    self.bind_scroll_canvas(canvas, body, window_id, min_width=1040)
    canvas.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    host.grid_rowconfigure(0, weight=1)
    host.grid_columnconfigure(0, weight=1)

    self.centro_body = body
    body.bind("<Button-1>", lambda _event: self.limpiar_filtros_visuales_centro())

    operaciones_panel = tk.Frame(body, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    operaciones_panel.pack(fill="both", expand=True, pady=(0, 12))
    tk.Label(operaciones_panel, text="Operaciones por buque", font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w", padx=14, pady=(12, 6))
    ops_frame = tk.Frame(operaciones_panel, bg=self.colors["bg_card"])
    ops_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))
    ops_cols = ("id", "buque", "inicio", "producto", "estado")
    self.centro_operaciones_tree = ttk.Treeview(ops_frame, columns=ops_cols, show="headings", height=7)
    for col, heading, width in [
        ("id", "ID", 55),
        ("buque", "Buque", 260),
        ("inicio", "Inicio", 130),
        ("producto", "Producto", 260),
        ("estado", "Estado", 120),
    ]:
        self.centro_operaciones_tree.heading(col, text=heading)
        self.centro_operaciones_tree.column(col, width=width, anchor="center")
    ops_y = ttk.Scrollbar(ops_frame, orient="vertical", command=self.centro_operaciones_tree.yview)
    ops_x = ttk.Scrollbar(ops_frame, orient="horizontal", command=self.centro_operaciones_tree.xview)
    self.centro_operaciones_tree.configure(yscrollcommand=ops_y.set, xscrollcommand=ops_x.set)
    self.centro_operaciones_tree.bind("<<TreeviewSelect>>", lambda _event: self.refrescar_operacion_centro_por_seleccion())
    self.centro_operaciones_tree.grid(row=0, column=0, sticky="nsew")
    ops_y.grid(row=0, column=1, sticky="ns")
    ops_x.grid(row=1, column=0, sticky="ew")
    ops_frame.grid_rowconfigure(0, weight=1)
    ops_frame.grid_columnconfigure(0, weight=1)

    self.centro_kpis_frame = tk.Frame(body, bg=self.colors["bg_main"])
    self.centro_kpis_frame.pack(fill="x", pady=(0, 12))
    self.centro_kpis_frame.bind("<Button-1>", lambda _event: self.limpiar_filtros_visuales_centro())

    top = tk.Frame(body, bg=self.colors["bg_main"])
    top.pack(fill="both", expand=True, pady=(0, 12))
    top.bind("<Button-1>", lambda _event: self.limpiar_filtros_visuales_centro())

    buque_panel = tk.Frame(top, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    buque_panel.pack(side="left", fill="both", expand=True, padx=(0, 8))
    tk.Label(buque_panel, text="Progreso visual por bodega", font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w", padx=14, pady=(12, 6))
    self.centro_buque_canvas = tk.Canvas(buque_panel, bg=self.colors["bg_card"], height=300, highlightthickness=0)
    self.centro_buque_canvas.pack(fill="both", expand=True, padx=14, pady=(0, 12))
    self.centro_buque_canvas.bind("<Button-1>", lambda _event: self.limpiar_filtros_visuales_centro())

    lectura_panel = tk.Frame(top, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1, width=360)
    lectura_panel.pack(side="right", fill="both")
    lectura_panel.pack_propagate(False)
    tk.Label(lectura_panel, text="Lectura ejecutiva", font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w", padx=14, pady=(12, 6))
    lectura_host = tk.Frame(lectura_panel, bg=self.colors["bg_card"])
    lectura_host.pack(fill="both", expand=True, padx=14, pady=(0, 12))
    self.centro_resumen_text = tk.Text(
        lectura_host,
        wrap="word",
        height=12,
        bd=0,
        relief="flat",
        bg=self.colors["bg_card"],
        fg=self.colors["text_dark"],
        insertbackground=self.colors["text_dark"],
        font=("Segoe UI", 10, "bold"),
    )
    lectura_scroll = ttk.Scrollbar(lectura_host, orient="vertical", command=self.centro_resumen_text.yview)
    self.centro_resumen_text.configure(yscrollcommand=lectura_scroll.set)
    self.centro_resumen_text.grid(row=0, column=0, sticky="nsew")
    lectura_scroll.grid(row=0, column=1, sticky="ns")
    lectura_host.grid_rowconfigure(0, weight=1)
    lectura_host.grid_columnconfigure(0, weight=1)
    self.actualizar_lectura_centro("Presione Buscar operacion, seleccione un buque y luego Generar datos.")

    self.centro_charts_frame = tk.Frame(body, bg=self.colors["bg_main"])
    self.centro_charts_frame.pack(fill="both", expand=True, pady=(0, 12))
    self.centro_charts_frame.bind("<Button-1>", lambda _event: self.limpiar_filtros_visuales_centro())

    self.centro_cuotas_tree = self.crear_tabla_centro(
        body,
        "Cuota vs descargado real",
        ("cliente", "producto", "bodega", "stowage_mt", "cuota_mt", "retirado_mt", "diferencia_mt", "avance_pct", "origen"),
        ("Cliente", "Producto", "Bodega", "Stowage MT", "Cuota MT", "Descargado MT", "Pendiente MT", "Avance %", "Origen"),
        side="top",
        height=8,
    )
    self.centro_alertas_tree = self.crear_tabla_centro(
        body,
        "Alertas operativas",
        ("severidad", "tipo", "mensaje"),
        ("Severidad", "Tipo", "Mensaje"),
        side="top",
        height=7,
    )
    self.centro_salud_operativa_tree = None
    self.centro_spc_tree = None
    self.centro_bloqueos_tree = None
    self.centro_excepciones_tree = None
    self.centro_auditoria_senior_tree = None
    self.centro_cierre_guiado_tree = None
    self.centro_modo_offline_tree = None
    self.centro_productividad_tree = None
    self.centro_control_plan_tree = None

    dibujar_buque_centro(self, [])
    render_kpis_operativos_centro(self, {})
    render_graficos_operativos_centro(self, {})


def cargar_centro_ejecutivo(self):
    self.cargar_operaciones_centro()


def cargar_operaciones_centro(self):
    def tarea():
        return self.api_get_operaciones_buque()

    def al_terminar(data):
        self.centro_ops_cache = data.get("data", []) if isinstance(data, dict) else []

        for item in self.centro_operaciones_tree.get_children():
            self.centro_operaciones_tree.delete(item)

        for op in self.centro_ops_cache:
            self.centro_operaciones_tree.insert(
                "",
                "end",
                values=(
                    op.get("id", ""),
                    op.get("nombre_buque", ""),
                    op.get("fecha_inicio", ""),
                    op.get("producto", ""),
                    op.get("estado", ""),
                ),
            )

        self.seleccionar_operacion_relevante_centro()
        render_kpis_operativos_centro(self, {})
        render_graficos_operativos_centro(self, {})
        dibujar_buque_centro(self, [])
        self.centro_estado_var.set(f"Operaciones cargadas: {len(self.centro_ops_cache)}. Seleccione un buque y presione Generar datos.")
        self.actualizar_lectura_centro(
            "Operaciones cargadas. Seleccione un buque y presione Generar datos. Luego cambie filtros para refrescar el tablero automaticamente.",
            self.colors["text_dark"],
        )

    self.ejecutar_en_segundo_plano(
        "Centro Ejecutivo",
        "Buscando operaciones. Por favor espere...",
        tarea,
        al_terminar,
    )


def seleccionar_operacion_centro_por_id(self, operacion_id):
    if not self.centro_operaciones_tree or not operacion_id:
        return False
    objetivo = str(operacion_id)
    for item in self.centro_operaciones_tree.get_children():
        valores = self.centro_operaciones_tree.item(item, "values")
        if valores and str(valores[0]) == objetivo:
            self.centro_operaciones_tree.selection_set(item)
            self.centro_operaciones_tree.focus(item)
            self.centro_operaciones_tree.see(item)
            return True
    return False


def seleccionar_operacion_relevante_centro(self):
    items = self.centro_operaciones_tree.get_children() if self.centro_operaciones_tree else []
    if not items:
        return False
    self.centro_operaciones_tree.selection_set(items[0])
    self.centro_operaciones_tree.focus(items[0])
    self.centro_operaciones_tree.see(items[0])
    return True


def refrescar_operacion_centro_por_seleccion(self):
    self.centro_filtros_precargados = False
    self.actualizar_lectura_centro(
        "Operacion seleccionada. Presione Generar datos. Luego, cualquier filtro aplicado actualiza el tablero automaticamente.",
        self.colors["text_dark"],
    )
    self.cargar_filtros_reporte_centro(silencioso=True)


def analizar_operacion_centro(self, silencioso=False):
    operacion_id = self.obtener_operacion_centro_seleccionada(silencioso=silencioso)
    if not operacion_id:
        return

    params = self.obtener_params_reporte_centro()

    def tarea():
        try:
            return self.api_get_reporte_buque(operacion_id, params)
        except Exception as exc:
            return {"status": "error", "message": str(exc)}

    def al_terminar(data):
        if not isinstance(data, dict):
            mensaje = "No se pudo generar datos. El backend no devolvio informacion valida."
            self.centro_estado_var.set(mensaje)
            if hasattr(self, "actualizar_lectura_centro"):
                self.actualizar_lectura_centro(mensaje, self.colors.get("danger", self.colors["text_dark"]))
            return

        if data.get("error") or data.get("detail") or data.get("status") == "error":
            detalle = data.get("message") or data.get("detail") or data.get("error") or "Error interno del backend."
            mensaje = f"No se pudo generar datos: {detalle}"
            self.centro_estado_var.set(mensaje)
            if hasattr(self, "actualizar_lectura_centro"):
                self.actualizar_lectura_centro(mensaje, self.colors.get("danger", self.colors["text_dark"]))
            return

        operacion = data.get("operacion") if isinstance(data.get("operacion"), dict) else {}
        bodegas = data.get("bodegas") if isinstance(data.get("bodegas"), list) else []
        kpis = data.get("kpis") if isinstance(data.get("kpis"), dict) else {}
        graficos = data.get("graficos") if isinstance(data.get("graficos"), dict) else {}
        alertas = data.get("alertas") if isinstance(data.get("alertas"), list) else []
        plan_viajes = data.get("plan_viajes") if isinstance(data.get("plan_viajes"), dict) else {}
        clientes = data.get("clientes") if isinstance(data.get("clientes"), list) else []

        self.render_control_operativo_centro({
            "operacion": operacion,
            "bodegas": bodegas,
            "kpis": kpis,
            "graficos": graficos,
            "alertas": alertas,
            "plan_viajes": plan_viajes,
            "cuotas_vs_retiro": [
                {
                    "cliente": row.get("empresa"),
                    "producto": "Cuota general" if str(row.get("producto") or "").strip().upper() in ("", "TODOS", "ALL") else row.get("producto"),
                    "bodega": row.get("bodega") or row.get("bodega_numero") or "Todas",
                    "bodega_numeros": row.get("bodega_numeros") or [],
                    "stowage_mt": self.safe_number(row.get("stowage_mt"), 0),
                    "cuota_mt": self.safe_number(row.get("cuota_mt"), 0),
                    "retirado_mt": self.safe_number(row.get("retirado_mt"), 0),
                    "diferencia_mt": self.safe_number(row.get("faltante_mt"), 0),
                    "avance_pct": row.get("avance_pct", 0),
                    "origen": row.get("origen_cuota", ""),
                }
                for row in clientes
                if isinstance(row, dict)
            ],
        })
        self.centro_estado_var.set(f"Datos generados para {operacion.get('nombre_buque', 'operacion seleccionada')}.")
        if not getattr(self, "centro_filtros_precargados", False):
            self.centro_filtros_precargados = True
            self.after(100, lambda: self.cargar_filtros_reporte_centro(silencioso=True))

    if silencioso:
        try:
            al_terminar(tarea())
        except Exception:
            return
    else:
        self.ejecutar_en_segundo_plano(
            "Centro Ejecutivo",
            "Generando datos ejecutivos desde el backend...",
            tarea,
            al_terminar,
        )


def programar_filtrado_centro(self, delay=550):
    if not self.obtener_operacion_centro_seleccionada(silencioso=True):
        return
    after_id = getattr(self, "centro_filter_after_id", None)
    if after_id:
        try:
            self.after_cancel(after_id)
        except Exception:
            pass
    self.centro_estado_var.set("Filtros modificados. Actualizando datos...")
    self.centro_filter_after_id = self.after(delay, lambda: self.analizar_operacion_centro(silencioso=True))


def obtener_operacion_centro_seleccionada(self, silencioso=False):
    seleccion = self.centro_operaciones_tree.selection() if self.centro_operaciones_tree else []
    if not seleccion:
        if not silencioso:
            messagebox.showwarning("Sin seleccion", "Seleccione una operacion de buque.")
        return None
    valores = self.centro_operaciones_tree.item(seleccion[0], "values")
    return self.safe_int(valores[0], None) if valores else None


def obtener_params_reporte_centro(self):
    params = {}
    empresa = self.centro_empresa_var.get().strip() if hasattr(self, "centro_empresa_var") else ""
    if empresa:
        params["empresa"] = empresa
    bodega = self.centro_bodega_var.get().strip() if hasattr(self, "centro_bodega_var") else ""
    if bodega:
        params["bodega_numero"] = bodega
    fecha_desde = self.centro_fecha_desde_var.get().strip() if hasattr(self, "centro_fecha_desde_var") else ""
    if fecha_desde:
        params["fecha_desde"] = fecha_desde
    fecha_hasta = self.centro_fecha_hasta_var.get().strip() if hasattr(self, "centro_fecha_hasta_var") else ""
    if fecha_hasta:
        params["fecha_hasta"] = fecha_hasta
    for key, var_name in [
        ("guia", "centro_guia_var"),
        ("producto", "centro_producto_var"),
        ("chofer", "centro_chofer_var"),
        ("placa", "centro_placa_var"),
        ("estado", "centro_estado_filtro_var"),
        ("etapa_qr", "centro_etapa_qr_var"),
    ]:
        var = getattr(self, var_name, None)
        value = var.get().strip() if var else ""
        if value:
            params[key] = value
    return params


def cargar_filtros_reporte_centro(self, silencioso=False):
    operacion_id = self.obtener_operacion_centro_seleccionada(silencioso=silencioso)
    if not operacion_id:
        return

    def tarea():
        data = self.api_get_reporte_buque_filtros(operacion_id)
        opciones = data.get("opciones", {}) if isinstance(data, dict) else {}
        if not any(opciones.get(key) for key in ("empresas", "guias", "productos", "choferes", "placas", "estados", "etapas_qr")):
            filas = self.api_get_boletas({"operacion_id": operacion_id})
            data["opciones"] = opciones_centro_desde_boletas(self, filas)
        return data

    def al_terminar(data):
        opciones = data.get("opciones", {})
        aplicar_opciones_centro(self, opciones)
        self.centro_estado_var.set("Filtros listos. Al cambiar un filtro, el tablero se actualiza automaticamente.")

    if silencioso:
        def worker_silencioso():
            try:
                data = tarea()
            except Exception:
                return
            try:
                self.after(0, lambda: al_terminar(data))
            except Exception:
                pass

        import threading
        threading.Thread(target=worker_silencioso, daemon=True).start()
    else:
        self.ejecutar_en_segundo_plano(
            "Filtros reporte",
            "Cargando filtros dinamicos...",
            tarea,
            al_terminar,
        )


def cargar_control_plan_centro(self):
    operacion_id = self.obtener_operacion_centro_seleccionada()
    if not operacion_id:
        return

    def tarea():
        return self.api_get_control_plan_operativo(operacion_id)

    def al_terminar(data):
        self.render_control_plan_centro(data)
        resumen = data.get("resumen", {}) if isinstance(data, dict) else {}
        self.centro_estado_var.set(
            "Control plan listo. "
            f"Estado: {resumen.get('estado_general', '-')}. "
            f"Score: {self.safe_number(resumen.get('score')):,.2f}%."
        )

    self.ejecutar_en_segundo_plano(
        "Control Plan",
        "Evaluando controles operativos de la operacion...",
        tarea,
        al_terminar,
    )


def cargar_salud_operativa_centro(self):
    operacion_id = self.obtener_operacion_centro_seleccionada()
    if not operacion_id:
        return

    def tarea():
        return self.api_get_salud_operativa(operacion_id)

    def al_terminar(data):
        self.render_salud_operativa_centro(data)
        resumen = data.get("resumen", {}) if isinstance(data, dict) else {}
        self.centro_estado_var.set(
            "Salud operativa lista. "
            f"Estado: {resumen.get('estado_general', '-')}. "
            f"Score: {self.safe_number(resumen.get('score_global')):,.2f}%. "
            f"Bloqueadores: {resumen.get('bloqueadores', 0)}."
        )

    self.ejecutar_en_segundo_plano(
        "Salud Operativa",
        "Calculando salud operativa de la operacion...",
        tarea,
        al_terminar,
    )


def cargar_spc_centro(self):
    operacion_id = self.obtener_operacion_centro_seleccionada()
    if not operacion_id:
        return

    def tarea():
        return self.api_get_spc_operativo(operacion_id)

    def al_terminar(data):
        self.render_spc_centro(data)
        resumen = data.get("resumen", {}) if isinstance(data, dict) else {}
        self.centro_estado_var.set(
            "SPC listo. "
            f"Estado: {resumen.get('estado_general', '-')}. "
            f"Senales: {resumen.get('senales', 0)}. "
            f"Fuera control: {resumen.get('fuera_control', 0)}."
        )

    self.ejecutar_en_segundo_plano(
        "SPC",
        "Calculando control estadistico del proceso...",
        tarea,
        al_terminar,
    )


def cargar_bloqueos_inteligentes_centro(self):
    operacion_id = self.obtener_operacion_centro_seleccionada()
    if not operacion_id:
        return

    def tarea():
        return self.api_get_bloqueos_inteligentes(operacion_id)

    def al_terminar(data):
        self.render_bloqueos_inteligentes_centro(data)
        resumen = data.get("resumen", {}) if isinstance(data, dict) else {}
        self.centro_estado_var.set(
            "Bloqueos inteligentes listos. "
            f"Estado: {resumen.get('estado_general', '-')}. "
            f"Bloqueos: {resumen.get('bloqueos', 0)}. "
            f"Advertencias: {resumen.get('advertencias', 0)}."
        )

    self.ejecutar_en_segundo_plano(
        "Bloqueos Inteligentes",
        "Evaluando bloqueos inteligentes de la operacion...",
        tarea,
        al_terminar,
    )


def cargar_excepciones_operativas_centro(self):
    operacion_id = self.obtener_operacion_centro_seleccionada()
    if not operacion_id:
        return

    def tarea():
        return self.api_get_excepciones_operativas(operacion_id)

    def al_terminar(data):
        self.render_excepciones_operativas_centro(data)
        resumen = data.get("resumen", {}) if isinstance(data, dict) else {}
        self.centro_estado_var.set(
            "Excepciones cargadas. "
            f"Abiertas: {resumen.get('abiertas', 0)}. "
            f"Altas/criticas: {resumen.get('criticas_altas', 0)}."
        )

    self.ejecutar_en_segundo_plano(
        "Excepciones",
        "Cargando bandeja de excepciones operativas...",
        tarea,
        al_terminar,
    )


def cargar_auditoria_senior_centro(self):
    operacion_id = self.obtener_operacion_centro_seleccionada()
    if not operacion_id:
        return

    def tarea():
        return self.api_get_auditoria_senior(operacion_id)

    def al_terminar(data):
        self.render_auditoria_senior_centro(data)
        kpis = data.get("kpis", {}) if isinstance(data, dict) else {}
        self.centro_estado_var.set(
            "Auditoria senior lista. "
            f"Nivel: {data.get('nivel', '-')}. "
            f"Score: {self.safe_number(data.get('score_general')):,.2f}%. "
            f"Hallazgos: {kpis.get('hallazgos', 0)}."
        )
        resumen = data.get("resumen", "") if isinstance(data, dict) else ""
        prioridades = data.get("prioridades", []) if isinstance(data, dict) else []
        texto = (
            f"{resumen}\n\n"
            f"Score senior: {self.safe_number(data.get('score_general')):,.2f}% | Nivel: {data.get('nivel', '-')}\n"
            f"Criticos: {kpis.get('criticos', 0)} | Altos: {kpis.get('altos', 0)} | Medios: {kpis.get('medios', 0)}\n\n"
            "Prioridades:\n"
        )
        for item in prioridades[:5]:
            texto += f"- {item.get('dimension', '')}: {item.get('titulo', '')}. Accion: {item.get('accion', '')}\n"
        self.actualizar_lectura_centro(texto, self.colors["danger"] if data.get("nivel") == "CRITICO" else self.colors["warning"] if data.get("nivel") == "OBSERVACION" else self.colors["success"])

    self.ejecutar_en_segundo_plano(
        "Auditoria Senior",
        "Ejecutando auditoria senior transversal de la operacion...",
        tarea,
        al_terminar,
    )


def cargar_cierre_guiado_centro(self):
    operacion_id = self.obtener_operacion_centro_seleccionada()
    if not operacion_id:
        return

    def tarea():
        return self.api_get_cierre_guiado(operacion_id)

    def al_terminar(data):
        self.centro_cierre_guiado_data = data
        self.render_cierre_guiado_centro(data)
        kpis = data.get("kpis", {}) if isinstance(data, dict) else {}
        estado = "LISTO" if data.get("puede_cerrar") else "BLOQUEADO"
        if data.get("requiere_confirmacion"):
            estado = "LISTO CON OBSERVACIONES"
        self.centro_estado_var.set(
            "Cierre guiado evaluado. "
            f"Estado: {estado}. "
            f"OK: {kpis.get('checks_ok', 0)} | "
            f"Pendientes: {kpis.get('checks_pendientes', 0)} | "
            f"Bloqueos: {kpis.get('checks_bloqueados', 0)}."
        )
        texto = (
            f"{data.get('resumen', '')}\n\n"
            f"Nivel: {data.get('nivel', '-')}\n"
            f"Guias total: {kpis.get('guias_total', 0)} | Completas: {kpis.get('guias_completas', 0)} | "
            f"En proceso: {kpis.get('guias_en_proceso', 0)} | Sin uso: {kpis.get('guias_sin_uso', 0)}\n"
            f"Excepciones abiertas: {kpis.get('excepciones_abiertas', 0)} | En revision: {kpis.get('excepciones_en_revision', 0)}\n\n"
            "Checklist de cierre:\n"
        )
        for item in data.get("checklist", [])[:8]:
            texto += f"- [{item.get('estado')}] {item.get('control')}: {item.get('evidencia')}\n"
        color = self.colors["success"] if data.get("nivel") == "LISTO" else self.colors["warning"] if data.get("puede_cerrar") else self.colors["danger"]
        self.actualizar_lectura_centro(texto, color)

    self.ejecutar_en_segundo_plano(
        "Cierre Operativo Guiado",
        "Validando checklist de cierre operativo guiado...",
        tarea,
        al_terminar,
    )


def cargar_modo_offline_centro(self):
    operacion_id = self.obtener_operacion_centro_seleccionada()
    if not operacion_id:
        return

    def tarea():
        return self.api_get_modo_offline(operacion_id)

    def al_terminar(data):
        self.centro_modo_offline_data = data
        self.render_modo_offline_centro(data)
        kpis = data.get("kpis", {}) if isinstance(data, dict) else {}
        self.centro_estado_var.set(
            "Modo offline evaluado. "
            f"Estado: {data.get('estado', '-')}. "
            f"Cache: {kpis.get('guias_cacheadas', 0)}/{kpis.get('guias_total', 0)} | "
            f"Bloqueos: {kpis.get('bloqueos', 0)} | Pendientes: {kpis.get('pendientes', 0)}."
        )
        texto = (
            f"{data.get('resumen', '')}\n\n"
            f"Estado: {data.get('estado', '-')}\n"
            f"Guias cacheadas: {kpis.get('guias_cacheadas', 0)}/{kpis.get('guias_total', 0)} "
            f"({self.formatear_numero(kpis.get('cobertura_cache_pct'), 2)}%)\n"
            f"QR activos: {kpis.get('qr_activos', 0)} | En proceso: {kpis.get('en_proceso', 0)} | "
            f"Completas: {kpis.get('completas', 0)} | SOF: {kpis.get('sof_total', 0)}\n\n"
            "Reglas offline:\n"
        )
        for regla in data.get("reglas", []):
            texto += f"- {regla}\n"
        color = self.colors["success"] if data.get("estado") == "LISTO_OFFLINE" else self.colors["warning"] if data.get("estado") == "LISTO_CON_OBSERVACIONES" else self.colors["danger"]
        self.actualizar_lectura_centro(texto, color)

    self.ejecutar_en_segundo_plano(
        "Modo Offline Blindado",
        "Evaluando cache, cola local, QR y sincronizacion offline...",
        tarea,
        al_terminar,
    )


def cargar_productividad_centro(self):
    operacion_id = self.obtener_operacion_centro_seleccionada()
    if not operacion_id:
        return

    def tarea():
        return self.api_get_productividad_operativa(operacion_id)

    def al_terminar(data):
        self.centro_productividad_data = data
        self.render_productividad_centro(data)
        resumen = data.get("resumen", {}) if isinstance(data, dict) else {}
        ranking = data.get("ranking", {}) if isinstance(data, dict) else {}
        mejor = ranking.get("mejor_chofer") or {}
        cuello = ranking.get("cuello_botella") or {}
        self.centro_estado_var.set(
            "Productividad calculada. "
            f"MT/h: {self.formatear_numero(resumen.get('mt_por_hora'), 2)} | "
            f"MT/viaje: {self.formatear_numero(resumen.get('peso_promedio_mt'), 2)} | "
            f"Duracion: {self.formatear_numero(resumen.get('duracion_prom_min'), 2)} min."
        )
        texto = (
            "Vista de Productividad\n\n"
            f"Guias: {self.formatear_numero(resumen.get('total_guias'))} | "
            f"Completas: {self.formatear_numero(resumen.get('completas'))} | "
            f"En proceso: {self.formatear_numero(resumen.get('en_proceso'))}\n"
            f"Descargado: {self.formatear_numero(resumen.get('descargado_mt'), 2)} MT | "
            f"Avance operativo: {self.formatear_numero(resumen.get('avance_operativo_pct'), 2)}%\n"
            f"Promedio por viaje: {self.formatear_numero(resumen.get('peso_promedio_mt'), 2)} MT | "
            f"Duracion promedio: {self.formatear_numero(resumen.get('duracion_prom_min'), 2)} min | "
            f"Productividad: {self.formatear_numero(resumen.get('mt_por_hora'), 2)} MT/h\n\n"
            f"Mejor rendimiento: {mejor.get('nombre', '-')}\n"
            f"Mayor cuello de botella: {cuello.get('nombre', '-')}\n\n"
            "Recomendaciones:\n"
        )
        for item in data.get("recomendaciones", [])[:6]:
            texto += f"- {item}\n"
        self.actualizar_lectura_centro(texto, self.colors["info"])

    self.ejecutar_en_segundo_plano(
        "Vista de Productividad",
        "Calculando productividad por chofer, cliente, producto y bodega...",
        tarea,
        al_terminar,
    )


def ejecutar_cierre_guiado_centro(self):
    operacion_id = self.obtener_operacion_centro_seleccionada()
    if not operacion_id:
        return

    data = getattr(self, "centro_cierre_guiado_data", None)
    if not isinstance(data, dict) or data.get("operacion", {}).get("id") != operacion_id:
        try:
            data = self.api_get_cierre_guiado(operacion_id)
            self.centro_cierre_guiado_data = data
            self.render_cierre_guiado_centro(data)
        except Exception as exc:
            messagebox.showerror("Cierre guiado", str(exc))
            return

    if not data.get("puede_cerrar"):
        messagebox.showwarning(
            "Cierre bloqueado",
            "El cierre guiado detecto bloqueos. Revise la tabla Cierre Operativo Guiado antes de cerrar.",
        )
        return

    comentario = simpledialog.askstring(
        "Ejecutar cierre guiado",
        "Comentario de cierre operativo:",
        parent=self,
    )
    if comentario is None:
        return

    forzar = bool(data.get("requiere_confirmacion"))
    mensaje = "Desea cerrar la operacion con cierre operativo guiado?"
    if forzar:
        mensaje = "Hay observaciones no criticas. Desea cerrar con confirmacion gerencial?"
    if not messagebox.askyesno("Confirmar cierre", mensaje):
        return

    def tarea():
        return self.api_ejecutar_cierre_guiado(
            operacion_id,
            {"comentario": comentario, "usuario": "desktop", "forzar": forzar},
        )

    def al_terminar(resultado):
        evaluacion = resultado.get("evaluacion", {}) if isinstance(resultado, dict) else {}
        self.centro_cierre_guiado_data = evaluacion
        self.render_cierre_guiado_centro(evaluacion)
        self.centro_estado_var.set(resultado.get("mensaje", "Operacion cerrada con cierre guiado."))
        messagebox.showinfo("Cierre guiado", resultado.get("mensaje", "Operacion cerrada correctamente."))
        self.cargar_operaciones_centro()

    self.ejecutar_en_segundo_plano(
        "Ejecutar cierre guiado",
        "Cerrando operacion con checklist guiado...",
        tarea,
        al_terminar,
    )


def generar_excepciones_desde_bloqueos_centro(self):
    operacion_id = self.obtener_operacion_centro_seleccionada()
    if not operacion_id:
        return

    def tarea():
        return self.api_generar_excepciones_desde_bloqueos(operacion_id)

    def al_terminar(data):
        self.centro_estado_var.set(data.get("mensaje", "Excepciones generadas desde bloqueos."))
        self.cargar_excepciones_operativas_centro()

    self.ejecutar_en_segundo_plano(
        "Generar excepciones",
        "Convirtiendo bloqueos inteligentes en excepciones gestionables...",
        tarea,
        al_terminar,
    )


def cerrar_excepcion_centro(self):
    tree = getattr(self, "centro_excepciones_tree", None)
    if tree is None:
        return
    seleccion = tree.selection()
    if not seleccion:
        messagebox.showwarning("Sin seleccion", "Seleccione una excepcion en la tabla Gestion de Excepciones.")
        return
    valores = tree.item(seleccion[0], "values")
    if not valores:
        return
    excepcion_id = self.safe_int(valores[0], None)
    if excepcion_id is None:
        messagebox.showwarning("Seleccion invalida", "La excepcion seleccionada no tiene ID valido.")
        return
    comentario = simpledialog.askstring("Cerrar excepcion", "Comentario de cierre:", parent=self)
    if not comentario:
        return

    def tarea():
        return self.api_cerrar_excepcion_operativa(excepcion_id, comentario)

    def al_terminar(data):
        self.centro_estado_var.set(data.get("mensaje", "Excepcion cerrada."))
        self.cargar_excepciones_operativas_centro()

    self.ejecutar_en_segundo_plano(
        "Cerrar excepcion",
        "Cerrando excepcion operativa...",
        tarea,
        al_terminar,
    )


def abrir_selector_fecha_centro(self, target):
    popup = tk.Toplevel(self)
    popup.title("Seleccionar fecha")
    popup.geometry("360x210")
    popup.configure(bg=self.colors["bg_card"])
    popup.transient(self)
    popup.grab_set()
    hoy = date.today()
    actual = self.centro_fecha_desde_var.get() if target == "desde" else self.centro_fecha_hasta_var.get()
    try:
        base = date.fromisoformat(actual) if actual else hoy
    except Exception:
        base = hoy
    dia_var = tk.StringVar(value=str(base.day))
    mes_var = tk.StringVar(value=self.meses_es()[base.month - 1])
    anio_var = tk.StringVar(value=str(base.year))
    contenido = tk.Frame(popup, bg=self.colors["bg_card"])
    contenido.pack(fill="both", expand=True, padx=18, pady=18)
    tk.Label(contenido, text="Fecha de filtro", font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w", pady=(0, 12))
    fila = tk.Frame(contenido, bg=self.colors["bg_card"])
    fila.pack(fill="x")
    ttk.Combobox(fila, textvariable=dia_var, values=[str(i) for i in range(1, 32)], state="readonly", width=6).pack(side="left", padx=(0, 8))
    ttk.Combobox(fila, textvariable=mes_var, values=self.meses_es(), state="readonly", width=14).pack(side="left", padx=(0, 8))
    ttk.Combobox(fila, textvariable=anio_var, values=[str(i) for i in range(hoy.year - 3, hoy.year + 6)], state="readonly", width=8).pack(side="left")

    def limpiar_fecha():
        if target == "desde":
            self.centro_fecha_desde_var.set("")
            self.centro_fecha_desde_larga_var.set("Desde")
        else:
            self.centro_fecha_hasta_var.set("")
            self.centro_fecha_hasta_larga_var.set("Hasta")
        popup.destroy()

    def aplicar():
        try:
            mes = self.meses_es().index(mes_var.get()) + 1
            seleccion = date(int(anio_var.get()), mes, int(dia_var.get()))
        except Exception:
            messagebox.showerror("Fecha invalida", "Seleccione una fecha valida.")
            return
        if target == "desde":
            self.centro_fecha_desde_var.set(seleccion.isoformat())
            self.centro_fecha_desde_larga_var.set(self.fecha_larga_es(seleccion.isoformat()))
        else:
            self.centro_fecha_hasta_var.set(seleccion.isoformat())
            self.centro_fecha_hasta_larga_var.set(self.fecha_larga_es(seleccion.isoformat()))
        popup.destroy()
        self.centro_estado_var.set("Fecha aplicada. Presione Generar datos para consultar el backend.")

    acciones = tk.Frame(contenido, bg=self.colors["bg_card"])
    acciones.pack(fill="x", pady=(18, 0))
    ttk.Button(acciones, text="Aplicar", style="Olive.TButton", command=aplicar).pack(side="left", padx=(0, 8))
    ttk.Button(acciones, text="Limpiar", style="Gray.TButton", command=limpiar_fecha).pack(side="left", padx=(0, 8))
    ttk.Button(acciones, text="Cancelar", style="Gray.TButton", command=popup.destroy).pack(side="left")


def exportar_centro(self):
    operacion_id = self.obtener_operacion_centro_seleccionada()
    if not operacion_id:
        return
    formato_ui = self.centro_exportar_formato_var.get().strip().lower()
    formato = "excel" if formato_ui == "excel" else "word" if formato_ui == "word" else "pdf"
    extension = ".xlsx" if formato == "excel" else ".docx" if formato == "word" else ".pdf"
    filetypes = [("Excel", "*.xlsx")] if formato == "excel" else [("Word", "*.docx")] if formato == "word" else [("PDF", "*.pdf")]
    ruta = filedialog.asksaveasfilename(
        title=f"Exportar reporte {formato_ui.upper()}",
        defaultextension=extension,
        filetypes=filetypes,
    )
    if not ruta:
        return
    params = self.obtener_params_reporte_centro()

    def tarea():
        return self.api_descargar_reporte_buque(operacion_id, formato, ruta, params)

    def al_terminar(_resultado):
        messagebox.showinfo("Reporte exportado", f"Archivo generado correctamente:\n{ruta}")

    self.ejecutar_en_segundo_plano(
        "Exportar",
        f"Generando reporte {formato_ui.upper()}...",
        tarea,
        al_terminar,
    )


def render_control_operativo_centro(self, data):
    operacion = data.get("operacion", {})
    kpis = data.get("kpis", {})
    graficos = data.get("graficos", {})
    cuotas = data.get("cuotas_vs_retiro", [])
    alertas = data.get("alertas", [])
    bodegas = data.get("bodegas", [])
    plan_viajes = data.get("plan_viajes", {}) or {}
    if not plan_viajes.get("mensaje"):
        promedio = self.safe_number(kpis.get("promedio_mt_camion"), 0)
        pendiente = self.safe_number(kpis.get("faltante_mt"), 0)
        viajes_necesarios = self.safe_int(kpis.get("viajes_estimados_necesarios"), 0)
        disponibles = self.safe_int(kpis.get("viajes_disponibles_aprobados"), 0)
        if promedio > 0 and pendiente > 0:
            if not viajes_necesarios:
                import math
                viajes_necesarios = int(math.ceil(pendiente / promedio))
            diferencia = disponibles - viajes_necesarios
            if diferencia > 0:
                mensaje = f"Promedio real por camion {promedio:,.2f} MT. Pendiente {pendiente:,.2f} MT: se estiman {viajes_necesarios} viajes; hay {disponibles} aprobados pendientes. Revise {diferencia} viajes que podrian no requerirse."
            elif diferencia < 0:
                mensaje = f"Promedio real por camion {promedio:,.2f} MT. Pendiente {pendiente:,.2f} MT: se estiman {viajes_necesarios} viajes; hay {disponibles} aprobados pendientes. Podrian faltar {abs(diferencia)} viajes."
            else:
                mensaje = f"Promedio real por camion {promedio:,.2f} MT. Pendiente {pendiente:,.2f} MT: se estiman {viajes_necesarios} viajes."
            plan_viajes = {"mensaje": mensaje}
        elif pendiente > 0:
            plan_viajes = {"mensaje": "Aun no hay pesos completos suficientes para estimar viajes restantes."}
    riesgo = "ALTO" if alertas else "CONTROLADO"
    color = self.colors["danger"] if riesgo == "ALTO" else self.colors["success"]
    self.actualizar_lectura_centro(
        (
            f"Buque: {operacion.get('nombre_buque', '')}\n"
            f"Estado: {operacion.get('estado', '')}\n"
            f"Guias: {kpis.get('total_guias', 0)} | Completas: {kpis.get('completas', 0)}\n"
            f"Descargado: {self.formatear_numero(self.valor_descargado_visible_centro(kpis), 2)} MT\n"
            f"Pendiente de descarga: {self.formatear_numero(kpis.get('faltante_mt'), 2)} MT\n"
            f"Avance: {self.safe_number(kpis.get('avance_descarga_pct')):,.2f}% | Riesgo: {riesgo}\n\n"
            f"Plan viajes:\n{plan_viajes.get('mensaje', 'Sin estimacion disponible.')}"
        ),
        color,
    )
    self.centro_estado_var.set(
        f"Lectura ejecutiva lista. Riesgo: {riesgo}. Avance: {self.safe_number(kpis.get('avance_descarga_pct')):,.2f}%."
    )
    render_kpis_operativos_centro(self, kpis)
    dibujar_buque_centro(self, bodegas)
    render_graficos_operativos_centro(self, graficos)
    render_tablas_operativas_centro(self, cuotas, alertas)


def actualizar_lectura_centro(self, texto, color=None):
    color = color or self.colors["text_dark"]
    widget = getattr(self, "centro_resumen_text", None)
    if widget is not None:
        widget.configure(state="normal", fg=color)
        widget.delete("1.0", "end")
        widget.insert("1.0", texto)
        widget.configure(state="disabled")
        return
    label = getattr(self, "centro_resumen_label", None)
    if label is not None:
        label.configure(text=texto, fg=color)


def opciones_centro_desde_boletas(self, filas):
    filas = filas or []
    def valores(campo):
        resultado = set()
        for fila in filas:
            if isinstance(fila, dict):
                valor = fila.get(campo)
            else:
                valor = None
            if valor not in (None, ""):
                resultado.add(str(valor).strip())
        return sorted(resultado)

    return {
        "empresas": valores("empresa"),
        "productos": valores("producto"),
        "bodegas": valores("bodega_numero"),
        "guias": valores("guia"),
        "choferes": valores("chofer"),
        "placas": valores("placa"),
        "estados": valores("estado"),
        "etapas_qr": valores("etapa_qr"),
    }


def aplicar_opciones_centro(self, opciones):
    opciones = opciones or {}
    empresas = [""] + [str(item) for item in opciones.get("empresas", []) if item not in (None, "")]
    bodegas_base = opciones.get("bodegas", []) or ["1", "2", "3", "4", "5"]
    bodegas = [""] + [str(item) for item in bodegas_base if item not in (None, "")]
    if hasattr(self, "centro_empresa_combo"):
        self.centro_empresa_combo["values"] = empresas
    if hasattr(self, "centro_bodega_combo"):
        self.centro_bodega_combo["values"] = bodegas
    for key, option_key in {
        "guia": "guias",
        "producto": "productos",
        "chofer": "choferes",
        "placa": "placas",
        "estado": "estados",
        "etapa_qr": "etapas_qr",
    }.items():
        widget = getattr(self, "centro_extra_filter_widgets", {}).get(key)
        if widget:
            widget["values"] = [""] + [str(item) for item in opciones.get(option_key, []) if item not in (None, "")]
    if hasattr(self, "centro_empresa_var") and self.centro_empresa_var.get() and self.centro_empresa_var.get() not in empresas:
        self.centro_empresa_var.set("")
    if hasattr(self, "centro_bodega_var") and self.centro_bodega_var.get() and self.centro_bodega_var.get() not in bodegas:
        self.centro_bodega_var.set("")


def render_kpis_operativos_centro(self, kpis):
    for widget in self.centro_kpis_frame.winfo_children():
        widget.destroy()
    descargado_visible = self.valor_descargado_visible_centro(kpis)
    cards = [
        ("Guias", self.formatear_numero(kpis.get("total_guias")), self.colors["accent"]),
        ("Completas", self.formatear_numero(kpis.get("completas")), self.colors["success"]),
        ("Pendientes", self.formatear_numero(kpis.get("pendientes")), self.colors["warning"]),
        ("Capacidad MT", self.formatear_numero(kpis.get("capacidad_mt"), 2), self.colors["info"]),
        ("Descargado MT", self.formatear_numero(descargado_visible, 2), self.colors["success"]),
        ("Pendiente MT", self.formatear_numero(kpis.get("faltante_mt"), 2), self.colors["warning"]),
        ("Avance", f"{self.safe_number(kpis.get('avance_descarga_pct')):,.2f}%", self.colors["accent"]),
        ("Duracion prom.", f"{self.safe_number(kpis.get('duracion_promedio_min')):,.2f} min", self.colors["muted"]),
        ("MT/camion", self.formatear_numero(kpis.get("promedio_mt_camion"), 2), self.colors["info"]),
        ("Viajes sug.", self.formatear_numero(kpis.get("viajes_estimados_necesarios")), self.colors["warning"]),
    ]
    grid = tk.Frame(self.centro_kpis_frame, bg=self.colors["bg_main"])
    grid.pack(fill="x")
    for idx, (title, value, color) in enumerate(cards):
        row = idx // 5
        col = idx % 5
        _crear_kpi_compacto_centro(self, grid, title, value, color, row, col)
    for col in range(5):
        grid.grid_columnconfigure(col, weight=1, uniform="centro_kpi")


def _crear_kpi_compacto_centro(self, parent, title, value, color, row, col):
    card = tk.Frame(
        parent,
        bg=self.colors["bg_card"],
        highlightbackground=self.colors["border"],
        highlightthickness=1,
        height=86,
    )
    card.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)
    card.grid_propagate(False)
    tk.Frame(card, bg=color, width=5).pack(side="left", fill="y")
    body = tk.Frame(card, bg=self.colors["bg_card"])
    body.pack(side="left", fill="both", expand=True, padx=11, pady=9)
    tk.Label(
        body,
        text=title,
        font=("Segoe UI", 9, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors["text_secondary"],
        anchor="w",
    ).pack(fill="x")
    tk.Label(
        body,
        text=str(value),
        font=("Segoe UI", 17, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors["text_dark"],
        anchor="w",
    ).pack(fill="x", pady=(6, 0))


def normalizar_valor_kg_centro(self, data, mt_key="retirado_mt", kg_key="retirado_kg"):
    normalizados = []
    if not isinstance(data, list):
        return normalizados
    for row in data:
        if not isinstance(row, dict):
            continue
        item = dict(row)
        item[kg_key] = self.valor_descargado_visible_centro(item, mt_key, kg_key)
        normalizados.append(item)
    return normalizados


def valor_descargado_visible_centro(self, row, mt_key="retirado_mt", kg_key="retirado_kg"):
    if not isinstance(row, dict):
        return 0
    mt_raw = row.get(mt_key)
    kg_raw = row.get(kg_key)
    mt = self.safe_number(mt_raw, 0)
    kg = self.safe_number(kg_raw, 0)
    if kg_raw not in (None, "") and (mt_raw in (None, "") or abs(kg) > abs(mt) * 10):
        return kg
    if mt_raw not in (None, ""):
        return mt
    return kg


def normalizar_estado_descarga_visible_centro(self, data):
    normalizados = []
    if not isinstance(data, list):
        return normalizados
    for row in data:
        if not isinstance(row, dict):
            continue
        item = dict(row)
        estado = str(item.get("estado") or "").lower()
        if "descargado" in estado:
            item["valor"] = self.safe_number(
                item.get("valor_kg", item.get("retirado_kg", item.get("valor"))),
                0,
            )
        normalizados.append(item)
    return normalizados


def render_graficos_operativos_centro(self, graficos):
    for widget in self.centro_charts_frame.winfo_children():
        widget.destroy()
    charts_grid = tk.Frame(self.centro_charts_frame, bg=self.colors["bg_main"])
    charts_grid.pack(fill="both", expand=True)
    charts_grid.bind("<Button-1>", lambda _event: self.limpiar_filtros_visuales_centro())
    bodegas_chart_base = graficos.get("avance_bodegas_detalle") or graficos.get("avance_bodegas", [])
    avance_bodegas_descargado = [
        {
            **row,
            "bodega_producto": f"{row.get('bodega') or 'Bodega ' + str(row.get('bodega_numero') or '')} | {row.get('producto') or 'Sin producto'}",
        }
        for row in bodegas_chart_base
        if isinstance(row, dict)
    ]
    retiro_cliente_mt = [
        {
            **row,
            "cliente_producto": f"{row.get('cliente') or row.get('empresa') or 'SIN CLIENTE'} | {('Cuota general' if str(row.get('producto') or '').strip().upper() in ('', 'TODOS', 'ALL') else row.get('producto'))}",
        }
        for row in graficos.get("retiro_por_cliente", [])
        if isinstance(row, dict)
    ]
    retiro_producto_mt = [
        {
            **row,
            "producto": "Cuota general" if str(row.get("producto") or "").strip().upper() in ("", "TODOS", "ALL") else row.get("producto"),
        }
        for row in graficos.get("retiro_por_producto", [])
        if isinstance(row, dict)
    ]
    tendencia_mt = graficos.get("tendencia_fecha", [])
    estado_descarga = graficos.get("estado_descarga", [])
    self.crear_chart_barras_interactivo_centro(
        charts_grid,
        "Descargado por bodega (MT)",
        avance_bodegas_descargado,
        "bodega_producto",
        "retirado_mt",
        0,
        0,
        lambda item: self.aplicar_filtro_centro_desde_click("bodega", item.get("bodega_numero") or item.get("bodega")),
    )
    self.crear_chart_barras_interactivo_centro(
        charts_grid,
        "Pendiente por bodega (MT)",
        avance_bodegas_descargado,
        "bodega_producto",
        "faltante_mt",
        0,
        1,
        lambda item: self.aplicar_filtro_centro_desde_click("bodega", item.get("bodega_numero") or item.get("bodega")),
    )
    self.crear_chart_circular(charts_grid, "Estado descarga", estado_descarga, "estado", "valor", 1, 0)
    self.crear_chart_barras_interactivo_centro(
        charts_grid,
        "Descargado por cliente (MT)",
        retiro_cliente_mt,
        "cliente_producto",
        "retirado_mt",
        1,
        1,
        lambda item: self.aplicar_filtro_centro_desde_click("empresa", item.get("cliente") or item.get("empresa")),
    )
    self.crear_chart_barras_interactivo_centro(
        charts_grid,
        "Descargado por producto (MT)",
        retiro_producto_mt,
        "producto",
        "retirado_mt",
        2,
        0,
        lambda item: self.aplicar_filtro_centro_desde_click("producto", item.get("producto")),
    )
    self.crear_chart_circular(charts_grid, "Estado de guias", graficos.get("estado_guias", []), "estado", "valor", 2, 1)
    self.crear_chart_lineal(charts_grid, "Tendencia diaria descargado (MT)", tendencia_mt, "fecha", "retirado_mt", 3, 0)
    self.crear_chart_barras(charts_grid, "Duracion por camion (min)", graficos.get("duracion_por_camion", []), "camion", "duracion_min", 3, 1)
    self.crear_chart_barras_interactivo_centro(
        charts_grid,
        "Avance por bodega (%)",
        avance_bodegas_descargado,
        "bodega_producto",
        "avance_pct",
        4,
        0,
        lambda item: self.aplicar_filtro_centro_desde_click("bodega", item.get("bodega_numero") or item.get("bodega")),
    )
    for col in range(2):
        charts_grid.grid_columnconfigure(col, weight=1, uniform="centro_charts")
    for row in range(5):
        charts_grid.grid_rowconfigure(row, weight=1, minsize=290)


def aplicar_filtro_centro_desde_click(self, key, value):
    if value in (None, ""):
        return
    self._centro_click_interactivo = True
    text = str(value).strip()
    if key == "bodega":
        import re
        match = re.search(r"\d+", text)
        text = match.group(0) if match else text

    mapping = {
        "empresa": getattr(self, "centro_empresa_var", None),
        "bodega": getattr(self, "centro_bodega_var", None),
        "producto": getattr(self, "centro_producto_var", None),
        "guia": getattr(self, "centro_guia_var", None),
        "chofer": getattr(self, "centro_chofer_var", None),
        "placa": getattr(self, "centro_placa_var", None),
    }
    var = mapping.get(key)
    if var is None:
        return
    var.set(text)
    self.centro_estado_var.set(f"Filtro aplicado: {key} = {text}. Actualizando tablero...")
    self.programar_filtrado_centro(delay=80)


def limpiar_filtros_visuales_centro(self):
    filtros = [
        "centro_empresa_var",
        "centro_bodega_var",
        "centro_guia_var",
        "centro_producto_var",
        "centro_chofer_var",
        "centro_placa_var",
        "centro_estado_filtro_var",
        "centro_etapa_qr_var",
    ]
    hubo_cambio = False
    for attr in filtros:
        var = getattr(self, attr, None)
        if var is not None and var.get():
            var.set("")
            hubo_cambio = True
    if hubo_cambio:
        self.centro_estado_var.set("Seleccion visual limpiada. Actualizando tablero completo...")
        self.programar_filtrado_centro(delay=80)


def resetear_filtro_visual_centro_si_fondo(self, widget):
    if getattr(self, "_centro_click_interactivo", False):
        self._centro_click_interactivo = False
        return
    try:
        current = widget.find_withtag("current")
    except Exception:
        current = ()
    if current:
        return
    self.limpiar_filtros_visuales_centro()


def crear_chart_barras_interactivo_centro(self, parent, title, data, label_key, value_key, row, col, on_click):
    canvas = self.crear_panel_chart(parent, title, row, col)
    if not isinstance(data, list):
        data = []

    raw_items = []
    for item in data[:10]:
        if not isinstance(item, dict):
            continue
        value = self.safe_number(item.get(value_key), 0)
        if value <= 0:
            continue
        label = str(item.get(label_key, "SIN DATO") or "SIN DATO")
        raw_items.append((label, value, item))

    if not raw_items:
        self.dibujar_sin_datos(canvas)
        return

    def draw(_event=None):
        canvas.delete("all")
        width = max(canvas.winfo_width(), 360)
        height = max(canvas.winfo_height(), 220)

        max_label_len = max((len(label) for label, _value, _original in raw_items), default=12)
        left = min(max(140, max_label_len * 8 + 18), int(width * 0.42))
        right = 96
        top = 16
        bar_h = 22
        gap = 10
        max_value = max([value for _, value, _ in raw_items] or [1]) or 1

        for idx, (label, value, original) in enumerate(raw_items):
            y = top + idx * (bar_h + gap)
            if y + bar_h > height - 8:
                break
            chart_w = max(width - left - right, 70)
            bar_w = int(chart_w * (value / max_value))
            max_label_chars = max(12, min(28, int((left - 18) / 7)))
            short_label = label[:max_label_chars] + "..." if len(label) > max_label_chars + 3 else label
            value_text = self.formatear_numero(value)
            value_x = left + max(bar_w, 2) + 6
            value_anchor = "w"
            if value_x + (len(value_text) * 7) > width - 8:
                value_x = width - 8
                value_anchor = "e"

            tag = f"bar_{idx}"
            color = self.color_bodega(label) if "bodega" in str(title).lower() or self.es_label_bodega(label) else self.colors["accent"]
            canvas.create_text(
                8,
                y + bar_h / 2,
                text=short_label,
                anchor="w",
                fill=self.colors["text_dark"],
                font=("Segoe UI", 9),
                tags=(tag,),
            )
            canvas.create_rectangle(
                left,
                y,
                left + max(bar_w, 2),
                y + bar_h,
                fill=color,
                outline="",
                tags=(tag,),
            )
            canvas.create_text(
                value_x,
                y + bar_h / 2,
                text=value_text,
                anchor=value_anchor,
                fill=self.colors["text_secondary"],
                font=("Segoe UI", 9, "bold"),
                tags=(tag,),
            )
            canvas.create_rectangle(0, y - 2, width, y + bar_h + 2, fill="", outline="", tags=(tag,))

            def click_barra(_event, item=original):
                on_click(item)
                return "break"

            canvas.tag_bind(tag, "<Button-1>", click_barra)
            canvas.tag_bind(tag, "<Enter>", lambda _event: canvas.configure(cursor="hand2"))
            canvas.tag_bind(tag, "<Leave>", lambda _event: canvas.configure(cursor=""))

    self.bind_debounced_draw(canvas, draw)
    canvas.bind("<Button-1>", lambda _event, c=canvas: self.resetear_filtro_visual_centro_si_fondo(c))
    canvas.after(50, draw)


def render_tablas_operativas_centro(self, cuotas, alertas):
    for tree, rows in [(self.centro_cuotas_tree, cuotas), (self.centro_alertas_tree, alertas)]:
        for item in tree.get_children():
            tree.delete(item)
    for row in cuotas:
        self.centro_cuotas_tree.insert(
            "",
            "end",
            values=(
                row.get("cliente", ""),
                row.get("producto", ""),
                row.get("bodega") or row.get("bodega_numero") or "Todas",
                self.formatear_numero(row.get("stowage_mt"), 2),
                self.formatear_numero(row.get("cuota_mt"), 2),
                self.formatear_numero(row.get("retirado_mt"), 2),
                self.formatear_numero(row.get("diferencia_mt"), 2),
                f"{self.safe_number(row.get('avance_pct')):,.2f}%",
                row.get("origen", ""),
            ),
        )
    for row in alertas:
        self.centro_alertas_tree.insert("", "end", values=(row.get("severidad", ""), row.get("tipo", ""), row.get("mensaje", "")))


def render_control_plan_centro(self, data):
    tree = getattr(self, "centro_control_plan_tree", None)
    if tree is None:
        return
    for item in tree.get_children():
        tree.delete(item)
    controles = data.get("controles", []) if isinstance(data, dict) else []
    for row in controles:
        tree.insert(
            "",
            "end",
            values=(
                row.get("codigo", ""),
                row.get("proceso", ""),
                row.get("ctq", ""),
                row.get("estado", ""),
                row.get("valor", ""),
                row.get("responsable", ""),
                row.get("reaccion", ""),
            ),
        )
    if not controles:
        tree.insert("", "end", values=("", "Sin datos", "", "", "", "", "Presione Control plan para consultar."))


def render_salud_operativa_centro(self, data):
    tree = getattr(self, "centro_salud_operativa_tree", None)
    if tree is None:
        return
    for item in tree.get_children():
        tree.delete(item)
    dimensiones = data.get("dimensiones", []) if isinstance(data, dict) else []
    for row in dimensiones:
        tree.insert(
            "",
            "end",
            values=(
                row.get("codigo", ""),
                row.get("nombre", ""),
                f"{self.safe_number(row.get('score')):,.2f}%",
                row.get("estado", ""),
                row.get("valor", ""),
                row.get("detalle", ""),
                row.get("accion", ""),
            ),
        )
    if not dimensiones:
        tree.insert("", "end", values=("", "Sin datos", "", "", "", "", "Presione Salud operativa para consultar."))


def render_spc_centro(self, data):
    tree = getattr(self, "centro_spc_tree", None)
    if tree is None:
        return
    for item in tree.get_children():
        tree.delete(item)
    metricas = data.get("metricas", []) if isinstance(data, dict) else []
    for row in metricas:
        unidad = row.get("unidad", "")
        tree.insert(
            "",
            "end",
            values=(
                row.get("codigo", ""),
                row.get("nombre", ""),
                self.formatear_numero(row.get("n")),
                f"{self.formatear_numero(row.get('promedio'), 2)} {unidad}",
                f"{self.formatear_numero(row.get('lcl'), 2)} {unidad}",
                f"{self.formatear_numero(row.get('ucl'), 2)} {unidad}",
                self.formatear_numero(row.get("sigma"), 2),
                self.formatear_numero(row.get("senales_count")),
                row.get("estado", ""),
                row.get("recomendacion", ""),
            ),
        )
    if not metricas:
        tree.insert("", "end", values=("", "Sin datos", "", "", "", "", "", "", "", "Presione SPC para consultar."))


def render_bloqueos_inteligentes_centro(self, data):
    tree = getattr(self, "centro_bloqueos_tree", None)
    if tree is None:
        return
    for item in tree.get_children():
        tree.delete(item)
    bloqueos = data.get("bloqueos", []) if isinstance(data, dict) else []
    for row in bloqueos:
        tree.insert(
            "",
            "end",
            values=(
                row.get("severidad", ""),
                row.get("tipo", ""),
                row.get("guia", ""),
                row.get("empresa", ""),
                row.get("producto", ""),
                row.get("chofer", ""),
                row.get("placa", ""),
                row.get("estado_asignacion") or row.get("estado", ""),
                row.get("motivo", ""),
                row.get("accion", ""),
            ),
        )
    if not bloqueos:
        tree.insert(
            "",
            "end",
            values=(
                "CONTROLADO",
                "SIN_BLOQUEOS",
                "",
                "",
                "",
                "",
                "",
                "",
                "No hay bloqueos inteligentes detectados.",
                "Mantener monitoreo operativo.",
            ),
        )


def render_excepciones_operativas_centro(self, data):
    tree = getattr(self, "centro_excepciones_tree", None)
    if tree is None:
        return
    for item in tree.get_children():
        tree.delete(item)
    excepciones = data.get("data", []) if isinstance(data, dict) else []
    for row in excepciones:
        tree.insert(
            "",
            "end",
            values=(
                row.get("id", ""),
                row.get("severidad", ""),
                row.get("estado", ""),
                row.get("tipo", ""),
                row.get("guia", ""),
                row.get("empresa", ""),
                row.get("producto", ""),
                row.get("responsable", ""),
                row.get("titulo", ""),
                row.get("accion_recomendada", ""),
            ),
        )
    if not excepciones:
        tree.insert(
            "",
            "end",
            values=(
                "",
                "CONTROLADO",
                "",
                "SIN_EXCEPCIONES",
                "",
                "",
                "",
                "",
                "No hay excepciones operativas abiertas.",
                "Genere desde bloqueos o registre manualmente si aplica.",
            ),
        )


def render_auditoria_senior_centro(self, data):
    tree = getattr(self, "centro_auditoria_senior_tree", None)
    if tree is None:
        return
    for item in tree.get_children():
        tree.delete(item)
    hallazgos = data.get("hallazgos", []) if isinstance(data, dict) else []
    for row in hallazgos:
        tree.insert(
            "",
            "end",
            values=(
                row.get("dimension", ""),
                row.get("severidad", ""),
                row.get("estado", ""),
                row.get("titulo", ""),
                row.get("evidencia", ""),
                row.get("riesgo", ""),
                row.get("accion", ""),
                row.get("responsable", ""),
            ),
        )
    if not hallazgos:
        tree.insert(
            "",
            "end",
            values=(
                "CONTROLADO",
                "BAJA",
                "OK",
                "Sin hallazgos senior relevantes.",
                "Capas operativas sin brechas visibles.",
                "Mantener monitoreo.",
                "Continuar control operativo normal.",
                "Supervisor operacion",
            ),
        )


def render_cierre_guiado_centro(self, data):
    tree = getattr(self, "centro_cierre_guiado_tree", None)
    if tree is None:
        return
    for item in tree.get_children():
        tree.delete(item)
    checklist = data.get("checklist", []) if isinstance(data, dict) else []
    for row in checklist:
        tree.insert(
            "",
            "end",
            values=(
                row.get("codigo", ""),
                row.get("categoria", ""),
                row.get("estado", ""),
                row.get("control", ""),
                row.get("evidencia", ""),
                row.get("accion", ""),
                row.get("responsable", ""),
            ),
        )
    if not checklist:
        tree.insert(
            "",
            "end",
            values=(
                "CIERRE",
                "Sin datos",
                "PENDIENTE",
                "Cierre operativo guiado",
                "Presione Cierre guiado para evaluar.",
                "Ejecute el checklist antes de cerrar la operacion.",
                "Supervisor operacion",
            ),
        )


def render_modo_offline_centro(self, data):
    tree = getattr(self, "centro_modo_offline_tree", None)
    if tree is None:
        return
    for item in tree.get_children():
        tree.delete(item)
    checklist = data.get("checklist", []) if isinstance(data, dict) else []
    for row in checklist:
        tree.insert(
            "",
            "end",
            values=(
                row.get("codigo", ""),
                row.get("categoria", ""),
                row.get("estado", ""),
                row.get("control", ""),
                row.get("evidencia", ""),
                row.get("accion", ""),
                row.get("responsable", ""),
            ),
        )
    if not checklist:
        tree.insert(
            "",
            "end",
            values=(
                "OFFLINE",
                "Sin datos",
                "PENDIENTE",
                "Modo offline blindado",
                "Presione Modo offline para evaluar.",
                "Sincronice handhelds antes del turno.",
                "Operador patio / TI",
            ),
        )


def render_productividad_centro(self, data):
    tree = getattr(self, "centro_productividad_tree", None)
    if tree is None:
        return
    for item in tree.get_children():
        tree.delete(item)

    def insertar_grupo(dimension, rows):
        for row in rows or []:
            tree.insert(
                "",
                "end",
                values=(
                    dimension,
                    row.get("nombre", ""),
                    self.formatear_numero(row.get("viajes")),
                    self.formatear_numero(row.get("completos")),
                    self.formatear_numero(row.get("descargado_mt"), 2),
                    self.formatear_numero(row.get("mt_por_viaje"), 2),
                    self.formatear_numero(row.get("duracion_prom_min"), 2),
                    self.formatear_numero(row.get("mt_por_hora"), 2),
                    self.formatear_numero(row.get("score"), 2),
                ),
            )

    if isinstance(data, dict) and data.get("error"):
        tree.insert("", "end", values=("Error", str(data.get("error")), "", "", "", "", "", "", ""))
        return

    insertar_grupo("Chofer", data.get("por_chofer", []) if isinstance(data, dict) else [])
    insertar_grupo("Placa", data.get("por_placa", []) if isinstance(data, dict) else [])
    insertar_grupo("Cliente", data.get("por_cliente", []) if isinstance(data, dict) else [])
    insertar_grupo("Producto", data.get("por_producto", []) if isinstance(data, dict) else [])
    insertar_grupo("Bodega", data.get("por_bodega", []) if isinstance(data, dict) else [])

    if not tree.get_children():
        tree.insert(
            "",
            "end",
            values=(
                "Productividad",
                "Sin datos",
                "",
                "",
                "",
                "",
                "",
                "",
                "Presione Productividad para consultar.",
            ),
        )


def dibujar_buque_centro(self, bodegas):
    if not hasattr(self, "centro_buque_canvas"):
        return
    canvas = self.centro_buque_canvas
    canvas.delete("all")
    width = max(canvas.winfo_width(), 560)
    height = max(canvas.winfo_height(), 290)
    x0, x1 = 18, width - 18
    y0, y1 = 46, height - 36
    canvas.create_polygon(x0, y0, x1 - 70, y0, x1, (y0 + y1) / 2, x1 - 70, y1, x0, y1, fill=self.colors["bg_topbar"], outline=self.colors["accent"], width=2)
    if not bodegas:
        canvas.create_text(width / 2, height / 2, text="Sin bodegas cargadas", fill=self.colors["text_dark"], font=("Segoe UI", 12, "bold"))
        return
    filtro_bodega = ""
    try:
        filtro_bodega = str(self.centro_bodega_var.get()).strip()
    except Exception:
        filtro_bodega = ""
    seg_w = max((x1 - x0 - 92) / 5, 82)
    start_x = x0 + 14
    font_size = 8 if seg_w < 150 else 9
    for idx, numero in enumerate([5, 4, 3, 2, 1]):
        row = next((item for item in bodegas if int(item.get("bodega_numero") or 0) == numero), {})
        capacidad = self.safe_number(row.get("capacidad_mt"), 0)
        producto = str(row.get("producto") or "").strip()
        if producto.upper() in ("SIN PRODUCTO", "NONE", "NULL", "TODOS"):
            producto = ""
        if len(producto) > 18:
            producto = producto[:15] + "..."
        retirado = self.safe_number(row.get("retirado_mt"), 0)
        retirado_visible = self.valor_descargado_visible_centro(row)
        faltante = self.safe_number(row.get("faltante_mt"), capacidad)
        pct_restante = max(0, min(1, faltante / capacidad)) if capacidad else 0
        pct_avance = max(0, min(100, self.safe_number(row.get("avance_pct"), 0)))
        x = start_x + idx * seg_w
        hold_top = y0 + 18
        hold_bottom = y1 - 18
        fill_h = int((hold_bottom - hold_top) * pct_restante)
        color = self.color_bodega(numero) if hasattr(self, "color_bodega") else self.colors["accent"]
        tag = f"bodega_{numero}"
        selected = filtro_bodega == str(numero)
        outline_color = "#FFFFFF" if selected else "#00D1FF"
        outline_width = 3 if selected else 1
        hold_left = x
        hold_right = x + seg_w - 12
        canvas.create_rectangle(
            hold_left,
            hold_top,
            hold_right,
            hold_bottom,
            fill="#FFFFFF",
            outline=outline_color,
            width=outline_width,
            tags=(tag,),
        )
        if fill_h > 0:
            fill_top = hold_bottom - fill_h
            canvas.create_rectangle(
                hold_left,
                fill_top,
                hold_right,
                hold_bottom,
                fill=color,
                outline="",
                tags=(tag,),
            )
            canvas.create_line(hold_left + 2, fill_top, hold_right - 2, fill_top, fill="#07111F", width=2, tags=(tag,))
        canvas.create_rectangle(x, hold_top, x + seg_w - 12, hold_top + 8, fill="#07111F", outline="", tags=(tag,))
        text_font_size = max(7, font_size - 1) if producto else font_size
        if seg_w < 135:
            producto_linea = f"\n{producto[:10]}" if producto else ""
            text = (
                f"B{numero}{producto_linea}\n"
                f"Cap {capacidad:,.0f}\n"
                f"D {retirado_visible:,.0f} ({pct_avance:,.0f}%)\n"
                f"P {faltante:,.0f} ({pct_restante * 100:,.0f}%)"
            )
        else:
            titulo = f"B{numero}" if not producto else f"B{numero} | {producto}"
            text = (
                f"{titulo}\n"
                f"Cap {capacidad:,.2f} MT\n"
                f"D {retirado_visible:,.2f} ({pct_avance:,.2f}%)\n"
                f"P {faltante:,.2f} ({pct_restante * 100:,.2f}%)"
            )
        canvas.create_text(
            x + (seg_w - 12) / 2,
            (hold_top + hold_bottom) / 2,
            text=text,
            fill="#050B14",
            font=("Segoe UI", text_font_size, "bold"),
            justify="center",
            tags=(tag,),
        )
        def click_bodega(_event, num=numero):
            self.aplicar_filtro_centro_desde_click("bodega", num)
            return "break"

        canvas.tag_bind(tag, "<Button-1>", click_bodega)
        canvas.tag_bind(tag, "<Enter>", lambda _event: canvas.configure(cursor="hand2"))
        canvas.tag_bind(tag, "<Leave>", lambda _event: canvas.configure(cursor=""))
    canvas.create_text(width / 2, 20, text="Visual: cada bodega se vacia conforme peso lleno - peso vacio se descuenta contra su capacidad MT", fill=self.colors["text_dark"], font=("Segoe UI", 9, "bold"))
    canvas.bind("<Button-1>", lambda _event, c=canvas: self.resetear_filtro_visual_centro_si_fondo(c))


def crear_tabla_centro(self, parent, title, columns, headings, side="top", height=8):
    panel = tk.Frame(parent, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    pack_opts = {"fill": "both", "expand": True, "pady": (0, 12)}
    if side in ("left", "right"):
        pack_opts = {"side": side, "fill": "both", "expand": True, "padx": (0, 8) if side == "left" else (0, 0)}
    panel.pack(**pack_opts)
    tk.Label(panel, text=title, font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w", padx=14, pady=(12, 6))
    frame = tk.Frame(panel, bg=self.colors["bg_card"])
    frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=height)
    for col, heading in zip(columns, headings):
        tree.heading(col, text=heading)
        tree.column(col, width=320 if col == "mensaje" else 150, anchor="center" if col != "mensaje" else "w")
    y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=y.set, xscrollcommand=x.set)
    tree.grid(row=0, column=0, sticky="nsew")
    y.grid(row=0, column=1, sticky="ns")
    x.grid(row=1, column=0, sticky="ew")
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    return tree

