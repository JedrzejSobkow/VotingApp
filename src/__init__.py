from .controllers.app_c import AppController

from .screens.login_s import show_login_screen
from .screens.main_s import show_main_screen
from .screens.votings_list_s import show_votings_list_screen
from .screens.vote_details_s import show_vote_screen
from .screens.create_vote_s import show_create_vote_screen
from .screens.reminder_config_s import show_reminder_config_screen
from .screens.view_results_s import show_poll_result_screen
from .screens.user_management_s import show_manage_users_screen
from .screens.create_user_s import show_create_user_screen

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
