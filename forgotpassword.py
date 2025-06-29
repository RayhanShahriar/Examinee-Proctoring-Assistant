import tkinter as tk
from tkinter import Label, Button, Entry, messagebox
import sqlite3


conn = sqlite3.connect("users.db")
cursor = conn.cursor()


class ForgotPasswordPage:
    def __init__(self, root):
        self.root = root
        self.root.title("Forgot Password")
        self.root.geometry("500x400")
        self.root.config(bg="#2E2F5B")
        self.show_forgot_password_screen()

    def show_forgot_password_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(
            self.root,
            text="Forgot Password",
            font=("Helvetica", 22, "bold"),
            bg="#2E2F5B",
            fg="#F4D35E",
        ).pack(pady=10)

        
        Label(
            self.root,
            text="Enter your Username or Email:",
            font=("Helvetica", 12),
            bg="#2E2F5B",
            fg="#F4D35E",
        ).pack(pady=5)
        self.username_email_entry = Entry(
            self.root,
            font=("Helvetica", 12),
            bg="#FAF0CA",
            fg="#000000",
            relief="flat",
            bd=2,
        )
        self.username_email_entry.pack(pady=5, ipadx=10, ipady=5)

     
        Label(
            self.root,
            text="Enter New Password:",
            font=("Helvetica", 12),
            bg="#2E2F5B",
            fg="#F4D35E",
        ).pack(pady=5)
        self.new_password_entry = Entry(
            self.root,
            show="*",
            font=("Helvetica", 12),
            bg="#FAF0CA",
            fg="#000000",
            relief="flat",
            bd=2,
        )
        self.new_password_entry.pack(pady=5, ipadx=10, ipady=5)

        Label(
            self.root,
            text="Confirm New Password:",
            font=("Helvetica", 12),
            bg="#2E2F5B",
            fg="#F4D35E",
        ).pack(pady=5)
        self.confirm_password_entry = Entry(
            self.root,
            show="*",
            font=("Helvetica", 12),
            bg="#FAF0CA",
            fg="#000000",
            relief="flat",
            bd=2,
        )
        self.confirm_password_entry.pack(pady=5, ipadx=10, ipady=5)

       
        Button(
            self.root,
            text="Reset Password",
            command=self.reset_password,
            font=("Helvetica", 14),
            bg="#505581",
            fg="white",
            relief="flat",
        ).pack(pady=20, ipadx=10, ipady=5)

 
        Button(
            self.root,
            text="Back to Login",
            command=self.go_back_to_login,
            font=("Helvetica", 10),
            bg="#505581",
            fg="white",
            relief="flat",
        ).pack(pady=10)

    def reset_password(self):
        username_or_email = self.username_email_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        cursor.execute(
            "SELECT * FROM users WHERE username = ? OR email = ?",
            (username_or_email, username_or_email),
        )
        user = cursor.fetchone()

        if user:
            cursor.execute(
                "UPDATE users SET password = ? WHERE id = ?", (new_password, user[0])
            )
            conn.commit()
            messagebox.showinfo("Success", "Password reset successfully!")
            self.go_back_to_login()
        else:
            messagebox.showerror("Error", "Username or email not found.")

    def go_back_to_login(self):
        self.root.destroy()
        from login_signup import LoginSignupApp

        root = tk.Tk()
        LoginSignupApp(root)
        root.mainloop()
