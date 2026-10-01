import os
import sys


base_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))

if base_dir and base_dir not in sys.path:
    sys.path.insert(0, base_dir)

tcl_dir = os.path.join(base_dir, "_tcl_data")
tk_dir = os.path.join(base_dir, "_tk_data")

if os.path.isdir(tcl_dir):
    os.environ["TCL_LIBRARY"] = tcl_dir

if os.path.isdir(tk_dir):
    os.environ["TK_LIBRARY"] = tk_dir
