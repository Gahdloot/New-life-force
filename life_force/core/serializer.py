from rest_framework import serializers
from .models import Client, Organization



class ClientCompleteRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
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
        fields = [
            "company_name",
            "location",
   
        ]