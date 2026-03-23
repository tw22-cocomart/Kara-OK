import tkinter as tk
from PIL import Image, ImageTk  # Required for handling images

class KaraOKApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kara-OK!")
        self.root.geometry("950x600")
        self.root.configure(bg="#CCEEFF")

        # --- Top Navigation Bar ---
        nav_bar = tk.Frame(self.root, bg="#283593", height=45)
        nav_bar.pack(fill="x", side="top")
        
        for item in ["Home", "Karaoke", "SongBook", "Settings"]:
            btn = tk.Button(nav_bar, text=item, bg="#283593", fg="white", 
                            font=("Courier", 11, "bold"), bd=0, padx=20, cursor="hand2")
            btn.pack(side="left", pady=8)

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
            # UPDATED: Using the specific filename of your uploaded image
            # Make sure this file is in the same folder as your .py script!
            original_img = Image.open(r"C:\Users\Kaye Visera\OneDrive\Documents\songbook\songbook.jpg") 
            
            # Resize image to fit the frame
            resized_img = original_img.resize((550, 350), Image.Resampling.LANCZOS)
            self.bg_image = ImageTk.PhotoImage(resized_img)
            
            video_display = tk.Label(video_box, image=self.bg_image, bg="black")
            video_display.pack(expand=True, fill="both")
            
            # Overlay text on top of the image (Adjusted rely to 0.9 to stay at bottom)
            overlay_text = tk.Label(video_display, text="28830 | My Heart Will Go On | Celine Dion", 
                                   fg="yellow", bg="black", font=("Courier", 14, "bold"),
                                   highlightthickness=0, bd=0)
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