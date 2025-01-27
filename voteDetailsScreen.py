import tkinter as tk
from tkinter import StringVar, messagebox
from firebase_communication import fetch_vote_data, save_vote, get_user_data



def create_rounded_button(canvas, x, y, text, command, bg_color, text_color):
    """
    Creates a rounded button on a Tkinter canvas.

    Parameters:
    - canvas: The canvas object where the button will be drawn.
    - x: The x-coordinate of the top-left corner of the button.
    - y: The y-coordinate of the top-left corner of the button.
    - text: The text displayed on the button.
    - command: The function to be executed when the button is clicked.
    - bg_color: The background color of the button.
    - text_color: The color of the text on the button.
    """
    radius = 20  
    canvas.create_arc(x, y, x + 2 * radius, y + 2 * radius, start=90, extent=90, fill=bg_color, outline="")
    canvas.create_arc(x + 200 - 2 * radius, y, x + 200, y + 2 * radius, start=0, extent=90, fill=bg_color, outline="")
    canvas.create_arc(x, y + 60 - 2 * radius, x + 2 * radius, y + 60, start=180, extent=90, fill=bg_color, outline="")
    canvas.create_arc(x + 200 - 2 * radius, y + 60 - 2 * radius, x + 200, y + 60, start=270, extent=90, fill=bg_color, outline="")
    canvas.create_rectangle(x + radius, y, x + 200 - radius, y + 60, fill=bg_color, outline="")
    canvas.create_rectangle(x, y + radius, x + 200, y + 60 - radius, fill=bg_color, outline="")

    canvas.create_text(x + 100, y + 30, text=text, fill=text_color, font=("Arial", 12, "bold"))
    canvas.tag_bind(canvas.create_rectangle(x, y, x + 200, y + 60, outline="", fill=""), "<Button-1>", command)

def on_confirm_click(event, selected_option_id, app_controller):
    """
    Handles the click event when the user confirms their vote.
    
    It checks whether a valid option has been selected and attempts to save the vote. 
    If successful, a confirmation message is shown, and the app switches to the main screen.
    
    Parameters:
    - event: The event triggered by the button click.
    - selected_option_id: The ID of the selected option to vote for.
    - app_controller: The controller that manages the app's state.
    """
    print(selected_option_id)
    if selected_option_id in [None, 'None']:
        messagebox.showerror("Błąd", "Musisz wybrać opcję, aby zagłosować!")
        return

    try:
        save_vote(app_controller.userId, app_controller.chosenVotingId, selected_option_id)
        
        messagebox.showinfo("Potwierdzenie", "Twój głos został zapisany. Dziękujemy za udział w głosowaniu!")
        app_controller.switch_to("main")
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się zapisać głosu: {e}")

def show_vote_screen(root, app_controller):
    """
    Displays the voting screen with the voting options and metadata. 

    It fetches the relevant voting data, shows the title, deadline, and voting options, 
    and allows the user to vote.

    Parameters:
    - root: The Tkinter window that contains the interface.
    - app_controller: The controller that manages the app's state.
    """
    voting_id = app_controller.chosenVotingId
    user_data = get_user_data(app_controller.userId) 
    voting_data = fetch_vote_data(voting_id)

    if not voting_data:
        messagebox.showerror("Błąd", "Nie znaleziono danych głosowania.")
        return

    for widget in root.winfo_children():
        widget.destroy()

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
    selected_option.set(None)  

    for option in voting_data['options']:
        option_id = option["id"]
        option_name = option["value"]
        option_button = tk.Radiobutton(options_frame, text=option_name, variable=selected_option, value=option_id, bg="#d9b3ff", font=("Arial", 12), anchor="w", justify="center")
        option_button.pack(anchor="center", pady=5)

    button_canvas = tk.Canvas(root, width=600, height=100, bg="#d9b3ff", highlightthickness=0)
    button_canvas.pack()

    create_rounded_button(button_canvas, 100, 20, "ZATWIERDŹ", lambda e: on_confirm_click(e, selected_option.get(), app_controller), "#9b6fbf", "#fff")
    create_rounded_button(button_canvas, 300, 20, "ANULUJ", lambda e: app_controller.switch_to("votingsList"), "#bf6fa6", "#fff")
