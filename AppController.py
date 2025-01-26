import tkinter as tk
from loginScreen import show_login_screen
from mainScreen import show_main_screen  # Import the main screen after login
from votingsListScreen import show_votings_list_screen  # Import the new votings list screen
from voteDetailsScreen import show_vote_screen
from createVoteScreen import show_create_vote_screen
from reminderConfigScreen import show_reminder_config_screen
from viewResultsScreen import show_poll_result_screen
from userManagementScreen import show_manage_users_screen
from createUserScreen import show_create_user_screen
# Import other screens you might have

class AppController:

    userId = None
    userRole = None
    chosenVotingId = None
    isSettingUpReminder = False
    isShowingResults = False

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Application")
        self.root.geometry("600x600")
        self.root.configure(bg="#d9b3ff")

        # Dictionary to store different screens
        self.screens = {}

    def add_screen(self, screen_name, screen_function):
        """Adds a screen to the application."""
        self.screens[screen_name] = screen_function

    def switch_to(self, screen_name):
        """Switches to the screen."""
        screen_function = self.screens.get(screen_name)
        if screen_function:
            screen_function(self.root, self)  # Pass app_controller to switch screens
        else:
            print(f"Screen '{screen_name}' not found.")

    def start(self):
        """Starts the application."""
        self.switch_to("login")  # Start with the login screen
        self.root.mainloop()

if __name__ == "__main__":
    app = AppController()
    app.add_screen("login", show_login_screen)
    app.add_screen("main", show_main_screen)  # Add the main screen after login
    app.add_screen("votingsList", show_votings_list_screen)  # Add votings list screen
    app.add_screen("voteDetails", show_vote_screen)
    app.add_screen("createVoting", show_create_vote_screen)
    app.add_screen("reminderConfig", show_reminder_config_screen)
    app.add_screen("pollResults", show_poll_result_screen)
    app.add_screen("userManagement", show_manage_users_screen)    
    app.add_screen("userCreation", show_create_user_screen)



    # Add other screens when needed
    app.start()
