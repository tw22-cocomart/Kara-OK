import tkinter as tk
import ctypes

# Windows API constant for title bar color
DWMWA_CAPTION_COLOR = 35

def create_login_app():
    root = tk.Tk()
    root.title("Kara-OK!")
    root.geometry("500x550")
    root.configure(bg="white")

    # --- TITLE BAR COLOR (Windows Only) ---
    try:
        root.update()
        hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
        # Hex for #4A61E1 reversed to BGR format: 0xE1614A
        title_color = 0xE1614A  
        ctypes.windll.dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_CAPTION_COLOR, ctypes.byref(ctypes.c_int(title_color)), 4
        )
    except Exception as e:
        print(f"Title bar color not supported: {e}")

    # --- UI STYLING ---
    primary_blue = "#4A61E1"
    button_lime = "#E6FFC1"
    font_mono = ("Courier New", 12, "bold")
    header_font = ("Courier New", 18, "bold")

    # Main Center Container
    main_frame = tk.Frame(root, bg="white", padx=40)
    main_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Header: LOG IN
    tk.Label(
        main_frame, text="LOG IN", 
        font=header_font, fg=primary_blue, bg="white"
    ).pack(pady=(0, 30))

    # Helper function for input fields
    def create_input_field(label_text, is_password=False):
        tk.Label(
            main_frame, text=label_text, font=font_mono, 
            fg=primary_blue, bg="white", anchor="w"
        ).pack(fill="x", pady=(10, 2))
        
        # Entry with the specific blue border
        entry = tk.Entry(
            main_frame, font=("Courier New", 12), bd=0, 
            highlightthickness=1, 
            highlightbackground=primary_blue, 
            highlightcolor=primary_blue, 
            relief="flat",
            show="*" if is_password else ""
        )
        entry.pack(fill="x", ipady=10, ipadx=10)
        return entry

    # Input Fields (Matching your new image)
    create_input_field("Username")
    create_input_field("Password", is_password=True)

    # Log In Button (With the lime/yellow gradient look)
    login_btn = tk.Button(
        main_frame, 
        text="Log In", 
        font=font_mono, 
        fg=primary_blue, 
        bg=button_lime, 
        activebackground="#D7F7A0", # Slightly darker lime when clicked
        relief="groove", 
        bd=1, 
        highlightbackground=primary_blue,
        padx=50, 
        pady=5, 
        cursor="hand2"
    )
    login_btn.pack(pady=40)

    root.mainloop()

if __name__ == "__main__":
    create_login_app()