import tkinter as tk
from tkinter import ttk

from .lazy import LazyNotebook


def install_roles_permisos_screen(app_class):
    app_class.show_roles_permisos = show_roles_permisos
    app_class.build_roles_usuarios_tab = build_roles_usuarios_tab
    app_class.build_roles_asignacion_tab = build_roles_asignacion_tab
    app_class.render_rbac_catalogo = render_rbac_catalogo
    app_class.toggle_rbac_rol = toggle_rbac_rol
    app_class.marcar_todos_rbac_roles = marcar_todos_rbac_roles
    app_class.limpiar_rbac_roles = limpiar_rbac_roles
    app_class.obtener_rbac_rol_ids = obtener_rbac_rol_ids
    app_class.cargar_rbac_usuario_seleccionado = cargar_rbac_usuario_seleccionado
    app_class.guardar_rbac_asignacion_front = guardar_rbac_asignacion_front


def show_roles_permisos(self):
    self.clear_content()
    self.highlight_sidebar_button("Roles y Permisos")

    self.rbac_catalogo = {"usuarios": [], "roles": [], "permisos": []}
    self.rbac_usuario_var = tk.StringVar()
    self.rbac_rol_var = tk.StringVar()
    self.rbac_nombre_var = tk.StringVar()
    self.rbac_usuario_login_var = tk.StringVar()
    self.rbac_email_var = tk.StringVar()
    self.rbac_nuevo_rol_var = tk.StringVar()
    self.rbac_nuevo_rol_desc_var = tk.StringVar()
    self.rbac_permisos_tree = None
    self.rbac_roles_tree = None
    self.rbac_usuario_combo = None
    self.rbac_roles_checked = set()

    self.create_page_title(
        self.content,
        "Roles y Permisos",
        "Administre usuarios, roles y permisos por modulo.",
    )

    tabs_host = tk.Frame(self.content, bg=self.colors["bg_main"])
    tabs_host.pack(fill="both", expand=True, padx=25, pady=(0, 20))

    self.rbac_tabs = LazyNotebook(tabs_host)
    self.rbac_tabs.pack(fill="both", expand=True)

    usuarios_tab = tk.Frame(self.rbac_tabs.notebook, bg=self.colors["bg_main"])
    asignacion_tab = tk.Frame(self.rbac_tabs.notebook, bg=self.colors["bg_main"])

    self.rbac_tabs.add(usuarios_tab, "Usuarios", lambda frame: self.build_roles_usuarios_tab(frame), build_now=True)
    self.rbac_tabs.add(asignacion_tab, "Asignacion de Accesos", lambda frame: self.build_roles_asignacion_tab(frame))


def build_roles_usuarios_tab(self, parent):
    panel = tk.Frame(parent, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    panel.pack(fill="x", padx=2, pady=8)

    tk.Label(panel, text="Usuario", font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w", padx=14, pady=(12, 6))

    form = tk.Frame(panel, bg=self.colors["bg_card"])
    form.pack(fill="x", padx=14, pady=(0, 10))

    for idx, (var, label) in enumerate([
        (self.rbac_nombre_var, "Nombre"),
        (self.rbac_usuario_login_var, "Usuario"),
        (self.rbac_email_var, "Email"),
    ]):
        box = tk.Frame(form, bg=self.colors["bg_card"])
        box.grid(row=0, column=idx, sticky="ew", padx=5, pady=4)
        tk.Label(box, text=label, font=("Segoe UI", 9, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w")
        ttk.Entry(box, textvariable=var).pack(fill="x")
        form.grid_columnconfigure(idx, weight=1)

    actions = tk.Frame(panel, bg=self.colors["bg_card"])
    actions.pack(fill="x", padx=14, pady=(0, 12))
    ttk.Button(actions, text="Crear/Actualizar usuario", style="Olive.TButton", command=self.crear_rbac_usuario_front).pack(side="left", padx=(0, 8))


def build_roles_asignacion_tab(self, parent):
    panel = tk.Frame(parent, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    panel.pack(fill="both", expand=True, padx=2, pady=8)

    header = tk.Frame(panel, bg=self.colors["bg_card"])
    header.pack(fill="x", padx=14, pady=(12, 6))
    tk.Label(header, text="Asignacion por usuario", font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(side="left")
    ttk.Button(header, text="Cargar catalogo", style="Gray.TButton", command=self.cargar_rbac_catalogo_front).pack(side="right")

    combo_grid = tk.Frame(panel, bg=self.colors["bg_card"])
    combo_grid.pack(fill="x", padx=14, pady=(0, 12))

    usuario_box = tk.Frame(combo_grid, bg=self.colors["bg_card"])
    usuario_box.grid(row=0, column=0, sticky="ew", padx=5)
    tk.Label(usuario_box, text="Usuario", font=("Segoe UI", 9, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w")
    self.rbac_usuario_combo = ttk.Combobox(usuario_box, textvariable=self.rbac_usuario_var, state="readonly")
    self.rbac_usuario_combo.pack(fill="x")
    self.rbac_usuario_combo.bind("<<ComboboxSelected>>", lambda _e: self.limpiar_rbac_roles())

    combo_grid.grid_columnconfigure(0, weight=1)

    roles_panel = tk.Frame(panel, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    roles_panel.pack(fill="both", expand=False, padx=14, pady=(0, 12))
    roles_header = tk.Frame(roles_panel, bg=self.colors["bg_card"])
    roles_header.pack(fill="x", padx=10, pady=(10, 6))
    tk.Label(roles_header, text="Roles disponibles", font=("Segoe UI", 12, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(side="left")
    ttk.Button(roles_header, text="Marcar roles", style="Gray.TButton", command=self.marcar_todos_rbac_roles).pack(side="right", padx=(8, 0))
    ttk.Button(roles_header, text="Limpiar roles", style="Gray.TButton", command=self.limpiar_rbac_roles).pack(side="right")

    roles_table = tk.Frame(roles_panel, bg=self.colors["bg_card"])
    roles_table.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    role_columns = ("check", "id", "nombre", "descripcion")
    self.rbac_roles_tree = ttk.Treeview(roles_table, columns=role_columns, show="headings", height=8, selectmode="browse")
    for col, heading, width in [
        ("check", "", 55),
        ("id", "ID", 60),
        ("nombre", "Rol", 180),
        ("descripcion", "Descripcion", 680),
    ]:
        self.rbac_roles_tree.heading(col, text=heading)
        self.rbac_roles_tree.column(col, width=width, anchor="center" if col != "descripcion" else "w")
    self.rbac_roles_tree.bind("<ButtonRelease-1>", lambda event: self.toggle_rbac_rol(event))
    roles_scroll_y = ttk.Scrollbar(roles_table, orient="vertical", command=self.rbac_roles_tree.yview)
    roles_scroll_x = ttk.Scrollbar(roles_table, orient="horizontal", command=self.rbac_roles_tree.xview)
    self.rbac_roles_tree.configure(yscrollcommand=roles_scroll_y.set, xscrollcommand=roles_scroll_x.set)
    self.rbac_roles_tree.grid(row=0, column=0, sticky="nsew")
    roles_scroll_y.grid(row=0, column=1, sticky="ns")
    roles_scroll_x.grid(row=1, column=0, sticky="ew")
    roles_table.grid_rowconfigure(0, weight=1)
    roles_table.grid_columnconfigure(0, weight=1)

    actions = tk.Frame(panel, bg=self.colors["bg_card"])
    actions.pack(fill="x", padx=14, pady=(0, 8))
    ttk.Button(actions, text="Buscar usuario", style="Gray.TButton", command=self.cargar_rbac_usuario_seleccionado).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Guardar accesos", style="Olive.TButton", command=self.guardar_rbac_asignacion_front).pack(side="left", padx=(0, 8))
    ttk.Button(actions, text="Marcar permisos", style="Gray.TButton", command=self.marcar_todos_rbac_permisos).pack(side="left")

    table_frame = tk.Frame(panel, bg=self.colors["bg_card"])
    table_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))

    columns = ("id", "modulo", "accion", "codigo", "descripcion")
    self.rbac_permisos_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=18, selectmode="extended")

    for col, heading, width in [
        ("id", "ID", 55),
        ("modulo", "Modulo", 170),
        ("accion", "Accion", 120),
        ("codigo", "Codigo", 190),
        ("descripcion", "Descripcion", 420),
    ]:
        self.rbac_permisos_tree.heading(col, text=heading)
        self.rbac_permisos_tree.column(col, width=width, anchor="center" if col != "descripcion" else "w")

    scroll_y = ttk.Scrollbar(table_frame, orient="vertical", command=self.rbac_permisos_tree.yview)
    scroll_x = ttk.Scrollbar(table_frame, orient="horizontal", command=self.rbac_permisos_tree.xview)
    self.rbac_permisos_tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
    self.rbac_permisos_tree.grid(row=0, column=0, sticky="nsew")
    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
    table_frame.grid_rowconfigure(0, weight=1)
    table_frame.grid_columnconfigure(0, weight=1)


def render_rbac_catalogo(self):
    usuarios = self.rbac_catalogo.get("usuarios", [])
    roles = self.rbac_catalogo.get("roles", [])
    permisos = self.rbac_catalogo.get("permisos", [])

    if getattr(self, "rbac_usuario_combo", None) is not None:
        self.rbac_usuario_combo["values"] = [f"{u['id']} | {u['nombre']} ({u['usuario']})" for u in usuarios]

    roles_tree = getattr(self, "rbac_roles_tree", None)
    if roles_tree is not None:
        for item in roles_tree.get_children():
            roles_tree.delete(item)
        for rol in roles:
            rol_id = rol.get("id")
            roles_tree.insert(
                "",
                "end",
                iid=f"rol_{rol_id}",
                values=(
                    "[x]" if rol_id in self.rbac_roles_checked else "[ ]",
                    rol_id,
                    rol.get("nombre", ""),
                    rol.get("descripcion", ""),
                ),
            )

    tree = getattr(self, "rbac_permisos_tree", None)
    if tree is None:
        return

    for item in tree.get_children():
        tree.delete(item)

    for permiso in permisos:
        tree.insert(
            "",
            "end",
            values=(
                permiso.get("id", ""),
                permiso.get("modulo", ""),
                permiso.get("accion", ""),
                permiso.get("codigo", ""),
                permiso.get("descripcion", ""),
            ),
        )


def toggle_rbac_rol(self, event=None):
    tree = getattr(self, "rbac_roles_tree", None)
    if tree is None:
        return
    item = tree.identify_row(event.y) if event is not None else tree.focus()
    if not item:
        return
    valores = tree.item(item, "values")
    if not valores:
        return
    rol_id = self.safe_int(valores[1], None)
    if not rol_id:
        return
    if rol_id in self.rbac_roles_checked:
        self.rbac_roles_checked.remove(rol_id)
        valores = ("[ ]", *valores[1:])
    else:
        self.rbac_roles_checked.add(rol_id)
        valores = ("[x]", *valores[1:])
    tree.item(item, values=valores)


def marcar_todos_rbac_roles(self):
    tree = getattr(self, "rbac_roles_tree", None)
    if tree is None:
        return
    self.rbac_roles_checked = set()
    for item in tree.get_children():
        valores = tree.item(item, "values")
        rol_id = self.safe_int(valores[1], None) if valores else None
        if rol_id:
            self.rbac_roles_checked.add(rol_id)
            tree.item(item, values=("[x]", *valores[1:]))


def limpiar_rbac_roles(self):
    tree = getattr(self, "rbac_roles_tree", None)
    if tree is None:
        return
    self.rbac_roles_checked = set()
    for item in tree.get_children():
        valores = tree.item(item, "values")
        if valores:
            tree.item(item, values=("[ ]", *valores[1:]))


def obtener_rbac_rol_ids(self):
    return sorted(getattr(self, "rbac_roles_checked", set()))


def cargar_rbac_usuario_seleccionado(self):
    usuario_id = self.extraer_id_combo(self.rbac_usuario_var.get())
    if not usuario_id:
        return
    try:
        data = self.api_get_rbac_usuario(usuario_id)
        roles = data.get("roles", [])
        permisos = data.get("permisos", [])
        self.rbac_roles_checked = {r.get("id") for r in roles if r.get("id")}
        self.render_rbac_catalogo()

        permiso_ids = {p.get("id") for p in permisos}
        tree = getattr(self, "rbac_permisos_tree", None)
        if tree is not None:
            tree.selection_remove(tree.selection())
            for item in tree.get_children():
                valores = tree.item(item, "values")
                if valores and self.safe_int(valores[0], None) in permiso_ids:
                    tree.selection_add(item)
    except Exception as e:
        from tkinter import messagebox
        messagebox.showerror("Error usuario", str(e))


def guardar_rbac_asignacion_front(self):
    from tkinter import messagebox

    usuario_id = self.extraer_id_combo(self.rbac_usuario_var.get())
    if not usuario_id:
        messagebox.showwarning("Usuario requerido", "Debe seleccionar un usuario.")
        return

    rol_ids = self.obtener_rbac_rol_ids()
    if not rol_ids:
        messagebox.showwarning("Roles requeridos", "Debe marcar al menos un rol.")
        return

    permiso_ids = self.obtener_rbac_permiso_ids()
    if not permiso_ids:
        messagebox.showwarning("Permisos requeridos", "Debe seleccionar al menos un permiso.")
        return

    try:
        self.api_asignar_rbac({
            "usuario_id": usuario_id,
            "rol_ids": rol_ids,
            "permiso_ids": permiso_ids,
        })
        messagebox.showinfo("Accesos guardados", "Roles y permisos asignados correctamente.")
    except Exception as e:
        messagebox.showerror("Error permisos", str(e))
