import json
import os
import sys
import tkinter as tk
import ttkbootstrap as ttkb
from ttkbootstrap.constants import *

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

with open(resource_path("dummy_tools.json"), "r", encoding="utf-8") as f:
    dummy_tools = json.load(f)

themes = sorted(ttkb.Style().theme_names())

class ThemePreview:
    def __init__(self, root):
        self.root = root
        self.root.title("ttkbootstrap 主題預覽 - 切換主題即時預覽")
        self.root.geometry("900x680")

        self.theme_var = tk.StringVar(value="flatly")
        selector_frame = ttkb.Frame(root, padding=10)
        selector_frame.pack(fill=tk.X, padx=10, pady=5)
        ttkb.Label(selector_frame, text="選擇主題：", font=("微软雅黑", 11)).pack(side=tk.LEFT, padx=5)
        combo = ttkb.Combobox(selector_frame, textvariable=self.theme_var,
                              values=themes, state="readonly", width=20)
        combo.pack(side=tk.LEFT, padx=5)
        combo.bind("<<ComboboxSelected>>", self.change_theme)

        self.progress = ttkb.Progressbar(root, mode='determinate', length=400, maximum=100)
        self.progress.pack(pady=(10, 0))
        self.progress['value'] = 70

        canvas_frame = ttkb.Frame(root)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=5)

        self.canvas = tk.Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
        self.scrollbar = ttkb.Scrollbar(canvas_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttkb.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        self.create_cards()
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def change_theme(self, event):
        theme = self.theme_var.get()
        self.root.style.theme_use(theme)
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.create_cards()

    def create_cards(self):
        style = self.root.style
        self.scrollable_frame.columnconfigure(0, weight=1, uniform="col")
        self.scrollable_frame.columnconfigure(1, weight=1, uniform="col")

        row = 0
        col = 0
        for idx, tool in enumerate(dummy_tools):
            card = ttkb.LabelFrame(self.scrollable_frame, text="", padding=10, bootstyle="info")
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            style_name = f"Tool{idx}.TButton"
            bg = tool.get("button_color", "#0078D7")
            fg = tool.get("text_color", "#FFFFFF")
            font_size = tool.get("font_size", 12)

            style.configure(style_name,
                            background=bg,
                            foreground=fg,
                            font=("微软雅黑", font_size, "bold"),
                            borderwidth=2,
                            focusthickness=2,
                            focuscolor=style.colors.get('primary'))

            btn = ttkb.Button(card, text=tool["name"], style=style_name)
            btn.pack(fill=tk.X, pady=(5, 5))

            desc = tool.get("description", "")
            if desc:
                desc_label = ttkb.Label(card, text=desc, font=("微软雅黑", 9), foreground="gray")
                desc_label.pack(fill=tk.X, pady=(0, 5))

            col += 1
            if col > 1:
                col = 0
                row += 1

if __name__ == "__main__":
    # 清除可能残留的根窗口（解决单根窗口冲突）
    try:
        if tk._default_root:
            tk._default_root.destroy()
    except:
        pass

    root = ttkb.Window(themename="flatly")
    app = ThemePreview(root)
    root.mainloop()
