import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from firebase_communication import update_voting_with_reminder

def show_reminder_config_screen(root, app_controller):
    """
    Display the screen for configuring reminder settings for voting.

    This function allows the user to configure:
    - The interval (in days) between reminders.
    - The date for sending the first reminder.
    - The date for sending the last reminder.
    - The method of sending reminders (SMS, E-mail, or both).

    Parameters:
        root (tk.Tk): The root Tkinter window where the reminder configuration screen will be displayed.
        app_controller (object): The application controller that manages user interactions and screen transitions.

    Returns:
        None
    """
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Aplikacja do głosowania - Konfiguracja powiadomień")
    root.geometry("700x500")
    root.configure(bg="#d3a9d3")

    tk.Label(root, text="Aplikacja do głosowania", font=("Arial", 18, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
    tk.Label(root, text="konfiguracja powiadomień", font=("Arial", 14), bg="#d3a9d3").pack(pady=(0, 15))

    frame = tk.Frame(root, bg="#d3a9d3")
    frame.pack(padx=20, pady=10, fill="both", expand=True)

    tk.Label(frame, text="Interwał przypomnień (liczba dni)", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
    interval_entry = tk.Entry(frame, font=("Arial", 12), width=20)
    interval_entry.grid(row=0, column=1, pady=5, padx=10)

    tk.Label(frame, text="Kiedy wysłać pierwsze powiadomienie", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
    start_date = DateEntry(frame, font=("Arial", 12), width=18, date_pattern="dd.mm.yyyy")
    start_date.grid(row=1, column=1, pady=5, padx=10)

    tk.Label(frame, text="Kiedy wysłać ostatnie powiadomienie", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
    end_date = DateEntry(frame, font=("Arial", 12), width=18, date_pattern="dd.mm.yyyy")
    end_date.grid(row=2, column=1, pady=5, padx=10)

    tk.Label(frame, text="Metoda powiadomień", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=3, column=0, sticky="w", pady=5)
    method_combobox = ttk.Combobox(frame, font=("Arial", 12), values=["SMS", "E-mail", "SMS, E-mail"], state="readonly", width=18)
    method_combobox.grid(row=3, column=1, pady=5, padx=10)
    method_combobox.current(0)

    button_frame = tk.Frame(root, bg="#d3a9d3")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Dodaj", command=lambda: add_reminder(interval_entry, start_date, end_date, method_combobox, app_controller), font=("Arial", 14), bg="#c49bd6", width=15).pack(side="left", padx=20)
    tk.Button(button_frame, text="Anuluj", command=lambda: cancel(root, app_controller), font=("Arial", 14), bg="#f3a1b4", width=15).pack(side="left", padx=20)

def add_reminder(interval_entry, start_date, end_date, method_combobox, app_controller):
    """
    Add a reminder to the selected voting by validating and sending the reminder configuration.

    This function:
    - Validates the input fields (interval, start date, end date, and notification method).
    - Sends the reminder configuration to the Firebase database if valid.
    - Displays success or error messages based on input validation.

    Parameters:
        interval_entry (tk.Entry): The entry widget for the interval (in days) between reminders.
        start_date (tkcalendar.DateEntry): The DateEntry widget for selecting the start date.
        end_date (tkcalendar.DateEntry): The DateEntry widget for selecting the end date.
        method_combobox (ttk.Combobox): The combobox widget for selecting the notification method (SMS, E-mail, or both).
        app_controller (object): The application controller that manages the current voting and screen transitions.

    Returns:
        None
    """
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
    """
    Cancel the reminder configuration process and return to the main screen.

    This function displays a confirmation dialog before switching to the main screen if the user decides to cancel the configuration.

    Parameters:
        root (tk.Tk): The root Tkinter window where the reminder configuration screen is displayed.
        app_controller (object): The application controller responsible for managing screen transitions.

    Returns:
        None
    """
    if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz anulować?"):
        app_controller.switch_to("main")
