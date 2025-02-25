import tkinter as tk
from tkinter import Canvas, Scrollbar
from ..database.firebase_communication import fetch_votes_from_db, fetch_user_vote_status
from datetime import datetime

def create_rounded_button(canvas, x, y, text, command, bg_color, text_color):
    """
    Creates a rounded button on a canvas.

    Parameters:
        canvas (tk.Canvas): The canvas to draw the button on.
        x (int): The x-coordinate of the top-left corner of the button.
        y (int): The y-coordinate of the top-left corner of the button.
        text (str): The text to be displayed on the button.
        command (function): The function to be called when the button is clicked.
        bg_color (str): The background color of the button.
        text_color (str): The text color on the button.
    """
    radius = 20  # Corner radius
    canvas.create_arc(x, y, x + 2 * radius, y + 2 * radius, start=90, extent=90, fill=bg_color, outline="")
    canvas.create_arc(x + 200 - 2 * radius, y, x + 200, y + 2 * radius, start=0, extent=90, fill=bg_color, outline="")
    canvas.create_arc(x, y + 60 - 2 * radius, x + 2 * radius, y + 60, start=180, extent=90, fill=bg_color, outline="")
    canvas.create_arc(x + 200 - 2 * radius, y + 60 - 2 * radius, x + 200, y + 60, start=270, extent=90, fill=bg_color, outline="")
    canvas.create_rectangle(x + radius, y, x + 200 - radius, y + 60, fill=bg_color, outline="")
    canvas.create_rectangle(x, y + radius, x + 200, y + 60 - radius, fill=bg_color, outline="")

    canvas.create_text(x + 100, y + 30, text=text, fill=text_color, font=("Arial", 12, "bold"))
    canvas.tag_bind(canvas.create_rectangle(x, y, x + 200, y + 60, outline="", fill=""), "<Button-1>", command)

def populate_vote_list(frame, votes, app_controller):
    """
    Populates the frame with voting options as buttons.

    Parameters:
        frame (tk.Frame): The frame to populate with vote buttons.
        votes (list): List of vote data dictionaries.
        app_controller (AppController): The app controller managing the app state.
    """
    for i, vote in enumerate(votes):
        # Check if the voting is assigned to the logged-in user
        user_vote_status = fetch_user_vote_status(vote['id'], app_controller.userId)

        # Check if the voting has ended
        voting_end_date = vote['deadline']
        voting_end_date = datetime(year=int(voting_end_date[-4:]), month=int(voting_end_date[-7:-5]), day=int(voting_end_date[-10:-8])) 

        current_date = datetime.now()
        
        command = None

        if user_vote_status and 'option_ref' in user_vote_status:  # If user has voted
            bg_color = "#bf80ff"  # Purple for voted
            if app_controller.isSettingUpReminder:
                command = lambda v=vote: on_vote_click(v, app_controller)
        elif voting_end_date < current_date:
            bg_color = "#ff4d4d"  # Red for ended voting
        else:
            bg_color = "#80b3ff"  # Blue for active voting and not yet voted
            command = lambda v=vote: on_vote_click(v, app_controller)

        if app_controller.isShowingResults:
            command = lambda v=vote: on_vote_click(v, app_controller)

        button = tk.Button(
            frame,
            text=f"{vote['title']} | do: {voting_end_date } | zagłosowało {vote['votes']}",
            bg=bg_color,
            font=("Arial", 12),
            anchor="w",
            padx=10,
            pady=5,
            relief="flat",
            command=command,
        )
        button.pack(fill="x", padx=5, pady=2)

def on_vote_click(vote, app_controller):
    """
    Handle the vote click, navigate to the voting screen.

    Parameters:
        vote (dict): The selected vote data.
        app_controller (AppController): The app controller managing the app state.
    """
    app_controller.chosenVotingId = vote['id']
    if app_controller.isSettingUpReminder:
        app_controller.switch_to("reminderConfig")
    elif app_controller.isShowingResults:
        app_controller.switch_to("pollResults")
    else:
        app_controller.switch_to("voteDetails")

def show_votings_list_screen(root, app_controller):
    """
    Displays the voting list screen.

    Parameters:
        root (tk.Tk): The root window of the Tkinter app.
        app_controller (AppController): The app controller managing the app state.
    """
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Aplikacja do głosowania\nzagłosuj", bg="#d9b3ff", font=("Arial", 20, "italic"), fg="black").pack(pady=10)

    frame_container = tk.Frame(root, bg="#d9b3ff")
    frame_container.pack(fill="both", expand=True, padx=20, pady=10)

    canvas = tk.Canvas(frame_container, bg="#d9b3ff", highlightthickness=0)
    scrollbar = Scrollbar(frame_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#d9b3ff")

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    if app_controller.isSettingUpReminder or app_controller.isShowingResults:
        votes_data = fetch_votes_from_db(app_controller.userId, True)
    else:
        votes_data = fetch_votes_from_db(app_controller.userId, False)
    populate_vote_list(scrollable_frame, votes_data, app_controller)

    button_canvas = tk.Canvas(root, width=600, height=100, bg="#d9b3ff", highlightthickness=0)
    button_canvas.pack()

    create_rounded_button(button_canvas, 150, 20, "Wróć", lambda e: app_controller.switch_to("main"), "#9b6fbf", "#fff")
