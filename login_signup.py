import tkinter as tk
from tkinter import Label, Button, Entry, messagebox
import os
import sqlite3
import PIL.Image as Image
import PIL.ImageTk as ImageTk

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        full_name TEXT,
        email TEXT,
        phone TEXT
    )
""")
conn.commit()


class LoginSignupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EPA-Login")
        self.root.geometry("800x600")
        self.root.config(bg="#2E2F5B")
        self.show_login_screen()

    def show_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

     
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        login_frame = tk.Frame(self.root, bg="#2E2F5B")
        login_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        for i in range(8):
            login_frame.grid_rowconfigure(i, weight=1)
        login_frame.grid_columnconfigure(1, weight=1)

        image_path = os.path.join("images", "login_images.png")
        self.image = Image.open(image_path)
        self.image = self.image.resize((200, 200), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_label = Label(login_frame, image=self.image_tk, bg="#2E2F5B")
        self.image_label.grid(row=0, column=0, rowspan=6, padx=20, pady=10, sticky="n")

        Label(
            login_frame,
            text="Login",
            font=("Helvetica", 22, "bold"),
            bg="#2E2F5B",
            fg="#F4D35E",
        ).grid(row=0, column=1, pady=10, sticky="w")
        Label(
            login_frame,
            text="Username:",
            font=("Helvetica", 12),
            bg="#2E2F5B",
            fg="#F4D35E",
        ).grid(row=1, column=1, sticky="w")
        self.username_entry = Entry(
            login_frame,
            font=("Helvetica", 12),
            bg="#FAF0CA",
            fg="#000000",
            relief="flat",
            bd=2,
        )
        self.username_entry.grid(
            row=2, column=1, padx=10, pady=5, ipady=5, ipadx=10, sticky="ew"
        )

        Label(
            login_frame,
            text="Password:",
            font=("Helvetica", 12),
            bg="#2E2F5B",
            fg="#F4D35E",
        ).grid(row=3, column=1, sticky="w")
        self.password_entry = Entry(
            login_frame,
            show="*",
            font=("Helvetica", 12),
            bg="#FAF0CA",
            fg="#000000",
            relief="flat",
            bd=2,
        )
        self.password_entry.grid(
            row=4, column=1, padx=10, pady=5, ipady=5, ipadx=10, sticky="ew"
        )

        self.login_button = Button(
            login_frame,
            text="Login",
            command=self.login,
            font=("Helvetica", 14),
            bg="#505581",
            fg="white",
            activebackground="#43496C",
            activeforeground="white",
            relief="flat",
        )
        self.login_button.grid(row=5, column=1, pady=20, ipadx=10, ipady=5, sticky="ew")

        self.signup_button = Button(
            login_frame,
            text="Don't have an account? Signup",
            command=self.show_signup_screen,
            font=("Helvetica", 10),
            bg="#505581",
            fg="white",
            activebackground="#43496C",
            activeforeground="white",
            relief="flat",
        )
        self.signup_button.grid(row=6, column=1, pady=10, sticky="ew")

        self.forgot_password_button = Button(
            login_frame,
            text="Forgot Password?",
            command=self.show_forgot_password_screen,
            font=("Helvetica", 10),
            bg="#505581",
            fg="white",
            activebackground="#43496C",
            activeforeground="white",
            relief="flat",
        )
        self.forgot_password_button.grid(row=7, column=1, pady=10, sticky="ew")

    def show_forgot_password_screen(self):
        self.clear_frame()
        from forgotpassword import ForgotPasswordPage

        ForgotPasswordPage(self.root)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        user = cursor.fetchone()

        if user:
            logged_in_user = username
            from menu import MenuPage

            self.clear_frame()
            MenuPage(self.root, logged_in_user)
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    def show_signup_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        signup_frame = tk.Frame(self.root, bg="#2E2F5B")
        signup_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        for i in range(8):
            signup_frame.grid_rowconfigure(i, weight=1)
            signup_frame.grid_columnconfigure(1, weight=1)

        image_path = os.path.join("images", "login_image.png")
        self.image = Image.open(image_path)
        self.image = self.image.resize((200, 200), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_label = Label(signup_frame, image=self.image_tk, bg="#2E2F5B")
        self.image_label.grid(row=0, column=0, rowspan=6, padx=20, pady=10, sticky="n")

        Label(
            signup_frame,
            text="Signup",
            font=("Helvetica", 22, "bold"),
            bg="#2E2F5B",
            fg="#F4D35E",
        ).grid(row=0, column=1, pady=10, sticky="w")

        # Additional fields for signup
        Label(
            signup_frame,
            text="Full Name:",
            font=("Helvetica", 12),
            bg="#2E2F5B",
            fg="#F4D35E",
        ).grid(row=1, column=1, sticky="w")
        self.signup_full_name_entry = Entry(
            signup_frame,
            font=("Helvetica", 12),
            bg="#FAF0CA",
            fg="#000000",
            relief="flat",
            bd=2,
        )
        self.signup_full_name_entry.grid(
            row=2, column=1, padx=10, pady=5, ipady=5, ipadx=10, sticky="ew"
        )

        Label(
            signup_frame,
            text="Username:",
            font=("Helvetica", 12),
            bg="#2E2F5B",
            fg="#F4D35E",
        ).grid(row=3, column=1, sticky="w")
        self.signup_username_entry = Entry(
            signup_frame,
            font=("Helvetica", 12),
            bg="#FAF0CA",
            fg="#000000",
            relief="flat",
            bd=2,
        )
        self.signup_username_entry.grid(
            row=4, column=1, padx=10, pady=5, ipady=5, ipadx=10, sticky="ew"
        )

        Label(
            signup_frame,
            text="Password:",
            font=("Helvetica", 12),
            bg="#2E2F5B",
            fg="#F4D35E",
        ).grid(row=5, column=1, sticky="w")
        self.signup_password_entry = Entry(
            signup_frame,
            show="*",
            font=("Helvetica", 12),
            bg="#FAF0CA",
            fg="#000000",
            relief="flat",
            bd=2,
        )
        self.signup_password_entry.grid(
            row=6, column=1, padx=10, pady=5, ipady=5, ipadx=10, sticky="ew"
        )

        Label(
            signup_frame,
            text="Email:",
            font=("Helvetica", 12),
            bg="#2E2F5B",
            fg="#F4D35E",
        ).grid(row=7, column=1, sticky="w")
        self.signup_email_entry = Entry(
            signup_frame,
            font=("Helvetica", 12),
            bg="#FAF0CA",
            fg="#000000",
            relief="flat",
            bd=2,
        )
        self.signup_email_entry.grid(
            row=8, column=1, padx=10, pady=5, ipady=5, ipadx=10, sticky="ew"
        )

        Label(
            signup_frame,
            text="Phone:",
            font=("Helvetica", 12),
            bg="#2E2F5B",
            fg="#F4D35E",
        ).grid(row=9, column=1, sticky="w")
        self.signup_phone_entry = Entry(
            signup_frame,
            font=("Helvetica", 12),
            bg="#FAF0CA",
            fg="#000000",
            relief="flat",
            bd=2,
        )
        self.signup_phone_entry.grid(
            row=10, column=1, padx=10, pady=5, ipady=5, ipadx=10, sticky="ew"
        )

        # Signup and back buttons
        self.signup_button = Button(
            signup_frame,
            text="Signup",
            command=self.signup,
            font=("Helvetica", 14),
            bg="#505581",
            fg="white",
            activebackground="#43496C",
            activeforeground="white",
            relief="flat",
        )
        self.signup_button.grid(
            row=11, column=1, pady=20, ipadx=10, ipady=5, sticky="ew"
        )

        Button(
            signup_frame,
            text="Back to Login",
            command=self.show_login_screen,
            font=("Helvetica", 10),
            bg="#505581",
            fg="white",
            activebackground="#43496C",
            activeforeground="white",
            relief="flat",
        ).grid(row=12, column=1, pady=10, sticky="ew")

    def signup(self):
        full_name = self.signup_full_name_entry.get()
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()
        email = self.signup_email_entry.get()
        phone = self.signup_phone_entry.get()

        try:
            cursor.execute(
                "INSERT INTO users (username, password, full_name, email, phone) VALUES (?, ?, ?, ?, ?)",
                (username, password, full_name, email, phone),
            )
            conn.commit()
            messagebox.showinfo("Success", "Account created successfully!")
            self.show_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LoginSignupApp(root)
    root.mainloop()
