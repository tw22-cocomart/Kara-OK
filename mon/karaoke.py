import tkinter as tk
from PIL import Image, ImageTk  # Required for handling images
import vlc
import os

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

        # --- VIDEO AREA (LOCAL VIDEO PLAYER) ---

        video_box = tk.Frame(left_frame, bg="black", highlightbackground="#448AFF", highlightthickness=2)
        video_box.pack(pady=(10, 10), fill="both", expand=True)

        video_panel = tk.Frame(video_box, bg="black")
        video_panel.pack(fill="both", expand=True)

        # ===============================
        # FIX VLC DLL PATH
        # ===============================
        vlc_path = r"C:\Program Files\VideoLAN\VLC"
        os.environ['PATH'] = vlc_path + ";" + os.environ['PATH']

        # ===============================
        # VLC SETUP
        # ===============================
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # 🎬 Video file
        base_dir = os.path.dirname(os.path.abspath(__file__))
        video_path = os.path.join(base_dir, "sample.mp4")

        print("Loading video:", video_path)

        if not os.path.exists(video_path):
            tk.Label(video_panel, text=f"❌ File not found:\n{video_path}",
                    fg="white", bg="black").pack(expand=True)
        else:
            media = self.instance.media_new(video_path)
            self.player.set_media(media)

            self.root.update_idletasks()
            handle = video_panel.winfo_id()

            if os.name == "nt":
                self.player.set_hwnd(handle)
            else:
                self.player.set_xwindow(handle)

            self.player.play()

        # ===============================
        # CONTROLS
        # ===============================
        controls = tk.Frame(video_box, bg="#222")
        controls.pack(fill="x")

        tk.Button(controls, text="▶ Play", command=self.player.play).pack(side="left", padx=5)
        tk.Button(controls, text="⏸ Pause", command=self.player.pause).pack(side="left", padx=5)
        tk.Button(controls, text="⏹ Stop", command=self.player.stop).pack(side="left", padx=5)

        # ===============================
        # KARAOKE TEXT
        # ===============================
        overlay_text = tk.Label(video_box,
            text="28830 | My Heart Will Go On | Celine Dion",
            fg="yellow", bg="black",
            font=("Courier", 14, "bold")
        )
        overlay_text.place(relx=0.5, rely=0.9, anchor="center")

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
