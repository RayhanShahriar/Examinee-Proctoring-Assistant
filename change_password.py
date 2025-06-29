import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
import sqlite3


conn = sqlite3.connect("users.db")
cursor = conn.cursor()


class ChangePasswordPage:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.logged_in_user = logged_in_user
        self.root.title("Change Password")
        self.root.configure(bg="#1E1F3B")

        self.show_change_password_screen()

    def show_change_password_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        Label(
            self.root,
            text="Change Password",
            font=("Helvetica", 18, "bold"),
            bg="#1E1F3B",
            fg="#F4D35E",
        ).pack(pady=20)

        Label(
            self.root,
            text="Current Password:",
            font=("Helvetica", 12),
            bg="#1E1F3B",
            fg="#B3B6D3",
        ).pack(pady=5)
        self.current_password_entry = Entry(
            self.root, show="*", font=("Helvetica", 12), width=25
        )
        self.current_password_entry.pack(pady=5)

        Label(
            self.root,
            text="New Password:",
            font=("Helvetica", 12),
            bg="#1E1F3B",
            fg="#B3B6D3",
        ).pack(pady=5)
        self.new_password_entry = Entry(
            self.root, show="*", font=("Helvetica", 12), width=25
        )
        self.new_password_entry.pack(pady=5)

        change_button = Button(
            self.root,
            text="Change Password",
            command=self.change_password,
            font=("Helvetica", 14, "bold"),
            bg="#3AA17E",
            fg="white",
            relief="flat",
            activebackground="#2F8764",
        )
        change_button.pack(pady=20)

        back_button = Button(
            self.root,
            text="Back",
            command=self.go_back,
            font=("Helvetica", 12),
            bg="#D9534F",
            fg="white",
            relief="flat",
            activebackground="#C64540",
        )
        back_button.pack(pady=10)

    def change_password(self):
        current_password = self.current_password_entry.get()
        new_password = self.new_password_entry.get()

       
        cursor.execute(
            "SELECT * FROM users WHERE username = ? AND password = ?",
            (self.logged_in_user, current_password),
        )
        user = cursor.fetchone()

        if user:
           
            cursor.execute(
                "UPDATE users SET password = ? WHERE username = ?",
                (new_password, self.logged_in_user),
            )
            conn.commit()
            messagebox.showinfo("Success", "Password changed successfully!")
            self.go_back()
        else:
            messagebox.showerror("Error", "Current password is incorrect.")

    def go_back(self):
        from menu import MenuPage

        self.clear_frame()
        MenuPage(self.root, self.logged_in_user)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
