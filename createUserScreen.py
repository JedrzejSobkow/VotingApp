import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import bcrypt
from firebase_communication import check_email_exists, add_new_user_to_db



def show_create_user_screen(container, app_controller):
    # Usuwanie poprzednich widżetów w kontenerze
    for widget in container.winfo_children():
        widget.destroy()

    container.configure(bg="#d3a9d3")

    # Nagłówek
    tk.Label(container, text="Aplikacja do głosowania", font=("Arial", 18, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
    tk.Label(container, text="dodaj nowego użytkownika", font=("Arial", 14), bg="#d3a9d3").pack(pady=(0, 15))

    # Formularz dodawania użytkownika
    form_frame = tk.Frame(container, bg="#d3a9d3")
    form_frame.pack(padx=20, pady=10, fill="x")

    # Pole na imię i nazwisko
    tk.Label(form_frame, text="Imię i nazwisko:", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
    name_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    name_entry.grid(row=0, column=1, pady=5)

    # Pole na e-mail
    tk.Label(form_frame, text="E-mail:", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
    email_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    email_entry.grid(row=1, column=1, pady=5)

    # Pole na hasło
    tk.Label(form_frame, text="Hasło:", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
    password_entry = tk.Entry(form_frame, font=("Arial", 12), width=30, show="*")
    password_entry.grid(row=2, column=1, pady=5)

    # Pole na numer telefonu
    tk.Label(form_frame, text="Numer telefonu:", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=3, column=0, sticky="w", pady=5)
    phone_entry = tk.Entry(form_frame, font=("Arial", 12), width=30)
    phone_entry.grid(row=3, column=1, pady=5)

    # Pole wyboru roli
    tk.Label(form_frame, text="Rola:", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=4, column=0, sticky="w", pady=5)
    role_var = tk.StringVar()
    role_dropdown = ttk.Combobox(form_frame, textvariable=role_var, font=("Arial", 12), state="readonly", width=28)
    role_dropdown["values"] = ["admin", "user", "host"]
    role_dropdown.grid(row=4, column=1, pady=5)

    # Przycisk ZAPISZ i ANULUJ
    action_buttons_frame = tk.Frame(container, bg="#d3a9d3")
    action_buttons_frame.pack(pady=(20, 10))

    tk.Button(action_buttons_frame, text="ZAPISZ", font=("Arial", 14), bg="#c49bd6", width=15, 
              command=lambda: save_new_user(name_entry.get(), email_entry.get(), password_entry.get(), phone_entry.get(), role_var.get(), app_controller)).pack(side="left", padx=10)

    tk.Button(action_buttons_frame, text="ANULUJ", font=("Arial", 14), bg="#c49bd6", width=15, 
              command=lambda: app_controller.switch_to("main")).pack(side="right", padx=10)

# Funkcja zapisania nowego użytkownika

def save_new_user(name, email, password, phone, role, app_controller):
    """Zapisuje nowego użytkownika pośrednio przez firebase_communication."""
    if not (name and email and password and phone and role):
        messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione!")
        return

    # Sprawdzenie, czy email już istnieje
    if check_email_exists(email):
        messagebox.showerror("Błąd", "Użytkownik z tym adresem email już istnieje!")
        return

    # Hashowanie hasła
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Dodanie użytkownika do bazy danych
    add_new_user_to_db(name, email, hashed_password, phone, role)

    # Wyświetlenie komunikatu o sukcesie
    messagebox.showinfo("Sukces", f"Nowy użytkownik został dodany: {name}")

    # Powrót do poprzedniego ekranu
    app_controller.switch_to("main")