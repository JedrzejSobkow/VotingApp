# import tkinter as tk
# from tkinter import ttk

# def show_poll_result_screen(container, app_controller):
#     # Usuwanie poprzednich widżetów w kontenerze
#     for widget in container.winfo_children():
#         widget.destroy()

#     container.configure(bg="#d3a9d3")

#     # Tytuł wyników
#     tk.Label(container, text="Aplikacja do głosowania", font=("Arial", 18, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
#     tk.Label(container, text="przeglądaj wyniki", font=("Arial", 14), bg="#d3a9d3").pack(pady=(0, 15))

#     # Szczegóły głosowania
#     details_frame = tk.Frame(container, bg="#d3a9d3")
#     details_frame.pack(padx=20, pady=10, fill="x")

#     tk.Label(details_frame, text="Tytuł: Wybór prezydenta LIDL", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")
#     tk.Label(details_frame, text="Dostępne do: 12.12.2024", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")
#     tk.Label(details_frame, text="Autor: Jędrzej Sobków", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")
#     tk.Label(details_frame, text="Stan głosowania: 9/13", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")

#     # Wyniki głosowania
#     result_frame = tk.Frame(container, bg="#d3a9d3")
#     result_frame.pack(padx=20, pady=20, fill="x")

#     results = [
#         {"candidate": "Michał Mazgis", "percentage": "22.22%", "bg": "#ff9999"},
#         {"candidate": "Maciej Praczuk", "percentage": "55.56%", "bg": "#99ff99"},
#         {"candidate": "Bohdan Pivtorak", "percentage": "22.22%", "bg": "#ff9999"},
#     ]

#     for result in results:
#         tk.Frame(result_frame, bg=result["bg"]).pack(fill="x", pady=5, padx=5)
#         tk.Label(result_frame, text=f"{result['candidate']} - {result['percentage']}", font=("Arial", 12), bg=result["bg"], anchor="w").pack(fill="x", pady=2, padx=10)

#     # Przycisk powrotu
#     tk.Button(container, text="POWRÓT", command=lambda: app_controller.show_previous_screen(container), font=("Arial", 14), bg="#c49bd6", width=15).pack(pady=20)



import tkinter as tk
from tkinter import ttk
from firebase_communication import get_voting_details, get_voting_results

def show_poll_result_screen(container, app_controller):
    # Usuwanie poprzednich widżetów w kontenerze
    for widget in container.winfo_children():
        widget.destroy()

    container.configure(bg="#d3a9d3")

    # Pobierz ID wybranego głosowania
    voting_id = app_controller.chosenVotingId

    # Pobierz szczegóły głosowania z Firebase
    voting_details = get_voting_details(voting_id)
    results = get_voting_results(voting_id)

    # Tytuł wyników
    tk.Label(container, text="Aplikacja do głosowania", font=("Arial", 18, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
    tk.Label(container, text="przeglądaj wyniki", font=("Arial", 14), bg="#d3a9d3").pack(pady=(0, 15))

    # Szczegóły głosowania
    details_frame = tk.Frame(container, bg="#d3a9d3")
    details_frame.pack(padx=20, pady=10, fill="x")

    tk.Label(details_frame, text=f"Tytuł: {voting_details['title']}", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")
    tk.Label(details_frame, text=f"Dostępne do: {voting_details['deadline']}", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")
    tk.Label(details_frame, text=f"Autor: {voting_details['author'].get().to_dict().get('name', 'Nieznany autor')}", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")
    tk.Label(details_frame, text=f"Stan głosowania: {voting_details['votes_cast']}/{voting_details['total_users']}", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")

    # Wyniki głosowania
    result_frame = tk.Frame(container, bg="#d3a9d3")
    result_frame.pack(padx=20, pady=20, fill="x")

    for result in results:
        print(result)
        tk.Frame(result_frame, bg=result["bg"]).pack(fill="x", pady=5, padx=5)
        tk.Label(result_frame, text=f"{result['candidate']} - {result['percentage']}", font=("Arial", 12), bg=result["bg"], anchor="w").pack(fill="x", pady=2, padx=10)

    # Przycisk powrotu
    tk.Button(container, text="POWRÓT", command=lambda: app_controller.switch_to("main"), font=("Arial", 14), bg="#c49bd6", width=15).pack(pady=20)
