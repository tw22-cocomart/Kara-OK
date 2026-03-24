import tkinter as tk
import service  # ✅ NEW: pull songs dynamically

class SongbookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        
        primary_blue = "#4A61E1"
        nav_dark_blue = "#2c3e8c"
        font_mono = ("Courier New", 11, "bold")
        song_font = ("Courier New", 12)
        nav_blue = "#283593"
        font_style = ("Courier New", 11, "bold")

        # --- Navigation Bar ---
        nav_frame = tk.Frame(self, bg=nav_blue, height=45)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)

        self.nav_buttons = {}
        self.nav_targets = {
            "Home": "HomeKaraokePage",
            "Karaoke": "LyricsPage",
            "SongBook": "SongbookPage",
            "Settings": "SettingsPage"
        }
        
        tabs = ["Home", "Karaoke", "SongBook", "Settings"]
        targets = ["HomeKaraokePage", "LyricsPage", "SongbookPage", "SettingsPage"]
        for tab, target in zip(tabs, targets):
            btn = tk.Button(
                nav_frame, text=tab, bg=nav_blue, fg="white", font=font_style,
                bd=0, padx=20, activebackground="#3d51b3", activeforeground="white",
                cursor="hand2", command=lambda t=target: controller.show_frame(t)
            )
            btn.pack(side="left", fill="y")
            self.nav_buttons[tab] = btn
            
        # --- Filter Bar ---
        filter_frame = tk.Frame(self, bg="white", pady=25)
        filter_frame.pack(fill="x", padx=50)

        for btn_text in ["Singer", "Title", "Favorites"]:
            tk.Button(
                filter_frame, text=btn_text, font=font_mono, fg=nav_dark_blue, bg="white",
                relief="flat", highlightthickness=1, highlightbackground=primary_blue,
                width=15, pady=6
            ).pack(side="left", padx=5)

        tk.Entry(
            filter_frame, font=("Courier New", 11), fg="grey",
            highlightthickness=1, highlightbackground=primary_blue, bd=0
        ).pack(side="left", fill="x", expand=True, padx=(15, 0), ipady=8)

        # --- Song Table ---
        table_container = tk.Frame(self, bg="white", padx=50)
        table_container.pack(fill="both", expand=True)

        def draw_gradient(event, start_color, end_color):
            canvas = event.widget
            canvas.delete("grad")
            w, h = event.width, event.height
            r1, g1, b1 = self.winfo_rgb(start_color)
            r2, g2, b2 = self.winfo_rgb(end_color)
            r1, g1, b1 = r1//256, g1//256, b1//256
            r2, g2, b2 = r2//256, g2//256, b2//256
            for i in range(h):
                nr = int(r1 + (r2 - r1) * (i / h))
                ng = int(g1 + (g2 - g1) * (i / h))
                nb = int(b1 + (r2 - b1) * (i / h))
                color = f'#{nr:02x}{ng:02x}{nb:02x}'
                canvas.create_line(0, i, w, i, fill=color, tags="grad")
            canvas.tag_lower("grad")

        # --- Featured Song (first one in catalog) ---
        service.init_backend()
        all_songs = service.get_all_songs()
        if all_songs:
            featured = all_songs[0]  # pick first song as featured
            feat_canvas = tk.Canvas(table_container, height=85, highlightthickness=1,
                                    highlightbackground=primary_blue, bd=0)
            feat_canvas.pack(fill="x", pady=(0, 10))
            feat_canvas.bind("<Configure>", lambda e: draw_gradient(e, "#e1f0ff", "#FFFFFF"))

            tk.Label(feat_canvas, text="✦ FEATURED SONG", font=font_mono,
                     fg=primary_blue, bg="#e1f0ff").place(x=20, y=10)
            tk.Label(feat_canvas, text=featured["id"], font=song_font, bg="#f0f8ff",
                     width=12, anchor="w").place(x=20, y=48)
            tk.Label(feat_canvas, text=featured["title"], font=song_font, bg="#f0f8ff",
                     width=35, anchor="w").place(x=150, y=48)
            tk.Label(feat_canvas, text=featured["artist"], font=song_font,
                     bg="#f0f8ff", anchor="w").place(relx=0.7, y=48)

        # --- Song List (dynamic) ---
        for song in all_songs[1:]:  # skip featured
            code = song["id"]
            title = song["title"]
            artist = song["artist"]
            is_highlighted = (code == "03297")  # example highlight

            if is_highlighted:
                row_canvas = tk.Canvas(table_container, height=50, highlightthickness=0, bd=0)
                row_canvas.pack(fill="x")
                row_canvas.bind("<Configure>", lambda e: draw_gradient(e, "#E6FFC1", "#FFFFFF"))
                tk.Label(row_canvas, text=code, font=song_font, bg="#f1ffd9",
                         fg=nav_dark_blue, width=12, anchor="w").place(x=20, y=12)
                tk.Label(row_canvas, text=title, font=song_font, bg="#f1ffd9",
                         fg=nav_dark_blue, width=35, anchor="w").place(x=150, y=12)
                tk.Label(row_canvas, text=artist, font=song_font, bg="#f1ffd9",
                         fg=nav_dark_blue, anchor="w").place(relx=0.7, y=12)
            else:
                row_frame = tk.Frame(table_container, bg="white", bd=0)
                row_frame.pack(fill="x")
                tk.Label(row_frame, text=code, font=song_font, bg="white",
                         fg=nav_dark_blue, width=12, anchor="w").pack(side="left", padx=(20, 0), pady=12)
                tk.Label(row_frame, text=title, font=song_font, bg="white",
                         fg=nav_dark_blue, width=35, anchor="w").pack(side="left", pady=12)
                artist_lbl = tk.Label(row_frame, text=artist, font=song_font,
                                      bg="white", fg=nav_dark_blue, anchor="w")
                artist_lbl.place(relx=0.7, rely=0.5, anchor="w")

            tk.Frame(table_container, bg=primary_blue, height=1).pack(fill="x")
