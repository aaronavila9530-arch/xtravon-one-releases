import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


def install_liquidaciones_choferes_screen(app_class):
    def _liq_text_fg(self):
        return "#F4F8FF"

    def _liq_muted_fg(self):
        return "#B9D8FF"

    def api_get_liquidaciones_filtros(self, params=None):
        import requests

        respuesta = requests.get(
            f"{self.api_base}/liquidaciones-choferes/filtros",
            params=params or {},
            timeout=60,
        )
        if respuesta.status_code != 200:
            raise RuntimeError(self.obtener_detalle_error(respuesta))
        return respuesta.json()

    def api_get_liquidaciones_resumen(self, params=None):
        import requests

        respuesta = requests.get(
            f"{self.api_base}/liquidaciones-choferes/resumen",
            params=params or {},
            timeout=90,
        )
        if respuesta.status_code != 200:
            raise RuntimeError(self.obtener_detalle_error(respuesta))
        return respuesta.json()

    def api_descargar_liquidaciones(self, formato, ruta, params=None):
        import requests

        payload = dict(params or {})
        payload["formato"] = formato
        respuesta = requests.get(
            f"{self.api_base}/liquidaciones-choferes/exportar",
            params=payload,
            timeout=120,
        )
        if respuesta.status_code != 200:
            raise RuntimeError(self.obtener_detalle_error(respuesta))
        try:
            with open(ruta, "wb") as archivo:
                archivo.write(respuesta.content)
            return ruta
        except PermissionError:
            base, extension = os.path.splitext(ruta)
            alternativa = f"{base}_nuevo{extension}"
            with open(alternativa, "wb") as archivo:
                archivo.write(respuesta.content)
            return alternativa

    def show_liquidaciones_choferes(self):
        self.clear_content()
        self.highlight_sidebar_button("Liquidaciones Choferes")

        self.liq_filters = {}
        self.liq_widgets = {}
        self.liq_operaciones = []
        self.liq_data = None

        self.create_page_title(
            self.content,
            "Liquidaciones Choferes",
            "Controle viajes, duracion y MT descargadas por empresa, producto y chofer.",
        )

        outer = tk.Frame(self.content, bg=self.colors["bg_main"])
        outer.pack(fill="both", expand=True)
        canvas = tk.Canvas(outer, bg=self.colors["bg_main"], highlightthickness=0)
        scroll_y = ttk.Scrollbar(outer, orient="vertical", command=canvas.yview)
        scroll_x = ttk.Scrollbar(outer, orient="horizontal", command=canvas.xview)
        body = tk.Frame(canvas, bg=self.colors["bg_main"])
        window_id = canvas.create_window((0, 0), window=body, anchor="nw")
        canvas.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        body.bind("<Configure>", lambda _e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfigure(window_id, width=max(e.width, 1220)))
        canvas.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.bind_scroll_canvas(canvas, body, window_id, min_width=1220)

        filters = tk.Frame(body, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
        filters.pack(fill="x", padx=18, pady=(0, 12))

        top = tk.Frame(filters, bg=self.colors["bg_card"])
        top.pack(fill="x", padx=12, pady=12)
        ttk.Button(top, text="Buscar operacion", style="Olive.TButton", command=self.cargar_liquidaciones_filtros).pack(side="left", padx=(0, 8))
        ttk.Button(top, text="Generar liquidacion", style="Olive.TButton", command=self.generar_liquidaciones).pack(side="left", padx=(0, 8))
        ttk.Button(top, text="Limpiar", style="Gray.TButton", command=self.limpiar_liquidaciones).pack(side="left", padx=(0, 8))
        ttk.Button(top, text="Exportar", style="Gray.TButton", command=self.exportar_liquidaciones).pack(side="left", padx=(0, 8))
        self.liq_formato_var = tk.StringVar(value="xlsx")
        ttk.Combobox(top, textvariable=self.liq_formato_var, values=["xlsx", "pdf"], state="readonly", width=7).pack(side="left")

        grid = tk.Frame(filters, bg=self.colors["bg_card"])
        grid.pack(fill="x", padx=12, pady=(0, 12))

        campos = [
            ("operacion", "Operacion", 44),
            ("empresa", "Empresa", 24),
            ("producto", "Producto", 24),
            ("chofer", "Chofer", 30),
            ("placa", "Placa", 18),
            ("guia", "Guia", 18),
            ("fecha_desde", "Desde YYYY-MM-DD", 16),
            ("fecha_hasta", "Hasta YYYY-MM-DD", 16),
        ]
        for idx, (key, label, width) in enumerate(campos):
            row = idx // 4
            col = idx % 4
            box = tk.Frame(grid, bg=self.colors["bg_card"])
            box.grid(row=row, column=col, sticky="ew", padx=6, pady=5)
            tk.Label(
                box,
                text=label,
                font=("Segoe UI", 9, "bold"),
                bg=self.colors["bg_card"],
                fg=_liq_text_fg(self),
            ).pack(anchor="w")
            var = tk.StringVar()
            self.liq_filters[key] = var
            if key in ("fecha_desde", "fecha_hasta"):
                widget = ttk.Entry(box, textvariable=var, width=width)
                widget.pack(fill="x")
            else:
                widget = self.crear_selector_filtrable_despacho(box, var, width=width)
                widget.pack(fill="x")
            self.liq_widgets[key] = widget
        for col in range(4):
            grid.grid_columnconfigure(col, weight=1)

        self.liq_status = tk.Label(
            body,
            text="Presione Buscar operacion para cargar filtros.",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors["bg_card"],
            fg=_liq_text_fg(self),
            anchor="w",
        )
        self.liq_status.pack(fill="x", padx=18, pady=(0, 12), ipady=10)

        self.liq_kpi_frame = tk.Frame(body, bg=self.colors["bg_main"])
        self.liq_kpi_frame.pack(fill="x", padx=18, pady=(0, 10))

        charts = tk.Frame(body, bg=self.colors["bg_main"])
        charts.pack(fill="x", padx=18, pady=(0, 10))
        charts.grid_columnconfigure(0, weight=1, uniform="liq_charts")
        charts.grid_columnconfigure(1, weight=1, uniform="liq_charts")
        charts.grid_rowconfigure(0, weight=1)
        charts.grid_rowconfigure(1, weight=1)
        self.liq_chart_chofer = self._crear_lienzo_liquidacion(charts, "MT por chofer", 0, 0)
        self.liq_chart_empresa = self._crear_lienzo_liquidacion(charts, "MT por empresa", 0, 1)
        self.liq_chart_producto = self._crear_lienzo_liquidacion(charts, "MT por producto", 1, 0, 2)

        table_panel = tk.Frame(body, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
        table_panel.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        tk.Label(
            table_panel,
            text="Detalle de liquidacion",
            font=("Segoe UI", 14, "bold"),
            bg=self.colors["bg_card"],
            fg=_liq_text_fg(self),
        ).pack(anchor="w", padx=12, pady=(10, 4))
        table_wrap = tk.Frame(table_panel, bg=self.colors["bg_card"])
        table_wrap.pack(fill="both", expand=True, padx=12, pady=(0, 12))
        cols = ("guia", "empresa", "producto", "chofer", "placa", "estado", "fecha", "mt", "duracion")
        self.liq_tree = ttk.Treeview(table_wrap, columns=cols, show="headings", height=14)
        self.liq_tree._xtravon_columns = cols
        self.liq_tree._xtravon_filters = {col: tk.StringVar() for col in cols}
        self.liq_tree._xtravon_all_rows = []
        headers = {
            "guia": "Guia", "empresa": "Empresa", "producto": "Producto", "chofer": "Chofer",
            "placa": "Placa", "estado": "Estado", "fecha": "Fecha", "mt": "MT", "duracion": "Min",
        }
        for col in cols:
            self.liq_tree.heading(
                col,
                text=f"{headers[col]} ▼",
                command=lambda c=col: self.abrir_filtro_columna_despacho(self.liq_tree, c),
            )
            self.liq_tree.column(col, width=135, anchor="center")
        sy = ttk.Scrollbar(table_wrap, orient="vertical", command=self.liq_tree.yview)
        sx = ttk.Scrollbar(table_wrap, orient="horizontal", command=self.liq_tree.xview)
        self.liq_tree.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        self.liq_tree.grid(row=0, column=0, sticky="nsew")
        sy.grid(row=0, column=1, sticky="ns")
        sx.grid(row=1, column=0, sticky="ew")
        table_wrap.grid_rowconfigure(0, weight=1)
        table_wrap.grid_columnconfigure(0, weight=1)

    def _crear_lienzo_liquidacion(self, parent, titulo, row=0, column=0, columnspan=1):
        panel = tk.Frame(parent, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
        panel.grid(row=row, column=column, columnspan=columnspan, sticky="nsew", padx=5, pady=5)
        tk.Label(
            panel,
            text=titulo,
            font=("Segoe UI", 12, "bold"),
            bg=self.colors["bg_card"],
            fg=_liq_text_fg(self),
        ).pack(anchor="w", padx=10, pady=(8, 0))
        canvas = tk.Canvas(panel, bg=self.colors["bg_card"], height=230, highlightthickness=0)
        canvas.pack(fill="both", expand=True, padx=10, pady=10)
        return canvas

    def obtener_params_liquidaciones(self):
        params = {}
        operacion_val = self.liq_filters.get("operacion", tk.StringVar()).get().strip()
        if operacion_val:
            try:
                params["operacion_id"] = int(operacion_val.split("|")[0].strip())
            except Exception:
                pass
        if not params.get("operacion_id"):
            activa = getattr(self, "operacion_activa", None)
            if not activa:
                try:
                    activa = self.api_get_operacion_activa()
                    self.operacion_activa = activa
                except Exception:
                    activa = None
            if activa and activa.get("id"):
                params["operacion_id"] = int(activa.get("id"))
                if hasattr(self, "liq_filters") and not self.liq_filters["operacion"].get().strip():
                    etiqueta = (
                        f"{activa.get('id')} | {activa.get('buque') or activa.get('nombre_buque') or ''} | "
                        f"{activa.get('fecha_inicio') or activa.get('fecha') or ''} | {activa.get('estado') or ''}"
                    )
                    self.liq_filters["operacion"].set(etiqueta)
        for key in ("empresa", "producto", "chofer", "placa", "guia", "fecha_desde", "fecha_hasta"):
            value = self.liq_filters.get(key, tk.StringVar()).get().strip()
            if value:
                params[key] = value
        return params

    def cargar_liquidaciones_filtros(self):
        def tarea():
            return self.api_get_liquidaciones_filtros(self.obtener_params_liquidaciones())

        def ok(data):
            self.liq_operaciones = data.get("operaciones", [])
            operaciones = [item.get("label", "") for item in self.liq_operaciones]
            opciones = data.get("opciones", {})
            self.configurar_combo_filtrable_despacho(self.liq_widgets["operacion"], operaciones, self.liq_filters["operacion"])
            for key, source in {
                "empresa": "empresas",
                "producto": "productos",
                "chofer": "choferes",
                "placa": "placas",
                "guia": "guias",
            }.items():
                self.configurar_combo_filtrable_despacho(self.liq_widgets[key], opciones.get(source, []), self.liq_filters[key])
            if not self.liq_filters["operacion"].get() and data.get("operacion"):
                op_id = data["operacion"].get("id")
                for label in operaciones:
                    if label.startswith(f"{op_id} |"):
                        self.liq_filters["operacion"].set(label)
                        break
                if not self.liq_filters["operacion"].get():
                    op = data.get("operacion") or {}
                    self.liq_filters["operacion"].set(
                        f"{op.get('id')} | {op.get('nombre_buque') or op.get('buque') or ''} | {op.get('fecha_inicio') or ''} | {op.get('estado') or ''}"
                    )
            total_guias = len(opciones.get("guias", []))
            total_choferes = len(opciones.get("choferes", []))
            self.liq_status.configure(
                text=f"Filtros cargados: {len(operaciones)} operacion(es), {total_guias} guia(s), {total_choferes} chofer(es). Presione Generar liquidacion."
            )

        self.ejecutar_en_segundo_plano("Liquidaciones", "Cargando filtros...", tarea, ok)

    def generar_liquidaciones(self):
        def tarea():
            return self.api_get_liquidaciones_resumen(self.obtener_params_liquidaciones())

        def ok(data):
            self.liq_data = data
            op = data.get("operacion") or {}
            self.liq_status.configure(text=f"Liquidacion generada para {op.get('nombre_buque', '')}.")
            self.render_liquidaciones(data)

        self.ejecutar_en_segundo_plano("Liquidaciones", "Generando liquidacion...", tarea, ok)

    def limpiar_liquidaciones(self):
        for var in self.liq_filters.values():
            var.set("")
        self.liq_data = None
        self.render_liquidaciones({"kpis": {}, "detalle": [], "por_chofer": [], "por_empresa": [], "por_producto": []})
        self.liq_status.configure(text="Filtros limpios.")

    def render_liquidaciones(self, data):
        for widget in self.liq_kpi_frame.winfo_children():
            widget.destroy()
        k = data.get("kpis", {}) or {}
        cards = [
            ("Guias asignadas", k.get("guias_asignadas", 0), "accent"),
            ("Completadas", k.get("guias_completadas", 0), "success"),
            ("Pendientes", k.get("guias_pendientes", 0), "warning"),
            ("MT descargadas", self.formatear_numero(k.get("mt_cargadas", 0), 2), "success"),
            ("Duracion total", f"{self.formatear_numero(k.get('duracion_total_min', 0), 2)} min", "info"),
            ("Promedio viaje", f"{self.formatear_numero(k.get('duracion_promedio_min', 0), 2)} min", "info"),
            ("Choferes", k.get("choferes", 0), "accent"),
            ("Empresas", k.get("empresas", 0), "accent"),
        ]
        for idx, (title, value, tone) in enumerate(cards):
            card = tk.Frame(self.liq_kpi_frame, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
            card.grid(row=idx // 4, column=idx % 4, sticky="ew", padx=5, pady=5)
            tk.Frame(card, bg=self.colors.get(tone, self.colors["accent"]), height=5).pack(fill="x")
            tk.Label(
                card,
                text=title,
                font=("Segoe UI", 10, "bold"),
                bg=self.colors["bg_card"],
                fg=_liq_text_fg(self),
            ).pack(anchor="w", padx=12, pady=(10, 2))
            tk.Label(
                card,
                text=str(value),
                font=("Segoe UI", 19, "bold"),
                bg=self.colors["bg_card"],
                fg=_liq_text_fg(self),
            ).pack(anchor="w", padx=12, pady=(0, 12))
        for col in range(4):
            self.liq_kpi_frame.grid_columnconfigure(col, weight=1)

        self._dibujar_barras_liquidacion(self.liq_chart_chofer, data.get("por_chofer", []), "chofer")
        self._dibujar_barras_liquidacion(self.liq_chart_empresa, data.get("por_empresa", []), "empresa")
        self._dibujar_barras_liquidacion(self.liq_chart_producto, data.get("por_producto", []), "producto")

        for item in self.liq_tree.get_children():
            self.liq_tree.delete(item)
        for row in data.get("detalle", []):
            self.liq_tree.insert("", "end", values=(
                row.get("guia", ""),
                row.get("empresa", ""),
                row.get("producto", ""),
                row.get("chofer", ""),
                row.get("placa", ""),
                row.get("estado", ""),
                row.get("fecha", ""),
                self.formatear_numero(row.get("mt", 0), 2),
                self.formatear_numero(row.get("duracion_min", 0), 2),
            ))
        self.inicializar_filtros_tabla_despacho(self.liq_tree)

    def _dibujar_barras_liquidacion(self, canvas, data, label_key):
        canvas.delete("all")
        width = max(canvas.winfo_width(), 320)
        chart_height = max(canvas.winfo_height(), 210)
        y = 20
        rows = list(data or [])[:8]
        if not rows:
            canvas.create_text(width / 2, 110, text="Sin datos para mostrar", fill=_liq_muted_fg(self), font=("Segoe UI", 11, "bold"))
            return
        max_value = max([float(item.get("mt") or 0) for item in rows] + [1])
        label_width = min(280, max(130, int(width * 0.36)))
        value_width = 130
        bar_x = label_width + 16
        bar_max = max(60, width - bar_x - value_width - 24)
        row_gap = max(24, min(32, int((chart_height - 34) / max(len(rows), 1))))
        label_limit = max(14, int(label_width / 7))

        def ellipsize(text, limit):
            text = str(text or "SIN DATO").strip() or "SIN DATO"
            if len(text) <= limit:
                return text
            return text[: max(1, limit - 1)].rstrip() + "..."

        for item in rows:
            label = ellipsize(item.get(label_key, "SIN DATO"), label_limit)
            value = float(item.get("mt") or 0)
            bar_w = int(bar_max * (value / max_value)) if max_value else 0
            if value > 0:
                bar_w = max(bar_w, 2)
            value_text = self.formatear_numero(value, 2)
            canvas.create_text(
                8,
                y + 9,
                text=label,
                anchor="w",
                fill=_liq_text_fg(self),
                font=("Segoe UI", 9, "bold"),
            )
            canvas.create_rectangle(
                bar_x,
                y,
                bar_x + bar_w,
                y + 18,
                fill=self.colors["accent"],
                outline="",
            )
            value_x = min(bar_x + bar_w + 8, width - 8)
            anchor = "w" if value_x < width - value_width else "e"
            canvas.create_text(
                value_x,
                y + 9,
                text=value_text,
                anchor=anchor,
                fill=_liq_text_fg(self),
                font=("Segoe UI", 9, "bold"),
            )
            y += row_gap

    def exportar_liquidaciones(self):
        formato = self.liq_formato_var.get() or "xlsx"
        extension = ".pdf" if formato == "pdf" else ".xlsx"
        ruta = filedialog.asksaveasfilename(
            title="Exportar liquidacion",
            defaultextension=extension,
            filetypes=[("PDF", "*.pdf")] if formato == "pdf" else [("Excel", "*.xlsx")],
        )
        if not ruta:
            return

        def tarea():
            return self.api_descargar_liquidaciones(formato, ruta, self.obtener_params_liquidaciones())

        def ok(ruta_final):
            messagebox.showinfo("Liquidacion exportada", f"Archivo generado correctamente:\n{ruta_final}")

        self.ejecutar_en_segundo_plano("Liquidaciones", "Exportando liquidacion...", tarea, ok)

    app_class.api_get_liquidaciones_filtros = api_get_liquidaciones_filtros
    app_class.api_get_liquidaciones_resumen = api_get_liquidaciones_resumen
    app_class.api_descargar_liquidaciones = api_descargar_liquidaciones
    app_class.show_liquidaciones_choferes = show_liquidaciones_choferes
    app_class._crear_lienzo_liquidacion = _crear_lienzo_liquidacion
    app_class.obtener_params_liquidaciones = obtener_params_liquidaciones
    app_class.cargar_liquidaciones_filtros = cargar_liquidaciones_filtros
    app_class.generar_liquidaciones = generar_liquidaciones
    app_class.limpiar_liquidaciones = limpiar_liquidaciones
    app_class.render_liquidaciones = render_liquidaciones
    app_class._dibujar_barras_liquidacion = _dibujar_barras_liquidacion
    app_class.exportar_liquidaciones = exportar_liquidaciones
