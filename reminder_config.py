import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

class ReminderConfigScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja do głosowania - Konfiguracja powiadomień")
        self.geometry("700x500")
        self.configure(bg="#d3a9d3")

        self.create_widgets()

    def create_widgets(self):
        # Tytuł aplikacji
        tk.Label(self, text="Aplikacja do głosowania", font=("Arial", 18, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
        tk.Label(self, text="konfiguracja powiadomień", font=("Arial", 14), bg="#d3a9d3").pack(pady=(0, 15))

        # Główna ramka
        frame = tk.Frame(self, bg="#d3a9d3")
        frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Interwał przypomnień
        tk.Label(frame, text="Interwał przypomnień (liczba dni)", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=0, column=0, sticky="w", pady=5)
        self.interval_entry = tk.Entry(frame, font=("Arial", 12), width=20)
        self.interval_entry.grid(row=0, column=1, pady=5, padx=10)

        # Data pierwszego powiadomienia
        tk.Label(frame, text="Kiedy wysłać pierwsze powiadomienie", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=1, column=0, sticky="w", pady=5)
        self.start_date = DateEntry(frame, font=("Arial", 12), width=18, date_pattern="dd.mm.yyyy")
        self.start_date.grid(row=1, column=1, pady=5, padx=10)

        # Data ostatniego powiadomienia
        tk.Label(frame, text="Kiedy wysłać ostatnie powiadomienie", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=2, column=0, sticky="w", pady=5)
        self.end_date = DateEntry(frame, font=("Arial", 12), width=18, date_pattern="dd.mm.yyyy")
        self.end_date.grid(row=2, column=1, pady=5, padx=10)

        # Metoda powiadomień
        tk.Label(frame, text="Metoda powiadomień", font=("Arial", 12), bg="#d3a9d3", anchor="w").grid(row=3, column=0, sticky="w", pady=5)
        self.method_combobox = ttk.Combobox(frame, font=("Arial", 12), values=["SMS", "E-mail", "SMS, E-mail"], state="readonly", width=18)
        self.method_combobox.grid(row=3, column=1, pady=5, padx=10)
        self.method_combobox.current(0)

        # Przyciski na dole
        button_frame = tk.Frame(self, bg="#d3a9d3")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Dodaj", command=self.add_reminder, font=("Arial", 14), bg="#c49bd6", width=15).pack(side="left", padx=20)
        tk.Button(button_frame, text="Anuluj", command=self.cancel, font=("Arial", 14), bg="#f3a1b4", width=15).pack(side="left", padx=20)

    def add_reminder(self):
        interval = self.interval_entry.get()
        start_date = self.start_date.get_date()
        end_date = self.end_date.get_date()
        method = self.method_combobox.get()

        if not interval or not interval.isdigit():
            messagebox.showerror("Błąd", "Proszę podać prawidłowy interwał dni.")
            return

        if start_date > end_date:
            messagebox.showerror("Błąd", "Data pierwszego powiadomienia nie może być późniejsza niż ostatniego.")
            return

        messagebox.showinfo("Sukces", f"Przypomnienie zostało dodane:\nInterwał: {interval} dni\nOd: {start_date}\nDo: {end_date}\nMetoda: {method}")

    def cancel(self):
        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz anulować?"):
            self.destroy()

if __name__ == "__main__":
    app = ReminderConfigScreen()
    app.mainloop()
