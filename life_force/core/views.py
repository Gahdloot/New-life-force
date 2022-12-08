from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from rest_framework import status
from .models import Client, Organization, User
from .serializer import ClientCompleteRegistrationSerializer, OrganizationCompleteRegistrationSerializer, ClientMarketplace
from .filter import ClientFilter
from .verification import Verify
from django_filters.utils import translate_validation
# Create your views here.




@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    data = {}
    data['success'] = True
    data['message'] = 'Nigeria collects only 500,000 pints yearly, which represent only 36.7%\ of blood donation capacity. You can help make up for the 73.3%\ shortfall.'
    return Response(data)


@api_view(['POST'])
@permission_classes([AllowAny])
def Client_sign_up(request):
    """
    Accepts only email and password only
    """
    try:
        Account = Client.objects.get(email=request.data)
        return Response({'success':False, 'message':'email exist already'}, status=status.HTTP_226_IM_USED)
    except:
    
        user = Client.objects.create(email=request.data['email'], password=request.data['password'])
        user.base_role = User.Role.CLIENT
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'user': user.email, 'token': token.key, 'base_role': user.base_role})



@api_view(['POST'])
@permission_classes([AllowAny])
def Organization_sign_up(request):
    """
    Accepts only email and password only
    """
    try:
        Account = Organization.objects.get(email=request.data)
        return Response({'success':False, 'message':'email exist already'}, status=status.HTTP_226_IM_USED)
    except:
    
        user = Organization.objects.create(email=request.data['email'], password=request.data['password'])
        user.base_role = User.Role.ORGANIZATION
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'user': user.email, 'token': token.key})





@api_view(["GET"])
@permission_classes([AllowAny])
def login_user(request):

    data = {}
    try:

        Account = Client.objects.get(email=request.data['email'])
    except Client.DoesNotExist:
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
        return Response({'sucess':False,"400": f'Account doesnt exist'})





@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_client_registration(request):
    try:
        Account = Client.objects.get(email=request.user.email)
    except Client.DoesNotExist:
        return Response({'sucess':False, 'message':'account doesnot exist'})
    serializer = ClientCompleteRegistrationSerializer(instance=Account, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'sucess':True,'message':'Registration complete'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def complete_orgaanization_registration(request):
    try:
        Account = Organization.objects.get(email=request.user.email)
    except Client.DoesNotExist:
        return Response({'sucess':False, 'message':'account doesnot exist'})
    serializer = OrganizationCompleteRegistrationSerializer(instance=Account, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response({'sucess':False,'message':'Registration complete'})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def kyc_verification(request):
    if request.user.base_role == User.Role.CLIENT or request.user.base_role == User.Role.ANON:
        vr = Verify()
        if vr.nin_verification(number=request.data['nin']):
            try:
                Account = Client.objects.get(email=request.user.email)
                Account.nin = request.data['nin']
                Account.is_verified = True
                return Response({'sucess':True, 'message':'Nin updated'}, status=status.HTTP_202_ACCEPTED)
            except Client.DoesNotExist:
                return Response({'sucess':False, 'message':'account doesnot exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            #trsh line for modification
            Account = Client.objects.get(email=request.user.email)
            Account.nin = request.data['nin']
            Account.is_verified = True
            #end of trash line
            return Response({'sucess':True, 'message':'nin not verified originally'}, status=status.HTTP_412_PRECONDITION_FAILED) 
    elif request.user.base_role == User.Role.ORGANIZATION:
        if Verify.nin_verification(number=request.data['cac']):
            try:
                Account = Organization.objects.get(email=request.user.email)
                Account.CAC = request.data['cac']
                Account.is_verified = True
            except Organization.DoesNotExist:
                return Response({'sucess':False, 'message':'account doesnot exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'sucess':False, 'message':'CAC not verified'}, status=status.HTTP_412_PRECONDITION_FAILED) 
            
    
    return Response({'sucess':False, 'message':f'Cannot find a user role {request.user.email}  {request.user.base_role}'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    if request.user.base_role == User.Role.CLIENT or request.user.base_role == User.Role.ANON:
        try:

            Account = Client.objects.get(email=request.user.email)
            serializer = ClientCompleteRegistrationSerializer(Account)
            return Response(serializer.data, status=status.HTTP_302_FOUND)
        except Client.DoesNotExist:
            return Response({'sucess':False, 'message':'email doesnot exist'}, status=status.HTTP_302_FOUND)
    elif request.user.base_role == User.Role.ORGANIZATION:
        try:

            Account = Client.objects.get(email=request.user.email)
            serializer = ClientCompleteRegistrationSerializer(Account)
            return Response({serializer.data}, status=status.HTTP_302_FOUND)
        except Client.DoesNotExist:
            return Response({'sucess':False, 'message':'email doesnot exist'}, status=status.HTTP_302_FOUND)
    return Response({'sucess':False, 'message':'email doesnot exist'}, status=status.HTTP_302_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def marketpalce(request):
    all_accounts = Client.objects.all()
    filterset = ClientFilter(request.GET, queryset=all_accounts)
    if filterset.is_valid():
        queryset = filterset.qs
    else:
        raise translate_validation(filterset.errors)
    serializer = ClientMarketplace(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_token(request):
    account = User.objects.get(email=request.data['email'])
    token = Token.objects.get_or_create(user=account)[0].key
    return Response({'email': account.email, 'token': token})