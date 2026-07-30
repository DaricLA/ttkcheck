# -*- coding: utf-8 -*-
"""
ttkbootstrap 主题预览 – 基于成功示例，展示自定义工具卡片
"""
import json
import os
import sys
import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *


def resource_path(relative_path):
    """获取资源路径，兼容 PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class ThemePreview(tb.Window):
    THEMES = [
        "cosmo", "flatly", "litera", "minty", "lumen",
        "sandstone", "solar", "superhero", "darkly", "vapor",
        "cyborg", "pulse", "united", "yeti", "morph", "journal"
    ]

    def __init__(self):
        super().__init__(
            title="VSAPE 工具箱主题预览",
            themename="cosmo",
            size=(1000, 720),
            resizable=(True, True)
        )
        self.center_window()

        # ---------- 读取演示工具配置 ----------
        with open(resource_path("dummy_tools.json"), "r", encoding="utf-8") as f:
            self.dummy_tools = json.load(f)

        # ---------- 顶部：主题切换 ----------
        top_frame = tb.Frame(self, padding=15)
        top_frame.pack(fill=X)

        tb.Label(top_frame, text="选择主题：", font=("", 12, "bold")).pack(side=LEFT, padx=(0, 10))

        self.theme_var = tk.StringVar(value="cosmo")
        theme_combo = tb.Combobox(
            top_frame,
            textvariable=self.theme_var,
            values=self.THEMES,
            width=20,
            state="readonly"
        )
        theme_combo.pack(side=LEFT, padx=5)
        theme_combo.bind("<<ComboboxSelected>>", self.on_theme_change)

        tb.Button(top_frame, text="切换", command=self.on_theme_change, bootstyle=PRIMARY).pack(side=LEFT, padx=5)

        self.theme_label = tb.Label(top_frame, text=f"当前主题：cosmo", font=("", 10))
        self.theme_label.pack(side=RIGHT)

        # ---------- 进度条演示 ----------
        self.progress = tb.Progressbar(self, mode='determinate', length=400, maximum=100, bootstyle=INFO)
        self.progress.pack(pady=(10, 0))
        self.progress['value'] = 70

        # ---------- 卡片网格（可滚动） ----------
        canvas_frame = tb.Frame(self)
        canvas_frame.pack(fill=BOTH, expand=YES, padx=15, pady=5)

        self.canvas = tk.Canvas(canvas_frame, borderwidth=0, highlightthickness=0)
        self.scrollbar = tb.Scrollbar(canvas_frame, orient=VERTICAL, command=self.canvas.yview)
        self.scrollable_frame = tb.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", self._on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

        # 首次创建卡片
        self.create_cards()
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # 状态栏
        status_bar = tb.Label(
            self,
            text="ttkbootstrap 主题预览 · 支持自定义按钮颜色与字体大小",
            bootstyle="secondary",
            anchor=W,
            padding=8
        )
        status_bar.pack(side=BOTTOM, fill=X)

    def center_window(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.geometry(f"+{x}+{y}")

    def on_theme_change(self, event=None):
        theme = self.theme_var.get()
        self.style.theme_use(theme)
        self.theme_label.config(text=f"当前主题：{theme}")
        # 主题切换后重建卡片，确保新样式应用
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.create_cards()

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def create_cards(self):
        style = self.style
        self.scrollable_frame.columnconfigure(0, weight=1, uniform="col")
        self.scrollable_frame.columnconfigure(1, weight=1, uniform="col")

        row = 0
        col = 0
        for idx, tool in enumerate(self.dummy_tools):
            # 卡片容器
            card = tb.LabelFrame(self.scrollable_frame, text="", padding=10, bootstyle="info")
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            # 创建按钮样式（保持自定义颜色与字体）
            style_name = f"Tool{idx}.TButton"
            bg = tool.get("button_color", "#0078D7")
            fg = tool.get("text_color", "#FFFFFF")
            font_size = tool.get("font_size", 12)

            style.configure(
                style_name,
                background=bg,
                foreground=fg,
                font=("微软雅黑", font_size, "bold"),
                borderwidth=2,
                focusthickness=2,
                focuscolor=style.colors.get('primary')
            )

            btn = tb.Button(card, text=tool["name"], style=style_name)
            btn.pack(fill=X, pady=(5, 5))

            desc = tool.get("description", "")
            if desc:
                desc_label = tb.Label(card, text=desc, font=("微软雅黑", 9), foreground="gray")
                desc_label.pack(fill=X, pady=(0, 5))

            col += 1
            if col > 1:
                col = 0
                row += 1


if __name__ == "__main__":
    app = ThemePreview()
    app.mainloop()
