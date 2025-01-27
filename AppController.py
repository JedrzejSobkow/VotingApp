import tkinter as tk
from loginScreen import show_login_screen
from mainScreen import show_main_screen
from votingsListScreen import show_votings_list_screen
from voteDetailsScreen import show_vote_screen
from createVoteScreen import show_create_vote_screen
from reminderConfigScreen import show_reminder_config_screen
from viewResultsScreen import show_poll_result_screen
from userManagementScreen import show_manage_users_screen
from createUserScreen import show_create_user_screen

class AppController:
    """
    Main application controller for managing screens and user context.

    Attributes:
        userId (int): The ID of the currently logged-in user.
        userRole (str): The role of the currently logged-in user.
        chosenVotingId (int): The ID of the currently selected voting.
        isSettingUpReminder (bool): Indicates whether the user is setting up a reminder.
        isShowingResults (bool): Indicates whether the user is viewing voting results.
    """

    userId = None
    userRole = None
    chosenVotingId = None
    isSettingUpReminder = False
    isShowingResults = False

    def __init__(self):
        """
        Initializes the AppController instance and sets up the main application window.
        """
        self.root = tk.Tk()
        self.root.title("Application")
        self.root.geometry("600x800")
        self.root.configure(bg="#d9b3ff")
        self.screens = {}

    def add_screen(self, screen_name, screen_function):
        """
        Adds a screen to the application.

        Args:
            screen_name (str): The name of the screen.
            screen_function (callable): The function to render the screen.
        """
        self.screens[screen_name] = screen_function

    def switch_to(self, screen_name):
        """
        Switches to the specified screen.

        Args:
            screen_name (str): The name of the screen to switch to.
        """
        screen_function = self.screens.get(screen_name)
        if screen_function:
            screen_function(self.root, self)
        else:
            print(f"Screen '{screen_name}' not found.")

    def start(self):
        """
        Starts the application and initializes the first screen.
        """
        self.switch_to("login")
        self.root.mainloop()

if __name__ == "__main__":
    app = AppController()
    app.add_screen("login", show_login_screen)
    app.add_screen("main", show_main_screen)
    app.add_screen("votingsList", show_votings_list_screen)
    app.add_screen("voteDetails", show_vote_screen)
    app.add_screen("createVoting", show_create_vote_screen)
    app.add_screen("reminderConfig", show_reminder_config_screen)
    app.add_screen("pollResults", show_poll_result_screen)
    app.add_screen("userManagement", show_manage_users_screen)
    app.add_screen("userCreation", show_create_user_screen)
    app.start()
