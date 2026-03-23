import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import hashlib

# ===============================
# HASH FUNCTION
# ===============================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ===============================
# DATABASE CONNECTION
# ===============================
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="karaoke_system"
        )
        return connection
    except Error as e:
        messagebox.showerror("Database Error", str(e))
        return None


# ===============================
# MAIN APP
# ===============================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("User System")
        self.root.geometry("400x300")
        self.show_login()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ===========================
    # SIGNUP
    # ===========================
    def show_signup(self):
        self.clear()

        tk.Label(self.root, text="Signup", font=("Arial", 16)).pack(pady=10)

        username = tk.Entry(self.root)
        email = tk.Entry(self.root)
        password = tk.Entry(self.root, show="*")

        tk.Label(self.root, text="Username").pack()
        username.pack()

        tk.Label(self.root, text="Email").pack()
        email.pack()

        tk.Label(self.root, text="Password").pack()
        password.pack()

        def register():
            conn = create_connection()
            if not conn:
                return

            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                    (username.get(), email.get(), hash_password(password.get()))
                )
                conn.commit()
                messagebox.showinfo("Success", "Account created!")
                self.show_login()
            except Error as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.root, text="Signup", command=register).pack(pady=10)
        tk.Button(self.root, text="Go to Login", command=self.show_login).pack()

    # ===========================
    # LOGIN
    # ===========================
    def show_login(self):
        self.clear()

        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        email = tk.Entry(self.root)
        password = tk.Entry(self.root, show="*")

        tk.Label(self.root, text="Email").pack()
        email.pack()

        tk.Label(self.root, text="Password").pack()
        password.pack()

        def login_user():
            conn = create_connection()
            if not conn:
                return

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email.get(),))
            user = cursor.fetchone()

            if user and user['password'] == hash_password(password.get()):
                messagebox.showinfo("Success", "Login successful")
                self.show_profile(user)
            else:
                messagebox.showerror("Error", "Invalid credentials")

        tk.Button(self.root, text="Login", command=login_user).pack(pady=10)
        tk.Button(self.root, text="Go to Signup", command=self.show_signup).pack()

    # ===========================
    # PROFILE
    # ===========================
    def show_profile(self, user):
        self.clear()

        tk.Label(self.root, text="Profile", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text=f"Username: {user['username']}").pack()
        tk.Label(self.root, text=f"Email: {user['email']}").pack()

        tk.Button(self.root, text="Logout", command=self.show_login).pack(pady=20)


# ===============================
# RUN APP
# ===============================
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
