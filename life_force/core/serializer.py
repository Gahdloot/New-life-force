from rest_framework import serializers
from .models import Client, Organization



class ClientSignup(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'email', 
            'password'
            ]




class ClientCompleteRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        read_only_fields = ['email', 'password']
        fields = [
            "first_name",
            "last_name",
            "phone_number",
            "location",
            "age",
            "weight",
            "blood_group",
            "wants_to_donate",
   
        ]

class OrganizationCompleteRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        read_only_fields = ['email', 'password']
        fields = [
            "company_name",
            "location",
   
        ]

class ClientMarketplace(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['first_name',
                    'last_name',
                    'blood_group',
                    'age',
                    'weight',
                    'is_verified']