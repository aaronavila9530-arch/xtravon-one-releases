import calendar
import tkinter as tk
from datetime import date
from tkinter import messagebox, ttk


MESES_ES = [
    "",
    "enero",
    "febrero",
    "marzo",
    "abril",
    "mayo",
    "junio",
    "julio",
    "agosto",
    "septiembre",
    "octubre",
    "noviembre",
    "diciembre",
]


def install_issue_log_screen(app_class):
    app_class.show_issue_log = show_issue_log
    app_class.api_get_issue_log_filtros = api_get_issue_log_filtros
    app_class.api_get_issue_log = api_get_issue_log
    app_class.api_crear_issue_log = api_crear_issue_log
    app_class.api_actualizar_issue_log = api_actualizar_issue_log
    app_class.api_eliminar_issue_log = api_eliminar_issue_log
    app_class.cargar_issue_log_filtros = cargar_issue_log_filtros
    app_class.buscar_issue_log = buscar_issue_log
    app_class.guardar_issue_log = guardar_issue_log
    app_class.editar_issue_log = editar_issue_log
    app_class.eliminar_issue_log = eliminar_issue_log
    app_class.limpiar_issue_form = limpiar_issue_form
    app_class.abrir_calendario_issue = abrir_calendario_issue
    app_class.actualizar_fecha_larga_issue = actualizar_fecha_larga_issue
    app_class.actualizar_subcategorias_sof = actualizar_subcategorias_sof


def show_issue_log(self):
    self.clear_content()
    self.highlight_sidebar_button("SOF")

    self.issue_log_cache = []
    self.issue_log_operaciones = []
    self.issue_log_base_operaciones = []
    self.issue_log_tree = None
    self.issue_editing_id = None
    self.issue_operacion_var = tk.StringVar()
    self.issue_buque_var = tk.StringVar()
    self.issue_filtro_operacion_var = tk.StringVar()
    self.issue_filtro_cliente_var = tk.StringVar()
    self.issue_filtro_producto_var = tk.StringVar()
    self.issue_filtro_bodega_var = tk.StringVar()
    self.issue_filtro_tipo_var = tk.StringVar()
    self.issue_filtro_subcategoria_var = tk.StringVar()
    self.issue_tipo_var = tk.StringVar(value="OPERATIVO")
    self.issue_subcategoria_var = tk.StringVar()
    self.issue_bodega_var = tk.StringVar()
    self.issue_subcategorias_catalogo = {
        "DEMORA": [
            "Fallo de grua",
            "Camiones",
            "Maquinaria - almeja",
            "Maquinaria - back hoe",
            "Maquinaria - payloader",
            "Maquinaria - bobcat",
            "Maquinaria - shore grab",
            "Maquinaria - shore crane",
            "Apertura de bodega",
            "Cierre de bodega",
            "Dano en grua del buque",
            "Almeja de buque",
            "Clima",
            "Marejada",
            "Rotura de cabos",
            "Viento",
            "Otros",
        ],
        "OPERATIVO": ["Inicio de operacion", "Cambio de turno", "Parada operativa", "Reinicio operativo", "Otros"],
        "INCIDENTE": ["Seguridad", "Equipo", "Documento", "Camion", "Otros"],
        "DOCUMENTAL": ["Guia", "Marchamo", "Peso", "Aprobacion", "Otros"],
        "SEGURIDAD": ["Acceso", "QR invalido", "Alerta de cuota", "Otros"],
        "PESO": ["Peso fuera de rango", "Diferencia de peso", "Reproceso", "Otros"],
        "QR": ["QR invalido", "Escaneo duplicado", "Escaneo fuera de flujo", "Otros"],
        "OTROS": ["Otros"],
    }
    self.issue_fecha_desde_var = tk.StringVar()
    self.issue_fecha_desde_larga_var = tk.StringVar(value="-")
    self.issue_fecha_hasta_var = tk.StringVar()
    self.issue_fecha_hasta_larga_var = tk.StringVar(value="-")
    self.issue_fecha_var = tk.StringVar()
    self.issue_fecha_larga_var = tk.StringVar(value="-")
    self.issue_hora_desde_hh_var = tk.StringVar(value="08")
    self.issue_hora_desde_mm_var = tk.StringVar(value="00")
    self.issue_hora_hasta_hh_var = tk.StringVar(value="08")
    self.issue_hora_hasta_mm_var = tk.StringVar(value="00")
    self.issue_evento_var = tk.StringVar()
    self.issue_default_operacion_id = None

    self.create_page_title(
        self.content,
        "SOF",
        "Statement of Facts por buque, con demoras, bodegas, filtros e historial bajo demanda.",
    )

    wrapper = tk.Frame(self.content, bg=self.colors["bg_main"])
    wrapper.pack(fill="both", expand=True, padx=25, pady=(0, 20))

    canvas = tk.Canvas(wrapper, bg=self.colors["bg_main"], highlightthickness=0)
    scroll_y = ttk.Scrollbar(wrapper, orient="vertical", command=canvas.yview)
    scroll_x = ttk.Scrollbar(wrapper, orient="horizontal", command=canvas.xview)
    body = tk.Frame(canvas, bg=self.colors["bg_main"])

    window_id = canvas.create_window((0, 0), window=body, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    self.bind_scroll_canvas(canvas, body, window_id, min_width=1040)
    canvas.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    wrapper.grid_rowconfigure(0, weight=1)
    wrapper.grid_columnconfigure(0, weight=1)

    top = tk.Frame(body, bg=self.colors["bg_main"])
    top.pack(fill="x")

    form = tk.Frame(top, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    form.pack(fill="x", pady=(10, 0))

    tk.Label(form, text="Agregar evento", font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w", padx=14, pady=(12, 6))

    grid = tk.Frame(form, bg=self.colors["bg_card"])
    grid.pack(fill="x", padx=14)

    fields = [
        ("Operacion abierta / evento operativo", self.issue_operacion_var, "operacion"),
        ("Fecha", self.issue_fecha_var, "fecha"),
        ("Hora desde / hasta", None, "hora"),
        ("Tipo", self.issue_tipo_var, "tipo"),
        ("Subcategoria", self.issue_subcategoria_var, "subcategoria"),
        ("Bodega asociada", self.issue_bodega_var, "bodega"),
        ("Evento", self.issue_evento_var, "evento"),
    ]

    for idx, (label, var, key) in enumerate(fields):
        row = idx // 2
        col = idx % 2
        box = tk.Frame(grid, bg=self.colors["bg_card"])
        box.grid(row=row, column=col, sticky="ew", padx=6, pady=5)
        tk.Label(box, text=label, font=("Segoe UI", 9, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w")
        if key == "operacion":
            widget = ttk.Combobox(box, textvariable=var, state="normal", width=45)
            self.issue_operacion_combo = widget
        elif key == "tipo":
            widget = ttk.Combobox(box, textvariable=var, state="readonly", values=["OPERATIVO", "INCIDENTE", "DEMORA", "DOCUMENTAL", "SEGURIDAD", "PESO", "QR", "OTROS"])
            widget.bind("<<ComboboxSelected>>", lambda _e: self.actualizar_subcategorias_sof())
            self.issue_tipo_combo = widget
        elif key == "subcategoria":
            widget = ttk.Combobox(box, textvariable=var, state="readonly", values=[])
            self.issue_subcategoria_combo = widget
        elif key == "bodega":
            widget = ttk.Combobox(box, textvariable=var, state="readonly", values=["", "1", "2", "3", "4", "5"])
            self.issue_bodega_combo = widget
        elif key == "fecha":
            row_box = tk.Frame(box, bg=self.colors["bg_card"])
            row_box.pack(fill="x")
            widget = ttk.Entry(row_box, textvariable=self.issue_fecha_larga_var, state="readonly")
            widget.pack(side="left", fill="x", expand=True)
            ttk.Button(row_box, text="Calendario", style="Gray.TButton", command=lambda: self.abrir_calendario_issue("fecha")).pack(side="left", padx=(6, 0))
            continue
        elif key == "hora":
            row_box = tk.Frame(box, bg=self.colors["bg_card"])
            row_box.pack(fill="x")
            tk.Label(row_box, text="Desde", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 5))
            ttk.Spinbox(row_box, from_=0, to=23, textvariable=self.issue_hora_desde_hh_var, width=5, format="%02.0f").pack(side="left")
            tk.Label(row_box, text=":", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
            ttk.Spinbox(row_box, from_=0, to=59, textvariable=self.issue_hora_desde_mm_var, width=5, format="%02.0f").pack(side="left")
            tk.Label(row_box, text="Hasta", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 9, "bold")).pack(side="left", padx=(12, 5))
            ttk.Spinbox(row_box, from_=0, to=23, textvariable=self.issue_hora_hasta_hh_var, width=5, format="%02.0f").pack(side="left")
            tk.Label(row_box, text=":", bg=self.colors["bg_card"], fg=self.colors["text_dark"], font=("Segoe UI", 11, "bold")).pack(side="left", padx=5)
            ttk.Spinbox(row_box, from_=0, to=59, textvariable=self.issue_hora_hasta_mm_var, width=5, format="%02.0f").pack(side="left")
            continue
        else:
            widget = ttk.Entry(box, textvariable=var, width=48)
        widget.pack(fill="x")

    for col in range(2):
        grid.grid_columnconfigure(col, weight=1)

    tk.Label(form, text="La fecha se guarda normalizada y se muestra LONG en espanol.", font=("Segoe UI", 9, "bold"), bg=self.colors["bg_card"], fg=self.colors["accent"]).pack(anchor="w", padx=20, pady=(0, 6))

    actions = tk.Frame(form, bg=self.colors["bg_card"])
    actions.pack(fill="x", padx=14, pady=(8, 14))
    self.issue_guardar_btn = ttk.Button(actions, text="Agregar", style="Olive.TButton", command=self.guardar_issue_log)
    self.issue_guardar_btn.pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Limpiar", style="Gray.TButton", command=self.limpiar_issue_form).pack(side="left")

    filtros = tk.Frame(top, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    filtros.pack(fill="x", pady=(10, 0))
    tk.Label(filtros, text="Filtros", font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w", padx=14, pady=(12, 6))

    filter_grid = tk.Frame(filtros, bg=self.colors["bg_card"])
    filter_grid.pack(fill="x", padx=14)
    for idx, (label, var, key) in enumerate([
        ("Operacion", self.issue_filtro_operacion_var, "operacion_filtro"),
        ("Cliente", self.issue_filtro_cliente_var, "cliente_filtro"),
        ("Producto", self.issue_filtro_producto_var, "producto_filtro"),
        ("Bodega", self.issue_filtro_bodega_var, "bodega_filtro"),
        ("Tipo", self.issue_filtro_tipo_var, "tipo_filtro"),
        ("Subcategoria", self.issue_filtro_subcategoria_var, "subcategoria_filtro"),
        ("Desde", self.issue_fecha_desde_larga_var, "desde"),
        ("Hasta", self.issue_fecha_hasta_larga_var, "hasta"),
    ]):
        box = tk.Frame(filter_grid, bg=self.colors["bg_card"])
        box.grid(row=idx // 3, column=idx % 3, sticky="ew", padx=6, pady=5)
        tk.Label(box, text=label, font=("Segoe UI", 9, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w")
        if key in ("operacion_filtro", "cliente_filtro", "producto_filtro", "bodega_filtro", "tipo_filtro", "subcategoria_filtro"):
            widget = ttk.Combobox(box, textvariable=var, state="normal")
            widget.pack(fill="x")
        else:
            row_box = tk.Frame(box, bg=self.colors["bg_card"])
            row_box.pack(fill="x")
            widget = ttk.Entry(row_box, textvariable=var, state="readonly")
            widget.pack(side="left", fill="x", expand=True)
            ttk.Button(row_box, text="Calendario", style="Gray.TButton", command=lambda target=key: self.abrir_calendario_issue(target)).pack(side="left", padx=(6, 0))

        if key == "operacion_filtro":
            self.issue_filtro_operacion_combo = widget
        elif key == "cliente_filtro":
            self.issue_filtro_cliente_combo = widget
        elif key == "producto_filtro":
            self.issue_filtro_producto_combo = widget
        elif key == "bodega_filtro":
            self.issue_filtro_bodega_combo = widget
        elif key == "tipo_filtro":
            self.issue_tipo_filter_combo = widget
        elif key == "subcategoria_filtro":
            self.issue_filtro_subcategoria_combo = widget
    for col in range(3):
        filter_grid.grid_columnconfigure(col, weight=1)

    filter_actions = tk.Frame(filtros, bg=self.colors["bg_card"])
    filter_actions.pack(fill="x", padx=14, pady=(8, 14))
    ttk.Button(filter_actions, text="Cargar filtros", style="Gray.TButton", command=self.cargar_issue_log_filtros).pack(side="left", padx=(0, 8))
    ttk.Button(filter_actions, text="Buscar historial", style="Olive.TButton", command=self.buscar_issue_log).pack(side="left")

    panel = tk.Frame(body, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    panel.pack(fill="both", expand=True, pady=(12, 0))

    header = tk.Frame(panel, bg=self.colors["bg_card"])
    header.pack(fill="x", padx=14, pady=(12, 6))
    tk.Label(header, text="Historial Statement of Facts", font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(side="left")
    ttk.Button(header, text="Editar seleccionado", style="Gray.TButton", command=self.editar_issue_log).pack(side="right", padx=(8, 0))
    ttk.Button(header, text="Eliminar seleccionado", style="Gray.TButton", command=self.eliminar_issue_log).pack(side="right")

    table_frame = tk.Frame(panel, bg=self.colors["bg_card"])
    table_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    columns = ("id", "buque", "guia", "cliente", "producto", "placa", "bodega", "fecha_larga", "rango_hora", "tipo", "subcategoria", "evento")
    self.issue_log_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18)
    widths = {
        "id": 60,
        "buque": 180,
        "guia": 100,
        "cliente": 160,
        "producto": 150,
        "placa": 100,
        "bodega": 85,
        "fecha_larga": 190,
        "rango_hora": 120,
        "tipo": 150,
        "subcategoria": 210,
        "evento": 320,
    }
    for col in columns:
        self.issue_log_tree.heading(col, text=col.replace("_", " ").title())
        self.issue_log_tree.column(col, width=widths[col], anchor="w" if col == "evento" else "center")

    sy = ttk.Scrollbar(table_frame, orient="vertical", command=self.issue_log_tree.yview)
    sx = ttk.Scrollbar(table_frame, orient="horizontal", command=self.issue_log_tree.xview)
    self.issue_log_tree.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
    self.issue_log_tree.grid(row=0, column=0, sticky="nsew")
    sy.grid(row=0, column=1, sticky="ns")
    sx.grid(row=1, column=0, sticky="ew")
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)

    self.actualizar_subcategorias_sof()
    self.after(150, lambda: self.cargar_issue_log_filtros(silencioso=True))


def api_get_issue_log_filtros(self, params=None):
    import requests

    respuesta = requests.get(f"{self.api_base}/issue-log/filtros", params=params or {}, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_get_issue_log(self, params=None):
    import requests

    respuesta = requests.get(f"{self.api_base}/issue-log", params=params or {}, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_crear_issue_log(self, payload):
    import requests

    respuesta = requests.post(f"{self.api_base}/issue-log", json=payload, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_actualizar_issue_log(self, issue_id, payload):
    import requests

    respuesta = requests.put(f"{self.api_base}/issue-log/{issue_id}", json=payload, timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_eliminar_issue_log(self, issue_id):
    import requests

    respuesta = requests.delete(f"{self.api_base}/issue-log/{issue_id}", timeout=60)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def cargar_issue_log_filtros(self, silencioso=False):
    try:
        operacion_activa_fallback = None
        if not getattr(self, "issue_default_operacion_id", None):
            try:
                operacion_activa_fallback = getattr(self, "operacion_activa", None) or self.api_get_operacion_activa()
                if operacion_activa_fallback and operacion_activa_fallback.get("id"):
                    self.operacion_activa = operacion_activa_fallback
                    self.issue_default_operacion_id = operacion_activa_fallback.get("id")
            except Exception:
                operacion_activa_fallback = None
        data = self.api_get_issue_log_filtros(_issue_filter_params(self, include_text_filters=True))
        opciones = data.get("opciones", {})
        self.issue_log_operaciones = opciones.get("operaciones", [])
        self.issue_log_base_operaciones = opciones.get("guias", opciones.get("base_operaciones_actuales", []))
        operacion_activa = opciones.get("operacion_activa") or operacion_activa_fallback
        if operacion_activa:
            self.issue_default_operacion_id = operacion_activa.get("id")

        if operacion_activa and not self.issue_log_operaciones:
            self.issue_log_operaciones = [{
                "id": operacion_activa.get("id"),
                "buque": operacion_activa.get("buque") or operacion_activa.get("nombre_buque", ""),
                "fecha_inicio": operacion_activa.get("fecha_inicio") or operacion_activa.get("fecha", ""),
                "estado": operacion_activa.get("estado", ""),
                "label": (
                    f"{operacion_activa.get('id')} | "
                    f"{operacion_activa.get('buque') or operacion_activa.get('nombre_buque', '')} | "
                    f"{operacion_activa.get('fecha_inicio') or operacion_activa.get('fecha', '')} | "
                    f"{operacion_activa.get('estado', '')}"
                ),
            }]

        if not self.issue_log_base_operaciones and operacion_activa:
            self.issue_log_base_operaciones = [{
                "operacion_id": operacion_activa.get("id"),
                "base_operacion_id": "",
                "nombre_buque": operacion_activa.get("buque", ""),
                "guia": "SIN GUIA CARGADA",
                "cliente": "",
                "producto": "",
                "placa": "",
                "fecha": operacion_activa.get("fecha_inicio", ""),
            }]

        operacion_values = [item.get("label") or f"{item.get('id')} | {item.get('buque')} | {item.get('fecha_inicio')} | {item.get('estado')}" for item in self.issue_log_operaciones]
        self.issue_filtro_operacion_combo["values"] = operacion_values
        self.issue_operacion_combo["values"] = operacion_values

        if operacion_activa and not self.issue_filtro_operacion_var.get().strip():
            for idx, item in enumerate(self.issue_log_operaciones):
                if str(item.get("id")) == str(operacion_activa.get("id")) and idx < len(operacion_values):
                    self.issue_filtro_operacion_var.set(operacion_values[idx])
                    break

        if operacion_activa and not self.issue_operacion_var.get().strip():
            for idx, item in enumerate(self.issue_log_operaciones):
                if str(item.get("id")) == str(operacion_activa.get("id")) and idx < len(operacion_values):
                    self.issue_operacion_var.set(operacion_values[idx])
                    break

        self.issue_filtro_cliente_combo["values"] = opciones.get("clientes", [])
        self.issue_filtro_producto_combo["values"] = opciones.get("productos", [])
        tipos_base = ["OPERATIVO", "INCIDENTE", "DEMORA", "DOCUMENTAL", "SEGURIDAD", "PESO", "QR", "OTROS"]
        tipos = [tipo for tipo in (opciones.get("tipos", []) or []) if tipo != "STATEMENT_OF_FACTS"]
        tipos = list(dict.fromkeys(tipos + tipos_base))
        self.issue_tipo_filter_combo["values"] = tipos
        self.issue_filtro_subcategoria_combo["values"] = opciones.get("subcategorias", [])
        catalogo = opciones.get("subcategorias_catalogo")
        if isinstance(catalogo, dict) and catalogo:
            self.issue_subcategorias_catalogo = catalogo
        if hasattr(self, "issue_tipo_combo"):
            tipos_catalogo = opciones.get("tipos_catalogo") or ["OPERATIVO", "INCIDENTE", "DEMORA", "DOCUMENTAL", "SEGURIDAD", "PESO", "QR", "OTROS"]
            self.issue_tipo_combo["values"] = tipos_catalogo
        if hasattr(self, "issue_bodega_combo"):
            self.issue_bodega_combo["values"] = [""] + [str(item) for item in opciones.get("bodegas", ["1", "2", "3", "4", "5"])]
        self.issue_filtro_bodega_combo["values"] = [""] + [str(item) for item in opciones.get("bodegas", ["1", "2", "3", "4", "5"])]
        self.actualizar_subcategorias_sof()
        if not silencioso:
            messagebox.showinfo("Filtros", "Filtros cargados correctamente.")
    except Exception as exc:
        if not silencioso:
            messagebox.showerror("Error SOF", str(exc))


def _issue_params(self):
    return _issue_filter_params(self, include_text_filters=True)


def _issue_filter_params(self, include_text_filters=False):
    params = {}
    selected_operacion = _selected_filter_operacion(self)
    if selected_operacion:
        params["operacion_id"] = selected_operacion.get("id")
    elif getattr(self, "issue_default_operacion_id", None):
        params["operacion_id"] = self.issue_default_operacion_id
    if include_text_filters:
        if self.issue_filtro_cliente_var.get().strip():
            params["cliente"] = self.issue_filtro_cliente_var.get().strip()
        if self.issue_filtro_producto_var.get().strip():
            params["producto"] = self.issue_filtro_producto_var.get().strip()
        if self.issue_filtro_bodega_var.get().strip():
            params["bodega_numero"] = self.issue_filtro_bodega_var.get().strip()
        if self.issue_filtro_tipo_var.get().strip():
            params["tipo"] = self.issue_filtro_tipo_var.get().strip()
        if self.issue_filtro_subcategoria_var.get().strip():
            params["subcategoria"] = self.issue_filtro_subcategoria_var.get().strip()
    if self.issue_fecha_desde_var.get().strip():
        params["fecha_desde"] = self.issue_fecha_desde_var.get().strip()
    if self.issue_fecha_hasta_var.get().strip():
        params["fecha_hasta"] = self.issue_fecha_hasta_var.get().strip()
    return params


def buscar_issue_log(self):
    if self.issue_log_tree is None:
        return
    try:
        data = self.api_get_issue_log(_issue_params(self))
        self.issue_log_cache = data.get("data", [])
        for item in self.issue_log_tree.get_children():
            self.issue_log_tree.delete(item)
        for row in self.issue_log_cache:
            self.issue_log_tree.insert("", "end", values=(
                row.get("id", ""),
                row.get("buque", ""),
                row.get("guia", ""),
                row.get("cliente", ""),
                row.get("producto", ""),
                row.get("placa", ""),
                row.get("bodega_numero", ""),
                row.get("fecha_larga", ""),
                row.get("rango_hora", ""),
                row.get("tipo", ""),
                row.get("subcategoria", ""),
                row.get("evento", ""),
            ))
    except Exception as exc:
        messagebox.showerror("Error SOF", str(exc))


def guardar_issue_log(self):
    try:
        operacion_texto = self.issue_operacion_var.get().strip()
        if not operacion_texto:
            messagebox.showwarning("Operacion requerida", "Seleccione la operacion del evento SOF.")
            return

        selected = _selected_form_operacion(self)
        if not selected:
            messagebox.showwarning("Operacion requerida", "Seleccione una operacion valida del combo.")
            return

        payload = {
            "operacion_id": int(selected.get("id")),
            "base_operacion_id": None,
            "fecha": self.issue_fecha_var.get().strip(),
            "hora_desde_hh": int(self.issue_hora_desde_hh_var.get()),
            "hora_desde_mm": int(self.issue_hora_desde_mm_var.get()),
            "hora_hasta_hh": int(self.issue_hora_hasta_hh_var.get()),
            "hora_hasta_mm": int(self.issue_hora_hasta_mm_var.get()),
            "tipo": self.issue_tipo_var.get().strip() or "OPERATIVO",
            "subcategoria": self.issue_subcategoria_var.get().strip() or None,
            "bodega_numero": int(self.issue_bodega_var.get()) if self.issue_bodega_var.get().strip() else None,
            "evento": self.issue_evento_var.get().strip(),
            "comentario": "",
            "creado_por": "desktop",
        }
        if self.issue_editing_id:
            self.api_actualizar_issue_log(self.issue_editing_id, payload)
        else:
            self.api_crear_issue_log(payload)
        self.buscar_issue_log()
        self.limpiar_issue_form()
        messagebox.showinfo("SOF", "Evento guardado correctamente.")
    except Exception as exc:
        messagebox.showerror("Error SOF", str(exc))


def _selected_form_operacion(self):
    selected_text = self.issue_operacion_var.get().strip()
    if not selected_text:
        return None

    values = list(self.issue_operacion_combo["values"])
    idx = _find_combo_index(values, selected_text)
    if idx is None:
        return None

    if idx < 0 or idx >= len(self.issue_log_operaciones):
        return None

    return self.issue_log_operaciones[idx]


def _selected_filter_operacion(self):
    selected_text = self.issue_filtro_operacion_var.get().strip()
    if not selected_text:
        return None
    values = list(self.issue_filtro_operacion_combo["values"])
    idx = _find_combo_index(values, selected_text)
    if idx is None:
        return None
    if idx < 0 or idx >= len(self.issue_log_operaciones):
        return None
    return self.issue_log_operaciones[idx]


def _find_combo_index(values, text):
    text = str(text or "").strip()
    if not text:
        return None
    for idx, value in enumerate(values):
        if str(value).strip() == text:
            return idx
    text_lower = text.lower()
    matches = [idx for idx, value in enumerate(values) if text_lower in str(value).lower()]
    if len(matches) == 1:
        return matches[0]
    return None


def editar_issue_log(self):
    seleccion = self.issue_log_tree.selection() if self.issue_log_tree is not None else []
    if not seleccion:
        messagebox.showwarning("Sin seleccion", "Seleccione un evento para editar.")
        return

    issue_id = self.issue_log_tree.item(seleccion[0], "values")[0]
    row = next((item for item in self.issue_log_cache if str(item.get("id")) == str(issue_id)), None)
    if not row:
        messagebox.showwarning("No encontrado", "No se pudo ubicar el evento en cache. Presione Buscar historial.")
        return

    self.issue_editing_id = row.get("id")
    self.issue_fecha_var.set(row.get("fecha") or "")
    self.issue_fecha_larga_var.set(row.get("fecha_larga_es") or row.get("fecha_larga") or "-")
    self.issue_hora_desde_hh_var.set(str(row.get("hora_desde_hh") if row.get("hora_desde_hh") is not None else row.get("hora_hh", "08")).zfill(2))
    self.issue_hora_desde_mm_var.set(str(row.get("hora_desde_mm") if row.get("hora_desde_mm") is not None else row.get("hora_mm", "00")).zfill(2))
    self.issue_hora_hasta_hh_var.set(str(row.get("hora_hasta_hh") if row.get("hora_hasta_hh") is not None else row.get("hora_hh", "08")).zfill(2))
    self.issue_hora_hasta_mm_var.set(str(row.get("hora_hasta_mm") if row.get("hora_hasta_mm") is not None else row.get("hora_mm", "00")).zfill(2))
    self.issue_tipo_var.set(row.get("tipo") or "OPERATIVO")
    self.actualizar_subcategorias_sof()
    self.issue_subcategoria_var.set(row.get("subcategoria") or "")
    self.issue_bodega_var.set(str(row.get("bodega_numero") or ""))
    self.issue_evento_var.set(row.get("evento") or "")

    for idx, item in enumerate(self.issue_log_operaciones):
        if str(item.get("id")) == str(row.get("operacion_id")):
            values = list(self.issue_operacion_combo["values"])
            if idx < len(values):
                self.issue_operacion_var.set(values[idx])
            break

    self.issue_guardar_btn.configure(text="Guardar cambios")


def eliminar_issue_log(self):
    seleccion = self.issue_log_tree.selection() if self.issue_log_tree is not None else []
    if not seleccion:
        messagebox.showwarning("Sin seleccion", "Seleccione un evento para eliminar.")
        return
    issue_id = self.issue_log_tree.item(seleccion[0], "values")[0]
    if not messagebox.askyesno("Eliminar", "Desea eliminar este evento del statement of facts?"):
        return
    try:
        self.api_eliminar_issue_log(issue_id)
        self.buscar_issue_log()
    except Exception as exc:
        messagebox.showerror("Error SOF", str(exc))


def limpiar_issue_form(self):
    self.issue_editing_id = None
    self.issue_fecha_var.set("")
    self.issue_fecha_larga_var.set("-")
    self.issue_hora_desde_hh_var.set("08")
    self.issue_hora_desde_mm_var.set("00")
    self.issue_hora_hasta_hh_var.set("08")
    self.issue_hora_hasta_mm_var.set("00")
    self.issue_evento_var.set("")
    self.issue_subcategoria_var.set("")
    self.issue_bodega_var.set("")
    if hasattr(self, "issue_guardar_btn"):
        self.issue_guardar_btn.configure(text="Agregar")


def actualizar_subcategorias_sof(self):
    tipo = (self.issue_tipo_var.get() or "OPERATIVO").strip().upper()
    valores = self.issue_subcategorias_catalogo.get(tipo, [])
    if hasattr(self, "issue_subcategoria_combo"):
        self.issue_subcategoria_combo["values"] = valores
    if self.issue_subcategoria_var.get() and self.issue_subcategoria_var.get() not in valores:
        self.issue_subcategoria_var.set("")


def actualizar_fecha_larga_issue(self):
    try:
        valor = date.fromisoformat(self.issue_fecha_var.get().strip())
        self.issue_fecha_larga_var.set(f"{valor.day} de {MESES_ES[valor.month]} de {valor.year}")
    except Exception:
        self.issue_fecha_larga_var.set("-")


def _set_issue_date_target(self, target, value):
    largo = f"{value.day} de {MESES_ES[value.month]} de {value.year}"
    if target == "desde":
        self.issue_fecha_desde_var.set(value.isoformat())
        self.issue_fecha_desde_larga_var.set(largo)
    elif target == "hasta":
        self.issue_fecha_hasta_var.set(value.isoformat())
        self.issue_fecha_hasta_larga_var.set(largo)
    else:
        self.issue_fecha_var.set(value.isoformat())
        self.issue_fecha_larga_var.set(largo)


def abrir_calendario_issue(self, target="fecha"):
    popup = tk.Toplevel(self)
    popup.title("Seleccionar fecha")
    popup.geometry("360x230")
    popup.configure(bg=self.colors["bg_card"])
    popup.transient(self)

    today = date.today()
    year_var = tk.IntVar(value=today.year)
    month_var = tk.IntVar(value=today.month)

    controls = tk.Frame(popup, bg=self.colors["bg_card"])
    controls.pack(fill="x", padx=14, pady=12)
    ttk.Spinbox(controls, from_=2020, to=2100, textvariable=year_var, width=8).pack(side="left", padx=(0, 8))
    ttk.Combobox(controls, textvariable=month_var, state="readonly", width=8, values=list(range(1, 13))).pack(side="left")

    days = tk.Frame(popup, bg=self.colors["bg_card"])
    days.pack(fill="both", expand=True, padx=14, pady=(0, 12))

    def render_days():
        for child in days.winfo_children():
            child.destroy()
        _, total = calendar.monthrange(year_var.get(), month_var.get())
        for idx in range(total):
            day = idx + 1
            ttk.Button(days, text=str(day), command=lambda d=day: select_day(d)).grid(row=idx // 7, column=idx % 7, padx=2, pady=2, sticky="ew")

    def select_day(day):
        value = date(year_var.get(), month_var.get(), day)
        _set_issue_date_target(self, target, value)
        popup.destroy()

    ttk.Button(controls, text="Actualizar", style="Gray.TButton", command=render_days).pack(side="left", padx=8)
    render_days()
