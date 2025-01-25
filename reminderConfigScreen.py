import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from firebase_communication import update_voting_with_reminder

def show_reminder_config_screen(root, app_controller):
    """Funkcja do wyświetlania ekranu konfiguracji powiadomień."""
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Aplikacja do głosowania - Konfiguracja powiadomień")
    root.geometry("700x500")
    root.configure(bg="#d3a9d3")

    # Tytuł aplikacji
    tk.Label(root, text="Aplikacja do głosowania", font=("Arial", 18, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
    tk.Label(root, text="konfiguracja powiadomień", font=("Arial", 14), bg="#d3a9d3").pack(pady=(0, 15))

    # Główna ramka
    frame = tk.Frame(root, bg="#d3a9d3")
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    # Interwał przypomnień
    tk.Label(frame, text="Interwał przypomnień (liczba dni)", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
    interval_entry = tk.Entry(frame, font=("Arial", 12), width=20)
    interval_entry.grid(row=0, column=1, pady=5, padx=10)

    # Data pierwszego powiadomienia
    tk.Label(frame, text="Kiedy wysłać pierwsze powiadomienie", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
    start_date = DateEntry(frame, font=("Arial", 12), width=18, date_pattern="dd.mm.yyyy")
    start_date.grid(row=1, column=1, pady=5, padx=10)

    # Data ostatniego powiadomienia
    tk.Label(frame, text="Kiedy wysłać ostatnie powiadomienie", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
    end_date = DateEntry(frame, font=("Arial", 12), width=18, date_pattern="dd.mm.yyyy")
    end_date.grid(row=2, column=1, pady=5, padx=10)

    # Metoda powiadomień
    tk.Label(frame, text="Metoda powiadomień", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=3, column=0, sticky="w", pady=5)
    method_combobox = ttk.Combobox(frame, font=("Arial", 12), values=["SMS", "E-mail", "SMS, E-mail"], state="readonly", width=18)
    method_combobox.grid(row=3, column=1, pady=5, padx=10)
    method_combobox.current(0)

    # Przyciski na dole
    button_frame = tk.Frame(root, bg="#d3a9d3")
    button_frame.pack(pady=20)

    # Dodanie przycisków
    tk.Button(button_frame, text="Dodaj", command=lambda: add_reminder(interval_entry, start_date, end_date, method_combobox, app_controller), font=("Arial", 14), bg="#c49bd6", width=15).pack(side="left", padx=20)
    tk.Button(button_frame, text="Anuluj", command=lambda: cancel(root, app_controller), font=("Arial", 14), bg="#f3a1b4", width=15).pack(side="left", padx=20)

def add_reminder(interval_entry, start_date, end_date, method_combobox, app_controller):
    """Obsługuje dodawanie przypomnienia."""
    interval = interval_entry.get()
    start_date_val = start_date.get_date().strftime("%d.%m.%Y")
    start_date = start_date.get_date()

    end_date_val = end_date.get_date().strftime("%d.%m.%Y")
    end_date = end_date.get_date()
    method = method_combobox.get()

    if not interval or not interval.isdigit():
        messagebox.showerror("Błąd", "Proszę podać prawidłowy interwał dni.")
        return

    if start_date > end_date:
        messagebox.showerror("Błąd", "Data pierwszego powiadomienia nie może być późniejsza niż ostatniego.")
        return

    messagebox.showinfo("Sukces", f"Przypomnienie zostało dodane:\nInterwał: {interval} dni\nOd: {start_date_val}\nDo: {end_date_val}\nMetoda: {method}")
    # TODO INTERVAL VALIDATION
    update_voting_with_reminder(int(interval), str(start_date_val), str(end_date_val), method, app_controller.chosenVotingId)
    app_controller.switch_to("main")


def cancel(root, app_controller):
    """Obsługuje anulowanie konfiguracji."""
    if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz anulować?"):
        app_controller.switch_to("main")
