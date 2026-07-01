# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None
ROOT = Path(SPECPATH)
PY_ROOT = Path(sys.base_prefix)


datas = [
    (str(ROOT / "assets"), "assets"),
    (str(ROOT / "backend" / "Template" / "base_operaciones_camiones.xlsx"), "backend/Template"),
    (str(PY_ROOT / "Lib" / "tkinter"), "tkinter"),
    (str(PY_ROOT / "tcl" / "tcl8.6"), "_tcl_data"),
    (str(PY_ROOT / "tcl" / "tk8.6"), "_tk_data"),
]


binaries = [
    (str(PY_ROOT / "DLLs" / "tcl86t.dll"), "."),
    (str(PY_ROOT / "DLLs" / "tk86t.dll"), "."),
    (str(PY_ROOT / "DLLs" / "_tkinter.pyd"), "."),
]


hiddenimports = [
    "frontend",
    "frontend.ayuda_qa",
    "frontend.centro_ejecutivo",
    "frontend.gestion_profesional",
    "frontend.ia_ejecutiva",
    "frontend.informes",
    "frontend.issue_log",
    "frontend.lazy",
    "frontend.roles_permisos",
    "openpyxl",
    "qrcode",
    "requests",
    "speech_recognition",
    "tkinter",
    "_tkinter",
    "tkinter.ttk",
    "tkinter.filedialog",
    "tkinter.messagebox",
    "PIL",
    "PIL.Image",
    "PIL.ImageTk",
]


a = Analysis(
    ["main.py"],
    pathex=[str(ROOT)],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[str(ROOT / "installer" / "runtime_hooks" / "xtravon_tkinter_runtime.py")],
    excludes=[
        "matplotlib",
        "numpy",
        "pandas",
        "pytest",
        "uvicorn",
        "fastapi",
        "sqlalchemy",
        "psycopg2",
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="XTRAVON ONE",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(ROOT / "installer" / "xtravon_one.ico"),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="XTRAVON ONE",
)
