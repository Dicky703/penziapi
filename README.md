Penzi Dating Service App
Overview
Penzi is a dating service application built using Django and Django REST Framework. It allows users to interact with the service via SMS messages and provides matchmaking based on age range and location.

Components
The application consists of the following main components:

MatchProcessor: A class responsible for processing match messages to find potential matches based on age range and town.

PenziMessageView: An APIView subclass that handles incoming SMS messages and responds accordingly. It utilizes MatchProcessor to process match messages and interacts with the database to save user information and messages.

Installation
To run the Penzi Dating Service App locally, follow these steps:

Clone the repository:

bash
Copy code
git clone https://github.com/Dicky703/penziapi.git
Navigate to the project directory:

bash
Copy code
cd penzi-dating-service
Install the dependencies:

bash
Copy code
pip install -r requirements.txt
Configure the database settings in settings.py.

Run the migrations to create the database schema:

bash
Copy code
python manage.py migrate
Start the development server:

bash
Copy code
python manage.py runserver
Access the application at http://localhost:8000.

Usage
Send an SMS message to the designated number (e.g., 22141) with the following formats:

penzi: To initiate the dating service.
start#name#age#gender#county#town: To create a profile.
details#level_of_education#profession#marital_status#religion#ethnicity: To provide additional details for the profile.
MYSELF description: To provide a self-description.
match#age_range#town: To find potential matches based on age range and town.
NEXT: To see more potential matches.
Receive responses and updates from the Penzi Dating Service.

Configuration
Database: The application uses MySQL as the database backend. Configure the database connection parameters in settings.py.

Logging: Logging configuration is set up to log errors and exceptions to the console.

Dependencies
Django: A high-level Python web framework for rapid development.
Django REST Framework: A powerful and flexible toolkit for building Web APIs.
MySQL Connector: A Python driver for MySQL.
Requests: An elegant and simple HTTP library for Python.
Contributors
Dixon Lemayian
Contributor 1
License
This project is licensed under the MIT License - see the LICENSE file for details.

