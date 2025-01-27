import tkinter as tk
from tkinter import ttk
from firebase_communication import get_voting_details, get_voting_results

def show_poll_result_screen(container, app_controller):
    """
    Display the poll result screen, including voting details and results, in the given container.

    This function:
    - Clears any existing widgets in the container.
    - Retrieves voting details and results from Firestore.
    - Displays the voting title, deadline, author, and the number of votes cast versus total users.
    - Lists the results for each voting option with the number of votes and percentage.
    - Includes a "BACK" button to return to the main screen.

    Parameters:
        container (tk.Frame): The Tkinter container (e.g., a frame or window) in which the screen will be displayed.
        app_controller (object): The application controller that provides the current voting ID and manages screen transitions.

    Returns:
        None
    """
    for widget in container.winfo_children():
        widget.destroy()

    container.configure(bg="#d3a9d3")

    voting_id = app_controller.chosenVotingId

    voting_details = get_voting_details(voting_id)
    results = get_voting_results(voting_id)

    tk.Label(container, text="Aplikacja do głosowania", font=("Arial", 18, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
    tk.Label(container, text="przeglądaj wyniki", font=("Arial", 14), bg="#d3a9d3").pack(pady=(0, 15))

    details_frame = tk.Frame(container, bg="#d3a9d3")
    details_frame.pack(padx=20, pady=10, fill="x")

    tk.Label(details_frame, text=f"Tytuł: {voting_details['title']}", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")
    tk.Label(details_frame, text=f"Dostępne do: {voting_details['deadline']}", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")
    tk.Label(details_frame, text=f"Autor: {voting_details['author'].get().to_dict().get('name', 'Nieznany autor')}", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")
    tk.Label(details_frame, text=f"Stan głosowania: {voting_details['votes_cast']}/{voting_details['total_users']}", font=("Arial", 12), bg="#d3a9d3", anchor="w").pack(anchor="w")

    result_frame = tk.Frame(container, bg="#d3a9d3")
    result_frame.pack(padx=20, pady=20, fill="x")

    for result in results:
        print(result)
        tk.Frame(result_frame, bg=result["bg"]).pack(fill="x", pady=5, padx=5)
        tk.Label(result_frame, text=f"{result['candidate']} - {result['percentage']}", font=("Arial", 12), bg=result["bg"], anchor="w").pack(fill="x", pady=2, padx=10)

    tk.Button(container, text="POWRÓT", command=lambda: app_controller.switch_to("main"), font=("Arial", 14), bg="#c49bd6", width=15).pack(pady=20)
