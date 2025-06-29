import tkinter as tk
from tkinter import Label, Text, Button
import os

ALERTS_DIR = "alerts"


if not os.path.exists(ALERTS_DIR):
    os.makedirs(ALERTS_DIR)

def get_all_alerts():
    """Retrieve all alert messages from the alerts directory."""
    alerts = []
    for alert_filename in os.listdir(ALERTS_DIR):
        alert_path = os.path.join(ALERTS_DIR, alert_filename)
        if os.path.isfile(alert_path):
            with open(alert_path, 'r') as alert_file:
                alerts.append(alert_file.read())
    return alerts


class AlertsPage:
    def __init__(self, root, logged_in_user):
        self.root = root
        self.logged_in_user = logged_in_user
        self.root.title("Examinee Proctoring Assistant - Alerts")
        self.root.geometry("800x600")
        self.bg_color = "#2E2F5B"  
        self.label_color = "#F4D35E"  
        self.button_bg_color = "#505581"  
        self.button_fg_color = "#FFFFFF"  

        self.show_alerts()

    def show_alerts(self):
        self.clear_frame()
        self.root.configure(bg=self.bg_color)

       
        title_label = Label(
            self.root,
            text="Alerts",
            font=("Helvetica", 20),
            bg=self.bg_color,
            fg=self.label_color,
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

       
        self.alert_log_area = Text(
            self.root, height=20, width=80, bg="#FFFFFF", fg="#000000"
        )
        self.alert_log_area.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    
        return_button = Button(
            self.root,
            text="Back",
            command=self.return_to_menu,
            bg="#D9534F",
            fg=self.button_fg_color,
            font=("Helvetica", 14),
        )
        return_button.grid(row=2, column=0, pady=10)

      
        delete_button = Button(
            self.root,
            text="Delete Alerts",
            command=self.delete_alerts,
            bg="#FF5733",
            fg=self.button_fg_color,
            font=("Helvetica", 14),
        )
        delete_button.grid(row=2, column=1, pady=10)

        
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        
        self.load_alerts()

    def load_alerts(self):
        alerts = get_all_alerts() 
        if not alerts:
            self.alert_log_area.insert(tk.END, "No alerts found.\n")
        else:
            for alert in alerts:
                self.alert_log_area.insert(tk.END, f"{alert}\n")

    def delete_alerts(self):
        """Clear all the alerts from the text area and delete from the file system."""
        self.alert_log_area.delete(1.0, tk.END)
        
        for alert_filename in os.listdir(ALERTS_DIR):
            alert_path = os.path.join(ALERTS_DIR, alert_filename)
            if os.path.isfile(alert_path):
                os.remove(alert_path)

    def return_to_menu(self):
        from menu import MenuPage

        MenuPage(self.root, self.logged_in_user)

    def refresh_alerts(self):
        """Refresh the displayed alerts."""
        self.alert_log_area.delete(1.0, tk.END)
        self.load_alerts()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
