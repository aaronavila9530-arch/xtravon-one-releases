import tkinter as tk
from tkinter import messagebox, ttk
import subprocess
import threading
import unicodedata
import base64
import difflib
import os
import random
import re
import shutil
import time
import webbrowser


def install_ia_ejecutiva_screen(app_class):
    app_class.show_ia_ejecutiva = show_ia_ejecutiva
    app_class.api_get_ai_estado = api_get_ai_estado
    app_class.api_get_ai_operacion = api_get_ai_operacion
    app_class.api_chat_ai_operacion = api_chat_ai_operacion
    app_class.api_maritime_chat = api_maritime_chat
    app_class.ia_cargar_operaciones = ia_cargar_operaciones
    app_class.ia_generar = ia_generar
    app_class.ia_preguntar = ia_preguntar
    app_class.ia_abrir_mapa_meteo = ia_abrir_mapa_meteo
    app_class.ia_escuchar_portia = ia_escuchar_portia
    app_class.ia_leer_resultado = ia_leer_resultado
    app_class.ia_detener_voz = ia_detener_voz
    app_class.ia_silenciar_portia = ia_silenciar_portia
    app_class.ia_iniciar_escucha_continua = ia_iniciar_escucha_continua
    app_class.ia_detener_escucha_continua = ia_detener_escucha_continua
    app_class.ia_toggle_escucha_continua = ia_toggle_escucha_continua


def show_ia_ejecutiva(self):
    self.clear_content()
    self.highlight_sidebar_button("P.O.R.T.I.A")
    self.ia_operaciones_cache = []
    self.ia_operacion_var = tk.StringVar()
    self.ia_tipo_var = tk.StringVar(value="Resumen ejecutivo")
    self.ia_chat_var = tk.StringVar()
    self.ia_modo_var = tk.StringVar(value="Ejecutivo")
    self.ia_consulta_rapida_var = tk.StringVar(value="Briefing")
    self.ia_accion_voz_var = tk.StringVar(value="Leer respuesta")
    self.ia_buscar_web_var = tk.BooleanVar(value=False)
    self.ia_leer_respuesta_var = tk.BooleanVar(value=False)
    self.ia_mapa_url = None
    self.ia_voz_proceso = None
    self.ia_escucha_continua_activa = True
    self.ia_escucha_continua_thread = None
    self.ia_escucha_ocupada = False
    self.ia_estado_conversacion = "DORMIDA"
    self.ia_responder_por_voz = False
    self.ia_memoria = getattr(self, "ia_memoria", {})

    self.create_page_title(
        self.content,
        "P.O.R.T.I.A",
        "Port Operations & Risk Tactical Intelligence Assistant",
    )

    wrapper = tk.Frame(self.content, bg=self.colors["bg_main"])
    wrapper.pack(fill="both", expand=True, padx=25, pady=(0, 20))

    top = tk.Frame(wrapper, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    top.pack(fill="x", pady=(0, 12))

    tk.Label(top, text="Analisis de operacion", font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w", padx=14, pady=(12, 6))

    controls = tk.Frame(top, bg=self.colors["bg_card"])
    controls.pack(fill="x", padx=14, pady=(0, 12))
    ttk.Button(controls, text="Cargar operaciones", style="Gray.TButton", command=self.ia_cargar_operaciones).pack(side="left", padx=(0, 8))
    self.ia_operacion_combo = ttk.Combobox(controls, textvariable=self.ia_operacion_var, state="readonly", width=46)
    self.ia_operacion_combo.pack(side="left", padx=(0, 8))
    ttk.Combobox(
        controls,
        textvariable=self.ia_tipo_var,
        state="readonly",
        values=["Resumen ejecutivo", "SOF", "Riesgos operativos", "Tiempo estimado"],
        width=20,
    ).pack(side="left", padx=(0, 8))
    ttk.Button(controls, text="Generar analisis", style="Olive.TButton", command=self.ia_generar).pack(side="left")

    chat_panel = tk.Frame(wrapper, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    chat_panel.pack(fill="x", pady=(0, 12))
    tk.Label(
        chat_panel,
        text="Chat sobre la operacion",
        font=("Segoe UI", 13, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors["text_dark"],
    ).pack(anchor="w", padx=14, pady=(12, 4))
    tk.Label(
        chat_panel,
        text="Diga Portia, Oye Portia, Hola Portia o Portia estas ahi. No es necesario deletrear P.O.R.T.I.A.",
        font=("Segoe UI", 9),
        bg=self.colors["bg_card"],
        fg=self.colors["text_aux"],
    ).pack(anchor="w", padx=14, pady=(0, 6))
    chat_options = tk.Frame(chat_panel, bg=self.colors["bg_card"])
    chat_options.pack(fill="x", padx=14, pady=(0, 6))
    tk.Label(chat_options, text="Modo", font=("Segoe UI", 9, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(side="left", padx=(0, 6))
    ttk.Combobox(
        chat_options,
        textvariable=self.ia_modo_var,
        state="readonly",
        values=["Ejecutivo", "Operativo", "Reclamos", "Cliente", "Planificador"],
        width=16,
    ).pack(side="left", padx=(0, 12))
    ttk.Checkbutton(
        chat_options,
        text="Buscar web pública",
        variable=self.ia_buscar_web_var,
    ).pack(side="left")
    ttk.Checkbutton(
        chat_options,
        text="Leer respuesta",
        variable=self.ia_leer_respuesta_var,
    ).pack(side="left", padx=(12, 0))

    self.ia_consultas_rapidas = {
        "Briefing": "Portia, dame briefing ejecutivo de la operacion activa.",
        "Riesgos de hoy": "Aparentemente, cuales son los riesgos principales de esta operacion hoy?",
        "Tiempo de cierre": "Cuanto falta para terminar la operacion y que podria atrasarla?",
        "Cliente atrasado": "Que cliente va mas atrasado contra su cuota y cuanto le falta descargar?",
        "Bodega critica": "Que bodega requiere mayor atencion y por que?",
        "Clima puerto": "Como esta el clima y mar hoy en Puerto Caldera, Costa Rica?",
    }

    def usar_consulta_rapida():
        pregunta = self.ia_consultas_rapidas.get(self.ia_consulta_rapida_var.get())
        if pregunta:
            self.ia_chat_var.set(pregunta)

    quick_panel = tk.Frame(chat_panel, bg=self.colors["bg_card"])
    quick_panel.pack(fill="x", padx=14, pady=(0, 6))
    tk.Label(
        quick_panel,
        text="Consulta rapida",
        font=("Segoe UI", 9, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors["text_dark"],
    ).pack(side="left", padx=(0, 6))
    ttk.Combobox(
        quick_panel,
        textvariable=self.ia_consulta_rapida_var,
        state="readonly",
        values=list(self.ia_consultas_rapidas.keys()),
        width=24,
    ).pack(side="left", padx=(0, 8))
    ttk.Button(quick_panel, text="Usar", style="Gray.TButton", command=usar_consulta_rapida).pack(side="left")

    voice_panel = tk.Frame(chat_panel, bg=self.colors["bg_card"])
    voice_panel.pack(fill="x", padx=14, pady=(0, 8))
    self.ia_escucha_status_var = tk.StringVar(value="DORMIDA: diga Hey Portia, Hola Portia u Oye Portia para activar.")
    tk.Label(
        voice_panel,
        textvariable=self.ia_escucha_status_var,
        font=("Segoe UI", 9, "bold"),
        bg=self.colors["bg_card"],
        fg=self.colors["success"],
    ).pack(side="left", fill="x", expand=True)
    self.ia_escucha_toggle_btn = ttk.Button(
        voice_panel,
        text="Pausar escucha",
        style="Gray.TButton",
        command=self.ia_toggle_escucha_continua,
    )
    self.ia_escucha_toggle_btn.pack(side="right")
    self.ia_ultimo_audio_var = tk.StringVar(value="Ultimo audio detectado: -")
    tk.Label(
        chat_panel,
        textvariable=self.ia_ultimo_audio_var,
        font=("Segoe UI", 8),
        bg=self.colors["bg_card"],
        fg=self.colors["text_aux"],
    ).pack(anchor="w", padx=14, pady=(0, 8))

    chat_controls = tk.Frame(chat_panel, bg=self.colors["bg_card"])
    chat_controls.pack(fill="x", padx=14, pady=(0, 12))

    def ejecutar_accion_voz():
        accion = self.ia_accion_voz_var.get()
        if accion == "Leer respuesta":
            self.ia_leer_resultado()
        elif accion == "Detener voz":
            self.ia_detener_voz()
        elif accion == "Dormir":
            self.ia_silenciar_portia()

    ttk.Entry(chat_controls, textvariable=self.ia_chat_var).pack(side="left", fill="x", expand=True, padx=(0, 8))
    ttk.Button(chat_controls, text="Escuchar", style="Gray.TButton", command=self.ia_escuchar_portia).pack(side="left", padx=(0, 8))
    ttk.Button(chat_controls, text="Preguntar", style="Olive.TButton", command=self.ia_preguntar).pack(side="left")
    ttk.Combobox(
        chat_controls,
        textvariable=self.ia_accion_voz_var,
        state="readonly",
        values=["Leer respuesta", "Detener voz", "Dormir"],
        width=14,
    ).pack(side="left", padx=(8, 0))
    ttk.Button(chat_controls, text="Ejecutar", style="Gray.TButton", command=ejecutar_accion_voz).pack(side="left", padx=(6, 0))
    self.ia_mapa_btn = ttk.Button(chat_controls, text="Mapa", style="Gray.TButton", command=self.ia_abrir_mapa_meteo)
    self.ia_mapa_btn.pack(side="left", padx=(8, 0))
    self.ia_mapa_btn.configure(state="disabled")

    result_panel = tk.Frame(wrapper, bg=self.colors["bg_card"], highlightbackground=self.colors["border"], highlightthickness=1)
    result_panel.pack(fill="both", expand=True)
    tk.Label(result_panel, text="Resultado IA", font=("Segoe UI", 13, "bold"), bg=self.colors["bg_card"], fg=self.colors["text_dark"]).pack(anchor="w", padx=14, pady=(12, 6))
    text_frame = tk.Frame(result_panel, bg=self.colors["bg_card"])
    text_frame.pack(fill="both", expand=True, padx=14, pady=(0, 14))
    self.ia_resultado_text = tk.Text(
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
    y = ttk.Scrollbar(text_frame, orient="vertical", command=self.ia_resultado_text.yview)
    x = ttk.Scrollbar(text_frame, orient="horizontal", command=self.ia_resultado_text.xview)
    self.ia_resultado_text.configure(yscrollcommand=y.set, xscrollcommand=x.set)
    self.ia_resultado_text.grid(row=0, column=0, sticky="nsew")
    y.grid(row=0, column=1, sticky="ns")
    x.grid(row=1, column=0, sticky="ew")
    text_frame.grid_rowconfigure(0, weight=1)
    text_frame.grid_columnconfigure(0, weight=1)

    self.ia_resultado_text.insert(
        "1.0",
        "Presione Cargar operaciones para consultar el backend.\n"
        "P.O.R.T.I.A no consulta datos automaticamente al abrir esta pantalla.\n\n"
        "Uso recomendado:\n"
        "- Cargar operaciones: llena el selector sin analizar nada automaticamente.\n"
        "- Generar analisis: produce resumen, SOF, riesgos o tiempo estimado de la operacion seleccionada.\n"
        "- Preguntar: chat libre sobre la operacion, clima/mar, calado de puerto o ubicacion AIS.\n"
        "- Buscar web publica: amplifica consultas externas cuando no hay dato interno suficiente.\n",
    )
    self.after(800, self.ia_iniciar_escucha_continua)


PORTIA_WAKE_PATTERNS = (
    "oye portia",
    "oye p o r t i a",
    "oye porshia",
    "oye porcha",
    "oye porcia",
    "oye porzia",
    "oye portsha",
    "hey portia",
    "hey porshia",
    "hey porcha",
    "hey porcia",
    "hey porzia",
    "hey portsha",
    "hey p o r t i a",
    "hola portia",
    "hola porshia",
    "hola porcha",
    "hola porcia",
    "hola porzia",
    "hola portsha",
    "ola portia",
    "ola porshia",
    "ola porcha",
    "portia",
    "porthia",
    "portchia",
    "porshia",
    "porsha",
    "porcha",
    "porchia",
    "porsche",
    "porshe",
    "porscha",
    "porsh",
    "portion",
    "portilla",
    "porter",
    "porta",
    "porti",
    "porcia",
    "porzia",
    "portsha",
    "portya",
    "pourtia",
    "por tia",
    "hello portia",
    "hello porshia",
    "hello porcha",
    "hi portia",
    "hi porshia",
    "are you there portia",
    "are you there porshia",
    "estas ahi portia",
    "estas ahi porshia",
    "estas ahi porcha",
    "estas alli portia",
    "portia estas ahi",
    "porshia estas ahi",
)


def _powershell_exe():
    candidates = [
        os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "WindowsPowerShell", "v1.0", "powershell.exe"),
        os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "SysWOW64", "WindowsPowerShell", "v1.0", "powershell.exe"),
        shutil.which("powershell.exe"),
        shutil.which("powershell"),
        shutil.which("pwsh.exe"),
        shutil.which("pwsh"),
    ]
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            return candidate
    raise RuntimeError("No se encontro PowerShell en Windows para activar voz.")


def _normalizar_voz(texto):
    base = unicodedata.normalize("NFKD", texto or "")
    base = "".join(ch for ch in base if not unicodedata.combining(ch))
    return " ".join(base.lower().strip().split())


def _limpiar_comando_portia(texto):
    original = (texto or "").strip()
    normalizado = _normalizar_voz(original)
    for patron in PORTIA_WAKE_PATTERNS:
        patron_norm = _normalizar_voz(patron)
        if normalizado == patron_norm:
            return ""
        if normalizado.startswith(patron_norm + " "):
            palabras_patron = patron_norm.split()
            palabras_original = original.split()
            return " ".join(palabras_original[len(palabras_patron):]).strip()
    return original


def _tiene_wake_word_portia(texto):
    normalizado = _normalizar_voz(texto)
    if any(
        normalizado == _normalizar_voz(patron) or normalizado.startswith(_normalizar_voz(patron) + " ")
        for patron in PORTIA_WAKE_PATTERNS
    ):
        return True

    tokens = normalizado.replace(".", " ").replace(",", " ").split()
    if not tokens:
        return False

    objetivos = (
        "portia", "porshia", "porsha", "porcha", "porcia", "porzia",
        "porsche", "porshe", "porscha", "portsha", "portchia", "portilla",
        "porter", "porta", "porti", "pourtia",
    )

    for token in tokens[:4]:
        if len(token) < 4:
            continue
        if any(difflib.SequenceMatcher(None, token, objetivo).ratio() >= 0.68 for objetivo in objetivos):
            return True

    for idx in range(min(len(tokens) - 1, 3)):
        bigrama = f"{tokens[idx]} {tokens[idx + 1]}"
        if bigrama in ("por tia", "por tía", "p o", "p o r"):
            return True
        unido = f"{tokens[idx]}{tokens[idx + 1]}"
        if any(difflib.SequenceMatcher(None, unido, objetivo).ratio() >= 0.70 for objetivo in objetivos):
            return True

    return False


def _es_comando_silencio(texto):
    normalizado = _normalizar_voz(texto)
    comandos = (
        "detente",
        "stop",
        "mute",
        "quiet",
        "deja de hablar",
        "no hables",
        "deten la voz",
        "detener voz",
        "es todo",
        "eso es todo",
        "ya es todo",
        "es todo portia",
        "eso es todo portia",
        "gracias portia",
        "gracias porshia",
    )
    return any(comando in normalizado for comando in comandos)


def _parece_pregunta_o_comando(texto):
    normalizado = _normalizar_voz(texto)
    if not normalizado:
        return False
    palabras = normalizado.split()
    detonantes = (
        "cual", "cuanto", "cuando", "donde", "como", "que", "quien",
        "clima", "riesgo", "riesgos", "buque", "barco", "bodega",
        "cliente", "cuota", "descarga", "descargado", "pendiente",
        "calado", "puerto", "mar", "ola", "oleaje", "viento",
        "terminar", "finalizar", "ubicacion", "posicion", "sof",
    )
    if any(word in normalizado for word in detonantes):
        return True
    return len(palabras) >= 7


PORTIA_WAKE_PREFIXES = ("hey", "ey", "e", "8", "hola", "ola", "oye", "hello", "hi")
PORTIA_ACKS = (
    "Te escucho. Que necesita?",
    "Estoy a la orden. Digame.",
    "Aqui estoy. Como le ayudo?",
    "Le escucho. Indiqueme la consulta.",
    "A la orden. Que revisamos?",
)
PORTIA_NAMES = (
    "portia", "porshia", "porsha", "porcha", "porchia", "porcia", "porzia",
    "portsha", "portchia", "portya", "pourtia", "porsche", "porshe", "porscha",
    "porti", "portii", "portiiia", "porta", "porter", "portion",
    "porshya", "porchya", "pordia", "portiya", "portea", "pordea",
    "portiia", "portita", "porsita", "porchita",
)
PORTIA_DIRECT_WAKE_PHRASES = (
    "estas ahi portia",
    "estas ahi porshia",
    "estas ahi porcha",
    "estas alli portia",
    "portia estas ahi",
    "porshia estas ahi",
    "portia me escuchas",
    "porshia me escuchas",
    "portia puedes ayudarme",
    "porshia puedes ayudarme",
    "portia necesito ayuda",
    "porshia necesito ayuda",
    "are you there portia",
    "are you there porshia",
)


def _token_es_nombre_portia(token):
    token = _normalizar_voz(token)
    if token in PORTIA_NAMES:
        return True
    if len(token) < 5:
        return False
    return any(difflib.SequenceMatcher(None, token, objetivo).ratio() >= 0.84 for objetivo in PORTIA_NAMES)


def _compactar_voz(texto):
    return re.sub(r"[^a-z0-9]", "", _normalizar_voz(texto))


def _compacto_contiene_portia(texto):
    compacto = _compactar_voz(texto)
    variantes = (
        "portia", "porshia", "porsia", "porcia", "porzia", "porcha", "porchia",
        "portcha", "portchia", "portsha", "porsche", "porshe", "pordia",
        "portiya", "porti", "porta", "portea", "pordea", "portiia",
        "portita", "porsita", "porchita",
    )
    return bool(compacto) and any(variante in compacto for variante in variantes)


def _portia_ack():
    return random.choice(PORTIA_ACKS)


def _tokens_contienen_nombre_portia(tokens):
    for idx, token in enumerate(tokens):
        if _token_es_nombre_portia(token):
            return True
        if idx < len(tokens) - 1 and f"{tokens[idx]} {tokens[idx + 1]}" in (
            "por tia", "por dia", "por chia", "por sha", "por shea", "por sia", "por cia",
        ):
            return True
        if idx < len(tokens) - 2 and tokens[idx] == "por" and tokens[idx + 1] == "ti" and tokens[idx + 2] in ("a", "ah"):
            return True
        if idx < len(tokens) - 5 and tokens[idx:idx + 6] == ["p", "o", "r", "t", "i", "a"]:
            return True
    return False


def _fin_nombre_portia(tokens, inicio=0):
    if inicio >= len(tokens):
        return -1
    token = tokens[inicio]
    if _token_es_nombre_portia(token):
        return inicio + 1
    if inicio < len(tokens) - 1 and f"{tokens[inicio]} {tokens[inicio + 1]}" in (
        "por tia", "por dia", "por chia", "por sha", "por shea", "por sia", "por cia",
    ):
        return inicio + 2
    if inicio < len(tokens) - 2 and token == "por" and tokens[inicio + 1] == "ti" and tokens[inicio + 2] in ("a", "ah"):
        return inicio + 3
    if inicio < len(tokens) - 5 and tokens[inicio:inicio + 6] == ["p", "o", "r", "t", "i", "a"]:
        return inicio + 6
    return -1


def _tiene_wake_word_portia(texto):
    normalizado = _normalizar_voz(texto)
    if _compacto_contiene_portia(texto):
        tokens_tmp = normalizado.replace(".", " ").replace(",", " ").split()
        if (
            len(tokens_tmp) <= 3
            or (tokens_tmp and tokens_tmp[0] in PORTIA_WAKE_PREFIXES)
            or _parece_pregunta_o_comando(normalizado)
        ):
            return True
    if any(normalizado == frase or normalizado.startswith(frase + " ") for frase in PORTIA_DIRECT_WAKE_PHRASES):
        return True

    tokens = normalizado.replace(".", " ").replace(",", " ").split()
    if not tokens:
        return False

    if len(tokens) >= 2 and tokens[0] in PORTIA_WAKE_PREFIXES and _tokens_contienen_nombre_portia(tokens[1:6]):
        return True

    if len(tokens) >= 2 and tokens[0] in PORTIA_WAKE_PREFIXES and _compacto_contiene_portia(" ".join(tokens[1:6])):
        return True

    if tokens[0] == "p" and len(tokens) >= 6 and tokens[1:6] == ["o", "r", "t", "i", "a"]:
        return True

    if _tokens_contienen_nombre_portia(tokens[:6]) and any(
        frase in normalizado for frase in (
            "estas ahi", "estas alli", "me escuchas", "me oyes", "estas disponible",
            "necesito ayuda", "ayudame", "puedes ayudarme", "puede ayudarme",
        )
    ):
        return True

    if _tokens_contienen_nombre_portia(tokens[:4]) and len(tokens) > 1 and _parece_pregunta_o_comando(" ".join(tokens)):
        return True

    # Algunos motores reconocen "Hey Portia" como un prefijo aislado o incluso
    # como "8". Solo lo aceptamos cuando el resto ya parece una pregunta real.
    if tokens[0] in PORTIA_WAKE_PREFIXES and _parece_pregunta_o_comando(" ".join(tokens[1:])):
        return True

    if _es_comando_silencio(texto) and _tokens_contienen_nombre_portia(tokens):
        return True

    if any(comando in normalizado for comando in ("desconectate", "desconectar", "desactivate", "desactivar", "apagate", "deja de escuchar", "no escuches")) and _tokens_contienen_nombre_portia(tokens):
        return True

    return False


def _extraer_comando_inicial(texto):
    original = (texto or "").strip()
    normalizado = _normalizar_voz(original)
    tokens_norm = normalizado.split()
    tokens_original = original.split()
    if not tokens_norm:
        return ""

    if tokens_norm[0] in PORTIA_WAKE_PREFIXES:
        for idx in range(1, min(len(tokens_norm), 5)):
            fin = _fin_nombre_portia(tokens_norm, idx)
            if fin > idx:
                return " ".join(tokens_original[fin:]).strip()
        if _parece_pregunta_o_comando(" ".join(tokens_norm[1:])):
            return " ".join(tokens_original[1:]).strip()

    for frase in PORTIA_DIRECT_WAKE_PHRASES:
        if normalizado == frase:
            return ""
        if normalizado.startswith(frase + " "):
            return " ".join(tokens_original[len(frase.split()):]).strip()

    for idx, token in enumerate(tokens_norm[:3]):
        fin = _fin_nombre_portia(tokens_norm, idx)
        if fin > idx:
            return " ".join(tokens_original[fin:]).strip()

    return ""


def _es_saludo_portia(texto):
    normalizado = _normalizar_voz(texto)
    if not _tiene_wake_word_portia(texto):
        return False
    if _extraer_comando_inicial(texto):
        return False
    if _tiene_wake_word_portia(texto):
        return True
    saludos = (
        "estas ahi", "me escuchas", "estas disponible", "puedes ayudarme",
        "necesito ayuda", "hola", "ola", "oye", "hey", "hello", "hi",
    )
    return any(saludo in normalizado for saludo in saludos)


def _es_comando_desactivar(texto):
    normalizado = _normalizar_voz(texto)
    if not _tokens_contienen_nombre_portia(normalizado.split()):
        return False
    comandos = (
        "desconectate", "desconectar", "desactivate", "desactivarte", "desactivar", "apagate", "apagar escucha",
        "pausa escucha", "deja de escuchar", "no escuches",
    )
    return any(comando in normalizado for comando in comandos)


def _comando_control_portia(texto):
    if _es_comando_desactivar(texto):
        return "DESACTIVAR"
    if _es_comando_silencio(texto):
        return "DORMIR"
    if _es_saludo_portia(texto):
        return "SALUDO"
    return None


def _resumen_estado_portia(estado):
    estados = {
        "DORMIDA": "DORMIDA: diga Hey Portia, Hola Portia u Oye Portia para activar.",
        "ACTIVA": "ACTIVA: P.O.R.T.I.A esta lista para su pregunta.",
        "ESCUCHANDO": "ESCUCHANDO: termine su pregunta y espere un momento.",
        "PROCESANDO": "PROCESANDO: consultando IA/backend.",
        "HABLANDO": "HABLANDO: diga 'es todo Portia' o 'desconectate Portia'.",
        "PAUSADA": "PAUSADA: escucha continua desactivada. Use Reactivar escucha.",
    }
    return estados.get(estado, estado)


def _ia_set_estado(self, estado, texto=None, activo=True):
    self.ia_estado_conversacion = estado
    _ia_actualizar_estado_escucha(self, texto or _resumen_estado_portia(estado), activo)


def _ia_responder_estado(self, texto, hablar=True):
    if hasattr(self, "ia_resultado_text") and self.ia_resultado_text.winfo_exists():
        self.ia_resultado_text.delete("1.0", "end")
        self.ia_resultado_text.insert("1.0", f"P.O.R.T.I.A: {texto}")
    if hablar:
        threading.Thread(target=lambda: _hablar_breve(texto, timeout=8), daemon=True).start()


def _ia_texto_para_voz(texto, limite=420):
    limpio = re.sub(r"https?://\S+", "", str(texto or ""))
    limpio = re.sub(r"\s+", " ", limpio).strip()
    if not limpio:
        return ""
    if len(limpio) <= limite:
        return limpio
    return limpio[:limite].rsplit(" ", 1)[0].strip() + ". Tengo mas detalle en pantalla si desea ampliar."


def _ia_manejar_control_portia(self, texto):
    control = _comando_control_portia(texto)
    if control == "DESACTIVAR":
        self.ia_detener_voz()
        self.ia_escucha_continua_activa = False
        self.ia_escucha_ocupada = False
        self.ia_responder_por_voz = False
        _ia_set_estado(self, "PAUSADA", "P.O.R.T.I.A desactivada. Use Reactivar escucha para encenderla.", False)
        _ia_responder_estado(self, "Escucha desactivada.", hablar=False)
        return True
    if control == "DORMIR":
        _ia_portia_standby(self)
        return True
    if control == "SALUDO":
        ack = _portia_ack()
        _ia_set_estado(self, "ACTIVA", f"ACTIVA: {ack}", True)
        _ia_responder_estado(self, ack, hablar=True)
        return True
    return False


def _ia_navegar_a(self, pantalla):
    command = getattr(self, "screen_commands", {}).get(pantalla)
    if not command:
        return False
    try:
        self.on_sidebar_click(pantalla, command)
    except Exception:
        command()
    return True


def _ia_pantalla_desde_texto(texto):
    normalizado = _normalizar_voz(texto)
    opciones = (
        ("Centro Ejecutivo", ("centro ejecutivo", "dashboard", "tablero", "control ejecutivo", "gestion ejecutiva")),
        ("Operaciones Buque", ("operaciones buque", "operacion buque", "abrir operacion", "operaciones de buque")),
        ("Carga de Boletas", ("carga de boletas", "boletas", "guias", "cargar boletas", "cargar excel")),
        ("Historial de Buques", ("historial", "historial de buques", "buques cerrados", "operaciones cerradas")),
        ("SOF", ("sof", "statement of facts", "eventos", "issue log", "sucesos")),
        ("Informes", ("informes", "reportes", "reporte")),
        ("P.O.R.T.I.A", ("portia", "p o r t i a", "ia", "asistente")),
        ("Ayuda / Q&A", ("ayuda", "qa", "q&a", "manual", "guia de uso", "como hago")),
        ("Aprobaciones", ("aprobaciones", "aprobar", "pendientes de aprobacion")),
        ("Roles y Permisos", ("roles", "permisos", "usuarios")),
    )
    for pantalla, frases in opciones:
        if any(frase in normalizado for frase in frases):
            return pantalla
    return None


def _ia_set_pregunta_y_consultar(self, pregunta, responder_por_voz=False):
    if hasattr(self, "ia_chat_var"):
        self.ia_chat_var.set(pregunta)
    self.ia_responder_por_voz = responder_por_voz
    self.ia_preguntar()


def _ia_ejecutar_comando_operativo(self, comando, desde_voz=False):
    normalizado = _normalizar_voz(comando)
    if not normalizado:
        return False

    if any(verbo in normalizado for verbo in ("abre", "abrir", "ve a", "ir a", "muestra", "mostrar", "navega")):
        pantalla = _ia_pantalla_desde_texto(normalizado)
        if pantalla:
            _ia_set_estado(self, "PROCESANDO", f"Abriendo {pantalla}.", True)
            _ia_navegar_a(self, pantalla)
            _ia_responder_estado(self, f"Abriendo {pantalla}.", hablar=desde_voz)
            return True

    if "cargar operaciones" in normalizado or "buscar operaciones" in normalizado:
        _ia_set_estado(self, "PROCESANDO", "Cargando operaciones para analisis.", True)
        self.ia_cargar_operaciones()
        return True

    briefing = (
        "briefing", "estado general", "como vamos", "resumen operativo",
        "dame resumen", "dame el resumen", "situacion actual",
    )
    if any(frase in normalizado for frase in briefing):
        _ia_set_pregunta_y_consultar(
            self,
            "Dame un briefing ejecutivo de la operacion activa: avance, clientes atrasados, bodegas criticas, SOF, riesgos, clima si aplica y proximas acciones recomendadas.",
            responder_por_voz=desde_voz,
        )
        return True

    if "riesgo" in normalizado or "alerta" in normalizado:
        _ia_set_pregunta_y_consultar(
            self,
            "Aparentemente, cuales son los riesgos principales de esta operacion hoy y que accion recomiendas?",
            responder_por_voz=desde_voz,
        )
        return True

    if "tiempo" in normalizado and any(palabra in normalizado for palabra in ("cierre", "terminar", "finalizar", "falta")):
        _ia_set_pregunta_y_consultar(
            self,
            "Cuanto falta para terminar la operacion, cual es el tiempo estimado de cierre y que podria atrasarla?",
            responder_por_voz=desde_voz,
        )
        return True

    if "cliente" in normalizado and any(palabra in normalizado for palabra in ("atrasado", "cuota", "pendiente")):
        _ia_set_pregunta_y_consultar(
            self,
            "Que cliente va mas atrasado contra su cuota, cuanto ha descargado, cuanto tiene pendiente y que riesgo representa?",
            responder_por_voz=desde_voz,
        )
        return True

    if "bodega" in normalizado and any(palabra in normalizado for palabra in ("critica", "atrasada", "requiere", "pendiente")):
        _ia_set_pregunta_y_consultar(
            self,
            "Que bodega requiere mayor atencion, cuanto tiene pendiente de descarga y cual es la recomendacion operativa?",
            responder_por_voz=desde_voz,
        )
        return True

    if "sof" in normalizado or "statement" in normalizado or "sucesos" in normalizado:
        _ia_set_pregunta_y_consultar(
            self,
            "Resume el SOF de la operacion: demoras, categorias, duraciones, eventos criticos y puntos para reclamo.",
            responder_por_voz=desde_voz,
        )
        return True

    return False


def _es_comando_silencio(texto):
    normalizado = _normalizar_voz(texto)
    tokens = normalizado.split()
    frases = (
        "detente",
        "stop",
        "mute",
        "quiet",
        "deja de hablar",
        "no hables",
        "deten la voz",
        "detener voz",
        "es todo",
        "eso es todo",
        "ya es todo",
        "es todo portia",
        "eso es todo portia",
        "gracias portia",
        "gracias porshia",
    )
    if any(frase in normalizado for frase in frases):
        return True
    return bool(tokens and tokens[0] == "para" and _tokens_contienen_nombre_portia(tokens))


def _run_powershell(script, timeout=20):
    completed = subprocess.run(
        [_powershell_exe(), "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        capture_output=True,
        text=True,
        timeout=timeout,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )
    if completed.returncode != 0:
        raise RuntimeError((completed.stderr or completed.stdout or "No se pudo ejecutar voz en Windows.").strip())
    return (completed.stdout or "").strip()


def _reconocer_voz_windows():
    script = r"""
Add-Type -AssemblyName System.Speech
$cultures = @("es-ES", "es-MX", "es-US", "en-US")
$engine = $null
foreach ($cultureName in $cultures) {
  try {
    $culture = [System.Globalization.CultureInfo]::GetCultureInfo($cultureName)
    $engine = New-Object System.Speech.Recognition.SpeechRecognitionEngine($culture)
    break
  } catch {}
}
if ($null -eq $engine) {
  $engine = New-Object System.Speech.Recognition.SpeechRecognitionEngine
}
$grammar = New-Object System.Speech.Recognition.DictationGrammar
$engine.LoadGrammar($grammar)
$engine.SetInputToDefaultAudioDevice()
$engine.InitialSilenceTimeout = [TimeSpan]::FromSeconds(8)
$engine.BabbleTimeout = [TimeSpan]::FromSeconds(8)
$engine.EndSilenceTimeout = [TimeSpan]::FromSeconds(1.5)
$result = $engine.Recognize([TimeSpan]::FromSeconds(12))
if ($null -ne $result) { Write-Output $result.Text }
$engine.Dispose()
"""
    return _run_powershell(script, timeout=25)


def _reconocer_voz_python(timeout=8, phrase_time_limit=16, pause_threshold=1.15):
    try:
        import speech_recognition as sr
    except Exception as exc:
        raise RuntimeError(f"SpeechRecognition no esta instalado: {exc}")

    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 250
    recognizer.pause_threshold = pause_threshold
    recognizer.phrase_threshold = 0.35
    recognizer.non_speaking_duration = 0.55

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.35)
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            return ""

    errores = []
    for language in ("es-ES", "es-MX", "es-CR", "en-US"):
        try:
            return recognizer.recognize_google(audio, language=language)
        except sr.UnknownValueError:
            errores.append(f"{language}: no entendio audio")
        except Exception as exc:
            errores.append(f"{language}: {exc}")
    raise RuntimeError("; ".join(errores) or "No se pudo reconocer la voz.")


def _reconocer_voz(timeout=8, phrase_time_limit=16, pause_threshold=1.15):
    try:
        return _reconocer_voz_python(timeout=timeout, phrase_time_limit=phrase_time_limit, pause_threshold=pause_threshold)
    except Exception:
        return _reconocer_voz_windows()


def _crear_proceso_hablar_windows(texto):
    safe_text = (texto or "").replace("'", "''")
    script = f"""
Add-Type -AssemblyName System.Speech
$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speaker.Rate = 0
$speaker.Volume = 100
$speaker.Speak('{safe_text}')
$speaker.Dispose()
"""
    encoded = base64.b64encode(script.encode("utf-16le")).decode("ascii")
    return subprocess.Popen(
        [_powershell_exe(), "-NoProfile", "-ExecutionPolicy", "Bypass", "-EncodedCommand", encoded],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
    )


def _hablar_breve(texto, timeout=8):
    proceso = _crear_proceso_hablar_windows(texto)
    try:
        proceso.wait(timeout=timeout)
    except Exception:
        try:
            proceso.terminate()
        except Exception:
            pass


def api_get_ai_estado(self):
    import requests

    respuesta = requests.get(f"{self.api_base}/ai/estado", timeout=12)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_get_ai_operacion(self, operacion_id, tipo):
    import requests

    endpoint = {
        "Resumen ejecutivo": "resumen-ejecutivo",
        "SOF": "sof",
        "Riesgos operativos": "riesgos",
        "Tiempo estimado": "tiempo-finalizacion",
    }.get(tipo, "resumen-ejecutivo")
    respuesta = requests.get(f"{self.api_base}/ai/operacion/{operacion_id}/{endpoint}", timeout=35)
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_chat_ai_operacion(self, operacion_id, pregunta):
    import requests

    respuesta = requests.post(
        f"{self.api_base}/ai/operacion/{operacion_id}/chat",
        json={"pregunta": pregunta},
        timeout=35,
    )
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    return respuesta.json()


def api_maritime_chat(self, pregunta, operacion_id=None, modo="Ejecutivo", buscar_web=False, pantalla="P.O.R.T.I.A", respuesta_breve=True):
    import requests

    payload = {
        "pregunta": pregunta,
        "modo": modo,
        "buscar_web": bool(buscar_web),
        "pantalla": pantalla,
        "copiloto": True,
        "respuesta_breve": bool(respuesta_breve),
    }
    if operacion_id:
        payload["operacion_id"] = operacion_id
    respuesta = requests.post(
        f"{self.api_base}/ai/maritime-chat",
        json=payload,
        timeout=35,
    )
    if respuesta.status_code != 200:
        raise RuntimeError(self.obtener_detalle_error(respuesta))
    data = respuesta.json()
    return data


def ia_cargar_operaciones(self):
    def tarea():
        operaciones = []
        activa = None

        try:
            activa = self.api_get_operacion_activa()
        except Exception:
            activa = None

        try:
            data_abiertas = self.api_get_operaciones_buque(estado="ABIERTA")
            operaciones.extend(data_abiertas.get("data", []) if isinstance(data_abiertas, dict) else [])
        except Exception:
            pass

        if not operaciones:
            data_todas = self.api_get_operaciones_buque()
            operaciones.extend(data_todas.get("data", []) if isinstance(data_todas, dict) else [])

        if activa:
            activa_id = str(activa.get("id"))
            if not any(str(op.get("id")) == activa_id for op in operaciones):
                operaciones.insert(0, activa)

        deduplicadas = []
        vistos = set()
        for op in operaciones:
            op_id = str(op.get("id"))
            if not op_id or op_id in vistos:
                continue
            vistos.add(op_id)
            deduplicadas.append(op)

        return {"operaciones": deduplicadas, "activa": activa}

    def finalizar(resultado):
        self.ia_operaciones_cache = resultado.get("operaciones", [])
        activa = resultado.get("activa")
        values = [
            f"{op.get('id')} | {op.get('nombre_buque')} | {op.get('fecha_inicio')} | {op.get('estado')}"
            for op in self.ia_operaciones_cache
        ]
        self.ia_operacion_combo["values"] = values
        if values:
            selected_idx = 0
            if activa:
                activa_id = str(activa.get("id"))
                for idx, op in enumerate(self.ia_operaciones_cache):
                    if str(op.get("id")) == activa_id:
                        selected_idx = idx
                        break
            self.ia_operacion_var.set(values[selected_idx])
            seleccionada = self.ia_operaciones_cache[selected_idx]
            self.ia_memoria["operacion_id"] = seleccionada.get("id")
            self.ia_memoria["operacion_label"] = values[selected_idx]
            self.ia_memoria["buque"] = seleccionada.get("nombre_buque")
            self.ia_resultado_text.delete("1.0", "end")
            self.ia_resultado_text.insert("1.0", f"Operaciones cargadas: {len(values)}\nSeleccione una operacion y presione Generar analisis.\n")
        else:
            self.ia_resultado_text.delete("1.0", "end")
            self.ia_resultado_text.insert("1.0", "No se encontraron operaciones para analizar.\n")

    self.ejecutar_en_segundo_plano(
        "P.O.R.T.I.A",
        "Cargando operaciones desde el backend...",
        tarea,
        finalizar,
    )


def _ia_operacion_id(self):
    selected = self.ia_operacion_var.get().strip()
    values = list(self.ia_operacion_combo["values"])
    if not selected or selected not in values:
        messagebox.showwarning("Operacion requerida", "Seleccione una operacion.")
        return None
    idx = values.index(selected)
    return self.ia_operaciones_cache[idx].get("id")


def ia_generar(self):
    operacion_id = _ia_operacion_id(self)
    if not operacion_id:
        return
    tipo = self.ia_tipo_var.get()

    def tarea():
        return self.api_get_ai_operacion(operacion_id, tipo)

    def finalizar(data):
        self.ia_resultado_text.delete("1.0", "end")
        self.ia_resultado_text.insert("1.0", data.get("text", ""))

    self.ejecutar_en_segundo_plano(
        "P.O.R.T.I.A",
        "Generando analisis con IA...",
        tarea,
        finalizar,
    )


def ia_preguntar(self):
    pregunta = self.ia_chat_var.get().strip()
    if not pregunta:
        messagebox.showwarning("Pregunta requerida", "Escriba una pregunta sobre la operacion.")
        return
    if _ia_ejecutar_comando_operativo(self, pregunta, desde_voz=False):
        return
    operacion_id = None
    if hasattr(self, "ia_operacion_var") and hasattr(self, "ia_operacion_combo"):
        selected = self.ia_operacion_var.get().strip()
        values = list(self.ia_operacion_combo["values"])
        if selected and selected in values:
            idx = values.index(selected)
            operacion_id = self.ia_operaciones_cache[idx].get("id")
            self.ia_memoria["operacion_id"] = operacion_id
            self.ia_memoria["operacion_label"] = selected

    if not operacion_id:
        try:
            activa = self.api_get_operacion_activa()
            if activa:
                operacion_id = activa.get("id")
        except Exception:
            operacion_id = None

    _ia_set_estado(self, "PROCESANDO", "PROCESANDO: consultando operacion, clima, SOF o datos externos.", True)

    def tarea():
        return self.api_maritime_chat(
            pregunta,
            operacion_id,
            self.ia_modo_var.get(),
            self.ia_buscar_web_var.get(),
        )

    def finalizar(data):
        if not hasattr(self, "ia_imagenes_cache"):
            self.ia_imagenes_cache = []
        if hasattr(self, "ia_resultado_text") and self.ia_resultado_text.winfo_exists():
            self.ia_resultado_text.delete("1.0", "end")
            self.ia_resultado_text.insert(
                "1.0",
                f"Pregunta: {pregunta}\n\n{data.get('text', '')}",
            )
        self.ia_mapa_url = None
        if hasattr(self, "ia_mapa_btn"):
            self.ia_mapa_btn.configure(text="Abrir mapa", state="disabled")
        interactive_map_url = data.get("interactive_map_url")
        if interactive_map_url:
            self.ia_mapa_url = f"{self.api_base}{interactive_map_url}"
            if hasattr(self, "ia_mapa_btn"):
                label = "Abrir mapa buque" if data.get("interactive_map_type") == "buque" else "Abrir mapa clima"
                self.ia_mapa_btn.configure(text=label, state="normal")
        image_data = data.get("map_image_data")
        if image_data and hasattr(self, "ia_resultado_text") and self.ia_resultado_text.winfo_exists():
            try:
                imagen = tk.PhotoImage(data=image_data, format="png")
                self.ia_imagenes_cache.append(imagen)
                self.ia_resultado_text.insert("end", "\n\n")
                self.ia_resultado_text.image_create("end", image=imagen)
                caption = data.get("map_caption")
                if caption:
                    self.ia_resultado_text.insert("end", f"\n{caption}")
            except Exception:
                pass
        debe_leer = bool(getattr(self, "ia_responder_por_voz", False))
        if getattr(self, "ia_leer_respuesta_var", None) and self.ia_leer_respuesta_var.get():
            debe_leer = True
        self.ia_responder_por_voz = False
        self.ia_escucha_ocupada = False
        if debe_leer:
            _ia_set_estado(self, "HABLANDO", "HABLANDO: leyendo respuesta. Diga 'es todo Portia' o 'desconectate Portia'.", True)
            texto = data.get("text", "")
            if hasattr(self, "ia_resultado_text") and self.ia_resultado_text.winfo_exists():
                self.ia_leer_resultado()
            elif texto:
                self.ia_detener_voz()
                proceso = _crear_proceso_hablar_windows(_ia_texto_para_voz(texto))
                self.ia_voz_proceso = proceso
        else:
            _ia_set_estado(self, "DORMIDA", None, True)
    self.ejecutar_en_segundo_plano(
        "P.O.R.T.I.A",
        "Consultando la operacion con IA...",
        tarea,
        finalizar,
    )


def ia_escuchar_portia(self):
    def tarea():
        texto = _reconocer_voz(timeout=14, phrase_time_limit=30, pause_threshold=2.0)
        comando = _extraer_comando_inicial(texto) if _tiene_wake_word_portia(texto) else texto
        return {"texto": texto, "comando": comando}

    def finalizar(data):
        texto = data.get("texto") or ""
        comando = data.get("comando") or ""
        if not comando and _parece_pregunta_o_comando(texto):
            comando = texto
        if texto:
            _ia_set_ultimo_audio(self, texto)
        if texto and _ia_manejar_control_portia(self, texto):
            return
        if not texto:
            messagebox.showwarning("Sin voz detectada", "No se detecto audio claro. Intente de nuevo cerca del microfono.")
            return
        if not comando:
            self.ia_chat_var.set("")
            self.ia_resultado_text.delete("1.0", "end")
            self.ia_resultado_text.insert(
                "1.0",
                f"Escuche: {texto}\n\nDiga por ejemplo: Hey P.O.R.T.I.A, cuales son los riesgos de hoy?",
            )
            return
        self.ia_chat_var.set(comando)
        self.ia_preguntar()

    self.ejecutar_en_segundo_plano(
        "P.O.R.T.I.A",
        "Escuchando por microfono...",
        tarea,
        finalizar,
    )


def ia_iniciar_escucha_continua(self):
    if getattr(self, "ia_escucha_continua_thread", None) and self.ia_escucha_continua_thread.is_alive():
        return
    self.ia_escucha_continua_activa = True
    self.ia_estado_conversacion = "DORMIDA"

    def worker():
        while getattr(self, "ia_escucha_continua_activa", False):
            if getattr(self, "ia_escucha_ocupada", False):
                time.sleep(0.4)
                continue
            try:
                texto = _reconocer_voz(timeout=3, phrase_time_limit=5, pause_threshold=0.85)
            except Exception as exc:
                detalle = str(exc)
                if "no entendio audio" in detalle or "No se pudo reconocer" in detalle:
                    continue
                self.after(0, lambda e=exc: _ia_actualizar_estado_escucha(self, f"Escucha pausada: {e}", False))
                self.ia_escucha_continua_activa = False
                break

            if not getattr(self, "ia_escucha_continua_activa", False):
                break
            if not texto:
                continue
            if not _tiene_wake_word_portia(texto):
                continue

            self.ia_escucha_ocupada = True
            self.after(0, lambda t=texto: _ia_set_ultimo_audio(self, t))
            control = _comando_control_portia(texto)
            if control in ("DESACTIVAR", "DORMIR"):
                self.after(0, lambda t=texto: _ia_manejar_control_portia(self, t))
                self.ia_escucha_ocupada = False
                continue

            comando_inicial = _extraer_comando_inicial(texto)
            if comando_inicial and _parece_pregunta_o_comando(comando_inicial):
                self.ia_responder_por_voz = True
                self.after(0, lambda t=texto, c=comando_inicial: _ia_procesar_wake_word(self, t, c))
                continue

            self.after(0, lambda t=texto: _ia_mostrar_esperando_comando(self, t))
            try:
                _hablar_breve(_portia_ack())
                self.after(0, lambda: _ia_set_estado(self, "ESCUCHANDO", None, True))
                pregunta = _reconocer_voz(timeout=14, phrase_time_limit=30, pause_threshold=2.0)
            except Exception as exc:
                self.after(0, lambda e=exc: _ia_actualizar_estado_escucha(self, f"No pude escuchar la pregunta: {e}", True))
                self.ia_escucha_ocupada = False
                continue
            self.after(0, lambda t=pregunta: _ia_set_ultimo_audio(self, t))
            if pregunta and _comando_control_portia(pregunta):
                self.after(0, lambda t=pregunta: _ia_manejar_control_portia(self, t))
                self.ia_escucha_ocupada = False
                continue
            comando = pregunta if _parece_pregunta_o_comando(pregunta) else ""
            if not comando:
                self.after(0, lambda t=pregunta: _ia_mostrar_sin_comando(self, t))
                self.ia_escucha_ocupada = False
                continue
            self.ia_responder_por_voz = True
            self.after(0, lambda t=texto, c=comando: _ia_procesar_wake_word(self, t, c))

    self.ia_escucha_continua_thread = threading.Thread(target=worker, daemon=True)
    self.ia_escucha_continua_thread.start()
    _ia_set_estado(self, "DORMIDA", None, True)


def ia_detener_escucha_continua(self):
    self.ia_escucha_continua_activa = False
    _ia_set_estado(self, "PAUSADA", "PAUSADA: escucha continua desactivada. Use Reactivar escucha.", False)


def ia_toggle_escucha_continua(self):
    if getattr(self, "ia_escucha_continua_activa", False):
        self.ia_detener_escucha_continua()
    else:
        self.ia_iniciar_escucha_continua()


def _ia_actualizar_estado_escucha(self, texto, activo):
    if hasattr(self, "ia_escucha_status_var"):
        try:
            self.ia_escucha_status_var.set(texto)
        except Exception:
            pass
    if hasattr(self, "ia_escucha_toggle_btn"):
        try:
            self.ia_escucha_toggle_btn.configure(text="Pausar escucha" if activo else "Reactivar escucha")
        except Exception:
            pass


def _ia_set_ultimo_audio(self, texto):
    if hasattr(self, "ia_ultimo_audio_var"):
        try:
            self.ia_ultimo_audio_var.set(f"Ultimo audio detectado: {texto}")
        except Exception:
            pass


def _ia_mostrar_esperando_comando(self, texto):
    _ia_set_ultimo_audio(self, texto)
    ack = _portia_ack()
    _ia_set_estado(self, "ACTIVA", f"ACTIVA: {ack}", True)
    if hasattr(self, "ia_resultado_text") and self.ia_resultado_text.winfo_exists():
        self.ia_resultado_text.delete("1.0", "end")
        self.ia_resultado_text.insert("1.0", f"Escuche: {texto}\n\nP.O.R.T.I.A: {ack}\n")


def _ia_mostrar_sin_comando(self, texto):
    _ia_set_estado(self, "DORMIDA", "No pude captar una pregunta completa. Diga Hey Portia para intentar de nuevo.", True)
    if hasattr(self, "ia_resultado_text") and self.ia_resultado_text.winfo_exists():
        self.ia_resultado_text.delete("1.0", "end")
        self.ia_resultado_text.insert("1.0", f"Audio posterior: {texto or '-'}\n\nNo pude captar una pregunta completa.")


def _ia_portia_standby(self):
    self.ia_detener_voz()
    self.ia_escucha_ocupada = False
    self.ia_responder_por_voz = False
    _ia_set_estado(self, "DORMIDA", "DORMIDA: P.O.R.T.I.A queda en espera. Diga Hey Portia para reactivar.", True)
    if hasattr(self, "ia_resultado_text") and self.ia_resultado_text.winfo_exists():
        self.ia_resultado_text.delete("1.0", "end")
        self.ia_resultado_text.insert("1.0", "P.O.R.T.I.A en espera.\nDiga Hey Portia para reactivar.")


def _ia_procesar_wake_word(self, texto, comando):
    if getattr(self, "ia_escucha_ocupada", False) and not getattr(self, "ia_responder_por_voz", False):
        return
    if not hasattr(self, "ia_resultado_text") or not self.ia_resultado_text.winfo_exists():
        if hasattr(self, "portia_question_var") and comando:
            try:
                if hasattr(self, "portia_panel_visible") and not self.portia_panel_visible and hasattr(self, "toggle_portia_panel"):
                    self.toggle_portia_panel()
                self.portia_question_var.set(comando)
                if hasattr(self, "portia_status_var"):
                    self.portia_status_var.set(f"P.O.R.T.I.A: {_portia_ack()} Procesando: {comando}")
                threading.Thread(target=lambda: _hablar_breve(_portia_ack(), timeout=5), daemon=True).start()
                self.portia_preguntar_flotante()
            finally:
                self.ia_escucha_ocupada = False
                self.ia_responder_por_voz = False
        elif hasattr(self, "portia_status_var"):
            ack = _portia_ack()
            try:
                if hasattr(self, "portia_panel_visible") and not self.portia_panel_visible and hasattr(self, "toggle_portia_panel"):
                    self.toggle_portia_panel()
                self.portia_status_var.set(f"P.O.R.T.I.A: {ack}")
                if hasattr(self, "portia_resultado"):
                    self.portia_resultado.delete("1.0", "end")
                    self.portia_resultado.insert("1.0", f"Escuche: {texto}\n\nP.O.R.T.I.A: {ack}")
                threading.Thread(target=lambda: _hablar_breve(ack, timeout=5), daemon=True).start()
            finally:
                self.ia_escucha_ocupada = False
                self.ia_responder_por_voz = False
        return
    _ia_set_ultimo_audio(self, texto)
    if not comando:
        ack = _portia_ack()
        self.ia_resultado_text.delete("1.0", "end")
        self.ia_resultado_text.insert("1.0", f"Escuche: {texto}\n\nP.O.R.T.I.A: {ack}")
        self.ia_escucha_ocupada = False
        self.ia_responder_por_voz = False
        _ia_set_estado(self, "DORMIDA", "DORMIDA: P.O.R.T.I.A queda en espera para su pregunta.", True)
        return
    self.ia_escucha_ocupada = True
    self.ia_responder_por_voz = True
    self.ia_chat_var.set(comando)
    ack = _portia_ack()
    _ia_set_estado(self, "PROCESANDO", f"{ack} Procesando: {comando}", True)
    threading.Thread(target=lambda: _hablar_breve(ack, timeout=5), daemon=True).start()
    if _ia_ejecutar_comando_operativo(self, comando, desde_voz=True):
        self.ia_escucha_ocupada = False
        return
    self.ia_preguntar()


def ia_leer_resultado(self):
    texto = self.ia_resultado_text.get("1.0", "end").strip()
    if not texto:
        messagebox.showwarning("Sin texto", "No hay resultado para leer.")
        return
    texto = _ia_texto_para_voz(texto)
    if not texto:
        return
    self.ia_detener_voz()
    _ia_set_estado(self, "HABLANDO", "HABLANDO: leyendo respuesta. Diga 'es todo Portia' o 'desconectate Portia'.", True)

    def worker():
        try:
            proceso = _crear_proceso_hablar_windows(texto)
            self.ia_voz_proceso = proceso
            proceso.wait(timeout=120)
        except Exception:
            pass
        finally:
            self.ia_voz_proceso = None
            self.after(0, lambda: _ia_set_estado(self, "DORMIDA", None, True))

    hilo = threading.Thread(target=worker, daemon=True)
    hilo.start()


def ia_detener_voz(self):
    proceso = getattr(self, "ia_voz_proceso", None)
    if proceso and proceso.poll() is None:
        try:
            subprocess.run(
                ["taskkill", "/PID", str(proceso.pid), "/T", "/F"],
                capture_output=True,
                text=True,
                timeout=5,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        except Exception:
            try:
                proceso.terminate()
            except Exception:
                pass
    self.ia_voz_proceso = None
    if hasattr(self, "ia_escucha_status_var"):
        _ia_set_estado(self, "DORMIDA", "Voz detenida. P.O.R.T.I.A queda en espera.", True)


def ia_silenciar_portia(self):
    self.ia_detener_voz()
    self.ia_escucha_ocupada = False
    self.ia_responder_por_voz = False
    _ia_set_estado(self, "DORMIDA", "DORMIDA: diga Hey Portia cuando necesite ayuda.", True)


def ia_abrir_mapa_meteo(self):
    if not getattr(self, "ia_mapa_url", None):
        messagebox.showwarning("Sin mapa", "Primero consulte clima/mar de un puerto o ubicacion AIS de un buque.")
        return
    webbrowser.open(self.ia_mapa_url)
