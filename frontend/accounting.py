import tkinter as tk
from tkinter import messagebox, ttk

import requests


CUENTAS_CONTRAPARTIDA = [
    "2-01-01 Cuentas por pagar",
    "1-01-02 Bancos",
    "1-01-01 Caja",
]


def install_accounting_screen(app_class):
    app_class.show_accounting = show_accounting
    app_class.api_get_accounting_tipos_activo = api_get_accounting_tipos_activo
    app_class.api_get_accounting_activos = api_get_accounting_activos
    app_class.api_crear_accounting_activo = api_crear_accounting_activo
    app_class.accounting_cargar_activos = accounting_cargar_activos
    app_class.accounting_guardar_activo = accounting_guardar_activo
    app_class.accounting_limpiar_form = accounting_limpiar_form
    app_class.accounting_actualizar_regla_tipo = accounting_actualizar_regla_tipo
    app_class.accounting_render_activos = accounting_render_activos
    app_class.accounting_mostrar_detalle = accounting_mostrar_detalle


def show_accounting(self):
    self.clear_content()
    self.highlight_sidebar_button("Accounting")

    self.accounting_tipos = []
    self.accounting_tipo_labels = {}
    self.accounting_activos_cache = []
    self.accounting_vars = {
        "nombre": tk.StringVar(),
        "fecha_compra": tk.StringVar(value=str(__import__("datetime").date.today())),
        "tipo": tk.StringVar(),
        "monto": tk.StringVar(value="0.00"),
        "moneda": tk.StringVar(value="CRC"),
        "encargado": tk.StringVar(),
        "departamento": tk.StringVar(),
        "ubicacion": tk.StringVar(),
        "marca": tk.StringVar(),
        "modelo": tk.StringVar(),
        "serie": tk.StringVar(),
        "cuenta_contrapartida": tk.StringVar(value=CUENTAS_CONTRAPARTIDA[0]),
        "notas": tk.StringVar(),
    }
    self.accounting_regla_var = tk.StringVar(value="Seleccione un tipo de activo.")
    self.accounting_status_var = tk.StringVar(value="Listo. Cargue tipos y activos desde el backend.")

    self.create_page_title(
        self.content,
        "Accounting",
        "Activos fijos, asiento de alta y regla fiscal de depreciacion para Costa Rica.",
    )

    actions = tk.Frame(self.content, bg=self.colors["bg_main"])
    actions.pack(fill="x", padx=25, pady=(0, 10))
    ttk.Button(actions, text="Cargar activos", style="Olive.TButton", command=self.accounting_cargar_activos).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Guardar activo", style="Olive.TButton", command=self.accounting_guardar_activo).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Limpiar", style="Gray.TButton", command=self.accounting_limpiar_form).pack(side="left", padx=(0, 8))

    status = tk.Frame(self.content, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    status.pack(fill="x", padx=25, pady=(0, 10))
    tk.Label(status, textvariable=self.accounting_status_var, bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 10, "bold"), anchor="w").pack(fill="x", padx=14, pady=8)

    outer = tk.Frame(self.content, bg=self.colors["bg_main"])
    outer.pack(fill="both", expand=True, padx=25, pady=(0, 20))
    canvas = tk.Canvas(outer, bg=self.colors["bg_main"], highlightthickness=0)
    scroll_y = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
    scroll_x = ttk.Scrollbar(outer, orient="horizontal", command=canvas.xview)
    body = tk.Frame(canvas, bg=self.colors["bg_main"])
    window_id = canvas.create_window((0, 0), window=body, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    self.bind_scroll_canvas(canvas, body, window_id, min_width=1180)
    canvas.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    outer.grid_rowconfigure(0, weight=1)
    outer.grid_columnconfigure(0, weight=1)

    form_panel = tk.Frame(body, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    form_panel.pack(fill="x", pady=(0, 12))
    tk.Label(form_panel, text="Alta de activo", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 4))

    grid = tk.Frame(form_panel, bg=self.colors["bg_card"])
    grid.pack(fill="x", padx=14, pady=(0, 10))
    campos = [
        ("nombre", "Activo / descripcion", 34, "entry"),
        ("fecha_compra", "Fecha compra YYYY-MM-DD", 18, "entry"),
        ("tipo", "Tipo de activo CR", 28, "combo_tipo"),
        ("monto", "Monto", 16, "entry"),
        ("moneda", "Moneda", 10, "combo_moneda"),
        ("encargado", "Encargado", 24, "entry"),
        ("departamento", "Departamento", 22, "entry"),
        ("ubicacion", "Ubicacion", 24, "entry"),
        ("marca", "Marca", 18, "entry"),
        ("modelo", "Modelo", 18, "entry"),
        ("serie", "Serie", 20, "entry"),
        ("cuenta_contrapartida", "Credito contable", 30, "combo_cuenta"),
        ("notas", "Notas", 34, "entry"),
    ]
    for idx, (key, label, width, kind) in enumerate(campos):
        box = tk.Frame(grid, bg=self.colors["bg_card"])
        box.grid(row=idx // 4, column=idx % 4, sticky="ew", padx=6, pady=5)
        tk.Label(box, text=label, bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(anchor="w")
        if kind == "combo_tipo":
            widget = ttk.Combobox(box, textvariable=self.accounting_vars[key], values=[], state="readonly", width=width)
            widget.bind("<<ComboboxSelected>>", lambda _e: self.accounting_actualizar_regla_tipo())
            self.accounting_tipo_combo = widget
        elif kind == "combo_moneda":
            widget = ttk.Combobox(box, textvariable=self.accounting_vars[key], values=["CRC", "USD"], state="readonly", width=width)
        elif kind == "combo_cuenta":
            widget = ttk.Combobox(box, textvariable=self.accounting_vars[key], values=CUENTAS_CONTRAPARTIDA, state="readonly", width=width)
        else:
            widget = ttk.Entry(box, textvariable=self.accounting_vars[key], width=width)
        widget.pack(fill="x")
    for col in range(4):
        grid.grid_columnconfigure(col, weight=1)

    tk.Label(form_panel, textvariable=self.accounting_regla_var, bg=self.colors["bg_card"], fg=self.colors["text_secondary"], font=("Segoe UI", 10), anchor="w").pack(fill="x", padx=20, pady=(0, 12))

    self.accounting_kpi_frame = tk.Frame(body, bg=self.colors["bg_main"])
    self.accounting_kpi_frame.pack(fill="x", pady=(0, 12))

    split = tk.Frame(body, bg=self.colors["bg_main"])
    split.pack(fill="both", expand=True)

    table_panel = tk.Frame(split, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    table_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
    tk.Label(table_panel, text="Activos registrados", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 6))
    table_frame = tk.Frame(table_panel, bg=self.colors["bg_card"])
    table_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))
    columns = ("codigo", "nombre", "tipo", "compra", "monto", "dep_mensual", "encargado", "ubicacion")
    self.accounting_activos_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=14)
    for col, text, width in [
        ("codigo", "Codigo", 95), ("nombre", "Activo", 220), ("tipo", "Tipo", 190),
        ("compra", "Compra", 95), ("monto", "Monto", 110), ("dep_mensual", "Dep. mensual", 115),
        ("encargado", "Encargado", 140), ("ubicacion", "Ubicacion", 160),
    ]:
        self.accounting_activos_tree.heading(col, text=text)
        self.accounting_activos_tree.column(col, width=width, anchor="center")
    sy = ttk.Scrollbar(table_frame, orient="vertical", command=self.accounting_activos_tree.yview)
    sx = ttk.Scrollbar(table_frame, orient="horizontal", command=self.accounting_activos_tree.xview)
    self.accounting_activos_tree.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
    self.accounting_activos_tree.grid(row=0, column=0, sticky="nsew")
    sy.grid(row=0, column=1, sticky="ns")
    sx.grid(row=1, column=0, sticky="ew")
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)
    self.accounting_activos_tree.bind("<<TreeviewSelect>>", lambda _e: self.accounting_mostrar_detalle())

    detail_panel = tk.Frame(split, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1, width=360)
    detail_panel.pack(side="right", fill="both")
    detail_panel.pack_propagate(False)
    tk.Label(detail_panel, text="Asiento y depreciacion", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 13, "bold")).pack(anchor="w", padx=14, pady=(12, 6))
    self.accounting_detalle_text = tk.Text(detail_panel, height=18, bg=self.colors["bg_topbar"], fg=self.colors["text_dark"], insertbackground=self.colors["accent"], relief="flat", wrap="word", font=("Consolas", 9))
    self.accounting_detalle_text.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    self.accounting_render_activos([])
    self.accounting_cargar_activos()


def api_get_accounting_tipos_activo(self):
    respuesta = requests.get(f"{self.api_base}/accounting/activos/tipos", timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_get_accounting_activos(self):
    respuesta = requests.get(f"{self.api_base}/accounting/activos", timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_crear_accounting_activo(self, payload):
    respuesta = requests.post(f"{self.api_base}/accounting/activos", json=payload, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def accounting_cargar_activos(self):
    def tarea():
        return {
            "tipos": self.api_get_accounting_tipos_activo(),
            "activos": self.api_get_accounting_activos(),
        }

    def ok(data):
        tipos = data.get("tipos", {}).get("data", [])
        self.accounting_tipos = tipos
        labels = []
        self.accounting_tipo_labels = {}
        for tipo in tipos:
            label = f"{tipo.get('nombre')} | {tipo.get('porcentaje')}% | {tipo.get('vida_util')} anos"
            labels.append(label)
            self.accounting_tipo_labels[label] = tipo.get("codigo")
        self.accounting_tipo_combo["values"] = labels
        if labels and not self.accounting_vars["tipo"].get():
            self.accounting_vars["tipo"].set(labels[0])
            self.accounting_actualizar_regla_tipo()
        activos = data.get("activos", {}).get("data", [])
        self.accounting_activos_cache = activos
        self.accounting_render_activos(activos, data.get("activos", {}).get("kpis", {}))
        self.accounting_status_var.set(f"Activos cargados: {len(activos)}.")

    self.ejecutar_en_segundo_plano("Accounting", "Cargando activos y reglas fiscales...", tarea, ok)


def accounting_guardar_activo(self):
    label = self.accounting_vars["tipo"].get()
    tipo_codigo = self.accounting_tipo_labels.get(label, "OTRO")
    try:
        monto = float(str(self.accounting_vars["monto"].get()).replace(",", ""))
    except ValueError:
        messagebox.showwarning("Monto invalido", "Ingrese un monto numerico.", parent=self)
        return
    payload = {
        "nombre": self.accounting_vars["nombre"].get().strip(),
        "fecha_compra": self.accounting_vars["fecha_compra"].get().strip(),
        "tipo_codigo": tipo_codigo,
        "monto": monto,
        "moneda": self.accounting_vars["moneda"].get().strip() or "CRC",
        "encargado": self.accounting_vars["encargado"].get().strip() or None,
        "departamento": self.accounting_vars["departamento"].get().strip() or None,
        "ubicacion": self.accounting_vars["ubicacion"].get().strip() or None,
        "marca": self.accounting_vars["marca"].get().strip() or None,
        "modelo": self.accounting_vars["modelo"].get().strip() or None,
        "serie": self.accounting_vars["serie"].get().strip() or None,
        "cuenta_contrapartida": self.accounting_vars["cuenta_contrapartida"].get().strip(),
        "notas": self.accounting_vars["notas"].get().strip() or None,
        "creado_por": (getattr(self, "current_user", {}) or {}).get("usuario"),
    }
    if not payload["nombre"]:
        messagebox.showwarning("Activo requerido", "Ingrese el nombre o descripcion del activo.", parent=self)
        return

    def tarea():
        return self.api_crear_accounting_activo(payload)

    def ok(activo):
        self.accounting_status_var.set(f"Activo guardado: {activo.get('codigo')} con asiento de alta generado.")
        self.accounting_limpiar_form()
        self.accounting_cargar_activos()

    self.ejecutar_en_segundo_plano("Accounting", "Guardando activo y generando asiento contable...", tarea, ok)


def accounting_limpiar_form(self):
    for key, var in self.accounting_vars.items():
        if key == "fecha_compra":
            var.set(str(__import__("datetime").date.today()))
        elif key == "monto":
            var.set("0.00")
        elif key == "moneda":
            var.set("CRC")
        elif key == "cuenta_contrapartida":
            var.set(CUENTAS_CONTRAPARTIDA[0])
        elif key != "tipo":
            var.set("")
    self.accounting_actualizar_regla_tipo()


def accounting_actualizar_regla_tipo(self):
    label = self.accounting_vars["tipo"].get()
    codigo = self.accounting_tipo_labels.get(label)
    tipo = next((item for item in self.accounting_tipos if item.get("codigo") == codigo), None)
    if not tipo:
        self.accounting_regla_var.set("Seleccione un tipo de activo.")
        return
    self.accounting_regla_var.set(
        f"Regla CR: {tipo.get('nombre')} depreciacion linea recta {tipo.get('porcentaje')}% anual, "
        f"vida util {tipo.get('vida_util')} anos. Tambien queda registrado asiento mensual de depreciacion."
    )


def accounting_render_activos(self, activos, kpis=None):
    for widget in self.accounting_kpi_frame.winfo_children():
        widget.destroy()
    kpis = kpis or {}
    self.create_card(self.accounting_kpi_frame, "Activos", kpis.get("activos", len(activos or [])), self.colors["accent"])
    self.create_card(self.accounting_kpi_frame, "Monto total", f"{kpis.get('monto_total', 0):,.2f}", self.colors["success"])
    self.create_card(self.accounting_kpi_frame, "Dep. mensual", f"{kpis.get('depreciacion_mensual', 0):,.2f}", self.colors["warning"])

    for item in self.accounting_activos_tree.get_children():
        self.accounting_activos_tree.delete(item)
    for activo in activos or []:
        self.accounting_activos_tree.insert(
            "",
            "end",
            iid=str(activo.get("id")),
            values=(
                activo.get("codigo") or "",
                activo.get("nombre") or "",
                activo.get("tipo_nombre") or "",
                activo.get("fecha_compra") or "",
                f"{activo.get('monto', 0):,.2f}",
                f"{activo.get('depreciacion_mensual', 0):,.2f}",
                activo.get("encargado") or "",
                activo.get("ubicacion") or "",
            ),
        )


def accounting_mostrar_detalle(self):
    selected = self.accounting_activos_tree.selection()
    if not selected:
        return
    activo_id = str(selected[0])
    activo = next((item for item in self.accounting_activos_cache if str(item.get("id")) == activo_id), None)
    if not activo:
        return
    lineas = [
        f"{activo.get('codigo')} - {activo.get('nombre')}",
        f"Tipo: {activo.get('tipo_nombre')} | Metodo: {activo.get('metodo_depreciacion')}",
        f"Compra: {activo.get('fecha_compra')} | Monto: {activo.get('moneda')} {activo.get('monto', 0):,.2f}",
        f"Depreciacion: {activo.get('porcentaje_depreciacion')}% anual | {activo.get('depreciacion_mensual', 0):,.2f} mensual",
        f"Valor libros: {activo.get('valor_libros', 0):,.2f}",
        "",
        "Asiento de alta:",
    ]
    for row in (activo.get("asiento_alta") or {}).get("lineas", []):
        lineas.append(f"  {row.get('cuenta')} | Debe {row.get('debe', 0):,.2f} | Haber {row.get('haber', 0):,.2f}")
    lineas.append("")
    lineas.append("Asiento mensual de depreciacion:")
    for row in (activo.get("asiento_depreciacion") or {}).get("lineas", []):
        lineas.append(f"  {row.get('cuenta')} | Debe {row.get('debe', 0):,.2f} | Haber {row.get('haber', 0):,.2f}")
    lineas.append("")
    lineas.append(activo.get("base_legal") or "")
    self.accounting_detalle_text.delete("1.0", "end")
    self.accounting_detalle_text.insert("1.0", "\n".join(lineas))
