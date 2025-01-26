import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from firebase_communication import get_users, delete_user

def show_manage_users_screen(container, app_controller):
    # Usuwanie poprzednich widżetów w kontenerze
    for widget in container.winfo_children():
        widget.destroy()

    container.configure(bg="#d3a9d3")

    # Nagłówek
    tk.Label(container, text="Aplikacja do głosowania", font=("Arial", 18, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
    tk.Label(container, text="zarządzaj użytkownikami", font=("Arial", 14), bg="#d3a9d3").pack(pady=(0, 15))

    # Lista użytkowników
    users_frame = tk.Frame(container, bg="#d3a9d3")
    users_frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Pobieranie użytkowników z Firebase
    users = get_users()  # Zmieniono, aby pobierać dane z Firebase

    # Pasek przewijania
    canvas = tk.Canvas(users_frame, bg="#d3a9d3", highlightthickness=0)
    scrollbar = ttk.Scrollbar(users_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#d3a9d3")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Tworzenie widżetów dla użytkowników
    for user in users:
        user_frame = tk.Frame(scrollable_frame, bg="#d3a9d3")
        user_frame.pack(fill="x", pady=5, padx=5)

        tk.Label(user_frame, text="👤", font=("Arial", 14), bg="#d3a9d3").pack(side="left", padx=5)
        tk.Label(user_frame, text=user["name"], font=("Arial", 12), bg="#d3a9d3").pack(side="left", padx=10)
        tk.Label(user_frame, text=user["role"], font=("Arial", 12), bg="#d3a9d3").pack(side="left", padx=10)

        # Sprawdzenie, czy nie próbujemy usunąć aktualnie zalogowanego użytkownika
        if user["id"] == app_controller.userId:
            # Jeśli użytkownik jest aktualnie zalogowany, wyświetl tylko informację, bez opcji usunięcia
            tk.Label(user_frame, text="(Nie możesz usunąć swojego konta)", font=("Arial", 10), bg="#d3a9d3", fg="red").pack(side="right", padx=5)
        else:
            # Ikony akcji - przycisk do usunięcia
            tk.Button(user_frame, text="🗑", font=("Arial", 12), bg="#d3a9d3", command=lambda u=user: confirm_delete_user(u["id"], app_controller)).pack(side="right", padx=5)

    # Dodaj nowego użytkownika
    add_user_frame = tk.Frame(scrollable_frame, bg="#d3a9d3")
    add_user_frame.pack(fill="x", pady=5, padx=5)

    tk.Button(add_user_frame, text="+", font=("Arial", 14), bg="#d3a9d3", command=lambda: app_controller.switch_to("userCreation")).pack(side="left", padx=5)

    # Przycisk ZAPISZ i ANULUJ
    action_buttons_frame = tk.Frame(container, bg="#d3a9d3")
    action_buttons_frame.pack(pady=(20, 10))

    tk.Button(action_buttons_frame, text="POWRÓT", font=("Arial", 14), bg="#c49bd6", width=15, command=lambda: app_controller.switch_to("main")).pack(side="right", padx=10)

# Funkcja potwierdzenia przed usunięciem użytkownika
def confirm_delete_user(user_id, app_controller):
    # Potwierdzenie przed usunięciem
    if user_id == app_controller.userId:
        # Nie pozwalamy na usunięcie aktualnie zalogowanego użytkownika
        messagebox.showerror("Błąd", "Nie możesz usunąć swojego konta!")
    else:
        # Potwierdzenie usunięcia użytkownika
        confirm = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tego użytkownika?")
        if confirm:
            delete_user(user_id)
            messagebox.showinfo("Sukces", "Użytkownik został usunięty.")
            show_manage_users_screen(app_controller.switch_to("userManagement"), app_controller)  # Odświeżenie ekranu
