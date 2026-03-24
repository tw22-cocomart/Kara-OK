import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
from PIL import Image, ImageTk

from db import create_connection
from utils import hash_password

class LyricsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        
        nav_blue = "#2c3e8c"
        font_style = ("Courier New", 12, "bold")

        nav_frame = tk.Frame(self, bg=nav_blue, height=45)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)

        self.nav_buttons = {}
        self.nav_targets = {"Home": "HomeKaraokePage", "Karaoke": "LyricsPage", "SongBook": "SongbookPage", "Settings": "SettingsPage"}
        
        tabs = ["Home", "Karaoke", "SongBook", "Settings"]
        targets = ["HomeKaraokePage", "LyricsPage", "SongbookPage", "SettingsPage"]
        for tab, target in zip(tabs, targets):
            btn = tk.Button(nav_frame, text=tab, bg=nav_blue, fg="white", font=font_style, bd=0, padx=20, activebackground="#3d51b3", activeforeground="white", cursor="hand2", command=lambda t=target: controller.show_frame(t))
            btn.pack(side="left", fill="y")
            self.nav_buttons[tab] = btn

        content_container = tk.Frame(self, bg="white", padx=30, pady=20)
        content_container.pack(fill="both", expand=True)

        info_header = tk.Frame(content_container, bg="#e1f0ff", height=45, highlightthickness=1, highlightbackground="#448AFF")
        info_header.pack(side="top", fill="x", pady=(0, 15))
        info_header.pack_propagate(False)
        
        tk.Label(info_header, text="Currently Playing: 28830 | My Heart Will Go On...", font=("Courier New", 10, "bold"), fg="#2c3e8c", bg="#e1f0ff").pack(side="left", padx=10)
        tk.Label(info_header, text="Up Next: 10596, 1421, 17304", font=("Courier New", 10, "bold"), fg="#2c3e8c", bg="#e1f0ff").pack(side="right", padx=10)

        lower_content = tk.Frame(content_container, bg="white")
        lower_content.pack(fill="both", expand=True)

        tv_section = tk.Frame(lower_content, bg="white")
        tv_section.pack(side="left", expand=True, fill="both")

        video_box = tk.Frame(tv_section, bg="black", highlightthickness=2, highlightbackground="#448AFF")
        video_box.pack(fill="both", expand=True)

        try:
            img = Image.open("lyrics_screen.jpg")
            img = img.resize((850, 500), Image.Resampling.LANCZOS)
            self.photo = ImageTk.PhotoImage(img)
            display = tk.Label(video_box, image=self.photo, bg="black")
            display.pack(expand=True, fill="both")
            tk.Label(display, text="Every night in my dreams,\nI see you, I feel you", fg="white", bg="#2c3e8c", font=("Courier New", 20, "bold"), padx=20, pady=10).place(relx=0.5, rely=0.75, anchor="center")
            tk.Label(display, text="28830 | My Heart Will Go On | Celine Dion", fg="yellow", bg="black", font=("Courier New", 14, "bold"), padx=10).place(relx=0.5, rely=0.92, anchor="center")
        except Exception:
            tk.Label(video_box, text="TV MONITOR SCREEN", fg="white", bg="black", font=("Courier New", 16)).pack(expand=True)

        right_sidebar = tk.Frame(lower_content, bg="white", width=180)
        right_sidebar.pack(side="right", fill="y", padx=(20, 0))
        btn_container = tk.Frame(right_sidebar, bg="white")
        btn_container.pack(side="bottom")

        def style_btn(text, bg, fg, target):
            tk.Button(btn_container, text=text, font=("Courier New", 12, "bold"), bg=bg, fg=fg, width=12, pady=10, relief="flat", highlightthickness=1, highlightbackground="#448AFF", cursor="hand2", command=lambda: controller.show_frame(target)).pack(pady=5)

        style_btn("STOP", "#FFCDD2", "#C62828", "ScorePage")
        style_btn("ADD", "#E6FFC1", "#558B2F", "SongbookPage")
        style_btn("SKIP", "#E1F5FE", "#1565C0", "LyricsPage")
