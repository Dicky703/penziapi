from django.db import models

from django.db import models

class MessageFrom(models.Model):
    msisdn = models.CharField(max_length=15)
    message_content = models.TextField()  # Define a field to store the content of the message
    created_at = models.DateTimeField(auto_now_add=True)  # Assuming you want to track the creation time

    def __str__(self):
        return self.message_content

     
class MessageTo(models.Model):
    short_code = models.CharField(max_length=6)
    response_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.short_code

class Users(models.Model):
    name = models.CharField(max_length=255)
    age = models.IntegerField() 
    gender = models.CharField(max_length=10)
    county = models.CharField(max_length=255)
    town = models.CharField(max_length=255)
    msisdn = models.CharField(max_length = 15)
    level_of_education = models.CharField(max_length=255, blank=True, null=True)
    profession = models.CharField(max_length=255, blank=True, null=True)
    marital_status = models.CharField(max_length=50, blank=True, null=True)
    religion = models.CharField(max_length=50, blank=True, null=True)
    ethnicity = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()
    myself = models.TextField()
    registration_time = models.DateTimeField(auto_now_add=True)

    

    def __str__(self):
        return self.name
