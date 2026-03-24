import tkinter as tk
import ctypes
import random

# Windows constant for title bar color
DWMWA_CAPTION_COLOR = 35

def create_karaoke_player():
    root = tk.Tk()
    root.title("KARA-OK!")
    root.geometry("1150x750")
    root.configure(bg="white")

    # --- DEFINE STYLES (Fixed: These were missing or using 'self') ---
    nav_blue = "#2c3e8c"
    font_style = ("Courier New", 12, "bold")
    current_random_score = random.randint(80, 100)

    # --- TITLE BAR COLOR ---
    try:
        root.update()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        title_color = 0xE1614A  # Blue theme
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_CAPTION_COLOR, ctypes.byref(ctypes.c_int(title_color)), 4
        )
    except Exception: pass

    # --- NAVIGATION HEADER (Fixed: Removed 'self' and used 'root') ---
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

    # --- MAIN CONTENT ---
    content_container = tk.Frame(root, bg="white", padx=30, pady=20)
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
    
    tk.Label(video_box, text=str(current_random_score), fg="#FFFF99", bg="black", 
             font=("Courier New", 80, "bold")).place(relx=0.5, rely=0.55, anchor="center")
    
    tk.Label(video_box, text="Not Bad!", fg="white", bg="black", 
             font=("Courier New", 32, "bold")).place(relx=0.5, rely=0.8, anchor="center")

    # --- RIGHT SIDEBAR: CONTROLS ---
    right_sidebar = tk.Frame(lower_content, bg="white", width=180)
    right_sidebar.pack(side="right", fill="y", padx=(20, 0))
    
    btn_container = tk.Frame(right_sidebar, bg="white")
    btn_container.pack(side="bottom")

    def style_btn(text, bg_color):
        return tk.Button(btn_container, text=text, font=("Courier New", 12, "bold"), 
                         bg=bg_color, fg="#2c3e8c", width=12, pady=10, relief="flat", 
                         highlightthickness=1, highlightbackground="#448AFF", cursor="hand2")

    style_btn("STOP", "#FFCDD2").pack(pady=5)
    style_btn("ADD", "#E6FFC1").pack(pady=5)
    style_btn("SKIP", "#E1F5FE").pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    create_karaoke_player()