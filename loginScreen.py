import tkinter as tk
from tkinter import messagebox
from firebase_communication import login_user
import bcrypt

def show_login_screen(root, app_controller):
    """
    Displays the login screen.

    Args:
        root (tk.Tk): The main application container.
        app_controller (AppController): The application controller for managing screen transitions.
    """
    def on_login_click():
        """
        Handles the user login action when the button is clicked.
        Retrieves data from the input fields and passes it to the Firebase login function.
        """
        email = email_entry.get()
        password = password_entry.get()

        if email and password:
            login_user(email, password, app_controller)
        else:
            messagebox.showwarning("Błąd", "Uzupełnij wszystkie pola.")

    # Clear existing widgets in the main container
    for widget in root.winfo_children():
        widget.destroy()

    # Create login screen elements
    tk.Label(root, text="Zaloguj się", font=("Arial", 20, "bold"), bg="#d9b3ff", fg="black").pack(pady=10)
    tk.Label(root, text="E-mail", bg="#d9b3ff", fg="black").pack(pady=5)
    email_entry = tk.Entry(root, width=30)
    email_entry.pack(pady=5)

    tk.Label(root, text="Hasło", bg="#d9b3ff", fg="black").pack(pady=5)
    password_entry = tk.Entry(root, show="*", width=30)
    password_entry.pack(pady=5)

    login_button = tk.Button(root, text="Zaloguj się", command=on_login_click, bg="#9b6fbf", fg="white", width=20)
    login_button.pack(pady=20)
