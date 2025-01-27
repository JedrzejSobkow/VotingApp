import tkinter as tk
from tkinter import Canvas

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

def on_button_click(event, app_controller, screen_name):
    """
    Handles button clicks to switch between screens.

    Parameters:
        event (tk.Event): The event triggered by the button click.
        app_controller (object): The controller that manages the application's state.
        screen_name (str): The name of the screen to switch to.
    """
    if screen_name == "reminderConfig":
        app_controller.isSettingUpReminder = True
        app_controller.isShowingResults = False
        app_controller.switch_to("votingsList")
    elif screen_name == "pollResults":
        app_controller.isSettingUpReminder = False
        app_controller.isShowingResults = True
        app_controller.switch_to("votingsList")
    else:
        app_controller.isSettingUpReminder = False
        app_controller.isShowingResults = False
        app_controller.switch_to(screen_name)

def show_main_screen(root, app_controller):
    """
    Displays the main screen after login.

    Parameters:
        root (tk.Tk): The root window of the Tkinter application.
        app_controller (object): The controller that manages the application's state.
    """
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Aplikacja do głosowania", bg="#d9b3ff", font=("Arial", 20, "italic")).pack(pady=10)

    canvas = Canvas(root, width=500, height=400, bg="#d9b3ff", highlightthickness=0)
    canvas.pack()

    create_rounded_button(canvas, 50, 100, "Pokaż głosowania\noczekujące na mój głos", lambda e: on_button_click(e, app_controller, "votingsList"), "#b3a3ff", "#000")
    if app_controller.userRole in ["host", "admin"]:
        create_rounded_button(canvas, 260, 100, "Utwórz nowe\ngłosowanie", lambda e: on_button_click(e, app_controller, "createVoting"), "#cc99ff", "#000")
        create_rounded_button(canvas, 50, 180, "Konfiguruj\nprzypomnienia", lambda e: on_button_click(e, app_controller, "reminderConfig"), "#cc99ff", "#000")
        create_rounded_button(canvas, 260, 180, "Przeglądaj wyniki", lambda e: on_button_click(e, app_controller, "pollResults"), "#cc99ff", "#000")
        if app_controller.userRole == "admin":
            create_rounded_button(canvas, 150, 260, "Zarządzaj kontami\nużytkowników", lambda e: on_button_click(e, app_controller, "userManagement"), "#ff99cc", "#000")

    create_rounded_button(canvas, 150, 340, "Wyloguj", lambda e: on_button_click(e, app_controller, "login"), "#b0a0fa", "#000")
