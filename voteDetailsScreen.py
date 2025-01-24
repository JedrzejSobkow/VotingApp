import tkinter as tk
from tkinter import StringVar, messagebox
from firebase_communication import fetch_vote_data, save_vote, get_user_data



def create_rounded_button(canvas, x, y, text, command, bg_color, text_color):
    """Creates a rounded button on a canvas."""
    radius = 20  # Corner radius
    canvas.create_arc(x, y, x + 2 * radius, y + 2 * radius, start=90, extent=90, fill=bg_color, outline="")
    canvas.create_arc(x + 200 - 2 * radius, y, x + 200, y + 2 * radius, start=0, extent=90, fill=bg_color, outline="")
    canvas.create_arc(x, y + 60 - 2 * radius, x + 2 * radius, y + 60, start=180, extent=90, fill=bg_color, outline="")
    canvas.create_arc(x + 200 - 2 * radius, y + 60 - 2 * radius, x + 200, y + 60, start=270, extent=90, fill=bg_color, outline="")
    canvas.create_rectangle(x + radius, y, x + 200 - radius, y + 60, fill=bg_color, outline="")
    canvas.create_rectangle(x, y + radius, x + 200, y + 60 - radius, fill=bg_color, outline="")

    # Add text to the button
    canvas.create_text(x + 100, y + 30, text=text, fill=text_color, font=("Arial", 12, "bold"))

    # Add button event (invisible binding rectangle)
    canvas.tag_bind(canvas.create_rectangle(x, y, x + 200, y + 60, outline="", fill=""), "<Button-1>", command)

def on_confirm_click(event, selected_option_id, app_controller):
    """Handles the confirmation of a vote and saves it to Firestore."""
    print(selected_option_id)
    if selected_option_id in [None, 'None']:
        messagebox.showerror("Błąd", "Musisz wybrać opcję, aby zagłosować!")
        return

    try:
        # Save the vote to Firestore using the option's ID
        save_vote(app_controller.userId, app_controller.chosenVotingId, selected_option_id)
        
        messagebox.showinfo("Potwierdzenie", "Twój głos został zapisany. Dziękujemy za udział w głosowaniu!")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się zapisać głosu: {e}")

def show_vote_screen(root, app_controller):
    """Displays the vote screen for a specific vote."""
    # Pobierz dane głosowania
    voting_id = app_controller.chosenVotingId
    user_data = get_user_data(app_controller.userId)  # Pobierz dane użytkownika
    voting_data = fetch_vote_data(voting_id)

    if not voting_data:
        messagebox.showerror("Błąd", "Nie znaleziono danych głosowania.")
        return

    # Clear the main window
    for widget in root.winfo_children():
        widget.destroy()

    # Add title and metadata
    title_label = tk.Label(root, text="Aplikacja do głosowania\nzagłosuj", bg="#d9b3ff", font=("Arial", 20, "italic"), fg="black")
    title_label.pack(pady=10)

    metadata_frame = tk.Frame(root, bg="#d9b3ff")
    metadata_frame.pack(pady=10)

    vote_metadata = f"Tytuł: {voting_data['title']}\nDostępne do: {voting_data['deadline']}\nAutor: {voting_data['author_name']}\nStan głosowania: {voting_data['votes_status']}"
    metadata_label = tk.Label(metadata_frame, text=vote_metadata, bg="#d9b3ff", font=("Arial", 14), anchor="center", justify="center")
    metadata_label.pack()

    question_label = tk.Label(root, text=voting_data['content'], bg="#d9b3ff", font=("Arial", 14), anchor="center", justify="center")
    question_label.pack(pady=10)

    options_frame = tk.Frame(root, bg="#d9b3ff")
    options_frame.pack(pady=10)

    selected_option = StringVar()
    selected_option.set(None)  # Set to None initially, so no option is selected by default

    # Create RadioButtons for options with their respective IDs as the value
    for option in voting_data['options']:
        option_id = option["id"]
        option_name = option["value"]
        option_button = tk.Radiobutton(options_frame, text=option_name, variable=selected_option, value=option_id, bg="#d9b3ff", font=("Arial", 12), anchor="w", justify="center")
        option_button.pack(anchor="center", pady=5)

    # Button Canvas
    button_canvas = tk.Canvas(root, width=600, height=100, bg="#d9b3ff", highlightthickness=0)
    button_canvas.pack()

    # The 'ZATWIERDŹ' button now sends the ID of the selected option
    create_rounded_button(button_canvas, 100, 20, "ZATWIERDŹ", lambda e: on_confirm_click(e, selected_option.get(), app_controller), "#9b6fbf", "#fff")
    create_rounded_button(button_canvas, 300, 20, "ANULUJ", lambda e: app_controller.switch_to("votingsList"), "#bf6fa6", "#fff")
