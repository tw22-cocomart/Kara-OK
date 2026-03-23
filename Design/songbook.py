import tkinter as tk
import ctypes

DWMWA_CAPTION_COLOR = 35

def create_songbook():
    root = tk.Tk()
    root.title("Kara-OK!")
    root.geometry("1100x700")
    root.configure(bg="white")

    # --- COLORS ---
    primary_blue = "#4A61E1"
    nav_dark_blue = "#2c3e8c"
    font_mono = ("Courier New", 11, "bold")
    song_font = ("Courier New", 12)

    # --- TITLE BAR COLOR ---
    try:
        root.update()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        title_color = 0xE1614A 
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_CAPTION_COLOR, ctypes.byref(ctypes.c_int(title_color)), 4
        )
    except Exception: pass

    # --- NAVIGATION HEADER ---
    nav_blue = "#283593"
    font_style = ("Courier New", 11, "bold")

    nav_frame = tk.Frame(root, bg=nav_blue, height=45)
    nav_frame.pack(fill="x")
    nav_frame.pack_propagate(False)

    tabs = ["Home", "Karaoke", "SongBook", "Settings"]
    for tab in tabs:
        tk.Button(nav_frame, text=tab, bg=nav_blue, fg="white", 
                  font=font_style, bd=0, padx=20, activebackground="#3d51b3", 
                  activeforeground="white", cursor="hand2").pack(side="left", fill="y")
        
    # --- FILTER BUTTONS ---
    filter_frame = tk.Frame(root, bg="white", pady=25)
    filter_frame.pack(fill="x", padx=50)

    for btn_text in ["Singer", "Title", "Favorites"]:
        tk.Button(filter_frame, text=btn_text, font=font_mono, fg=nav_dark_blue, bg="white", 
                  relief="flat", highlightthickness=1, highlightbackground=primary_blue, 
                  width=15, pady=6).pack(side="left", padx=5)

    tk.Entry(filter_frame, font=("Courier New", 11), fg="grey", highlightthickness=1, 
             highlightbackground=primary_blue, bd=0).pack(side="left", fill="x", expand=True, padx=(15, 0), ipady=8)

    # --- SONG TABLE AREA ---
    table_container = tk.Frame(root, bg="white", padx=50)
    table_container.pack(fill="both", expand=True)

    def draw_gradient(event, start_color, end_color):
        canvas = event.widget
        canvas.delete("grad")
        w, h = event.width, event.height
        r1, g1, b1 = root.winfo_rgb(start_color)
        r2, g2, b2 = root.winfo_rgb(end_color)
        r1, g1, b1 = r1//256, g1//256, b1//256
        r2, g2, b2 = r2//256, g2//256, b2//256
        for i in range(h):
            nr = int(r1 + (r2 - r1) * (i / h))
            ng = int(g1 + (g2 - g1) * (i / h))
            nb = int(b1 + (b2 - b1) * (i / h))
            color = f'#{nr:02x}{ng:02x}{nb:02x}'
            canvas.create_line(0, i, w, i, fill=color, tags="grad")
        canvas.tag_lower("grad")

    # --- 1. FEATURED SONG ROW (Singer Aligned) ---
    feat_canvas = tk.Canvas(table_container, height=85, highlightthickness=1, 
                            highlightbackground=primary_blue, bd=0)
    feat_canvas.pack(fill="x", pady=(0, 10))
    feat_canvas.bind("<Configure>", lambda e: draw_gradient(e, "#e1f0ff", "#FFFFFF"))

    tk.Label(feat_canvas, text="✦ FEATURED SONG", font=font_mono, fg=primary_blue, bg="#e1f0ff").place(x=20, y=10)
    tk.Label(feat_canvas, text="15492", font=song_font, bg="#f0f8ff", width=12, anchor="w").place(x=20, y=48)
    tk.Label(feat_canvas, text="All These Ladies", font=song_font, bg="#f0f8ff", width=35, anchor="w").place(x=150, y=48)
    # Aligning BGYO to the 70% mark
    tk.Label(feat_canvas, text="BGYO", font=song_font, bg="#f0f8ff", anchor="w").place(relx=0.7, y=48)

    # --- REGULAR SONG LIST ---
    songs = [
        ("2609", "Pusong Bato", "Jovit Baldivino", False),
        ("28830", "My Heart Will Go On", "Celine Dion", False),
        ("10596", "Only Reminds Me Of You", "M.Y.M.P", True), 
        ("1421", "Akin Ka Na Lang", "Morissette Amon", False),
        ("17304", "Rolling In The Deep", "Adele", False),
    ]

    for code, title, artist, is_highlighted in songs:
        if is_highlighted:
            # --- 2. GREEN GRADIENT ROW (Singer Aligned) ---
            row_canvas = tk.Canvas(table_container, height=50, highlightthickness=0, bd=0)
            row_canvas.pack(fill="x")
            row_canvas.bind("<Configure>", lambda e: draw_gradient(e, "#E6FFC1", "#FFFFFF"))
            
            tk.Label(row_canvas, text=code, font=song_font, bg="#f1ffd9", fg=nav_dark_blue, width=12, anchor="w").place(x=20, y=12)
            tk.Label(row_canvas, text=title, font=song_font, bg="#f1ffd9", fg=nav_dark_blue, width=35, anchor="w").place(x=150, y=12)
            # Aligning M.Y.M.P to the 70% mark
            tk.Label(row_canvas, text=artist, font=song_font, bg="#f1ffd9", fg=nav_dark_blue, anchor="w").place(relx=0.7, y=12)
        else:
            # --- 3. STANDARD WHITE ROW (Singer Aligned) ---
            row_frame = tk.Frame(table_container, bg="white", bd=0)
            row_frame.pack(fill="x")
            
            tk.Label(row_frame, text=code, font=song_font, bg="white", fg=nav_dark_blue, width=12, anchor="w").pack(side="left", padx=(20, 0), pady=12)
            tk.Label(row_frame, text=title, font=song_font, bg="white", fg=nav_dark_blue, width=35, anchor="w").pack(side="left", pady=12)
            # Singer is placed at relx=0.7 within the frame for perfect alignment
            artist_lbl = tk.Label(row_frame, text=artist, font=song_font, bg="white", fg=nav_dark_blue, anchor="w")
            artist_lbl.place(relx=0.7, rely=0.5, anchor="w")

        tk.Frame(table_container, bg=primary_blue, height=1).pack(fill="x")

    root.mainloop()

if __name__ == "__main__":
    create_songbook()