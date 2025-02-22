# VotingApp

The **VotingApp** is a Python application that enables users to create and participate in online voting sessions. It utilizes Firebase Firestore for data storage and Tkinter for the graphical user interface.

## Features

- **Create Polls**: Users can create new voting sessions with multiple options.
- **Vote Participation**: Registered users can cast their votes.
- **Real-time Results**: Track the number of votes in real-time.
- **User Authentication**: Secure login using Firebase Authentication.

## Requirements

To run this application, you need the following:

- Python 3.x
- Tkinter (built into Python standard library)
- Firebase Admin SDK for Python (`firebase-admin`)

## Installation

### Step 1: Clone the Repository
```bash
git clone https://github.com/JedrzejSobkow/VotingApp.git
cd VotingApp
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Firebase
- Create a Firebase project and set up Firestore Database.
- Download `firebase_config.json` and place it in the project directory.

### Step 4: Run the Application
```bash
python main.py
```
