from django.shortcuts import redirect
from decimal import Decimal
from rest_framework import viewsets,status
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from .import serializers
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from rest_framework.response import Response
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse
# for email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    
class UserRegistrationView(APIView):
    serializer_class=serializers.ResistrationSerializer
    def post(self,request):
        serializer=self.serializer_class(data=request.data)

        if serializer.is_valid():
          user=serializer.save()
          token=default_token_generator.make_token(user)
          print("token",token)
          uid=urlsafe_base64_encode(force_bytes(user.pk))
          print("uid",uid)
          confirm_link=f"https://natures-paradise-stlb.onrender.com/register/active/{uid}/{token}/"
          email_subject="Confirm Your Email"
          email_body=render_to_string('confirm_mail.html',{"confirm_link":confirm_link})
          email=EmailMultiAlternatives(email_subject,'',to=[user.email])
          email.attach_alternative(email_body,"text/html")
          email.send()
          return Response({"uid": uid, "token": token}, status=201)  
        return Response(serializer.errors) 


def active(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return JsonResponse({'success': True, 'message': 'User activated successfully.'})
    else:
        return JsonResponse({'success': False, 'message': 'Activation link is invalid.'})
  

class UserLoginApiView(APIView):
    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(username=username, password=password)
            
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': "Invalid user for login .Please sign up!"}, status=400)
        return Response(serializer.errors, status=400)

class LogoutAPIview(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
    

class DepositView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        user = request.user  # Get the authenticated user
        print("Authenticated User:", user)

        if user.is_anonymous:
            return Response({"error": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        deposit_amount = request.data.get('amount')

        if not deposit_amount:
            return Response({"error": "Deposit amount is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
           
            deposit_amount = Decimal(deposit_amount)
            if deposit_amount <= 0:
                return Response({"error": "Deposit amount must be greater than zero."}, status=status.HTTP_400_BAD_REQUEST)

            # Update users balance
            user.balance += deposit_amount
            user.save()

          
            email_subject = "Deposit Confirmation"
            email_body = render_to_string('deposit_confirmation_mail.html', {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'deposit_amount': deposit_amount,
                'new_balance': user.balance,
            })

            # Send the email
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()

            return Response({"message": "Amount deposited successfully! A confirmation email has been sent.", "new_balance": user.balance}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

