import tkinter as tk
from tkinter import messagebox, ttk
from tkinter import filedialog
from datetime import date, datetime

from .lazy import LazyNotebook


def install_informes_screen(app_class):
    app_class.show_informes = show_informes
    app_class.build_informes_busqueda_tab = build_informes_busqueda_tab
    app_class.build_informes_detalle_tab = build_informes_detalle_tab
    app_class.cargar_informes_operaciones = cargar_informes_operaciones
    app_class.obtener_operacion_informe_seleccionada = obtener_operacion_informe_seleccionada
    app_class.ver_informe_seleccionado = ver_informe_seleccionado
    app_class.descargar_informe_seleccionado = descargar_informe_seleccionado
    app_class.obtener_parametros_informe = obtener_parametros_informe
    app_class.cargar_filtros_informe_seleccionado = cargar_filtros_informe_seleccionado
    app_class.aplicar_opciones_filtros_informes = aplicar_opciones_filtros_informes
    app_class.limpiar_filtros_informes = limpiar_filtros_informes
    app_class.abrir_selector_fecha_informe = abrir_selector_fecha_informe
    app_class.cargar_filtros_informe_desde_seleccion = cargar_filtros_informe_desde_seleccion
    app_class.render_informe_detalle = render_informe_detalle
    app_class.crear_tabla_informe = crear_tabla_informe
    app_class.crear_graficos_informe = crear_graficos_informe
    app_class.producto_visible_informe = producto_visible_informe


def show_informes(self):
    self.clear_content()
    self.highlight_sidebar_button("Informes")

    self.informes_tree = None
    self.informes_cache = []
    self.informes_detalle_body = None
    self.informes_exportar_formato_var = tk.StringVar(value="PDF")
    self.informes_tipo_reporte_var = tk.StringVar(value="Cliente ejecutivo")
    self.informes_estado_var = tk.StringVar(value="Listo. Presione Buscar informes para consultar operaciones.")
    self.informes_filter_vars = {
        "empresa": tk.StringVar(),
        "producto": tk.StringVar(),
        "bodega_numero": tk.StringVar(),
        "fecha_desde": tk.StringVar(),
        "fecha_hasta": tk.StringVar(),
    }
    self.informes_fecha_display_vars = {
        "fecha_desde": tk.StringVar(value="All dates"),
        "fecha_hasta": tk.StringVar(value="All dates"),
    }
    self.informes_filter_widgets = {}

    self.create_page_title(
        self.content,
        "Informes",
        "Busque operaciones por buque y abra el resumen operativo cuando lo necesite.",
    )

    tabs_host = tk.Frame(self.content, bg=self.colors["bg_main"])
    tabs_host.pack(fill="both", expand=True, padx=25, pady=(0, 20))

    self.informes_tabs = LazyNotebook(tabs_host)
    self.informes_tabs.pack(fill="both", expand=True)

    busqueda_tab = tk.Frame(self.informes_tabs.notebook, bg=self.colors["bg_main"])
    detalle_tab = tk.Frame(self.informes_tabs.notebook, bg=self.colors["bg_main"])

    self.informes_busqueda_tab = busqueda_tab
    self.informes_detalle_tab = detalle_tab

    self.informes_tabs.add(busqueda_tab, "Operaciones", lambda frame: self.build_informes_busqueda_tab(frame), build_now=True)
    self.informes_tabs.add(detalle_tab, "Informe en linea", lambda frame: self.build_informes_detalle_tab(frame))


def build_informes_busqueda_tab(self, parent):
    panel = tk.Frame(parent, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    panel.pack(fill="both", expand=True, padx=2, pady=8)

    header = tk.Frame(panel, bg=self.colors["bg_card"])
    header.pack(fill="x", padx=14, pady=(12, 8))
    tk.Label(header, text="Informes por buque", font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(side="left")
    ttk.Button(header, text="Buscar informes", style="Olive.TButton", command=self.cargar_informes_operaciones).pack(side="right")

    actions = tk.Frame(panel, bg=self.colors["bg_card"])
    actions.pack(fill="x", padx=14, pady=(0, 8))
    ttk.Button(actions, text="Ver informe", style="Gray.TButton", command=self.ver_informe_seleccionado).pack(side="left", padx=(0, 8))
    ttk.Combobox(
        actions,
        textvariable=self.informes_tipo_reporte_var,
        values=[
            "Cliente ejecutivo",
            "Operativo sintetizado",
            "SOF y alertas",
            "Productividad y documental",
            "Marchamos por viaje",
        ],
        state="readonly",
        width=30,
    ).pack(side="left", padx=(0, 8))
    ttk.Combobox(actions, textvariable=self.informes_exportar_formato_var, values=["PDF", "Excel", "CSV", "Word"], state="readonly", width=8).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Cargar filtros", style="Gray.TButton", command=self.cargar_filtros_informe_seleccionado).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Limpiar filtros", style="Gray.TButton", command=self.limpiar_filtros_informes).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Exportar", style="Gray.TButton", command=self.descargar_informe_seleccionado).pack(side="left")

    filtros = tk.Frame(panel, bg=self.colors["bg_card"])
    filtros.pack(fill="x", padx=14, pady=(0, 8))
    for idx, (key, label, kind) in enumerate([
        ("empresa", "Cliente", "combo"),
        ("producto", "Producto", "combo"),
        ("bodega_numero", "Bodega", "combo"),
        ("fecha_desde", "Desde", "date"),
        ("fecha_hasta", "Hasta", "date"),
    ]):
        box = tk.Frame(filtros, bg=self.colors["bg_card"])
        box.grid(row=0, column=idx, sticky="ew", padx=5, pady=4)
        tk.Label(box, text=label, font=("Segoe UI", 9, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w")
        if kind == "date":
            row = tk.Frame(box, bg=self.colors["bg_card"])
            row.pack(fill="x")
            ttk.Entry(row, textvariable=self.informes_fecha_display_vars[key], state="readonly").pack(side="left", fill="x", expand=True)
            ttk.Button(row, text="...", style="Gray.TButton", width=4, command=lambda campo=key: self.abrir_selector_fecha_informe(campo)).pack(side="left", padx=(4, 0))
        else:
            widget = ttk.Combobox(box, textvariable=self.informes_filter_vars[key], values=[], state="readonly")
            widget.pack(fill="x")
            self.informes_filter_widgets[key] = widget
        filtros.grid_columnconfigure(idx, weight=1)

    tk.Label(
        panel,
        textvariable=self.informes_estado_var,
        font=("Segoe UI", 10, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors["text_dark"],
        anchor="w",
    ).pack(fill="x", padx=14, pady=(0, 8))

    table_frame = tk.Frame(panel, bg=self.colors["bg_card"])
    table_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    columns = ("id", "codigo", "buque", "inicio", "cierre", "producto", "estado")
    self.informes_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=22)

    for col, heading, width in [
        ("id", "ID", 55),
        ("codigo", "Codigo", 180),
        ("buque", "Buque", 220),
        ("inicio", "Inicio", 130),
        ("cierre", "Cierre", 130),
        ("producto", "Producto", 220),
        ("estado", "Estado", 120),
    ]:
        self.informes_tree.heading(col, text=heading)
        self.informes_tree.column(col, width=width, anchor="center")

    scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.informes_tree.yview)
    scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.informes_tree.xview)
    self.informes_tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    self.informes_tree.bind("<<TreeviewSelect>>", self.cargar_filtros_informe_desde_seleccion)
    self.informes_tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)


def build_informes_detalle_tab(self, parent):
    host = tk.Frame(parent, bg=self.colors["bg_main"])
    host.pack(fill="both", expand=True, padx=2, pady=8)

    canvas = tk.Canvas(host, bg=self.colors["bg_main"], highlightthickness=0)
    scroll_y = ttk.Scrollbar(host, orient="vertical", command=canvas.yview)
    scroll_x = ttk.Scrollbar(host, orient="horizontal", command=canvas.xview)
    self.informes_detalle_body = tk.Frame(canvas, bg=self.colors["bg_main"])
    window_id = canvas.create_window((0, 0), window=self.informes_detalle_body, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    self.bind_scroll_canvas(canvas, self.informes_detalle_body, window_id, min_width=1080)
    canvas.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    host.grid_rowconfigure(0, weight=1)
    host.grid_columnconfigure(0, weight=1)

    panel = tk.Frame(self.informes_detalle_body, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    panel.pack(fill="x")
    tk.Label(
        panel,
        text=(
            "Seleccione una operacion y presione Ver informe.\n\n"
            "El informe en linea consolida cuotas, productos, bodegas, capacidad original, "
            "descargado, pendiente, avance, marchamos y alertas segun el tipo seleccionado."
        ),
        font=("Segoe UI", 12, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors.get("text_light", "#F4F8FF"),
        justify="left",
        wraplength=1100,
    ).pack(anchor="w", padx=14, pady=14)


def cargar_informes_operaciones(self):
    if self.informes_tree is None:
        return

    def tarea():
        return self.api_get_operaciones_buque()

    def al_terminar(data):
        self.informes_cache = data.get("data", []) if isinstance(data, dict) else []

        for item in self.informes_tree.get_children():
            self.informes_tree.delete(item)

        for operacion in self.informes_cache:
            self.informes_tree.insert(
                "",
                "end",
                values=(
                    operacion.get("id", ""),
                    operacion.get("codigo_operacion", ""),
                    operacion.get("nombre_buque", ""),
                    operacion.get("fecha_inicio", ""),
                    operacion.get("fecha_cierre", ""),
                    operacion.get("producto", ""),
                    operacion.get("estado", ""),
                ),
            )
        hijos = self.informes_tree.get_children()
        if len(hijos) == 1:
            self.informes_tree.selection_set(hijos[0])
            self.informes_tree.focus(hijos[0])
            self.cargar_filtros_informe_seleccionado(silencioso=True)
        self.informes_estado_var.set(f"Operaciones disponibles: {len(self.informes_cache)}. Seleccione una y presione Ver informe o Exportar.")

    self.ejecutar_en_segundo_plano(
        "Informes",
        "Buscando operaciones disponibles...",
        tarea,
        al_terminar,
    )


def obtener_operacion_informe_seleccionada(self):
    if self.informes_tree is None:
        return None

    seleccion = self.informes_tree.selection()
    if not seleccion:
        messagebox.showwarning("Sin seleccion", "Seleccione una operacion para el informe.")
        return None

    valores = self.informes_tree.item(seleccion[0], "values")
    operacion_id = self.safe_int(valores[0], None) if valores else None
    if not operacion_id:
        messagebox.showwarning("Seleccion invalida", "No se pudo leer la operacion seleccionada.")
        return None

    for operacion in self.informes_cache:
        if self.safe_int(operacion.get("id"), None) == operacion_id:
            return operacion

    return {"id": operacion_id}


def obtener_parametros_informe(self):
    params = {"tipo_reporte": _codigo_tipo_reporte(self.informes_tipo_reporte_var.get())}
    for key, var in getattr(self, "informes_filter_vars", {}).items():
        value = var.get().strip()
        if value:
            params[key] = self.safe_int(value, value) if key == "bodega_numero" else value
    return params


def limpiar_filtros_informes(self):
    for var in getattr(self, "informes_filter_vars", {}).values():
        var.set("")
    if hasattr(self, "informes_fecha_display_vars"):
        self.informes_fecha_display_vars["fecha_desde"].set("All dates")
        self.informes_fecha_display_vars["fecha_hasta"].set("All dates")


def aplicar_opciones_filtros_informes(self, opciones):
    mapa = {"empresa": "empresas", "producto": "productos", "bodega_numero": "bodegas"}
    for key, option_key in mapa.items():
        widget = self.informes_filter_widgets.get(key) if hasattr(self, "informes_filter_widgets") else None
        if widget is not None:
            widget["values"] = [""] + [str(v) for v in opciones.get(option_key, []) if v not in (None, "")]


def cargar_filtros_informe_desde_seleccion(self, _event=None):
    self.cargar_filtros_informe_seleccionado(silencioso=True)


def cargar_filtros_informe_seleccionado(self, silencioso=False):
    if silencioso:
        if self.informes_tree is None:
            return
        seleccion = self.informes_tree.selection()
        if not seleccion:
            return
        valores = self.informes_tree.item(seleccion[0], "values")
        operacion_id = self.safe_int(valores[0], None) if valores else None
        operacion = next(
            (
                item
                for item in self.informes_cache
                if self.safe_int(item.get("id"), None) == operacion_id
            ),
            {"id": operacion_id} if operacion_id else None,
        )
    else:
        operacion = self.obtener_operacion_informe_seleccionada()
    if not operacion:
        return

    def tarea():
        return self.api_get_reporte_buque_filtros(operacion.get("id"))

    def al_terminar(data):
        opciones = data.get("opciones", {}) if isinstance(data, dict) else {}
        self.aplicar_opciones_filtros_informes(opciones)
        self.informes_estado_var.set("Filtros cargados. Puede consultar sin filtros o seleccionar cliente, producto, bodega y rango.")

    self.ejecutar_en_segundo_plano(
        "Filtros de informe",
        "Cargando opciones de cliente, producto, bodega y fechas...",
        tarea,
        al_terminar,
    )


def _meses_en():
    return ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]


def _fecha_larga_en(fecha_iso):
    if not fecha_iso:
        return "All dates"
    try:
        fecha = datetime.strptime(str(fecha_iso)[:10], "%Y-%m-%d").date()
        return f"{fecha.strftime('%A')}, {_meses_en()[fecha.month - 1]} {fecha.day}, {fecha.year}"
    except Exception:
        return str(fecha_iso)


def abrir_selector_fecha_informe(self, campo):
    popup = tk.Toplevel(self)
    popup.title("Select date")
    popup.geometry("390x220")
    popup.configure(bg=self.colors["bg_card"])
    popup.transient(self)
    popup.grab_set()

    hoy = date.today()
    actual = self.informes_filter_vars.get(campo).get() if hasattr(self, "informes_filter_vars") else ""
    try:
        base = datetime.strptime(actual, "%Y-%m-%d").date() if actual else hoy
    except Exception:
        base = hoy

    dia_var = tk.StringVar(value=str(base.day))
    mes_var = tk.StringVar(value=_meses_en()[base.month - 1])
    anio_var = tk.StringVar(value=str(base.year))
    contenido = tk.Frame(popup, bg=self.colors["bg_card"])
    contenido.pack(fill="both", expand=True, padx=18, pady=18)
    tk.Label(contenido, text="Report date range", font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w", pady=(0, 12))
    fila = tk.Frame(contenido, bg=self.colors["bg_card"])
    fila.pack(fill="x")
    ttk.Combobox(fila, textvariable=dia_var, values=[str(i) for i in range(1, 32)], state="readonly", width=6).pack(side="left", padx=(0, 8))
    ttk.Combobox(fila, textvariable=mes_var, values=_meses_en(), state="readonly", width=16).pack(side="left", padx=(0, 8))
    ttk.Combobox(fila, textvariable=anio_var, values=[str(i) for i in range(hoy.year - 5, hoy.year + 6)], state="readonly", width=8).pack(side="left")

    def aplicar():
        try:
            fecha = date(int(anio_var.get()), _meses_en().index(mes_var.get()) + 1, int(dia_var.get()))
        except Exception:
            messagebox.showerror("Invalid date", "Select a valid date.")
            return
        self.informes_filter_vars[campo].set(fecha.isoformat())
        self.informes_fecha_display_vars[campo].set(_fecha_larga_en(fecha.isoformat()))
        popup.destroy()

    def limpiar():
        self.informes_filter_vars[campo].set("")
        self.informes_fecha_display_vars[campo].set("All dates")
        popup.destroy()

    acciones = tk.Frame(contenido, bg=self.colors["bg_card"])
    acciones.pack(fill="x", pady=(18, 0))
    ttk.Button(acciones, text="Apply", style="Olive.TButton", command=aplicar).pack(side="left", padx=(0, 8))
    ttk.Button(acciones, text="Clear", style="Gray.TButton", command=limpiar).pack(side="left", padx=(0, 8))
    ttk.Button(acciones, text="Cancel", style="Gray.TButton", command=popup.destroy).pack(side="left")


def ver_informe_seleccionado(self):
    operacion = self.obtener_operacion_informe_seleccionada()
    if not operacion:
        return

    params = self.obtener_parametros_informe()

    def tarea():
        return self.api_get_reporte_buque(operacion.get("id"), params)

    def al_terminar(data):
        self.informes_tabs.select(self.informes_detalle_tab)
        self.render_informe_detalle(data)
        self.informes_estado_var.set(f"Informe en linea generado: {self.informes_tipo_reporte_var.get()}.")

    self.ejecutar_en_segundo_plano(
        "Informe en linea",
        "Generando informe con graficos y KPIs...",
        tarea,
        al_terminar,
    )


def descargar_informe_seleccionado(self):
    operacion = self.obtener_operacion_informe_seleccionada()
    if not operacion:
        return

    formato_ui = self.informes_exportar_formato_var.get().strip().lower()
    formato = "excel" if formato_ui == "excel" else "csv" if formato_ui == "csv" else "word" if formato_ui == "word" else "pdf"
    extension = ".xlsx" if formato == "excel" else ".csv" if formato == "csv" else ".docx" if formato == "word" else ".pdf"
    filetypes = [("Excel", "*.xlsx")] if formato == "excel" else [("CSV", "*.csv")] if formato == "csv" else [("Word", "*.docx")] if formato == "word" else [("PDF", "*.pdf")]
    ruta = filedialog.asksaveasfilename(
        title=f"Exportar informe {formato_ui.upper()}",
        defaultextension=extension,
        filetypes=filetypes,
    )
    if not ruta:
        return

    params = self.obtener_parametros_informe()

    def tarea():
        return self.api_descargar_reporte_buque(operacion.get("id"), formato, ruta, params)

    def al_terminar(ruta_final):
        extra = "\n\nEl nombre cambio automaticamente porque el archivo original estaba bloqueado." if ruta_final != ruta else ""
        messagebox.showinfo("Informe exportado", f"Archivo generado correctamente:\n{ruta_final}{extra}")
        self.informes_estado_var.set(f"Informe exportado en formato {formato_ui.upper()}.")

    self.ejecutar_en_segundo_plano(
        "Exportar informe",
        f"Generando archivo {formato_ui.upper()} con KPIs y graficos...",
        tarea,
        al_terminar,
    )


def render_informe_detalle(self, data):
    if self.informes_detalle_body is None:
        return

    for widget in self.informes_detalle_body.winfo_children():
        widget.destroy()

    if not isinstance(data, dict):
        tk.Label(
            self.informes_detalle_body,
            text="No se pudo generar el informe en linea. El backend no devolvio informacion valida.",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors.get("danger", "#FF4D6D"),
            justify="left",
            wraplength=1100,
        ).pack(anchor="w", fill="x", padx=18, pady=18)
        return

    if data.get("error") or data.get("detail") or data.get("status") == "error":
        detalle = data.get("message") or data.get("detail") or data.get("error") or "Error interno del backend."
        tk.Label(
            self.informes_detalle_body,
            text=f"No se pudo generar el informe en linea:\n{detalle}",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["bg_card"],
            fg=self.colors.get("danger", "#FF4D6D"),
            justify="left",
            wraplength=1100,
        ).pack(anchor="w", fill="x", padx=18, pady=18)
        return

    operacion = data.get("operacion", {})
    tipo_reporte = _codigo_tipo_reporte(self.informes_tipo_reporte_var.get())
    kpis = data.get("kpis", {})
    cuotas = [
        {
            "cliente": row.get("empresa"),
            "producto": self.producto_visible_informe(row.get("producto")),
            "bodega_numero": row.get("bodega_numero"),
            "cuota_mt": row.get("cuota_mt"),
            "retirado_mt": row.get("retirado_mt"),
            "faltante_mt": row.get("faltante_mt"),
            "avance_pct": row.get("avance_pct"),
            "guias": row.get("guias"),
        }
        for row in data.get("clientes", [])
    ]
    productos = [
        {**row, "producto": self.producto_visible_informe(row.get("producto"))}
        for row in data.get("graficos", {}).get("retiro_por_producto", [])
        if isinstance(row, dict)
    ]
    alertas = data.get("alertas", [])
    sof = data.get("sof", [])
    sof_detalle = data.get("sof_detalle", [])
    bodegas = data.get("bodegas", [])
    bodegas = [
        {**row, "producto": self.producto_visible_informe(row.get("producto"))}
        for row in bodegas
        if isinstance(row, dict)
    ]
    cuotas_grafico = [
        {**row, "cliente_producto": f"{row.get('cliente') or row.get('empresa') or 'SIN CLIENTE'} | {row.get('producto') or 'Cuota general'}"}
        for row in cuotas
    ]
    bodegas_grafico = [
        {**row, "bodega_producto": f"{row.get('bodega') or 'Bodega ' + str(row.get('bodega_numero') or '')} | {row.get('producto') or 'Cuota general'}"}
        for row in bodegas
    ]
    graficos = data.get("graficos", {})
    resumen = data.get("resumen", {})

    header = tk.Frame(self.informes_detalle_body, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    header.pack(fill="x", pady=(0, 10))
    tk.Label(
        header,
        text=f"{self.informes_tipo_reporte_var.get()}: {operacion.get('nombre_buque', '')}",
        font=("Segoe UI", 15, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors["text_dark"],
    ).pack(anchor="w", padx=14, pady=(12, 2))
    tk.Label(
        header,
        text=f"Codigo: {operacion.get('codigo_operacion', '')} | Estado: {operacion.get('estado', '')} | Inicio: {operacion.get('fecha_inicio', '')}",
        font=("Segoe UI", 10, "bold"),
        bg=self.colors["bg_card"],
        fg="#4B4B4B",
    ).pack(anchor="w", padx=14, pady=(0, 12))

    lectura = tk.Frame(self.informes_detalle_body, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    lectura.pack(fill="x", pady=(0, 12))
    tk.Label(
        lectura,
        text=_lectura_reporte(tipo_reporte),
        justify="left",
        wraplength=1100,
        font=("Segoe UI", 10, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors["text_dark"],
    ).pack(anchor="w", padx=14, pady=12)

    if tipo_reporte == "sof":
        cards = tk.Frame(self.informes_detalle_body, bg=self.colors["bg_main"])
        cards.pack(fill="x", pady=(0, 12))
        total_eventos = sum(self.safe_number(row.get("eventos")) for row in sof)
        total_horas = sum(self.safe_number(row.get("horas")) for row in sof)
        demora_horas = sum(self.safe_number(row.get("horas")) for row in sof if row.get("tipo") == "DEMORA")
        self.create_card(cards, "Eventos SOF", self.formatear_numero(total_eventos), self.colors["accent"])
        self.create_card(cards, "Horas SOF", self.formatear_numero(total_horas, 2), self.colors["info"])
        self.create_card(cards, "Horas demora", self.formatear_numero(demora_horas, 2), self.colors["warning"])
        self.create_card(cards, "Categorias", self.formatear_numero(len({row.get("tipo") for row in sof})), self.colors["success"])
        self.crear_graficos_informe(
            [
                ("Horas por subcategoria", sof, "subcategoria", "horas", "barras"),
                ("Eventos por tipo", sof, "tipo", "eventos", "circular"),
            ]
        )
        self.crear_tabla_informe(
            self.informes_detalle_body,
            "SOF por categoria, subcategoria y bodega",
            ("tipo", "subcategoria", "bodega_numero", "eventos", "horas", "fecha_desde", "fecha_hasta"),
            {"tipo": "Tipo", "subcategoria": "Subcategoria", "bodega_numero": "Bodega", "eventos": "Eventos", "horas": "Horas", "fecha_desde": "Desde", "fecha_hasta": "Hasta"},
            sof,
            height=10,
        )
        self.crear_tabla_informe(
            self.informes_detalle_body,
            "Detalle SOF del buque",
            ("fecha_larga", "rango_hora", "tipo", "subcategoria", "bodega_numero", "guia", "cliente", "producto", "placa", "horas", "evento", "comentario", "creado_por"),
            {
                "fecha_larga": "Fecha",
                "rango_hora": "Hora",
                "tipo": "Tipo",
                "subcategoria": "Subcategoria",
                "bodega_numero": "Bodega",
                "guia": "Guia",
                "cliente": "Cliente",
                "producto": "Producto",
                "placa": "Placa",
                "horas": "Horas",
                "evento": "Evento",
                "comentario": "Comentario",
                "creado_por": "Usuario",
            },
            sof_detalle,
            height=14,
        )
        return

    cards = tk.Frame(self.informes_detalle_body, bg=self.colors["bg_main"])
    cards.pack(fill="x", pady=(0, 12))

    if tipo_reporte == "cliente":
        corte_cliente = data.get("corte_cliente", {}) if isinstance(data.get("corte_cliente"), dict) else {}
        corte_totales = corte_cliente.get("totales", {}) if isinstance(corte_cliente.get("totales"), dict) else {}
        self.create_card(cards, "Cuota total MT", self.formatear_numero(corte_totales.get("cuota_tm"), 2), self.colors["accent"])
        self.create_card(cards, "Descargado MT", self.formatear_numero(corte_totales.get("retirado_tm"), 2), self.colors["success"])
        self.create_card(cards, "Pendiente MT", self.formatear_numero(corte_totales.get("pendiente_tm"), 2), self.colors["warning"])
        self.create_card(cards, "Avance", f"{self.safe_number(corte_totales.get('avance_pct')):,.2f}%", self.colors["info"])
        corte_rows = [
            {
                "empresa": row.get("empresa"),
                "cuota_pct": row.get("cuota_pct"),
                "cuota_tm": row.get("cuota_tm"),
                "cuota_viajes": row.get("cuota_viajes"),
                "retirado_tm": row.get("retirado_tm"),
                "retirado_pct": row.get("retirado_pct"),
                "retirado_viajes": row.get("retirado_viajes"),
                "promedio_x_viaje": row.get("promedio_x_viaje"),
                "pendiente_tm": row.get("pendiente_tm"),
                "pendiente_viajes": row.get("pendiente_viajes"),
            }
            for row in corte_cliente.get("rows", []) or []
        ]
        self.crear_graficos_informe(
            [
                ("Descargado por cliente", cuotas, "cliente", "retirado_mt", "barras"),
                ("Pendiente por cliente", cuotas, "cliente", "faltante_mt", "barras"),
                ("Pendiente por bodega", graficos.get("faltante_bodegas", []), "bodega", "faltante_mt", "barras"),
                ("Tendencia diaria MT", graficos.get("tendencia_fecha", []), "fecha", "retirado_mt", "lineal"),
            ]
        )
        self.crear_tabla_informe(
            self.informes_detalle_body,
            "CORTE FINAL - CUOTA VS DESCARGADO",
            ("empresa", "cuota_pct", "cuota_tm", "cuota_viajes", "retirado_tm", "retirado_pct", "retirado_viajes", "promedio_x_viaje", "pendiente_tm", "pendiente_viajes"),
            {
                "empresa": "EMPRESA",
                "cuota_pct": "CUOTA %",
                "cuota_tm": "CUOTA T.M.",
                "cuota_viajes": "CUOTA # VIAJES",
                "retirado_tm": "RETIRADO T.M.",
                "retirado_pct": "RETIRADO %",
                "retirado_viajes": "RETIRADO # VIAJES",
                "promedio_x_viaje": "PROMEDIO X VIAJE",
                "pendiente_tm": "PENDIENTE T.M.",
                "pendiente_viajes": "PENDIENTE VIAJES",
            },
            corte_rows,
        )
        bodegas_cliente = data.get("reporte_bodegas_cliente", {}) if isinstance(data.get("reporte_bodegas_cliente"), dict) else {}
        bodega_headers = list(bodegas_cliente.get("headers", []) or [])
        bodega_columns = ["concepto"] + [f"col_{idx}" for idx, _header in enumerate(bodega_headers)]
        bodega_headings = {"concepto": "CONCEPTO"}
        for idx, header_text in enumerate(bodega_headers):
            bodega_headings[f"col_{idx}"] = header_text
        bodega_rows = []
        for row in bodegas_cliente.get("rows", []) or []:
            item = {"concepto": row.get("concepto")}
            for idx, value in enumerate(row.get("valores", []) or []):
                item[f"col_{idx}"] = value
            bodega_rows.append(item)
        self.crear_tabla_informe(
            self.informes_detalle_body,
            "REPORTE DE SALDOS POR BODEGA",
            tuple(bodega_columns),
            bodega_headings,
            bodega_rows,
            height=11,
        )
        self.crear_tabla_informe(
            self.informes_detalle_body,
            "Resumen operativo consolidado",
            ("severidad", "tipo", "mensaje"),
            {"severidad": "Severidad", "tipo": "Tipo", "mensaje": "Mensaje"},
            alertas,
            height=8,
        )
        return

    if tipo_reporte == "ejecutivo":
        self.create_card(cards, "Capacidad MT", self.formatear_numero(kpis.get("capacidad_mt"), 2), self.colors["accent"])
        self.create_card(cards, "Descargado MT", self.formatear_numero(kpis.get("retirado_mt"), 2), self.colors["success"])
        self.create_card(cards, "Pendiente MT", self.formatear_numero(kpis.get("faltante_mt"), 2), self.colors["warning"])
        self.create_card(cards, "Avance", f"{self.safe_number(kpis.get('avance_descarga_pct')):,.2f}%", self.colors["info"])
        self.crear_graficos_informe(
            [
                ("Descargado por bodega/producto", bodegas_grafico, "bodega_producto", "retirado_mt", "barras"),
                ("Estado descarga", graficos.get("estado_descarga", []), "estado", "valor", "circular"),
                ("Tendencia diaria", graficos.get("tendencia_fecha", []), "fecha", "retirado_mt", "lineal"),
                ("Descargado por producto", productos, "producto", "retirado_mt", "barras"),
            ]
        )

    elif tipo_reporte == "cuotas":
        total_cuota = sum(self.safe_number(row.get("cuota_mt")) for row in cuotas)
        total_descargado = sum(self.safe_number(row.get("retirado_mt")) for row in cuotas)
        total_pendiente = sum(self.safe_number(row.get("faltante_mt")) for row in cuotas)
        sobrecuotas = sum(1 for row in cuotas if self.safe_number(row.get("retirado_mt")) > self.safe_number(row.get("cuota_mt")) > 0)
        avance = (total_descargado / total_cuota * 100) if total_cuota else 0
        self.create_card(cards, "Cuota MT", self.formatear_numero(total_cuota, 2), self.colors["accent"])
        self.create_card(cards, "Descargado MT", self.formatear_numero(total_descargado, 2), self.colors["success"])
        self.create_card(cards, "Pendiente MT", self.formatear_numero(total_pendiente, 2), self.colors["warning"])
        self.create_card(cards, "Sobrecuotas", self.formatear_numero(sobrecuotas), self.colors["danger"])
        self.crear_graficos_informe(
            [
                ("Descargado por cliente/producto", cuotas_grafico, "cliente_producto", "retirado_mt", "barras"),
                ("Pendiente por cliente/producto", cuotas_grafico, "cliente_producto", "faltante_mt", "barras"),
                ("Avance por cliente/producto", cuotas_grafico, "cliente_producto", "avance_pct", "barras"),
                ("Viajes por cliente/producto", cuotas_grafico, "cliente_producto", "guias", "barras"),
            ]
        )

    elif tipo_reporte == "bodegas":
        self.create_card(cards, "Bodegas", self.formatear_numero(len(bodegas)), self.colors["accent"])
        self.create_card(cards, "Capacidad MT", self.formatear_numero(resumen.get("capacidad_mt"), 2), self.colors["info"])
        self.create_card(cards, "Descargado MT", self.formatear_numero(resumen.get("retirado_mt"), 2), self.colors["success"])
        self.create_card(cards, "Pendiente MT", self.formatear_numero(resumen.get("faltante_mt"), 2), self.colors["warning"])
        self.crear_graficos_informe(
            [
                ("Descargado por bodega/producto", bodegas_grafico, "bodega_producto", "retirado_mt", "barras"),
                ("Pendiente por bodega/producto", bodegas_grafico, "bodega_producto", "faltante_mt", "barras"),
                ("Avance por bodega/producto", bodegas_grafico, "bodega_producto", "avance_pct", "barras"),
                ("Estado descarga", graficos.get("estado_descarga", []), "estado", "valor", "circular"),
            ]
        )

    elif tipo_reporte in ("alertas", "sof_alertas"):
        alertas_por_tipo = _conteo_por(alertas, "tipo")
        alertas_por_severidad = _conteo_por(alertas, "severidad")
        sof_demoras = [row for row in sof if row.get("tipo") == "DEMORA"]
        self.create_card(cards, "Alertas", self.formatear_numero(len(alertas)), self.colors["danger"])
        self.create_card(cards, "Severidad alta", self.formatear_numero(sum(1 for row in alertas if row.get("severidad") == "ALTA")), self.colors["danger"])
        self.create_card(cards, "Eventos demora", self.formatear_numero(sum(self.safe_number(row.get("eventos")) for row in sof_demoras)), self.colors["warning"])
        self.create_card(cards, "Horas demora", self.formatear_numero(sum(self.safe_number(row.get("horas")) for row in sof_demoras), 2), self.colors["info"])
        self.crear_graficos_informe(
            [
                ("Alertas por tipo", alertas_por_tipo, "label", "valor", "barras"),
                ("Alertas por severidad", alertas_por_severidad, "label", "valor", "circular"),
                ("Horas de demora SOF", sof_demoras, "subcategoria", "horas", "barras"),
            ]
        )

    elif tipo_reporte in ("productividad", "productividad_documental"):
        duraciones = graficos.get("duracion_por_camion", [])
        promedio = sum(self.safe_number(row.get("duracion_min")) for row in duraciones) / len(duraciones) if duraciones else 0
        toneladas_por_viaje = self.safe_number(kpis.get("retirado_mt")) / self.safe_number(kpis.get("completas"), 1) if self.safe_number(kpis.get("completas")) else 0
        self.create_card(cards, "Viajes", self.formatear_numero(kpis.get("total_guias")), self.colors["accent"])
        self.create_card(cards, "Completos", self.formatear_numero(kpis.get("completas")), self.colors["success"])
        self.create_card(cards, "Duracion prom.", f"{promedio:,.2f} min", self.colors["info"])
        self.create_card(cards, "MT/viaje", self.formatear_numero(toneladas_por_viaje, 2), self.colors["warning"])
        self.crear_graficos_informe(
            [
                ("Duracion por camion", duraciones, "camion", "duracion_min", "barras"),
                ("Tendencia diaria MT", graficos.get("tendencia_fecha", []), "fecha", "retirado_mt", "lineal"),
                ("Descargado por producto", productos, "producto", "retirado_mt", "barras"),
            ]
        )

    elif tipo_reporte == "documental":
        documental = data.get("documental", [])
        total_docs = sum(self.safe_number(row.get("guias")) for row in documental)
        aprobadas = sum(self.safe_number(row.get("guias")) for row in documental if row.get("aprobada"))
        pendientes_doc = total_docs - aprobadas
        self.create_card(cards, "Guias", self.formatear_numero(total_docs), self.colors["accent"])
        self.create_card(cards, "Aprobadas", self.formatear_numero(aprobadas), self.colors["success"])
        self.create_card(cards, "Pendientes", self.formatear_numero(pendientes_doc), self.colors["warning"])
        self.create_card(cards, "Estados", self.formatear_numero(len({row.get("estado") for row in documental})), self.colors["info"])
        self.crear_graficos_informe(
            [
                ("Guias por estado", documental, "estado", "guias", "barras"),
                ("Guias por etapa QR", documental, "etapa_qr", "guias", "circular"),
            ]
        )

    elif tipo_reporte == "marchamos":
        marchamos = data.get("marchamos", []) or []
        total_mt = sum(self.safe_number(row.get("retirado_mt")) for row in marchamos)
        self.create_card(cards, "Registros", self.formatear_numero(len(marchamos)), self.colors["accent"])
        self.create_card(cards, "MT asociado", self.formatear_numero(total_mt, 2), self.colors["success"])
        self.create_card(cards, "Choferes", self.formatear_numero(len({row.get("chofer") for row in marchamos if row.get("chofer")})), self.colors["info"])
        self.create_card(cards, "Empresas", self.formatear_numero(len({row.get("empresa") for row in marchamos if row.get("empresa")})), self.colors["warning"])
        self.crear_graficos_informe(
            [
                ("MT por empresa", marchamos, "empresa", "retirado_mt", "barras"),
                ("MT por producto", marchamos, "producto", "retirado_mt", "barras"),
                ("MT por chofer", marchamos, "chofer", "retirado_mt", "barras"),
            ]
        )

    if tipo_reporte not in ("ejecutivo", "cuotas", "bodegas", "alertas", "sof_alertas", "productividad", "productividad_documental", "documental", "marchamos"):
        self.create_card(cards, "Guias", self.formatear_numero(kpis.get("total_guias")), self.colors["accent"])
        self.create_card(cards, "Completas", self.formatear_numero(kpis.get("completas")), self.colors["success"])
        self.create_card(cards, "Descargado MT", self.formatear_numero(kpis.get("retirado_mt"), 2), self.colors["info"])
        self.create_card(cards, "Pendiente MT", self.formatear_numero(kpis.get("faltante_mt"), 2), self.colors["warning"])

    if tipo_reporte in ("ejecutivo", "bodegas"):
        self.crear_tabla_informe(
            self.informes_detalle_body,
            "Descarga por bodega",
            ("bodega_numero", "producto", "capacidad_mt", "retirado_mt", "faltante_mt", "avance_pct", "guias"),
            {"bodega_numero": "Bodega", "producto": "Producto", "capacidad_mt": "Capacidad MT", "retirado_mt": "Descargado MT", "faltante_mt": "Pendiente MT", "avance_pct": "Avance %", "guias": "Guias"},
            bodegas,
        )

    if tipo_reporte in ("ejecutivo", "cuotas"):
        self.crear_tabla_informe(
            self.informes_detalle_body,
            "Cuota vs descargado real",
            ("cliente", "producto", "bodega", "cuota_mt", "retirado_mt", "faltante_mt", "avance_pct", "guias"),
            {"cliente": "Cliente", "producto": "Producto", "bodega": "Bodega", "cuota_mt": "Cuota MT", "retirado_mt": "Descargado MT", "faltante_mt": "Pendiente MT", "avance_pct": "Avance %", "guias": "Guias"},
            cuotas,
        )

    if tipo_reporte in ("ejecutivo", "productividad", "productividad_documental"):
        self.crear_tabla_informe(
            self.informes_detalle_body,
            "Resumen por producto",
            ("producto", "guias", "retirado_mt"),
            {"producto": "Producto", "guias": "Guias", "retirado_mt": "Descargado MT"},
            productos,
            height=7,
        )
        self.crear_tabla_informe(
            self.informes_detalle_body,
            "Duracion por camion",
            ("camion", "guia", "empresa", "producto", "placa", "duracion_min"),
            {"camion": "Camion", "guia": "Guia", "empresa": "Empresa", "producto": "Producto", "placa": "Placa", "duracion_min": "Duracion min"},
            [
                {**row, "producto": self.producto_visible_informe(row.get("producto"))}
                for row in data.get("graficos", {}).get("duracion_por_camion", [])
                if isinstance(row, dict)
            ],
            height=9,
        )

    if tipo_reporte in ("ejecutivo", "alertas", "sof_alertas", "documental", "productividad_documental"):
        self.crear_tabla_informe(
            self.informes_detalle_body,
            "Alertas operativas",
            ("severidad", "tipo", "mensaje"),
            {"severidad": "Severidad", "tipo": "Tipo", "mensaje": "Mensaje"},
            alertas,
            height=8,
        )

    if tipo_reporte in ("documental", "productividad_documental"):
        self.crear_tabla_informe(
            self.informes_detalle_body,
            "Estado documental",
            ("estado", "etapa_qr", "aprobada", "guias"),
            {"estado": "Estado", "etapa_qr": "Etapa QR", "aprobada": "Aprobada", "guias": "Guias"},
            data.get("documental", []),
            height=10,
        )

    if tipo_reporte == "sof_alertas":
        self.crear_tabla_informe(
            self.informes_detalle_body,
            "SOF por categoria y subcategoria",
            ("tipo", "subcategoria", "bodega_numero", "eventos", "horas", "fecha_desde", "fecha_hasta"),
            {"tipo": "Tipo", "subcategoria": "Subcategoria", "bodega_numero": "Bodega", "eventos": "Eventos", "horas": "Horas", "fecha_desde": "Desde", "fecha_hasta": "Hasta"},
            sof,
            height=10,
        )

    if tipo_reporte == "marchamos":
        self.crear_tabla_informe(
            self.informes_detalle_body,
            "Marchamos por viaje",
            ("guia", "empresa", "producto", "chofer", "placa", "bodega_numero", "numero_tolva", "marchamos", "peso_vacio", "peso_lleno", "retirado_mt", "fecha"),
            {
                "guia": "Guia",
                "empresa": "Empresa",
                "producto": "Producto",
                "chofer": "Chofer",
                "placa": "Placa",
                "bodega_numero": "Bodega",
                "numero_tolva": "Tolva",
                "marchamos": "Marchamos",
                "peso_vacio": "Peso vacio",
                "peso_lleno": "Peso lleno",
                "retirado_mt": "MT",
                "fecha": "Fecha",
            },
            data.get("marchamos", []),
            height=14,
        )


def producto_visible_informe(self, producto):
    valor = str(producto or "").strip()
    if valor.upper() in ("", "TODOS", "ALL", "SIN PRODUCTO", "NONE", "NULL"):
        return "Cuota general"
    return valor


def crear_tabla_informe(self, parent, titulo, columns, headings, data, height=10):
    panel = tk.Frame(parent, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    panel.pack(fill="both", expand=True, pady=(0, 12))

    tk.Label(panel, text=titulo, font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w", padx=14, pady=(12, 6))

    table_frame = tk.Frame(panel, bg=self.colors["bg_card"])
    table_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=height)
    for col in columns:
        tree.heading(col, text=headings.get(col, col))
        tree.column(col, width=180 if col != "mensaje" else 520, anchor="center" if col != "mensaje" else "w")

    for row in data or []:
        values = []
        for col in columns:
            value = row.get(col, "")
            if isinstance(value, float):
                value = f"{value:,.2f}"
            values.append(value)
        tree.insert("", "end", values=values)

    scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)


def crear_graficos_informe(self, specs):
    if not specs:
        return
    panel = tk.Frame(self.informes_detalle_body, bg=self.colors["bg_main"])
    panel.pack(fill="both", expand=True, pady=(0, 12))
    for idx, (titulo, data, label_key, value_key, chart_type) in enumerate(specs):
        row = idx // 2
        col = idx % 2
        if chart_type == "circular":
            self.crear_chart_circular(panel, titulo, data or [], label_key, value_key, row, col)
        elif chart_type == "lineal":
            self.crear_chart_lineal(panel, titulo, data or [], label_key, value_key, row, col)
        else:
            self.crear_chart_barras(panel, titulo, data or [], label_key, value_key, row, col)
    for col in range(2):
        panel.grid_columnconfigure(col, weight=1, uniform="informes_charts")
    for row in range((len(specs) + 1) // 2):
        panel.grid_rowconfigure(row, weight=1, minsize=290)


def _conteo_por(rows, key):
    conteo = {}
    for row in rows or []:
        label = str(row.get(key) or "SIN DATO")
        conteo[label] = conteo.get(label, 0) + 1
    return [{"label": label, "valor": valor} for label, valor in sorted(conteo.items())]


def _lectura_reporte(tipo):
    textos = {
        "cliente": "Reportes principales del cliente: corte final y saldos por bodega, mejorados con KPIs, graficos y lectura ejecutiva.",
        "ejecutivo": "Vista gerencial completa: capacidad, descargado, pendiente, avance, tendencia diaria, producto, bodega, cuotas y alertas.",
        "sof": "Statement of Facts: tiempos por suceso, categoria, subcategoria, bodega, detalle cronologico, usuario responsable y acumulados de demora.",
        "cuotas": "Control de cuota vs descargado: compara cuota por cliente/producto contra lo realmente descargado, pendiente, sobrecuotas, avance, viajes y riesgo operativo.",
        "bodegas": "Descarga por bodega: analiza capacidad, descargado, pendiente de descarga, avance porcentual, viajes y distribucion del trabajo por bodega.",
        "alertas": "Alertas operativas: resume severidades, tipos de alerta, eventos de demora, horas acumuladas e incidentes que requieren seguimiento.",
        "sof_alertas": "SOF y alertas: consolida el Statement of Facts con alertas operativas para reducir reportes sin perder eventos, demoras ni riesgos.",
        "productividad": "Productividad por camion: mide viajes, duracion promedio, toneladas por viaje, tendencias diarias y rendimiento por producto/camion.",
        "productividad_documental": "Productividad y documental: unifica rendimiento por camion, tendencia, producto y estado documental para seguimiento ejecutivo.",
        "documental": "Diferencias documentales: muestra aprobaciones, pendientes, estados operativos, etapas QR y riesgos de trazabilidad documental.",
        "marchamos": "Marchamos por viaje: lista los marchamos capturados en tercer escaneo, vinculados a guia, empresa, producto, chofer, placa, peso y bodega/tolva.",
    }
    return textos.get(tipo, textos["cliente"])


def _codigo_tipo_reporte(label):
    mapa = {
        "Cliente ejecutivo": "cliente",
        "Operativo sintetizado": "ejecutivo",
        "SOF y alertas": "sof_alertas",
        "Productividad y documental": "productividad_documental",
        "Resumen ejecutivo por buque": "ejecutivo",
        "SOF - Statement of Facts": "sof",
        "Cuotas vs descargado": "cuotas",
        "Descarga por bodega": "bodegas",
        "Alertas operativas": "alertas",
        "Productividad por camion": "productividad",
        "Diferencias documentales": "documental",
        "Marchamos por viaje": "marchamos",
    }
    return mapa.get(label, "ejecutivo")

