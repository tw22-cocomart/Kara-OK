import tkinter as tk
from PIL import Image, ImageTk 
import ctypes

# Windows constant for title bar color
DWMWA_CAPTION_COLOR = 35

def create_karaoke_player():
    root = tk.Tk()
    root.title("Kara-OK!")
    root.geometry("1150x700")
    root.configure(bg="white")

    # Define styles used in the app
    nav_blue = "#2c3e8c"
    font_style = ("Courier New", 12, "bold")

    # --- PRIMARY BLUE TITLE BAR ---
    try:
        root.update()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        title_color = 0xE1614A  # #4A61E1 reversed for Windows BGR
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_CAPTION_COLOR, ctypes.byref(ctypes.c_int(title_color)), 4
        )
    except Exception: pass

    # --- NAVIGATION HEADER ---
    nav_frame = tk.Frame(root, bg=nav_blue, height=45)
    nav_frame.pack(fill="x")
    nav_frame.pack_propagate(False)

    tabs = ["Home", "Karaoke", "SongBook", "Settings"]
    for tab in tabs:
        tk.Button(
            nav_frame, text=tab, bg=nav_blue, fg="white", 
            font=font_style, bd=0, padx=20, activebackground="#3d51b3", 
            activeforeground="white", cursor="hand2"
        ).pack(side="left", fill="y")

    # --- MAIN CONTENT CONTAINER ---
    content_container = tk.Frame(root, bg="white", padx=30, pady=20)
    content_container.pack(fill="both", expand=True)

    # --- TOP HEADER (Spanning full width) ---
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

    # TV Screen Display (Left Side)
    tv_section = tk.Frame(lower_content, bg="white")
    tv_section.pack(side="left", expand=True, fill="both")

    video_box = tk.Frame(tv_section, bg="black", highlightthickness=2, highlightbackground="#448AFF")
    video_box.pack(fill="both", expand=True)

    # --- IMAGE AND LYRIC OVERLAY SECTION ---
    try:
        # Load and resize the background image
        img = Image.open("lyrics_screen.jpg")
        img = img.resize((850, 500), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        
        display = tk.Label(video_box, image=photo, bg="black")
        display.image = photo # Keep reference
        display.pack(expand=True, fill="both")
        
        # 1. BLUE LYRIC OVERLAY (Middle Center)
        lyrics = tk.Label(
            display, 
            text="Every night in my dreams,\nI see you, I feel you", 
            fg="white", 
            bg="#2c3e8c", 
            font=("Courier New", 20, "bold"),
            padx=20,
            pady=10
        )
        lyrics.place(relx=0.5, rely=0.75, anchor="center")

        # 2. YELLOW SONG INFO OVERLAY (Bottom Center) - ADDED THIS PART
        overlay_text = tk.Label(
            display, 
            text="28830 | My Heart Will Go On | Celine Dion", 
            fg="yellow", 
            bg="black", 
            font=("Courier New", 14, "bold"),
            padx=10
        )
        overlay_text.place(relx=0.5, rely=0.92, anchor="center")

    except Exception as e:
        tk.Label(video_box, text=f"TV MONITOR SCREEN\nImage Not Found\n{e}", 
                 fg="white", bg="black", font=("Courier New", 16)).pack(expand=True)

    # --- RIGHT SIDEBAR: CONTROLS ---
    right_sidebar = tk.Frame(lower_content, bg="white", width=180)
    right_sidebar.pack(side="right", fill="y", padx=(20, 0))
    
    tk.Frame(right_sidebar, bg="white").pack(expand=True, fill="both")

    btn_container = tk.Frame(right_sidebar, bg="white")
    btn_container.pack(side="bottom")

    def style_btn(text, bg, fg):
        return tk.Button(btn_container, text=text, font=("Courier New", 12, "bold"), 
                         bg=bg, fg=fg, width=12, pady=10, relief="flat", 
                         highlightthickness=1, highlightbackground="#448AFF", cursor="hand2")

    style_btn("STOP", "#FFCDD2", "#C62828").pack(pady=5)
    style_btn("ADD", "#E6FFC1", "#558B2F").pack(pady=5)
    style_btn("SKIP", "#E1F5FE", "#1565C0").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_karaoke_player()