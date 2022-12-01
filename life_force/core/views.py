from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import status
from .models import Client, Organization
from .serializer import ClientCompleteRegistrationSerializer, OrganizationCompleteRegistrationSerializer
# Create your views here.


@api_view(['POST'])
def sign_up(request):
    """
    Accepts only email and password only
    """
    user = Client(email=request.data['email'], password=request.data['email'])
    user.save()
    token, created = Token.objects.get_or_create(user=user)
    return Response({'user': user.email, 'token': token.key})


@api_view(["POST"])
@permission_classes([AllowAny])
def login_user(request):

        data = {}
        try:

            Account = Client.objects.get(email=request.data['email'])
        except Client.DoesNotExist as e:
            return Response({'message':'email doesnot exist'})

        token = Token.objects.get_or_create(user=Account)[0].key
        print(token)
        if not Account.check_password(request.data['password'], Account.password):
            return Response({"message": "Incorrect Login credentials"})

        if Account:
            if Account.is_active:
                print(request.user)
                login(request, Account)
                data["message"] = "user logged in"
                data["email_address"] = Account.email

                Res = {"data": data, "token": token}

                return Response(Res)

            else:
                return Response({"400": f'Account not active'})

        else:
            return Response({"400": f'Account doesnt exist'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_client_registration(request):
    try:
        Account = Client.objects.get(email=request.data['email'])
    except Client.DoesNotExist:
        return Response({'sucess':False, 'message':'account doesnot exist'})
    serializer = ClientCompleteRegistrationSerializer(request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'message':'Registration complete'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_orgaanization_registration(request):
    Account = Organization.objects.get(email=request.data['email'])
    serializer = OrganizationCompleteRegistrationSerializer(request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'message':'Registration complete'})

