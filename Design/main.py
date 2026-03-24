import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ctypes
import random

# Windows API constant for title bar color
DWMWA_CAPTION_COLOR = 35

class KaraOKApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Kara-OK!")
        self.geometry("1150x750")
        self.configure(bg="white")
        
        # --- MAKE WINDOW FULL SCREEN (MAXIMIZED) ---
        self.state('zoomed')
        
        # --- GLOBAL TITLE BAR COLOR LOGIC ---
        try:
            self.update()
            hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
            # Windows uses BGR, so #4A61E1 becomes 0xE1614A
            title_color = 0xE1614A 
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_CAPTION_COLOR, ctypes.byref(ctypes.c_int(title_color)), 4
            )
        except Exception as e:
            print(f"Title bar color not supported: {e}")

        # The container holds all the frames
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # Initializing every single page class provided
        for F in (RegisterPage, LoginPage, HomeKaraokePage, LyricsPage, SongbookPage, SettingsPage, ScorePage):
            page_name = F.__name__
            frame = F(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start at the Register Page
        self.show_frame("RegisterPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        
        # Logic to randomize score whenever the ScorePage is shown
        if page_name == "ScorePage":
            frame.refresh_score()
            
        # --- NAVIGATION UNDERLINE LOGIC ---
        for f in self.frames.values():
            if hasattr(f, 'nav_buttons'):
                for btn_text, btn_obj in f.nav_buttons.items():
                    if f.nav_targets.get(btn_text) == page_name:
                        btn_obj.configure(font=("Courier New", 11, "bold", "underline"))
                    else:
                        btn_obj.configure(font=("Courier New", 11, "bold"))
        
        frame.tkraise()

# --- 1. REGISTER PAGE ---
class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        primary_blue = "#4A61E1"
        button_bg = "#E6FFC1"
        font_style = ("Courier New", 12, "bold")
        header_font = ("Courier New", 18, "bold")

        main_frame = tk.Frame(self, bg="white", padx=50, pady=20)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(main_frame, text="CREATE AN ACCOUNT", font=header_font, fg=primary_blue, bg="white").pack(pady=(0, 20))

        def create_input_field(label_text, is_password=False):
            tk.Label(main_frame, text=label_text, font=font_style, fg=primary_blue, bg="white", anchor="w").pack(fill="x", pady=(10, 2))
            entry = tk.Entry(main_frame, font=("Courier New", 12), bd=0, highlightthickness=1, highlightbackground=primary_blue, relief="flat", show="*" if is_password else "")
            entry.pack(fill="x", ipady=8)

        create_input_field("Email")
        create_input_field("Username")
        create_input_field("Password", True)
        create_input_field("Confirm Password", True)

        tk.Button(main_frame, text="Register", font=font_style, fg=primary_blue, bg=button_bg, relief="groove", bd=1, padx=40, pady=5, command=lambda: controller.show_frame("LoginPage")).pack(pady=40)

# --- 2. LOGIN PAGE ---
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        primary_blue = "#4A61E1"
        button_lime = "#E6FFC1"
        font_mono = ("Courier New", 12, "bold")
        header_font = ("Courier New", 18, "bold")

        main_frame = tk.Frame(self, bg="white", padx=40)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(main_frame, text="LOG IN", font=header_font, fg=primary_blue, bg="white").pack(pady=(0, 30))

        def create_input_field(label_text, is_password=False):
            tk.Label(main_frame, text=label_text, font=font_mono, fg=primary_blue, bg="white", anchor="w").pack(fill="x", pady=(10, 2))
            entry = tk.Entry(main_frame, font=("Courier New", 12), bd=0, highlightthickness=1, highlightbackground=primary_blue, relief="flat", show="*" if is_password else "")
            entry.pack(fill="x", ipady=10, ipadx=10)

        create_input_field("Username")
        create_input_field("Password", True)

        tk.Button(main_frame, text="Log In", font=font_mono, fg=primary_blue, bg=button_lime, relief="groove", bd=1, padx=50, pady=5, command=lambda: controller.show_frame("HomeKaraokePage")).pack(pady=40)

# --- 3. HOME (KARAOKE MAIN PAGE) ---
class HomeKaraokePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#CCEEFF")
        nav_blue = "#283593"
        font_style = ("Courier New", 11, "bold")

        nav_frame = tk.Frame(self, bg=nav_blue, height=45)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)

        self.nav_buttons = {}
        self.nav_targets = {"Home": "HomeKaraokePage", "Karaoke": "LyricsPage", "SongBook": "SongbookPage", "Settings": "SettingsPage"}
        
        tabs = [("Home", "HomeKaraokePage"), ("Karaoke", "LyricsPage"), ("SongBook", "SongbookPage"), ("Settings", "SettingsPage")]
        for tab, target in tabs:
            btn = tk.Button(nav_frame, text=tab, bg=nav_blue, fg="white", font=font_style, bd=0, padx=20, activebackground="#3d51b3", activeforeground="white", cursor="hand2", command=lambda t=target: controller.show_frame(t))
            btn.pack(side="left", fill="y")
            self.nav_buttons[tab] = btn

        main_container = tk.Frame(self, bg="#CCEEFF")
        main_container.pack(expand=True, fill="both", padx=15, pady=15)

        left_frame = tk.Frame(main_container, bg="#CCEEFF")
        left_frame.pack(side="left", expand=True, fill="both")

        video_box = tk.Frame(left_frame, bg="black", highlightbackground="#448AFF", highlightthickness=2)
        video_box.pack(pady=(10, 10), fill="both", expand=True)

        try:
            original_img = Image.open(r"C:\Users\Kaye Visera\OneDrive\Documents\songbook\songbook.jpg") 
            resized_img = original_img.resize((550, 350), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized_img)
            video_display = tk.Label(video_box, image=self.bg_image, bg="black")
            video_display.pack(expand=True, fill="both")
            tk.Label(video_display, text="28830 | My Heart Will Go On | Celine Dion", fg="yellow", bg="black", font=("Courier", 14, "bold")).place(relx=0.5, rely=0.9, anchor="center")
        except Exception:
            tk.Label(video_box, text="VIDEO MONITOR SCREEN", fg="white", bg="black", font=("Courier New", 16)).pack(expand=True)

        queue_frame = tk.Frame(left_frame, bg="white", bd=1, relief="solid")
        queue_frame.pack(fill="x", pady=10)
        tk.Label(queue_frame, text="Song Queue: 28830, 10596, 1421, 17304", bg="white", fg="#283593", font=("Courier", 10, "bold"), pady=15).pack()

        right_frame = tk.Frame(main_container, bg="white", width=320, bd=1, relief="solid")
        right_frame.pack(side="right", fill="y", padx=(15, 0))
        right_frame.pack_propagate(False)

        self.entry_var = tk.StringVar(value="")
        tk.Entry(right_frame, textvariable=self.entry_var, font=("Courier", 14), fg="#283593", bd=1, relief="solid", justify="center").pack(pady=30, padx=25, fill="x")
        
        keypad_frame = tk.Frame(right_frame, bg="white")
        keypad_frame.pack()
        buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'DEL', '0', 'RES']
        r, c = 0, 0
        for b in buttons:
            color = "#E1F5FE"
            if b == "DEL": color = "#FFCDD2"
            if b == "RES": color = "#DCEDC8"
            tk.Button(keypad_frame, text=b, width=7, height=2, bg=color, font=("Courier", 10, "bold"), command=lambda x=b: self.press(x)).grid(row=r, column=c, padx=4, pady=4)
            c+=1
            if c>2: c=0; r+=1

    def press(self, key):
        if key == "DEL": self.entry_var.set(self.entry_var.get()[:-1])
        elif key == "RES": self.entry_var.set("")
        else: self.entry_var.set(self.entry_var.get() + key)

# --- 4. LYRICS PAGE ---
class LyricsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
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

# --- 5. SONGBOOK PAGE ---
class SongbookPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        primary_blue = "#4A61E1"
        nav_dark_blue = "#2c3e8c"
        font_mono = ("Courier New", 11, "bold")
        song_font = ("Courier New", 12)
        nav_blue = "#283593"
        font_style = ("Courier New", 11, "bold")

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
            
        filter_frame = tk.Frame(self, bg="white", pady=25)
        filter_frame.pack(fill="x", padx=50)

        for btn_text in ["Singer", "Title", "Favorites"]:
            tk.Button(filter_frame, text=btn_text, font=font_mono, fg=nav_dark_blue, bg="white", relief="flat", highlightthickness=1, highlightbackground=primary_blue, width=15, pady=6).pack(side="left", padx=5)

        tk.Entry(filter_frame, font=("Courier New", 11), fg="grey", highlightthickness=1, highlightbackground=primary_blue, bd=0).pack(side="left", fill="x", expand=True, padx=(15, 0), ipady=8)

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
                nb = int(b1 + (b2 - b1) * (i / h))
                color = f'#{nr:02x}{ng:02x}{nb:02x}'
                canvas.create_line(0, i, w, i, fill=color, tags="grad")
            canvas.tag_lower("grad")

        feat_canvas = tk.Canvas(table_container, height=85, highlightthickness=1, highlightbackground=primary_blue, bd=0)
        feat_canvas.pack(fill="x", pady=(0, 10))
        feat_canvas.bind("<Configure>", lambda e: draw_gradient(e, "#e1f0ff", "#FFFFFF"))

        tk.Label(feat_canvas, text="✦ FEATURED SONG", font=font_mono, fg=primary_blue, bg="#e1f0ff").place(x=20, y=10)
        tk.Label(feat_canvas, text="15492", font=song_font, bg="#f0f8ff", width=12, anchor="w").place(x=20, y=48)
        tk.Label(feat_canvas, text="All These Ladies", font=song_font, bg="#f0f8ff", width=35, anchor="w").place(x=150, y=48)
        tk.Label(feat_canvas, text="BGYO", font=song_font, bg="#f0f8ff", anchor="w").place(relx=0.7, y=48)

        songs = [
            ("2609", "Pusong Bato", "Jovit Baldivino", False),
            ("28830", "My Heart Will Go On", "Celine Dion", False),
            ("10596", "Only Reminds Me Of You", "M.Y.M.P", True), 
            ("1421", "Akin Ka Na Lang", "Morissette Amon", False),
            ("17304", "Rolling In The Deep", "Adele", False),
        ]

        for code, title, artist, is_highlighted in songs:
            if is_highlighted:
                row_canvas = tk.Canvas(table_container, height=50, highlightthickness=0, bd=0)
                row_canvas.pack(fill="x")
                row_canvas.bind("<Configure>", lambda e: draw_gradient(e, "#E6FFC1", "#FFFFFF"))
                tk.Label(row_canvas, text=code, font=song_font, bg="#f1ffd9", fg=nav_dark_blue, width=12, anchor="w").place(x=20, y=12)
                tk.Label(row_canvas, text=title, font=song_font, bg="#f1ffd9", fg=nav_dark_blue, width=35, anchor="w").place(x=150, y=12)
                tk.Label(row_canvas, text=artist, font=song_font, bg="#f1ffd9", fg=nav_dark_blue, anchor="w").place(relx=0.7, y=12)
            else:
                row_frame = tk.Frame(table_container, bg="white", bd=0)
                row_frame.pack(fill="x")
                tk.Label(row_frame, text=code, font=song_font, bg="white", fg=nav_dark_blue, width=12, anchor="w").pack(side="left", padx=(20, 0), pady=12)
                tk.Label(row_frame, text=title, font=song_font, bg="white", fg=nav_dark_blue, width=35, anchor="w").pack(side="left", pady=12)
                artist_lbl = tk.Label(row_frame, text=artist, font=song_font, bg="white", fg=nav_dark_blue, anchor="w")
                artist_lbl.place(relx=0.7, rely=0.5, anchor="w")

            tk.Frame(table_container, bg=primary_blue, height=1).pack(fill="x")

# --- 6. SETTINGS PAGE ---
class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        primary_blue = "#4A61E1"
        button_bg = "#E6FFC1"
        nav_blue = "#2c3e8c"
        font_style = ("Courier New", 11, "bold")
        header_font = ("Courier New", 18, "bold")

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

        content_area = tk.Frame(self, bg="white")
        content_area.pack(fill="both", expand=True)

        sidebar = tk.Frame(content_area, bg="#f2f2f2")
        sidebar.place(relx=0, rely=0, relwidth=0.28, relheight=1)

        profile_box = tk.Frame(sidebar, bg="#7f8c8d", width=160, height=160)
        profile_box.pack(pady=(60, 15))

        tk.Label(sidebar, text="John Python", bg="#f2f2f2", font=("Courier New", 14, "bold")).pack()
        tk.Label(sidebar, text="@pythonprogramz", bg="#f2f2f2", fg="grey", font=("Courier New", 11)).pack()
        tk.Button(sidebar, text="logout", fg=primary_blue, bg="#f2f2f2", bd=0, font=("Courier New", 11, "underline"), cursor="hand2", command=lambda: controller.show_frame("LoginPage")).pack(side="bottom", pady=40)

        form_frame = tk.Frame(content_area, bg="white", padx=50)
        form_frame.place(relx=0.28, rely=0, relwidth=0.72, relheight=1)

        tk.Label(form_frame, text="USER PROFILE", font=header_font, fg=primary_blue, bg="white").pack(pady=(60, 40))

        def create_input(label_text, default_val):
            row = tk.Frame(form_frame, bg="white")
            row.pack(fill="x", pady=12, padx=(0, 50))
            tk.Label(row, text=label_text, font=font_style, fg=primary_blue, bg="white", width=12, anchor="e").pack(side="left", padx=15)
            entry = tk.Entry(row, font=("Courier New", 12), bd=0, highlightthickness=1, highlightbackground=primary_blue, highlightcolor=primary_blue)
            entry.insert(0, default_val)
            entry.pack(side="left", fill="x", expand=True, ipady=8)

        create_input("Name", "John Python")
        create_input("Username", "pythonprogramz")
        create_input("Email", "pythonprogrammingz")
        create_input("Password", "**********")

        tk.Button(form_frame, text="Save Changes", font=font_style, fg=primary_blue, bg=button_bg, activebackground="#D7F7A0", relief="groove", bd=1, padx=50, pady=10, cursor="hand2", command=lambda: messagebox.showinfo("Profile", "Changes Saved Successfully!")).pack(pady=40)

# --- 7. SCORE PAGE (INTEGRATED VERSION) ---
class ScorePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        nav_blue = "#2c3e8c"
        font_style = ("Courier New", 12, "bold")

        # --- NAVIGATION HEADER ---
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

        # --- MAIN CONTENT CONTAINER ---
        content_container = tk.Frame(self, bg="white", padx=30, pady=20)
        content_container.pack(fill="both", expand=True)

        # --- STATUS BAR ---
        info_header = tk.Frame(content_container, bg="#e1f0ff", height=45, highlightthickness=1, highlightbackground="#448AFF")
        info_header.pack(side="top", fill="x", pady=(0, 15))
        info_header.pack_propagate(False)
        
        tk.Label(info_header, text="Currently Playing: 28830 | My Heart Will Go On...", 
                 font=("Courier New", 10, "bold"), fg="#2c3e8c", bg="#e1f0ff").pack(side="left", padx=10)
        tk.Label(info_header, text="Up Next: 10596, 1421, 17304", 
                 font=("Courier New", 10, "bold"), fg="#2c3e8c", bg="#e1f0ff").pack(side="right", padx=10)

        # --- LOWER AREA (TV + Sidebar) ---
        lower_content = tk.Frame(content_container, bg="white")
        lower_content.pack(fill="both", expand=True)

        # TV Screen (Left Side)
        tv_section = tk.Frame(lower_content, bg="white")
        tv_section.pack(side="left", expand=True, fill="both")

        video_box = tk.Frame(tv_section, bg="black", highlightthickness=2, highlightbackground="#448AFF")
        video_box.pack(fill="both", expand=True)

        # --- SCORE TEXT OVERLAYS ---
        tk.Label(video_box, text="Highest Score: 99", fg="#448AFF", bg="black", 
                 font=("Courier New", 18, "bold")).place(relx=0.5, rely=0.2, anchor="center")
        
        tk.Label(video_box, text="YOUR SCORE:", fg="white", bg="black", 
                 font=("Courier New", 30, "bold")).place(relx=0.5, rely=0.35, anchor="center")
        
        self.score_label = tk.Label(video_box, text="0", fg="#FFFF99", bg="black", 
                                    font=("Courier New", 80, "bold"))
        self.score_label.place(relx=0.5, rely=0.55, anchor="center")
        
        tk.Label(video_box, text="Not Bad!", fg="white", bg="black", 
                 font=("Courier New", 32, "bold")).place(relx=0.5, rely=0.8, anchor="center")

        # --- RIGHT SIDEBAR: CONTROLS ---
        right_sidebar = tk.Frame(lower_content, bg="white", width=180)
        right_sidebar.pack(side="right", fill="y", padx=(20, 0))
        
        btn_container = tk.Frame(right_sidebar, bg="white")
        btn_container.pack(side="bottom")

        def style_btn(text, bg_color, target_page):
            return tk.Button(btn_container, text=text, font=("Courier New", 12, "bold"), 
                             bg=bg_color, fg="#2c3e8c", width=12, pady=10, relief="flat", 
                             highlightthickness=1, highlightbackground="#448AFF", cursor="hand2",
                             command=lambda: controller.show_frame(target_page))

        style_btn("STOP", "#FFCDD2", "ScorePage").pack(pady=5)
        style_btn("ADD", "#E6FFC1", "SongbookPage").pack(pady=5)
        style_btn("SKIP", "#E1F5FE", "LyricsPage").pack(pady=5)

    def refresh_score(self):
        self.score_label.config(text=str(random.randint(80, 100)))

if __name__ == "__main__":
    app = KaraOKApp()
    app.mainloop()

