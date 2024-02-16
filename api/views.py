import logging
import mysql.connector
from .models import Users, MessageFrom, MessageTo
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PenziMessageSerializer
from django.conf import settings

class MatchProcessor:
    def __init__(self, db_params):
        """
        Initialize MatchProcessor with database parameters and logger.
        """
        self.db_params = db_params
        self.last_processed_index = 0
        self.logger = logging.getLogger(__name__)  # Initialize logger

    def process_match_message(self, message_content):
        """
        Process match message to find potential matches based on age range and town.
        """
        try:
            if message_content.startswith('match#'):
                _, age_range_str, town = message_content.split('#')
                lower_age, upper_age = map(int, age_range_str.split('-'))

                connection = mysql.connector.connect(**self.db_params)
                cursor = connection.cursor()

                cursor.execute("SELECT * FROM api_users WHERE age BETWEEN %s AND %s AND town = %s", (lower_age, upper_age, town))
                potential_matches = cursor.fetchall()

                if not potential_matches:
                    connection.close()
                    return "No potential matches found."

                response = self.format_matches_response(potential_matches[:3])
                connection.close()

                response += "\nSend 'NEXT' to see more potential matches."
                return response

            elif message_content == 'NEXT':
                connection = mysql.connector.connect(**self.db_params)
                cursor = connection.cursor()

                cursor.execute("SELECT * FROM api_users LIMIT %s, 3", (self.last_processed_index,))
                potential_matches = cursor.fetchall()

                if not potential_matches:
                    connection.close()
                    return "No more potential matches found."

                response = self.format_matches_response(potential_matches)
                connection.close()

                self.last_processed_index += 3

                return response

            else:
                return "Please send a valid message in the format e.g, 'match#26_30#town' or 'NEXT'."

        except Exception as e:
            self.logger.exception("An error occurred while processing the message.")
            return "An error occurred while processing the message."

    def format_matches_response(self, potential_matches):
        """
        Format potential matches response.
        """
        response = ""
        for match in potential_matches:
            response += f"{match[1]}, aged: {match[2]}, MSISDN: {match[3]}"
        return response.strip()


class PenziMessageView(APIView):
    serializer_class = PenziMessageSerializer
    logger = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        """
        Initialize PenziMessageView with database parameters and MatchProcessor.
        """
        super().__init__(*args, **kwargs)
        self.db_params = {
            "host": "localhost",
            "database": "penzi",
            "user": "mpenzi",
            "password": "mpenzi2000"
        }
        self.match_processor = MatchProcessor(self.db_params)

    def post(self, request):
        """
        Handle POST requests.
        """
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            message_content = serializer.validated_data['message_content']
            msisdn = serializer.validated_data.get('msisdn')
            short_code = serializer.validated_data.get('short_code')

            response_message = self.generate_response_message(message_content)

            self.save_message_from(message_content, msisdn)
            self.save_message_to(response_message, short_code)

            if message_content.startswith('start#'):
                self.save_user_info(message_content, msisdn)
            elif message_content.startswith('details#'):
                self.update_user_info(msisdn, message_content)

            return Response({'message': response_message})
        except Exception as e:
            self.logger.exception("An error occurred while processing the request.")
            return Response({'error': 'An unexpected error occurred.'}, status=500)

    def generate_response_message(self, message_content): 
        """
        Generate response message based on message content.
        """
        if message_content.startswith('penzi'):
            return "Welcome to our dating service with 6000 potential dating partners! To register SMS start#name#age#gender#county#town to 22141. E.g., start#John Doe#26#Male#Nakuru#Naivasha"
        elif message_content.startswith('start#'):
            return self.process_start_message(message_content)
        elif message_content.startswith('details#'):
            return self.process_details_message(message_content)
        elif message_content.startswith('MYSELF'):
            return self.process_myself_message(message_content)
        elif message_content.startswith('match#') or message_content == 'NEXT': 
            return self.match_processor.process_match_message(message_content)
        else:
            return "Please send a message starting with the word 'penzi' to 22141."

    def save_message_from(self, message_content, msisdn):
        """
        Save message sender information to the database.
        """
        try:
            MessageFrom.objects.create(message_content=message_content, msisdn=msisdn)
        except Exception as e:
            self.logger.exception("Error while saving message sender.")

    def save_message_to(self, response_message, short_code):
        """
        Save response message to the database.
        """
        try:
            if response_message is not None:  
                MessageTo.objects.create(response_content=response_message, short_code=short_code)
            else:
                response_message = "response message is empty"
                MessageTo.objects.create(response_content=response_message, short_code=short_code)
        except Exception as e:
            self.logger.exception("Error while saving response message.")

    def save_user_info(self, message_content, msisdn):
        """
        Save user information to the database.
        """
        try:
            if not Users.objects.filter(msisdn=msisdn).exists():
                split_content = message_content.split('#')
                if len(split_content) >= 6:
                    name, age, gender, county, town = split_content[1:]
                    Users.objects.create(name=name, age=age, gender=gender, county=county, town=town, msisdn=msisdn)
        except Exception as e:
            self.logger.exception("Error while saving user information.")

    def update_user_info(self, msisdn, message_content):
        """
        Update user information in the database.
        """
        try:
            split_content = message_content.split("#")
            if len(split_content) >= 6:
                level_of_education, profession, marital_status, religion, ethnicity = split_content[1:6]
                user = Users.objects.get(msisdn=msisdn)
                user.level_of_education = level_of_education
                user.profession = profession
                user.marital_status = marital_status
                user.religion = religion
                user.ethnicity = ethnicity
                user.save()
        except Users.DoesNotExist:
            self.logger.exception("User does not exist.")
        except Exception as e:
            self.logger.exception("Error while updating user information.")

    def process_start_message(self, message_content):
        """
        Process start message.
        """
        try:
            split_content = message_content.split("#")
            if len(split_content) < 6:
                return "Less details provided"
            else:
                name = split_content[1]
                return f'Your profile has been created successfully {name}. SMS details#levelOfEducation#profession#maritalStatus#religion#ethnicity to 22141.'
        except Exception as e:
            self.logger.exception("Error while processing start message.")
            return "An error occurred while processing your request."

    def process_details_message(self, message_content):
        """
        Process details message.
        """
        try:
            split_content = message_content.split("#")
            if len(split_content) < 7:  
                return  "This is the last stage of registration. SMS a brief description of yourself to 22141 starting with the word MYSELF. E.g., MYSELF chocolate, lovely, sexy etc."
            else:
                msisdn = split_content[0]  
                level_of_education, profession, marital_status, religion, ethnicity = split_content[1:6]
                user = Users.objects.get(msisdn=msisdn)
                user.level_of_education = level_of_education
                user.profession = profession
                user.marital_status = marital_status
                user.religion = religion
                user.ethnicity = ethnicity
                user.save()
        except Users.DoesNotExist:
            self.logger.exception("User does not exist.")
        except Exception as e:
            self.logger.exception("Error while processing details message.")
            return "An error occurred while processing your request please enter details..."

    def process_myself_message(self, message_content):
        """
        Process MYSELF message.
        """
        try:
            description = message_content.split('MYSELF ')[1].strip()
            msisdn = self.request.data.get('msisdn')  

            user = Users.objects.get(msisdn=msisdn)
            user.description = description
            user.save()

            return "You are now registered for dating. To search for a MPENZI, SMS match#age#town to 22141 and meet the person of your dreams.E.g., match#23-25#Kisumu"
        except Users.DoesNotExist:
            self.logger.exception("User does not exist.")
            return "User not found."
        except Exception as e:
            self.logger.exception("Error while processing MYSELF message.")
            return "An error occurred while processing your request."
