import firebase_admin
from firebase_admin import credentials, firestore
import bcrypt
from tkinter import messagebox

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def login_user(email, password, app_controller):
    """
    Register a new user by collecting username, email, and password.
    Encrypt the password using SHA-256 before storing it in Firestore.
    If the username or email is already taken, show an error message.
    """
    try:
        users_ref = db.collection("users")
        query = users_ref.where("email", "==", email).stream()

        user_data = None
        for user in query:
            user_data = user.to_dict()
            print(user_data)

        if user_data and "passwordHash" in user_data:
            stored_password_hash = user_data["passwordHash"]

            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                messagebox.showinfo("Sukces", "Logowanie udane! Witaj!")
                app_controller.userId = user.id
                app_controller.userRole = user_data["role"]
                app_controller.switch_to("main")
            else:
                messagebox.showerror("Błąd", "Niepoprawne hasło.")
        else:
            messagebox.showerror("Błąd", "Nie znaleziono użytkownika o podanym adresie e-mail.")
    
    except Exception as e:
        print(e)
        messagebox.showerror("Błąd", "Wystąpił błąd podczas logowania.")

def fetch_vote_stats(voting_id):
    """
    Fetches vote statistics for a given voting.
    
    Args:
        voting_id (str): The ID of the voting.
    
    Returns:
        tuple: The number of users who voted and the total number of users.
    """
    total_users = 0
    users_voted = 0

    try:
        votes_query = db.collection("votes").where("voting_ref", "==", db.document(f"votings/{voting_id}"))
        votes = votes_query.stream()

        for vote in votes:
            total_users += 1
            vote_data = vote.to_dict()
            if "option_ref" in vote_data:
                users_voted += 1

    except Exception as e:
        print(f"Błąd podczas obliczania głosów: {e}")

    return users_voted, total_users

def create_voting(title, question, answers, date, is_anonymous, author_id, users_to_vote):
    """
    Creates a new voting in Firestore, adds voting options, and creates vote documents for users who need to vote.
    
    Args:
        title (str): The voting title.
        question (str): The question being asked in the voting.
        answers (list[str]): List of possible answers.
        date (str): The deadline for the voting (format "dd.mm.yyyy").
        is_anonymous (bool): Whether the voting is anonymous.
        author_id (str): The ID of the voting author.
        users_to_vote (list[str]): List of user IDs who need to vote.
    
    Returns:
        str: The ID of the created voting, or `None` in case of an error.
    """
    try:
        author_ref = db.collection("users").document(author_id)
        
        voting_data = {
            "title": title,
            "content": question,
            "deadline": date,
            "anon": is_anonymous,
            "author_ref": author_ref
        }
        voting_ref = db.collection("votings").add(voting_data)[1]  

        for answer in answers:
            if answer.strip():  
                option_data = {
                    "option": answer.strip(),
                    "voting_id": voting_ref
                }
                db.collection("options").add(option_data)

        for user_id in users_to_vote:
            user_ref = db.collection("users").document(user_id)
            vote_data = {
                "user_ref": user_ref,
                "voting_ref": voting_ref
            }
            db.collection("votes").add(vote_data)

        print(f"Głosowanie '{title}' zostało utworzone z ID: {voting_ref.id}")
        return voting_ref.id  
    except Exception as e:
        print(f"Błąd podczas tworzenia głosowania: {e}")
        return None


def get_users():
    """
    Fetches the list of users from the 'users' collection in Firestore.
    
    Returns:
        List[dict]: List of users in the format [{"user_id": "123", "name": "John Doe"}, ...]
    """
    users_ref = db.collection("users")  
    users = []

    try:
        docs = users_ref.stream()
        for doc in docs:
            user_data = doc.to_dict()
            users.append({
                "user_id": doc.id,       
                "name": user_data.get("name", "Nieznane")  
            })
    except Exception as e:
        print(f"Błąd podczas pobierania użytkowników: {e}")
    
    return users

def fetch_user_vote_status(voting_id, user_id):
    """
    Checks if a user has voted in a given voting.
    
    Args:
        voting_id (str): The voting ID.
        user_id (str): The user ID.
    
    Returns:
        dict or None: The vote document if the user has voted, or None if they haven't.
    """
    votes_ref = db.collection("votes")
    user_vote_query = votes_ref.where("user_ref", "==", db.collection("users").document(user_id)) \
                                .where("voting_ref", "==", db.collection("votings").document(voting_id))
    for vote_doc in user_vote_query.stream():
        return vote_doc.to_dict() 
    return None 


def fetch_votes_from_db(user_id=None, is_author=False):
    """
    Fetches voting data from Firestore and calculates statistics.
    
    Args:
        user_id (str or None): The user ID, if filtering by user.
        is_author (bool): Whether to fetch votings authored by the user.
    
    Returns:
        List[dict]: List of voting data with stats.
    """
    votes = []
    try:
        if user_id:
            user_ref = db.collection("users").document(user_id)
            all_votings_ref = db.collection("votings")

            if not is_author:
                user_votes_query = db.collection("votes").where("user_ref", "==", user_ref)
                user_votes = [vote.to_dict() for vote in user_votes_query.stream()]

                voting_ids = {vote["voting_ref"].id for vote in user_votes}  

            else:
                votings_ref = db.collection("votings").where("author_ref", "==", user_ref)
                votings_docs = votings_ref.stream()
                voting_ids = [voting_doc.id for voting_doc in votings_docs]


            for voting_id in voting_ids:
                voting_doc = all_votings_ref.document(voting_id).get()
                if voting_doc.exists:
                    voting_data = voting_doc.to_dict()
                    voting_data["id"] = voting_doc.id

                    users_voted, total_users = fetch_vote_stats(voting_doc.id)
                    voting_data["votes"] = f"{users_voted}/{total_users}"
                    votes.append(voting_data)
                
        else:
            votes_ref = db.collection("votings")
            for doc in votes_ref.stream():
                voting_data = doc.to_dict()
                voting_data["id"] = doc.id

                users_voted, total_users = fetch_vote_stats(doc.id)
                voting_data["votes"] = f"{users_voted}/{total_users}"
                votes.append(voting_data)

    except Exception as e:
        print(f"Błąd podczas pobierania głosowań: {e}")
    return votes


def update_voting_with_reminder(interval, start_date_val, end_date_val, method, votingId):
    """
    Updates a voting with reminder settings.
    
    Args:
        interval (str): The interval for the reminder.
        start_date_val (str): The start date of the reminder.
        end_date_val (str): The end date of the reminder.
        method (str): The method for the reminder (e.g., email, push).
        votingId (str): The voting ID.
    
    Returns:
        None
    """
    try:
        voting_ref = db.collection("votings").document(votingId)

        reminder_data = {
            "interval": interval,
            "start_date": start_date_val,
            "end_date": end_date_val,
            "method": method
        }

        voting_ref.update(reminder_data)


    except Exception as e:
        print(f"Błąd podczas aktualizacji głosowania: {e}")


def fetch_vote_data(voting_id):
    """
    Fetches the voting data and options from Firestore.
    
    Args:
        voting_id (str): The ID of the voting.
    
    Returns:
        dict: The voting data including options and author information.
    """
    try:
        voting_doc = db.collection("votings").document(voting_id).get()
        if not voting_doc.exists:
            raise ValueError("Nie znaleziono głosowania!")

        voting_data = voting_doc.to_dict()
        voting_data["id"] = voting_id

        options_query = db.collection("options").where("voting_id", "==", voting_doc.reference)
        options = [
            {
                "id": option.id, 
                "value": option.to_dict()["option"]  
            }
            for option in options_query.stream()
        ]
        voting_data["options"] = options

        author_ref = voting_data.get("author_ref")
        if author_ref:
            author_doc = author_ref.get()
            voting_data["author_name"] = author_doc.to_dict().get("name", "Nieznany autor")
        else:
            voting_data["author_name"] = "Nieznany autor"

        votes_query = db.collection("votes").where("voting_ref", "==", voting_doc.reference)
        votes = [vote.to_dict() for vote in votes_query.stream()]

        total_votes = len(votes) 
        votes_cast = sum(1 for vote in votes if "option_ref" in vote)  
        voting_data["votes_status"] = f"{votes_cast}/{total_votes}"

        return voting_data
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return None


def save_vote(user_id, voting_id, selected_option_id):
    """
    Save the user's vote in Firestore.

    This function checks if the user has already voted in a particular voting session. 
    If the user has voted, it updates their existing vote with the selected option.
    Otherwise, it creates a new vote entry for the user.

    Parameters:
        user_id (str): The ID of the user casting the vote.
        voting_id (str): The ID of the voting session.
        selected_option_id (str): The ID of the selected voting option.
    
    Returns:
        None
    """
    try:
        user_ref = db.collection("users").document(user_id)

        voting_ref = db.collection("votings").document(voting_id)

        option_ref = db.collection("options").document(selected_option_id)

        existing_vote_query = db.collection("votes").where("user_ref", "==", user_ref).where("voting_ref", "==", voting_ref)
        existing_vote = [doc for doc in existing_vote_query.stream()]
        
        if existing_vote:
            existing_vote[0].reference.update({"option_ref": option_ref})
        else:
            db.collection("votes").add({
                "user_ref": user_ref,
                "voting_ref": voting_ref,
                "option_ref": option_ref
            })
        
        print("Głos zapisany pomyślnie.")
    except Exception as e:
        print(f"Błąd podczas zapisywania głosu: {e}")



def get_user_data(user_id):
    """
    Fetch user data from Firestore based on the provided user ID.

    Parameters:
        user_id (str): The ID of the user whose data is being fetched.

    Returns:
        dict: A dictionary containing the user's data, or None if the user doesn't exist.
    """
    try:
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            return user_doc.to_dict()  
        else:
            return None
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return None
    

def get_voting_details(voting_id):
    """
    Retrieve details of a specific voting session, including the number of votes cast and total users.

    Parameters:
        voting_id (str): The ID of the voting session.

    Returns:
        dict: A dictionary containing the title, deadline, author, number of votes cast, 
              and total number of users in the voting session.
    """
    db = firestore.client()
    voting_doc = db.collection("votings").document(voting_id).get()
    votes_cast, total_users = fetch_vote_stats(voting_id)
    if voting_doc.exists:
        voting_data = voting_doc.to_dict()
        return {
            "title": voting_data["title"],
            "deadline": voting_data["deadline"],
            "author": voting_data["author_ref"],  
            "votes_cast": votes_cast,  
            "total_users": total_users  
        }
    return {}



def get_voting_results(voting_id):
    """
    Fetch the voting results, counting votes for each option and determining the winner.

    Parameters:
        voting_id (str): The ID of the voting session.

    Returns:
        list: A list of dictionaries containing the candidate name, votes received, 
              percentage of votes, and background color for each option.
    """
    voting_ref = db.collection("votings").document(voting_id)  

    options_ref = db.collection("options").where("voting_id", "==", voting_ref)
    options_docs = options_ref.stream()

    votes_ref = db.collection("votes").where("voting_ref", "==", voting_ref)
    votes_docs = votes_ref.stream()

    vote_counts = {}
    total_votes = 0

    for vote in votes_docs:
        vote_data = vote.to_dict()
        option_ref = vote_data.get("option_ref")  
        if option_ref:
            option_id = option_ref.id  
            vote_counts[option_id] = vote_counts.get(option_id, 0) + 1
            total_votes += 1

    results = []
    max_votes = max(vote_counts.values(), default=0)  

    for option in options_docs:
        option_data = option.to_dict()
        option_id = option.id
        votes_for_option = vote_counts.get(option_id, 0)  
        percentage = (votes_for_option / total_votes * 100) if total_votes > 0 else 0

        bg_color = "#99ff99" if votes_for_option == max_votes else "#ff9999"

        results.append({
            "candidate": option_data["option"],
            "votes": votes_for_option, 
            "percentage": f"{percentage:.2f}%",  
            "bg": bg_color  
        })

    return results


def check_email_exists(email):
    """
    Check if a user with the given email address exists in the Firestore database.

    Parameters:
        email (str): The email address to search for.

    Returns:
        bool: True if a user with the email exists, otherwise False.
    """
    db = firestore.client()
    users_ref = db.collection("users")
    existing_user = users_ref.where("email", "==", email).get()
    return len(existing_user) > 0

def add_new_user_to_db(name, email, hashed_password, phone, role):
    """
    Add a new user to the Firestore database with the provided details.

    Parameters:
        name (str): The name of the user.
        email (str): The email address of the user.
        hashed_password (str): The hashed password of the user.
        phone (str): The phone number of the user.
        role (str): The role of the user (e.g., 'admin', 'user').

    Returns:
        None
    """
    db = firestore.client()
    users_ref = db.collection("users")
    new_user = {
        "name": name,
        "email": email,
        "passwordHash": hashed_password,
        "phoneNumber": phone,
        "role": role
    }
    users_ref.add(new_user)

def get_users():
    """
    Retrieve a list of all users from the Firestore database.

    Returns:
        list: A list of dictionaries containing user names, roles, and document IDs.
    """
    users_ref = db.collection('users')  
    docs = users_ref.stream()

    users = []
    for doc in docs:
        user_data = doc.to_dict()
        users.append({
            "name": user_data["name"],
            "role": user_data["role"],
            "id": doc.id  
        })
    return users

def delete_user(user_id):
    """
    Delete a user from the Firestore database by user ID.

    Parameters:
        user_id (str): The ID of the user to be deleted.

    Returns:
        None
    """
    user_ref = db.collection('users').document(user_id)
    user_ref.delete()
    print(f"Użytkownik o ID {user_id} został usunięty.")