import firebase_admin
from firebase_admin import credentials, firestore
import bcrypt
from tkinter import messagebox

cred = credentials.Certificate("credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def login_user(email, password, app_controller):
    """Funkcja do logowania użytkownika za pomocą Firestore."""
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
                # Przejście do innego ekranu po udanym logowaniu
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
    """Fetches vote stats for a given voting."""
    total_users = 0
    users_voted = 0

    try:
        # Query votes for the specific voting
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
    Tworzy nowe głosowanie w Firestore, dodaje opcje głosowania i tworzy dokumenty `votes`
    dla użytkowników, którzy muszą zagłosować.
    
    Args:
        title (str): Tytuł głosowania.
        question (str): Treść pytania głosowania.
        answers (list[str]): Lista opcji odpowiedzi.
        date (str): Data zakończenia głosowania (format "dd.mm.yyyy").
        is_anonymous (bool): Czy głosowanie jest anonimowe.
        author_id (str): ID autora głosowania.
        users_to_vote (list[str]): Lista ID użytkowników, którzy muszą zagłosować.
    
    Returns:
        str: ID utworzonego głosowania lub `None` w przypadku błędu.
    """
    try:
        # Pobierz referencję autora
        author_ref = db.collection("users").document(author_id)
        
        # Dodaj głosowanie do kolekcji "votings"
        voting_data = {
            "title": title,
            "content": question,
            "deadline": date,
            "anon": is_anonymous,
            "author_ref": author_ref
        }
        voting_ref = db.collection("votings").add(voting_data)[1]  # Pobierz referencję nowego dokumentu

        # Dodaj opcje głosowania do kolekcji "options"
        for answer in answers:
            if answer.strip():  # Ignoruj puste odpowiedzi
                option_data = {
                    "option": answer.strip(),
                    "voting_id": voting_ref
                }
                db.collection("options").add(option_data)

        # Dodaj dokumenty do kolekcji "votes" dla każdego użytkownika
        for user_id in users_to_vote:
            user_ref = db.collection("users").document(user_id)
            vote_data = {
                "user_ref": user_ref,
                "voting_ref": voting_ref
            }
            db.collection("votes").add(vote_data)

        print(f"Głosowanie '{title}' zostało utworzone z ID: {voting_ref.id}")
        return voting_ref.id  # Zwróć ID utworzonego głosowania
    except Exception as e:
        print(f"Błąd podczas tworzenia głosowania: {e}")
        return None


def get_users():
    """
    Pobiera listę użytkowników z kolekcji 'users' w Firestore.
    
    Returns:
        List[dict]: Lista użytkowników w formacie [{"user_id": "123", "name": "Jan Kowalski"}, ...]
    """
    users_ref = db.collection("users")  # Kolekcja `users` w bazie danych
    users = []

    try:
        # Pobierz dokumenty użytkowników
        docs = users_ref.stream()
        for doc in docs:
            user_data = doc.to_dict()
            users.append({
                "user_id": doc.id,       # Pobieramy unikalny ID dokumentu jako user_id
                "name": user_data.get("name", "Nieznane")  # Pobieramy nazwę użytkownika
            })
    except Exception as e:
        print(f"Błąd podczas pobierania użytkowników: {e}")
    
    return users

def fetch_user_vote_status(voting_id, user_id):
    """Sprawdza, czy użytkownik zagłosował w danym głosowaniu."""
    # Pobieramy dokument z kolekcji "votes", gdzie user_ref odnosi się do userId
    votes_ref = db.collection("votes")
    user_vote_query = votes_ref.where("user_ref", "==", db.collection("users").document(user_id)) \
                                .where("voting_ref", "==", db.collection("votings").document(voting_id))
     # Sprawdzamy, czy użytkownik zagłosował (czy jest obecne pole "option_ref")
    for vote_doc in user_vote_query.stream():
        return vote_doc.to_dict()  # Zwraca dane dokumentu, w tym "option_ref" jeśli użytkownik zagłosował
    return None  # Zwraca None, jeśli użytkownik nie głosował


def fetch_votes_from_db(user_id=None, is_author=False):
    """Fetches voting data from Firestore and calculates stats."""
    votes = []
    try:
        if user_id:
            # Pobierz referencję do użytkownika
            user_ref = db.collection("users").document(user_id)
            all_votings_ref = db.collection("votings")

            if not is_author:
            # Pobierz dokumenty z kolekcji "votes", gdzie "user_ref" odpowiada podanemu użytkownikowi
                user_votes_query = db.collection("votes").where("user_ref", "==", user_ref)
                user_votes = [vote.to_dict() for vote in user_votes_query.stream()]

                # Pobierz głosowania związane z użytkownikiem
                voting_ids = {vote["voting_ref"].id for vote in user_votes}  # Zbiór ID głosowań

            else:
                votings_ref = db.collection("votings").where("author_ref", "==", user_ref)
                votings_docs = votings_ref.stream()
                voting_ids = [voting_doc.id for voting_doc in votings_docs]


            for voting_id in voting_ids:
                voting_doc = all_votings_ref.document(voting_id).get()
                if voting_doc.exists:
                    voting_data = voting_doc.to_dict()
                    voting_data["id"] = voting_doc.id

                    # Oblicz statystyki głosowania
                    users_voted, total_users = fetch_vote_stats(voting_doc.id)
                    voting_data["votes"] = f"{users_voted}/{total_users}"
                    votes.append(voting_data)
                
        else:
            # Pobierz wszystkie głosowania, jeśli nie podano user_id
            votes_ref = db.collection("votings")
            for doc in votes_ref.stream():
                voting_data = doc.to_dict()
                voting_data["id"] = doc.id

                # Oblicz statystyki głosowania
                users_voted, total_users = fetch_vote_stats(doc.id)
                voting_data["votes"] = f"{users_voted}/{total_users}"
                votes.append(voting_data)

    except Exception as e:
        print(f"Błąd podczas pobierania głosowań: {e}")
    return votes


def update_voting_with_reminder(interval, start_date_val, end_date_val, method, votingId):
    try:
        # Pobierz referencję do dokumentu głosowania o wybranym ID
        voting_ref = db.collection("votings").document(votingId)

        # Przygotuj dane do zaktualizowania
        reminder_data = {
            "interval": interval,
            "start_date": start_date_val,
            "end_date": end_date_val,
            "method": method
        }

        # Zaktualizuj dokument w kolekcji "votings"
        voting_ref.update(reminder_data)

        print(f"Głosowanie {app_controller.chosenVotingId} zostało zaktualizowane z nowymi danymi powiadomienia.")

    except Exception as e:
        print(f"Błąd podczas aktualizacji głosowania: {e}")


def fetch_vote_data(voting_id):
    """Fetch voting data and options from Firestore."""
    try:
        # Fetch voting details
        voting_doc = db.collection("votings").document(voting_id).get()
        if not voting_doc.exists:
            raise ValueError("Nie znaleziono głosowania!")

        voting_data = voting_doc.to_dict()
        voting_data["id"] = voting_id

        # Fetch options for the voting
        options_query = db.collection("options").where("voting_id", "==", voting_doc.reference)
        options = [
            {
                "id": option.id,  # Option's Firestore document ID
                "value": option.to_dict()["option"]  # Option's name
            }
            for option in options_query.stream()
        ]
        voting_data["options"] = options

        # Fetch author name from author_ref
        author_ref = voting_data.get("author_ref")
        if author_ref:
            author_doc = author_ref.get()
            voting_data["author_name"] = author_doc.to_dict().get("name", "Nieznany autor")
        else:
            voting_data["author_name"] = "Nieznany autor"

        # Calculate voting status (votes cast / total users)
        votes_query = db.collection("votes").where("voting_ref", "==", voting_doc.reference)
        votes = [vote.to_dict() for vote in votes_query.stream()]

        total_votes = len(votes)  # Total users associated with this voting
        votes_cast = sum(1 for vote in votes if "option_ref" in vote)  # Votes with `option_ref` present
        voting_data["votes_status"] = f"{votes_cast}/{total_votes}"

        return voting_data
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        return None


def save_vote(user_id, voting_id, selected_option_id):
    """Save the user's vote in Firestore."""
    try:
        # Pobierz referencję użytkownika
        user_ref = db.collection("users").document(user_id)

        # Pobierz referencję głosowania
        voting_ref = db.collection("votings").document(voting_id)

        # Pobierz referencję do opcji na podstawie jej ID
        option_ref = db.collection("options").document(selected_option_id)

        # Sprawdź, czy użytkownik już zagłosował
        existing_vote_query = db.collection("votes").where("user_ref", "==", user_ref).where("voting_ref", "==", voting_ref)
        existing_vote = [doc for doc in existing_vote_query.stream()]
        
        if existing_vote:
            # Zaktualizuj istniejący głos
            existing_vote[0].reference.update({"option_ref": option_ref})
        else:
            # Dodaj nowy głos
            db.collection("votes").add({
                "user_ref": user_ref,
                "voting_ref": voting_ref,
                "option_ref": option_ref
            })
        
        print("Głos zapisany pomyślnie.")
    except Exception as e:
        print(f"Błąd podczas zapisywania głosu: {e}")



def get_user_data(user_id):
    """Pobiera dane użytkownika z Firestore na podstawie user_id."""
    try:
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()
        
        if user_doc.exists:
            return user_doc.to_dict()  # Zwraca dane użytkownika jako słownik
        else:
            return None
    except Exception as e:
        print(f"Error fetching user data: {e}")
        return None
    

def get_voting_details(voting_id):
    db = firestore.client()
    voting_doc = db.collection("votings").document(voting_id).get()
    votes_cast, total_users = fetch_vote_stats(voting_id)
    if voting_doc.exists:
        voting_data = voting_doc.to_dict()
        return {
            "title": voting_data["title"],
            "deadline": voting_data["deadline"],
            "author": voting_data["author_ref"],  # Możesz zamienić author_ref na nazwisko, jeśli potrzebujesz dodatkowego zapytania
            "votes_cast": votes_cast,  # Liczba oddanych głosów
            "total_users": total_users  # Liczba użytkowników
        }
    return {}



def get_voting_results(voting_id):
    voting_ref = db.collection("votings").document(voting_id)  # Utwórz referencję na dokument głosowania

    # Pobierz wszystkie opcje związane z danym głosowaniem
    options_ref = db.collection("options").where("voting_id", "==", voting_ref)
    options_docs = options_ref.stream()

    # Pobierz wszystkie głosy związane z danym głosowaniem
    votes_ref = db.collection("votes").where("voting_ref", "==", voting_ref)
    votes_docs = votes_ref.stream()

    # Zlicz głosy na każdą opcję
    vote_counts = {}
    total_votes = 0

    for vote in votes_docs:
        vote_data = vote.to_dict()
        option_ref = vote_data.get("option_ref")  # Pobierz referencję na opcję
        if option_ref:
            option_id = option_ref.id  # ID opcji, na którą oddano głos
            vote_counts[option_id] = vote_counts.get(option_id, 0) + 1
            total_votes += 1

    # Przygotuj wyniki
    results = []
    max_votes = max(vote_counts.values(), default=0)  # Największa liczba głosów dla wygranych opcji

    for option in options_docs:
        option_data = option.to_dict()
        option_id = option.id
        votes_for_option = vote_counts.get(option_id, 0)  # Liczba głosów oddanych na tę opcję
        percentage = (votes_for_option / total_votes * 100) if total_votes > 0 else 0

        # Ustaw kolor tła dla wygranych opcji
        bg_color = "#99ff99" if votes_for_option == max_votes else "#ff9999"

        results.append({
            "candidate": option_data["option"],  # Nazwa opcji (np. imię i nazwisko kandydata)
            "votes": votes_for_option,  # Liczba głosów
            "percentage": f"{percentage:.2f}%",  # Procentowy udział głosów
            "bg": bg_color  # Kolor tła
        })

    return results
