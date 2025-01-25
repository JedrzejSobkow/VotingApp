import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
from firebase_communication import create_voting, get_users  # Dodaj funkcję `get_users` do pobierania użytkowników.


def add_question(frame, answers_entries):
    """Dodaje nowe pytanie z możliwością dodania odpowiedzi."""
    question_entry = tk.Entry(frame, width=30, font=("Arial", 10))
    question_entry.pack(side="left", padx=5)

    tk.Button(
        frame, text="+ dodaj odpowiedź", bg="#c0d890", font=("Arial", 10),
        command=lambda: add_answer(frame, answers_entries)
    ).pack(side="left", padx=5)

    return question_entry


def add_answer(frame, answers_entries):
    """Dodaje nową odpowiedź w pytaniu."""
    answer_frame = tk.Frame(frame, bg="#d3a9d3")
    answer_frame.pack(fill="x", pady=2)

    tk.Label(answer_frame, text="•", bg="#d3a9d3", font=("Arial", 10)).pack(side="left")
    answer_entry = tk.Entry(answer_frame, width=20, font=("Arial", 10))
    answer_entry.pack(side="left", padx=5)
    answers_entries.append(answer_entry)


def open_calendar(selected_date_label):
    """Otwiera okno wyboru daty."""
    def set_date():
        selected_date = calendar.get_date()
        selected_date_label.config(text=f"Wybrana data: {selected_date}")
        calendar_window.destroy()

    calendar_window = tk.Toplevel()
    calendar_window.title("Wybierz datę")
    calendar = Calendar(calendar_window, date_pattern="dd.mm.yyyy")
    calendar.pack(pady=10)
    tk.Button(calendar_window, text="Zatwierdź", command=set_date).pack(pady=5)


def submit(title_entry, question_entry, answers_entries, selected_date_label, is_anonymous, app_controller, selected_users):
    """Obsługuje zatwierdzenie formularza."""
    title = title_entry.get()
    question = question_entry.get()
    answers = [entry.get() for entry in answers_entries if entry.get()]
    date = selected_date_label.cget("text").replace("Wybrana data: ", "")
    anonymous = is_anonymous.get()
    users_to_vote = [user_id for user_id, var in selected_users.items() if var.get()]

    if not title or "Nie wybrano daty" in date or not question or not answers or not users_to_vote:
        messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione!")
        return

    # Funkcja do tworzenia głosowania w bazie danych.
    create_voting(title, question, answers, date, anonymous, app_controller.userId, users_to_vote)

    messagebox.showinfo("Sukces", f"Głosowanie '{title}' zostało stworzone na dzień {date}!")
    app_controller.switch_to("main")


def populate_user_list(users_frame, selected_users):
    """Pobiera listę użytkowników z bazy i wypełnia listę checkboxami."""
    users = get_users()  # Pobierz użytkowników z bazy danych (funkcja musi zwracać listę słowników z 'user_id' i 'name').

    for user in users:
        user_var = tk.BooleanVar()
        selected_users[user['user_id']] = user_var
        tk.Checkbutton(users_frame, text=user['name'], variable=user_var, bg="#e1e1e1", font=("Arial", 10), anchor="w").pack(fill="x", padx=5, pady=2)


def show_create_vote_screen(root, app_controller):
    """Wyświetla ekran tworzenia głosowania."""
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Aplikacja do głosowania - Stwórz głosowanie")
    root.geometry("500x700")
    root.configure(bg="#d3a9d3")

    tk.Label(root, text="Aplikacja do głosowania", font=("Arial", 16, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
    tk.Label(root, text="stwórz głosowanie", font=("Arial", 12), bg="#d3a9d3").pack(pady=(0, 10))

    # Sekcja tytułu
    tk.Label(root, text="Tytuł głosowania", font=("Arial", 10), bg="#d3a9d3").pack(anchor="w", padx=20)
    title_entry = tk.Entry(root, width=40, font=("Arial", 12))
    title_entry.pack(pady=5, padx=20)

    # Sekcja pytań i odpowiedzi
    tk.Label(root, text="Treść głosowania i odpowiedzi", font=("Arial", 10), bg="#d3a9d3").pack(anchor="w", padx=20)
    questions_frame = tk.Frame(root, bg="#d3a9d3")
    questions_frame.pack(fill="both", padx=20, pady=5)

    answers_entries = []
    question_entry = add_question(questions_frame, answers_entries)

    # Sekcja wyboru daty
    tk.Label(root, text="Data końca głosowania", font=("Arial", 10), bg="#d3a9d3").pack(anchor="w", padx=20, pady=(10, 0))
    selected_date_label = tk.Label(root, text="Nie wybrano daty", bg="#d3a9d3", font=("Arial", 10))
    selected_date_label.pack(pady=5)
    tk.Button(root, text="Wybierz datę", command=lambda: open_calendar(selected_date_label), bg="#c0d890",
              font=("Arial", 10)).pack(pady=5)

    # Checkbox dla anonimowości
    is_anonymous = tk.BooleanVar()
    tk.Checkbutton(root, text="Anonimowe", variable=is_anonymous, bg="#d3a9d3", font=("Arial", 10)).pack(anchor="w", padx=20)

    # Sekcja użytkowników
    tk.Label(root, text="Wybierz użytkowników", font=("Arial", 10), bg="#d3a9d3").pack(anchor="w", padx=20, pady=(10, 0))
    users_frame = tk.Frame(root, bg="#e1e1e1", relief="sunken", bd=1)
    users_frame.pack(fill="both", padx=20, pady=5, expand=True)

    # Dodanie przewijanej listy
    canvas = tk.Canvas(users_frame, bg="#e1e1e1")
    scrollbar = ttk.Scrollbar(users_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#e1e1e1")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    selected_users = {}
    populate_user_list(scrollable_frame, selected_users)

    # Przyciski akcji
    button_frame = tk.Frame(root, bg="#d3a9d3")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Dodaj", bg="#c49bd6", font=("Arial", 12),
              command=lambda: submit(title_entry, question_entry, answers_entries, selected_date_label,
                                     is_anonymous, app_controller, selected_users)).pack(side="left", padx=10)
    tk.Button(button_frame, text="Anuluj", bg="#f3a1b4", font=("Arial", 12),
              command=lambda: root.destroy()).pack(side="left", padx=10)
