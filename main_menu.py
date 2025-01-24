import tkinter as tk
from tkinter import messagebox

class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja do głosowania - Menu główne")
        self.geometry("600x400")
        self.configure(bg="#d3a9d3")

        self.create_widgets()

    def create_widgets(self):
        # Tytuł aplikacji
        tk.Label(self, text="Aplikacja do głosowania", font=("Arial", 16, "bold"), bg="#d3a9d3").pack(pady=10)

        # Kontener na przyciski
        button_frame = tk.Frame(self, bg="#d3a9d3")
        button_frame.pack(pady=20)

        # Przyciski menu w układzie dwie kolumny, jeden na dole
        button_config = {
            "font": ("Arial", 12),
            "width": 25,
            "height": 2,
            "relief": "raised"
        }

        # Lewa kolumna
        left_frame = tk.Frame(button_frame, bg="#d3a9d3")
        left_frame.grid(row=0, column=0, padx=10, pady=10)
        tk.Button(left_frame, text="Pokaż głosowania oczekujące", command=self.show_pending_votes, bg="#c49bd6", **button_config).pack(pady=10)
        tk.Button(left_frame, text="Konfiguruj przypomnienia", command=self.configure_reminders, bg="#c49bd6", **button_config).pack(pady=10)

        # Prawa kolumna
        right_frame = tk.Frame(button_frame, bg="#d3a9d3")
        right_frame.grid(row=0, column=1, padx=10, pady=10)
        tk.Button(right_frame, text="Utwórz nowe głosowanie", command=self.create_new_vote, bg="#c49bd6", **button_config).pack(pady=10)
        tk.Button(right_frame, text="Przeglądaj wyniki", command=self.view_results, bg="#c49bd6", **button_config).pack(pady=10)

        # Dolny przycisk
        tk.Button(self, text="Zarządzaj kontami użytkowników", command=self.manage_users, bg="#f3a1b4", **button_config).pack(pady=20)

    def show_pending_votes(self):
        messagebox.showinfo("Akcja", "Pokaż głosowania oczekujące na głos - funkcja w budowie")

    def create_new_vote(self):
        messagebox.showinfo("Akcja", "Utwórz nowe głosowanie - funkcja w budowie")

    def configure_reminders(self):
        messagebox.showinfo("Akcja", "Konfiguruj przypomnienia - funkcja w budowie")

    def view_results(self):
        messagebox.showinfo("Akcja", "Przeglądaj wyniki - funkcja w budowie")

    def manage_users(self):
        messagebox.showinfo("Akcja", "Zarządzaj kontami użytkowników - funkcja w budowie")

if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
