import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
import bcrypt
from firebase_communication import (
    login_user,
    fetch_vote_stats,
    create_voting,
    get_users,
    fetch_user_vote_status,
    save_vote,
    get_voting_details,
    get_voting_results,
)

class TestVotingApp(unittest.TestCase):

    @patch("firebase_communication.db.collection")
    def test_login_user_success(self, mock_db):
        mock_users_ref = mock_db.return_value
        mock_user_doc = MagicMock()
        mock_user_doc.to_dict.return_value = {"passwordHash": bcrypt.hashpw("password".encode("utf-8"), bcrypt.gensalt()).decode("utf-8"), "role": "admin"}
        mock_users_ref.where.return_value.stream.return_value = [mock_user_doc]

        app_controller = MagicMock()

        login_user("test@example.com", "password", app_controller)
        app_controller.switch_to.assert_called_once_with("main")

    @patch("firebase_communication.db.collection")
    def test_login_user_invalid_password(self, mock_db):
        mock_users_ref = mock_db.return_value
        mock_user_doc = MagicMock()
        mock_user_doc.to_dict.return_value = {"passwordHash": bcrypt.hashpw("password".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")}
        mock_users_ref.where.return_value.stream.return_value = [mock_user_doc]

        app_controller = MagicMock()

        with patch("firebase_communication.messagebox.showerror") as mock_showerror:
            login_user("test@example.com", "wrong_password", app_controller)
            mock_showerror.assert_called_once_with("Błąd", "Niepoprawne hasło.")

    @patch("firebase_communication.db.collection")
    def test_fetch_vote_stats(self, mock_db):
        mock_votes_ref = mock_db.return_value
        mock_vote_docs = [
            MagicMock(to_dict=MagicMock(return_value={"option_ref": "some_option"})),
            MagicMock(to_dict=MagicMock(return_value={})),
        ]
        mock_votes_ref.where.return_value.stream.return_value = mock_vote_docs

        users_voted, total_users = fetch_vote_stats("voting_id")
        self.assertEqual(users_voted, 1)
        self.assertEqual(total_users, 2)

    @patch("firebase_communication.db.collection")
    def test_create_voting_success(self, mock_db):
        mock_votings_ref = mock_db.return_value
        mock_voting_ref = MagicMock()
        mock_voting_ref.id = "new_voting_id"
        mock_votings_ref.add.return_value = (None, mock_voting_ref)

        voting_id = create_voting(
            "New Voting", "Is this a test?", ["Yes", "No"], "31.01.2025", False, "author_id", ["user1", "user2"]
        )
        self.assertEqual(voting_id, "new_voting_id")

    @patch("firebase_communication.db.collection")
    def test_get_users(self, mock_db):
        mock_users_ref = mock_db.return_value
        mock_user_docs = [
            MagicMock(id="user1", to_dict=MagicMock(return_value={"name": "Alice", "role": "user"})),
            MagicMock(id="user2", to_dict=MagicMock(return_value={"name": "Bob", "role": "admin"})),
        ]
        mock_users_ref.stream.return_value = mock_user_docs

        users = get_users()
        print("DUPA")
        print(users)
        self.assertEqual(users, [{"id": "user1", "name": "Alice", "role": "user"}, {"id": "user2", "name": "Bob", "role": "admin"}])

    @patch("firebase_communication.db.collection")
    def test_save_vote_new_vote(self, mock_db):
        mock_votes_ref = mock_db.return_value
        mock_votes_ref.where.return_value.stream.return_value = []
        mock_votes_ref.add = MagicMock()

        save_vote("user_id", "voting_id", "option_id")
        mock_votes_ref.add.assert_called_once()

    @patch("firebase_communication.db.collection")
    def test_get_voting_details(self, mock_db):
        mock_votings_ref = mock_db.return_value
        mock_voting_doc = MagicMock()
        mock_voting_doc.exists = True
        mock_voting_doc.to_dict.return_value = {
            "title": "Test Voting",
            "deadline": "31.01.2025",
            "author_ref": MagicMock(),
        }
        mock_votings_ref.document.return_value.get.return_value = mock_voting_doc

        details = get_voting_details("voting_id")
        self.assertEqual(details["title"], "Test Voting")
        self.assertEqual(details["deadline"], "31.01.2025")

  

if __name__ == "__main__":
    unittest.main()
