import tkinter as tk
from tkinter import ttk

class ViewResultsScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja do głosowania - Przeglądaj wyniki")
        self.geometry("800x600")
        self.configure(bg="#d3a9d3")

        self.create_widgets()

    def create_widgets(self):
        # Tytuł aplikacji
        tk.Label(self, text="Aplikacja do głosowania", font=("Arial", 18, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
        tk.Label(self, text="przeglądaj wyniki", font=("Arial", 14), bg="#d3a9d3").pack(pady=(0, 15))

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
            {"title": "Wybór prezydenta LIDL", "date": "12.11.2024"},
            {"title": "Głosowanie nad datą spotkania", "date": "12.10.2024"},
            {"title": "Głosowanie nad datą wykładu", "date": "12.12.2024"},
        ]

        for poll in polls:
            poll_frame = tk.Frame(scrollable_frame, bg="#f4c2f3", pady=10, padx=15, relief="groove", borderwidth=3)
            poll_frame.pack(fill="x", pady=10, padx=5)

            tk.Label(poll_frame, text=poll["title"], font=("Arial", 14, "bold"), bg="#f4c2f3", anchor="w").grid(row=0, column=0, sticky="w")
            tk.Label(poll_frame, text=f"do: {poll['date']}", font=("Arial", 12), bg="#f4c2f3", anchor="w").grid(row=1, column=0, sticky="w")

        # Przyciski nawigacyjne
        button_frame = tk.Frame(self, bg="#d3a9d3")
        button_frame.pack(pady=(20, 10))

        tk.Button(button_frame, text="Wróć", command=self.go_back, font=("Arial", 14), bg="#c49bd6", width=15).pack(side="left", padx=20)
        tk.Button(button_frame, text="Podgląd", command=self.show_poll_results, font=("Arial", 14), bg="#f3a1b4", width=15).pack(side="left", padx=20)

    def go_back(self):
        print("Wróć - funkcja w budowie")

    def show_poll_results(self):
        self.withdraw()
        PollResultScreen(self).mainloop()

class PollResultScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Aplikacja do głosowania - Wyniki")
        self.geometry("700x500")
        self.configure(bg="#d3a9d3")

        self.create_widgets()

    def create_widgets(self):
        # Tytuł wyników
        tk.Label(self, text="Aplikacja do głosowania", font=("Arial", 18, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
        tk.Label(self, text="przeglądaj wyniki", font=("Arial", 14), bg="#d3a9d3").pack(pady=(0, 15))

        # Szczegóły głosowania
        details_frame = tk.Frame(self, bg="#d3a9d3")
        details_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(details_frame, text="Tytuł: Wybór prezydenta LIDL", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")
        tk.Label(details_frame, text="Dostępne do: 12.12.2024", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")
        tk.Label(details_frame, text="Autor: Jędrzej Sobków", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")
        tk.Label(details_frame, text="Stan głosowania: 9/13", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")

        # Wyniki głosowania
        result_frame = tk.Frame(self, bg="#d3a9d3")
        result_frame.pack(padx=20, pady=20, fill="x")

        results = [
            {"candidate": "Michał Mazgis", "percentage": "22.22%", "bg": "#ff9999"},
            {"candidate": "Maciej Praczuk", "percentage": "55.56%", "bg": "#99ff99"},
            {"candidate": "Bohdan Pivtorak", "percentage": "22.22%", "bg": "#ff9999"},
        ]

        for result in results:
            tk.Frame(result_frame, bg=result["bg"]).pack(fill="x", pady=5, padx=5)
            tk.Label(result_frame, text=f"{result['candidate']} - {result['percentage']}", font=("Arial", 12), bg=result["bg"], anchor="w").pack(fill="x", pady=2, padx=10)

        # Przycisk powrotu
        tk.Button(self, text="POWRÓT", command=self.go_back, font=("Arial", 14), bg="#c49bd6", width=15).pack(pady=20)

    def go_back(self):
        self.destroy()
        self.master.deiconify()

if __name__ == "__main__":
    app = ViewResultsScreen()
    app.mainloop()
