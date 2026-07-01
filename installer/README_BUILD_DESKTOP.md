# XTRAVON ONE - Compilacion Desktop

## 1. Compilar ejecutable con PyInstaller

Ejecute desde CMD, ubicado en la raiz del proyecto:

```bat
python -m PyInstaller --clean --noconfirm XTRAVON_ONE.spec
```

Esto genera:

```text
dist\XTRAVON ONE\XTRAVON ONE.exe
```

## 2. Compilar instalador con Inno Setup

Ejecute:

```bat
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "installer\XTRAVON_ONE.iss"
```

Si Inno Setup esta instalado en `C:\Program Files\Inno Setup 6`, use:

```bat
"C:\Program Files\Inno Setup 6\ISCC.exe" "installer\XTRAVON_ONE.iss"
```

El instalador queda en:

```text
installer\Output\XTRAVON_ONE_Setup_1.0.0.exe
```

## Opcion directa

Tambien puede ejecutar:

```bat
installer\build_desktop.bat
```

## Incluido en el paquete

- Aplicacion desktop Tkinter.
- Assets de XTRAVON ONE.
- Icono del instalador.
- Template Excel `backend\Template\base_operaciones_camiones.xlsx`.

El archivo temporal de Excel `~$base_operaciones_camiones.xlsx` no se incluye.
