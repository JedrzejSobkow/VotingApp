import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import Calendar


class CreateVoteScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplikacja do głosowania - Stwórz głosowanie")
        self.geometry("500x600")
        self.configure(bg="#d3a9d3")

        self.create_widgets()

    def create_widgets(self):
        # Tytuł aplikacji
        tk.Label(self, text="Aplikacja do głosowania", font=("Arial", 16, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
        tk.Label(self, text="stwórz głosowanie", font=("Arial", 12), bg="#d3a9d3").pack(pady=(0, 10))

        # Sekcja tytułu głosowania
        tk.Label(self, text="Tytuł głosowania", font=("Arial", 10), bg="#d3a9d3").pack(anchor="w", padx=20)
        self.title_entry = tk.Entry(self, width=40, font=("Arial", 12))
        self.title_entry.pack(pady=5, padx=20)

        # Pytania i odpowiedzi
        tk.Label(self, text="Pytania i odpowiedzi", font=("Arial", 10), bg="#d3a9d3").pack(anchor="w", padx=20)
        self.questions_frame = tk.Frame(self, bg="#d3a9d3")
        self.questions_frame.pack(fill="both", padx=20, pady=5)

        self.add_question_button = tk.Button(self.questions_frame, text="+ Dodaj pytanie", command=self.add_question,
                                             bg="#c0d890", font=("Arial", 10))
        self.add_question_button.pack(pady=5, anchor="w")

        # Data zakończenia
        tk.Label(self, text="Data końca głosowania", font=("Arial", 10), bg="#d3a9d3").pack(anchor="w", padx=20,
                                                                                            pady=(10, 0))
        self.date_button = tk.Button(self, text="Wybierz datę", command=self.open_calendar, bg="#c0d890",
                                     font=("Arial", 10))
        self.date_button.pack(pady=5, padx=20)
        self.selected_date_label = tk.Label(self, text="Nie wybrano daty", bg="#d3a9d3", font=("Arial", 10))
        self.selected_date_label.pack(pady=5)

        # Anonimowe checkbox
        self.is_anonymous = tk.BooleanVar()
        tk.Checkbutton(self, text="Anonimowe", variable=self.is_anonymous, bg="#d3a9d3", font=("Arial", 10)).pack(
            anchor="w", padx=20)

        # Przyciski akcji
        button_frame = tk.Frame(self, bg="#d3a9d3")
        button_frame.pack(pady=20)

        tk.Button(button_frame, text="Dodaj", bg="#c49bd6", font=("Arial", 12), command=self.submit).pack(side="left",
                                                                                                          padx=10)
        tk.Button(button_frame, text="Anuluj", bg="#f3a1b4", font=("Arial", 12), command=self.cancel).pack(side="left",
                                                                                                           padx=10)

    def add_question(self):
        question_frame = tk.Frame(self.questions_frame, bg="#d3a9d3")
        question_frame.pack(fill="x", pady=5)

        question_entry = tk.Entry(question_frame, width=30, font=("Arial", 10))
        question_entry.pack(side="left", padx=5)

        tk.Button(question_frame, text="+ dodaj odpowiedź", bg="#c0d890", font=("Arial", 10),
                  command=lambda: self.add_answer(question_frame)).pack(side="left", padx=5)

    def add_answer(self, question_frame):
        answer_frame = tk.Frame(question_frame, bg="#d3a9d3")
        answer_frame.pack(fill="x", pady=2)

        tk.Label(answer_frame, text="•", bg="#d3a9d3", font=("Arial", 10)).pack(side="left")
        answer_entry = tk.Entry(answer_frame, width=20, font=("Arial", 10))
        answer_entry.pack(side="left", padx=5)

    def open_calendar(self):
        def set_date():
            selected_date = calendar.get_date()
            self.selected_date_label.config(text=f"Wybrana data: {selected_date}")
            calendar_window.destroy()

        calendar_window = tk.Toplevel(self)
        calendar_window.title("Wybierz datę")
        calendar = Calendar(calendar_window, date_pattern="dd.mm.yyyy")
        calendar.pack(pady=10)
        tk.Button(calendar_window, text="Zatwierdź", command=set_date).pack(pady=5)

    def submit(self):
        title = self.title_entry.get()
        date = self.selected_date_label.cget("text").replace("Wybrana data: ", "")
        anonymous = self.is_anonymous.get()

        if not title or "Nie wybrano daty" in date:
            messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione!")
            return

        # Tutaj można dodać logikę zapisu danych
        messagebox.showinfo("Sukces", f"Głosowanie '{title}' zostało stworzone na dzień {date}!")

    def cancel(self):
        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz anulować?"):
            self.destroy()


if __name__ == "__main__":
    app = CreateVoteScreen()
    app.mainloop()
