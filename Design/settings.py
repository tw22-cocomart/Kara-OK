import tkinter as tk
import ctypes

# Windows API constant for title bar color
DWMWA_CAPTION_COLOR = 35

def create_app():
    root = tk.Tk()
    root.title("Kara-OK!")
    root.geometry("1100x700")
    root.configure(bg="white")

    # --- THE COLORS ---
    primary_blue = "#4A61E1"
    button_bg = "#E6FFC1"
    nav_blue = "#2c3e8c"
    
    # --- TITLE BAR COLOR LOGIC ---
    try:
        root.update()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        title_color = 0xE1614A  
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_CAPTION_COLOR, ctypes.byref(ctypes.c_int(title_color)), 4
        )
    except Exception as e:
        print(f"Title bar color not supported: {e}")

    # --- FONTS ---
    font_style = ("Courier New", 11, "bold")
    header_font = ("Courier New", 18, "bold")

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

    # --- MAIN CONTENT ---
    content_area = tk.Frame(root, bg="white")
    content_area.pack(fill="both", expand=True)

    # Sidebar - MODIFIED to use relative width for auto-scaling
    # It now takes up 28% of the window width (relwidth=0.28)
    sidebar = tk.Frame(content_area, bg="#f2f2f2")
    sidebar.place(relx=0, rely=0, relwidth=0.28, relheight=1)

    # Center-aligned Profile Content
    profile_box = tk.Frame(sidebar, bg="#7f8c8d", width=160, height=160)
    profile_box.pack(pady=(60, 15))

    tk.Label(sidebar, text="John Python", bg="#f2f2f2", font=("Courier New", 14, "bold")).pack()
    tk.Label(sidebar, text="@pythonprogramz", bg="#f2f2f2", fg="grey", font=("Courier New", 11)).pack()
    
    tk.Button(sidebar, text="logout", fg=primary_blue, bg="#f2f2f2", 
              bd=0, font=("Courier New", 11, "underline"), cursor="hand2").pack(side="bottom", pady=40)

    # Form Area - MODIFIED to start where the sidebar ends (relx=0.28)
    form_frame = tk.Frame(content_area, bg="white", padx=50)
    form_frame.place(relx=0.28, rely=0, relwidth=0.72, relheight=1)

    tk.Label(
        form_frame, text="USER PROFILE", 
        font=header_font, fg=primary_blue, bg="white"
    ).pack(pady=(60, 40))

    def create_input(label_text, default_val):
        row = tk.Frame(form_frame, bg="white")
        row.pack(fill="x", pady=12, padx=(0, 50))
        
        tk.Label(row, text=label_text, font=font_style, fg=primary_blue, 
                 bg="white", width=12, anchor="e").pack(side="left", padx=15)
        
        entry = tk.Entry(row, font=("Courier New", 12), bd=0, 
                         highlightthickness=1, highlightbackground=primary_blue, 
                         highlightcolor=primary_blue)
        entry.insert(0, default_val)
        entry.pack(side="left", fill="x", expand=True, ipady=8)

    create_input("Name", "John Python")
    create_input("Username", "pythonprogramz")
    create_input("Email", "pythonprogrammingz")
    create_input("Password", "**********")

    tk.Button(
        form_frame, text="Save Changes", font=font_style, 
        fg=primary_blue, bg=button_bg, activebackground="#D7F7A0",
        relief="groove", bd=1, padx=50, pady=10, cursor="hand2"
    ).pack(pady=40)

    root.mainloop()

if __name__ == "__main__":
    create_app()


