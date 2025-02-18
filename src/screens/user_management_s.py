import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ..database.firebase_communication import get_users, delete_user

def show_manage_users_screen(container, app_controller):
    """
    Display the 'Manage Users' screen, allowing the administrator to manage users by viewing their information and deleting accounts.

    This function:
    - Clears any existing widgets in the container.
    - Retrieves the list of users from the Firebase database.
    - Displays user details such as name and role in a scrollable frame.
    - Provides an option to delete users, except for the currently logged-in user.
    - Includes a button to navigate to the user creation screen and a back button to return to the main screen.

    Parameters:
        container (tk.Frame): The Tkinter container (e.g., a frame or window) in which the screen will be displayed.
        app_controller (object): The application controller that manages user information and screen transitions.

    Returns:
        None
    """
    for widget in container.winfo_children():
        widget.destroy()

    container.configure(bg="#d3a9d3")

    tk.Label(container, text="Aplikacja do głosowania", font=("Arial", 18, "bold"), bg="#d3a9d3").pack(pady=(10, 5))
    tk.Label(container, text="zarządzaj użytkownikami", font=("Arial", 14), bg="#d3a9d3").pack(pady=(0, 15))

    users_frame = tk.Frame(container, bg="#d3a9d3")
    users_frame.pack(padx=20, pady=10, fill="both", expand=True)

    users = get_users() 

    canvas = tk.Canvas(users_frame, bg="#d3a9d3", highlightthickness=0)
    scrollbar = ttk.Scrollbar(users_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#d3a9d3")

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    for user in users:
        user_frame = tk.Frame(scrollable_frame, bg="#d3a9d3")
        user_frame.pack(fill="x", pady=5, padx=5)

        tk.Label(user_frame, text="👤", font=("Arial", 14), bg="#d3a9d3").pack(side="left", padx=5)
        tk.Label(user_frame, text=user["name"], font=("Arial", 12), bg="#d3a9d3").pack(side="left", padx=10)
        tk.Label(user_frame, text=user["role"], font=("Arial", 12), bg="#d3a9d3").pack(side="left", padx=10)

        if user["id"] == app_controller.userId:
            tk.Label(user_frame, text="(Nie możesz usunąć swojego konta)", font=("Arial", 10), bg="#d3a9d3", fg="red").pack(side="right", padx=5)
        else:
            tk.Button(user_frame, text="🗑", font=("Arial", 12), bg="#d3a9d3", command=lambda u=user: confirm_delete_user(u["id"], app_controller)).pack(side="right", padx=5)

    add_user_frame = tk.Frame(scrollable_frame, bg="#d3a9d3")
    add_user_frame.pack(fill="x", pady=5, padx=5)

    tk.Button(add_user_frame, text="+", font=("Arial", 14), bg="#d3a9d3", command=lambda: app_controller.switch_to("userCreation")).pack(side="left", padx=5)

    action_buttons_frame = tk.Frame(container, bg="#d3a9d3")
    action_buttons_frame.pack(pady=(20, 10))

    tk.Button(action_buttons_frame, text="POWRÓT", font=("Arial", 14), bg="#c49bd6", width=15, command=lambda: app_controller.switch_to("main")).pack(side="right", padx=10)

def confirm_delete_user(user_id, app_controller):
    """
    Confirm the deletion of a user account.

    This function displays a confirmation dialog for deleting a user account. If confirmed, it calls the `delete_user` function and updates the screen.

    Parameters:
        user_id (str): The ID of the user to be deleted.
        app_controller (object): The application controller responsible for managing the user interface and user data.

    Returns:
        None
    """
    if user_id == app_controller.userId:
        messagebox.showerror("Błąd", "Nie możesz usunąć swojego konta!")
    else:
        confirm = messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć tego użytkownika?")
        if confirm:
            delete_user(user_id)
            messagebox.showinfo("Sukces", "Użytkownik został usunięty.")
            show_manage_users_screen(app_controller.switch_to("userManagement"), app_controller)  # Odświeżenie ekranu
