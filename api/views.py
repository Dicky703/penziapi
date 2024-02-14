from .models import Users, MessageFrom, MessageTo
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PenziMessageSerializer
import logging
import random

class PenziMessageView(APIView):
    serializer_class = PenziMessageSerializer 
    logger = logging.getLogger(__name__)  # Define logger

    def post(self, request):
        # Deserialize the request data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Extract validated data
        message_content = serializer.validated_data['message_content']
        msisdn = serializer.validated_data.get('msisdn')
        short_code = serializer.validated_data.get('short_code')
        
        # Generate response message
        response_message = self.generate_response_message(message_content)
        
        # Save message sender and response to the database
        self.save_message_from(message_content, msisdn)
        self.save_message_to(response_message, short_code)

        # Route based on message content
        if message_content.startswith('start#'):
            self.save_user_info(message_content, msisdn)
        elif message_content.startswith('details#'):
            self.update_user_info(msisdn, message_content)

        # Return response
        return Response({'message': response_message})

    def generate_response_message(self, message_content):
        # Log message generation
        logger = logging.getLogger(__name__)
        logger.debug(f"Generating response message for content: {message_content}")

        # Generate response based on message content
        if message_content.startswith('penzi'):
            response_message = "Welcome to our dating service with 6000 potential dating partners! To register SMS start#name#age#gender#county#town to 22141. E.g., start#John Doe#26#Male#Nakuru#Naivasha"
        elif message_content.startswith('start#'):
            response_message = self.process_start_message(message_content)
        elif message_content.startswith('details#'):
            response_message = self.process_details_message(message_content)
        elif message_content.startswith('MYSELF'):
            response_message = self.process_myself_message(message_content)
        elif message_content.startswith('Match'):
            response_message = self.process_match_message(message_content)
        else:
            response_message = "Please send a message starting with the word 'penzi' to 22141."

        # Log generated response
        logger.debug(f"Generated response message: {response_message}")
        return response_message

    def save_message_from(self, message_content, msisdn):
        # Save message sender to the database
        MessageFrom.objects.create(message_content=message_content, msisdn=msisdn)

    def save_message_to(self, response_message, short_code):
        # Save response message to the database
        if response_message is not None:  
            MessageTo.objects.create(response_content=response_message, short_code=short_code)
        else:
            response_message = "response message is empty"
            MessageTo.objects.create(response_content=response_message, short_code=short_code)

    def save_user_info(self, message_content, msisdn):
        # Save user information to the database if user does not exist
        if not Users.objects.filter(msisdn=msisdn).exists():
            split_content = message_content.split('#')
            if len(split_content) >= 6:
                name, age, gender, county, town = split_content[1:]
                Users.objects.create(name=name, age=age, gender=gender, county=county, town=town, msisdn=msisdn) 

    def update_user_info(self, msisdn, message_content):
        # Update user information in the database
        split_content = message_content.split("#")
        if len(split_content) >= 6:
            level_of_education, profession, marital_status, religion, ethnicity = split_content[1:6]
            try:
                user = Users.objects.get(msisdn=msisdn)
                user.level_of_education = level_of_education
                user.profession = profession
                user.marital_status = marital_status
                user.religion = religion
                user.ethnicity = ethnicity
                user.save()
            except Users.DoesNotExist:
                pass

    def process_start_message(self, message_content):
        # Process start message
        split_content = message_content.split("#")
        if len(split_content) < 6:
            return "Less details provided"
        else:
            name = split_content[1]
            return f'Your profile has been created successfully {name}. SMS details#levelOfEducation#profession#maritalStatus#religion#ethnicity to 22141.'

    def process_details_message(self, message_content):
        # Process details message
        split_content = message_content.split("#")
        if len(split_content) < 7:  
            return  "This is the last stage of registration. SMS a brief description of yourself to 22141 starting with the word MYSELF. E.g., MYSELF chocolate, lovely, sexy etc."
        else:
            msisdn = split_content[0]  
            level_of_education, profession, marital_status, religion, ethnicity = split_content[1:6]
            try:
                user = Users.objects.get(msisdn=msisdn)
                user.age = age  # Update age
                user.level_of_education = level_of_education
                user.profession = profession
                user.marital_status = marital_status
                user.religion = religion
                user.ethnicity = ethnicity
                user.save()

            except Users.DoesNotExist:
                pass
        
    def process_myself_message(self, message_content):
        # Process MYSELF message
        description = message_content.split('MYSELF ')[1].strip()  
        msisdn = self.request.data.get('msisdn')  
    
        try:
            user = Users.objects.get(msisdn=msisdn)
            user.description = description  # Update description
            user.save()
        
            return "You are now registered for dating. To search for a MPENZI, SMS match#age#town to 22141 and meet the person of your dreams. E.g., match#23-25#Kisumu."
        except Users.DoesNotExist:
            return "User not found."

    def process_match_message(self, message_content):
        # Process Match message
        _, age_range, location = message_content.split('#')
        lower_age, upper_age = map(int, age_range.split('-'))
        potential_matches = Users.objects.filter(age__gte=lower_age, age__lte=upper_age, county=location)
        if potential_matches.exists():
            selected_matches = random.sample(list(potential_matches), min(3, potential_matches.count()))
            response = []
            for match in selected_matches:
                response.append(f"{match.name}, aged {match.age}, MSISDN: {match.msisdn}, ")
            return ', '.join(response)
        else:
            return "No matches found based on the provided criteria."
