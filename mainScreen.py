import tkinter as tk
from tkinter import Canvas

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

def on_button_click(event, app_controller, screen_name):
    """Handles button clicks to switch between screens."""
    app_controller.switch_to(screen_name)

def show_main_screen(root, app_controller):
    """Main screen after login."""
    # Clear the current window
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Aplikacja do głosowania", bg="#d9b3ff", font=("Arial", 20, "italic")).pack(pady=10)

    # Create canvas
    canvas = Canvas(root, width=500, height=400, bg="#d9b3ff", highlightthickness=0)
    canvas.pack()

    # Create buttons and link them to screens
    create_rounded_button(canvas, 50, 100, "Pokaż głosowania\noczekujące na mój głos", lambda e: on_button_click(e, app_controller, "votingsList"), "#b3a3ff", "#000")
    if app_controller.userRole in ["host", "admin"]:
        create_rounded_button(canvas, 260, 100, "Utwórz nowe\ngłosowanie", lambda e: on_button_click(e, app_controller, "createVoting"), "#cc99ff", "#000")
        create_rounded_button(canvas, 50, 180, "Konfiguruj\nprzypomnienia", lambda e: on_button_click(e, app_controller, "reminderScreen"), "#cc99ff", "#000")
        create_rounded_button(canvas, 260, 180, "Przeglądaj wyniki", lambda e: on_button_click(e, app_controller, "resultsScreen"), "#cc99ff", "#000")
        if app_controller.userRole == "admin":
            create_rounded_button(canvas, 150, 260, "Zarządzaj kontami\nużytkowników", lambda e: on_button_click(e, app_controller, "userManagementScreen"), "#ff99cc", "#000")
