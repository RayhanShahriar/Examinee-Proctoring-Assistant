from tkinter import Label, Button
from proctoring import ProctoringApp
from recordings import RecordingsPage
from alerts import AlertsPage
from login_signup import LoginSignupApp
from change_password import ChangePasswordPage  


class MenuPage:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.logged_in_user = logged_in_user
        self.root.title("Examinee Proctoring Assistant - Menu")
        self.root.geometry("800x600")
        self.root.configure(bg="#1E1F3B")

        self.show_menu()

    def show_menu(self):
        self.clear_frame()

        for i in range(7):  
            self.root.grid_rowconfigure(i, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        Label(
            self.root,
            text=f"Logged in as: {self.logged_in_user}",
            bg="#1E1F3B",
            fg="#B3B6D3",
            font=("Helvetica", 12),
        ).grid(row=0, column=0, pady=10, sticky="n")

        Label(
            self.root,
            text="Welcome to the Examinee Proctoring Assistant",
            bg="#1E1F3B",
            fg="#F4D35E",
            font=("Helvetica", 20, "bold"),
        ).grid(row=1, column=0, pady=20, sticky="n")

        button_options = {
            "font": ("Helvetica", 16, "bold"),
            "width": 20,
            "height": 2,
            "relief": "flat",
            "fg": "white",
        }

        proctoring_button = Button(
            self.root,
            text="Proctoring",
            command=self.open_proctoring,
            bg="#3AA17E",
            activebackground="#2F8764",
            **button_options,
        )
        proctoring_button.grid(row=2, column=0, pady=10, sticky="n")

        recordings_button = Button(
            self.root,
            text="Recordings",
            command=self.open_recordings,
            bg="#3A6EA1",
            activebackground="#2F5487",
            **button_options,
        )
        recordings_button.grid(row=3, column=0, pady=10, sticky="n")

        alerts_button = Button(
            self.root,
            text="Alerts",
            command=self.open_alerts,
            bg="#F4A259",
            activebackground="#D97A33",
            **button_options,
        )
        alerts_button.grid(row=4, column=0, pady=10, sticky="n")

        change_password_button = Button(
            self.root,
            text="Change Password",
            command=self.open_change_password,
            bg="#FFC107",
            activebackground="#FFB300",
            **button_options,
        )
        change_password_button.grid(row=5, column=0, pady=10, sticky="n")

        logout_button = Button(
            self.root,
            text="Logout",
            command=self.logout,
            bg="#D9534F",
            activebackground="#C64540",
            **button_options,
        )
        logout_button.grid(row=6, column=0, pady=20, sticky="n")

    def open_proctoring(self):
        self.clear_frame()
        ProctoringApp(self.root, self.logged_in_user)

    def open_recordings(self):
        self.clear_frame()
        RecordingsPage(self.root, self.logged_in_user)

    def open_alerts(self):
        self.clear_frame()
        AlertsPage(self.root, self.logged_in_user)

    def open_change_password(self):
        self.clear_frame()
        ChangePasswordPage(self.root, self.logged_in_user)

    def logout(self):
        self.clear_frame()
        LoginSignupApp(self.root)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
