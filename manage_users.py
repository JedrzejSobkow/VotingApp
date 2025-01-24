import tkinter as tk
from tkinter import ttk

class ManageUsersScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja do głosowania - Zarządzaj użytkownikami")
        self.geometry("800x600")
        self.configure(bg="#d3a9d3")

        self.create_widgets()

    def create_widgets(self):
        # Tytuł aplikacji
        tk.Label(self, text="Aplikacja do głosowania", font=("Arial", 18, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
        tk.Label(self, text="zarządzaj użytkownikami", font=("Arial", 14), bg="#d3a9d3").pack(pady=(0, 15))

        # Lista użytkowników
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

        # Przykładowi użytkownicy
        users = [
            {"name": "Jędrzej Sobków", "role": "organizator"},
            {"name": "Michał Kułacz", "role": "głosujący"},
            {"name": "Nadal Zawalny", "role": "organizator"},
            {"name": "Gorbacz Michal", "role": "organizator"},
        ]

        for user in users:
            user_frame = tk.Frame(scrollable_frame, bg="#f4c2f3", pady=5, padx=10, relief="groove", borderwidth=2)
            user_frame.pack(fill="x", pady=5, padx=5)

            tk.Label(user_frame, text=user["name"], font=("Arial", 12), bg="#f4c2f3", anchor="w", width=30).grid(row=0, column=0, sticky="w")
            tk.Label(user_frame, text=user["role"], font=("Arial", 12), bg="#f4c2f3", anchor="w", width=15).grid(row=0, column=1, sticky="w")

            tk.Button(user_frame, text="🗑️", command=lambda u=user: self.delete_user(u), font=("Arial", 12), bg="#f3a1b4", width=4).grid(row=0, column=2, padx=5)
            tk.Button(user_frame, text="✏️", command=lambda u=user: self.edit_user(u), font=("Arial", 12), bg="#c49bd6", width=4).grid(row=0, column=3, padx=5)

        # Dodaj użytkownika
        tk.Button(scrollable_frame, text="+", command=self.add_user, font=("Arial", 14), bg="#99cc99", width=4).pack(anchor="w", pady=10, padx=5)

        # Przyciski na dole
        button_frame = tk.Frame(self, bg="#d3a9d3")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="ZAPISZ", command=self.save_changes, font=("Arial", 14), bg="#c49bd6", width=15).pack(side="left", padx=20)
        tk.Button(button_frame, text="ANULUJ", command=self.cancel_changes, font=("Arial", 14), bg="#f3a1b4", width=15).pack(side="left", padx=20)

    def delete_user(self, user):
        print(f"Usunięto użytkownika: {user['name']}")

    def edit_user(self, user):
        print(f"Edytowano użytkownika: {user['name']}")

    def add_user(self):
        print("Dodano nowego użytkownika")

    def save_changes(self):
        print("Zapisano zmiany")

    def cancel_changes(self):
        print("Anulowano zmiany")

if __name__ == "__main__":
    app = ManageUsersScreen()
    app.mainloop()
