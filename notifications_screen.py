import tkinter as tk
from tkinter import ttk

class NotificationsScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja do głosowania - Konfiguracja powiadomień")
        self.geometry("450x600")
        self.configure(bg="#d3a9d3")

        self.create_widgets()

    def create_widgets(self):
        # Tytuł aplikacji
        tk.Label(self, text="Aplikacja do głosowania", font=("Arial", 18, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
        tk.Label(self, text="konfiguracja powiadomień", font=("Arial", 14), bg="#d3a9d3").pack(pady=(0, 15))

        # Kontener na listę głosowań
        list_frame = tk.Frame(self, bg="#d3a9d3")
        list_frame.pack(padx=20, pady=10, fill="both", expand=True)

        canvas = tk.Canvas(list_frame, bg="#d3a9d3", highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#d3a9d3")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Dodaj dane do listy
        polls = [
            {"title": "Wybór prezydenta LIDL", "date": "12.12.2024", "votes": "9/13"},
            {"title": "Głosowanie nad datą spotkania", "date": "12.12.2024", "votes": "12/22"},
            {"title": "Głosowanie nad datą wykładu", "date": "12.12.2024", "votes": "12/22"},
            {"title": "Kto prowadzącym wykładu", "date": "21.11.2025", "votes": "12/12"},
        ]

        for poll in polls:
            poll_frame = tk.Frame(scrollable_frame, bg="#f4c2f3", pady=10, padx=15, relief="groove", borderwidth=3)
            poll_frame.pack(fill="x", pady=10, padx=5)

            tk.Label(poll_frame, text=poll["title"], font=("Arial", 14, "bold"), bg="#f4c2f3", anchor="w").grid(row=0, column=0, sticky="w")
            tk.Label(poll_frame, text=f"do: {poll['date']}   |   zagłosowało {poll['votes']}", font=("Arial", 12), bg="#f4c2f3", anchor="w").grid(row=1, column=0, sticky="w")

        # Przyciski nawigacyjne
        button_frame = tk.Frame(self, bg="#d3a9d3")
        button_frame.pack(pady=(20, 10))

        tk.Button(button_frame, text="Wróć", command=self.go_back, font=("Arial", 14), bg="#c49bd6", width=15, height=2).pack(side="left", padx=20)
        tk.Button(button_frame, text="Konfiguruj", command=self.configure_notifications, font=("Arial", 14), bg="#f3a1b4", width=15, height=2).pack(side="left", padx=20)

    def go_back(self):
        print("Wróć - funkcja w budowie")

    def configure_notifications(self):
        print("Konfiguruj - funkcja w budowie")

if __name__ == "__main__":
    app = NotificationsScreen()
    app.mainloop()
