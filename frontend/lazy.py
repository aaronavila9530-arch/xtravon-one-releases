from tkinter import ttk


class LazyNotebook:
    def __init__(self, parent):
        self.notebook = ttk.Notebook(parent)
        self._builders = {}
        self._built = set()
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def pack(self, **kwargs):
        self.notebook.pack(**kwargs)

    def add(self, frame, text, builder=None, build_now=False):
        self.notebook.add(frame, text=text)
        if builder:
            self._builders[str(frame)] = (frame, builder)
        if build_now and builder:
            self.build(frame)

    def select(self, frame):
        self.notebook.select(frame)
        self.build(frame)

    def build(self, frame):
        frame_key = str(frame)
        if frame_key in self._built:
            return

        item = self._builders.get(frame_key)
        if not item:
            self._built.add(frame_key)
            return

        target, builder = item
        builder(target)
        self._built.add(frame_key)

    def _on_tab_changed(self, _event=None):
        selected = self.notebook.select()
        if selected:
            item = self._builders.get(selected)
            if item:
                self.build(item[0])
