import tkinter as tk
import ctypes

# This constant is used by the Windows API to target the title bar color
DWMWA_CAPTION_COLOR = 35

def create_app():
    root = tk.Tk()
    root.title("Kara-OK!")
    root.geometry("600x700")
    root.configure(bg="white")

    # --- THE TITLE BAR COLOR LOGIC ---
    # This works on Windows 10 (build 22000+) and Windows 11
    try:
        root.update() # Required so the window has a handle (HWND)
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        # Color is in 0x00BBGGRR format (Hex reversed)
        title_color = 0xE1614A  # Hex for #4A61E1 reversed
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_CAPTION_COLOR, ctypes.byref(ctypes.c_int(title_color)), 4
        )
    except Exception as e:
        print(f"Title bar color not supported on this OS: {e}")

    # --- UI STYLING ---
    primary_blue = "#4A61E1"
    button_bg = "#E6FFC1"
    font_style = ("Courier New", 12, "bold")
    header_font = ("Courier New", 18, "bold")

    main_frame = tk.Frame(root, bg="white", padx=50, pady=20)
    main_frame.pack(expand=True)

    tk.Label(
        main_frame, text="CREATE AN ACCOUNT", 
        font=header_font, fg=primary_blue, bg="white"
    ).pack(pady=(0, 20))

    def create_input_field(label_text, is_password=False):
        tk.Label(
            main_frame, text=label_text, font=font_style, 
            fg=primary_blue, bg="white", anchor="w"
        ).pack(fill="x", pady=(10, 2))
        
        entry = tk.Entry(
            main_frame, font=("Courier New", 12), bd=0, 
            highlightthickness=1, highlightbackground=primary_blue, 
            highlightcolor=primary_blue, relief="flat",
            show="*" if is_password else ""
        )
        entry.pack(fill="x", ipady=8)
        return entry

    create_input_field("Email")
    create_input_field("Username")
    create_input_field("Password", is_password=True)
    create_input_field("Confirm Password", is_password=True)

    tk.Button(
        main_frame, text="Register", font=font_style, 
        fg=primary_blue, bg=button_bg, activebackground="#D7F7A0",
        relief="groove", bd=1, padx=40, pady=5, cursor="hand2"
    ).pack(pady=40)

    root.mainloop()

if __name__ == "__main__":
    create_app()