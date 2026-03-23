import tkinter as tk
from PIL import Image, ImageTk 
import ctypes

# Windows constant for title bar color
DWMWA_CAPTION_COLOR = 35

class KaraOKApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kara-OK!")
        self.root.geometry("950x600")
        self.root.configure(bg="#CCEEFF")

        # Define missing variables
        nav_blue = "#283593"
        font_style = ("Courier New", 11, "bold")

        # --- THE TITLE BAR COLOR LOGIC ---
        try:
            self.root.update()
            hwnd = ctypes.windll.user32.GetParent(self.root.winfo_id())
            title_color = 0xE1614A  # #4A61E1 reversed
            ctypes.windll.dwmapi.DwmSetWindowAttribute(
                hwnd, DWMWA_CAPTION_COLOR, ctypes.byref(ctypes.c_int(title_color)), 4
            )
        except Exception as e:
            print(f"Title bar color not supported: {e}")

        # --- NAVIGATION HEADER (Now correctly indented inside __init__) ---
        nav_frame = tk.Frame(self.root, bg=nav_blue, height=45)
        nav_frame.pack(fill="x")
        nav_frame.pack_propagate(False)

        tabs = ["Home", "Karaoke", "SongBook", "Settings"]
        for tab in tabs:
            tk.Button(
                nav_frame, text=tab, bg=nav_blue, fg="white", 
                font=font_style, bd=0, padx=20, activebackground="#3d51b3", 
                activeforeground="white", cursor="hand2"
            ).pack(side="left", fill="y")

        # --- Main Layout Container ---
        main_container = tk.Frame(self.root, bg="#CCEEFF")
        main_container.pack(expand=True, fill="both", padx=15, pady=15)

        # Left Column (Video & Queue)
        left_frame = tk.Frame(main_container, bg="#CCEEFF")
        left_frame.pack(side="left", expand=True, fill="both")

        # --- IMAGE / VIDEO AREA ---
        video_box = tk.Frame(left_frame, bg="black", highlightbackground="#448AFF", highlightthickness=2)
        video_box.pack(pady=(10, 10), fill="both", expand=True)

        try:
            # Note: Ensure this path is correct for your specific computer
            original_img = Image.open(r"C:\Users\Kaye Visera\OneDrive\Documents\songbook\songbook.jpg") 
            resized_img = original_img.resize((550, 350), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized_img)
            
            video_display = tk.Label(video_box, image=self.bg_image, bg="black")
            video_display.pack(expand=True, fill="both")
            
            overlay_text = tk.Label(video_display, text="28830 | My Heart Will Go On | Celine Dion", 
                                   fg="yellow", bg="black", font=("Courier", 14, "bold"))
            overlay_text.place(relx=0.5, rely=0.9, anchor="center")
            
        except Exception as e:
            tk.Label(video_box, text=f"Image Not Found\n{e}", fg="white", bg="black").pack(expand=True)

        # Song Queue
        queue_frame = tk.Frame(left_frame, bg="white", bd=1, relief="solid")
        queue_frame.pack(fill="x", pady=10)
        tk.Label(queue_frame, text="Song Queue: 28830, 10596, 1421, 17304", 
                 bg="white", fg="#283593", font=("Courier", 10), pady=15).pack()

        # Right Column (Keypad)
        right_frame = tk.Frame(main_container, bg="white", width=320, bd=1, relief="solid")
        right_frame.pack(side="right", fill="y", padx=(15, 0))
        right_frame.pack_propagate(False)

        # Input Display
        self.entry_var = tk.StringVar(value="")
        input_entry = tk.Entry(right_frame, textvariable=self.entry_var, font=("Courier", 14), 
                               fg="#283593", bd=1, relief="solid", justify="center")
        input_entry.pack(pady=30, padx=25, fill="x")
        
        # Keypad
        keypad_frame = tk.Frame(right_frame, bg="white")
        keypad_frame.pack()

        buttons = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'DEL', '0', 'RES']
        r, c = 0, 0
        for b in buttons:
            color = "#E1F5FE"
            if b == "DEL": color = "#FFCDD2"
            if b == "RES": color = "#DCEDC8"
            
            btn = tk.Button(keypad_frame, text=b, width=7, height=2, bg=color, 
                            font=("Courier", 10, "bold"), command=lambda x=b: self.press(x))
            btn.grid(row=r, column=c, padx=4, pady=4)
            c+=1
            if c>2: c=0; r+=1

    def press(self, key):
        if key == "DEL":
            self.entry_var.set(self.entry_var.get()[:-1])
        elif key == "RES":
            print(f"Reserving: {self.entry_var.get()}")
            self.entry_var.set("")
        else:
            self.entry_var.set(self.entry_var.get() + key)

if __name__ == "__main__":
    root = tk.Tk()
    app = KaraOKApp(root)
    root.mainloop()