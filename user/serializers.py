from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'balance', 'is_admin', 'created_at', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True},
            'confirm_password': {'write_only': True}
        }

    def validate(self, attrs):
        #password validation
        if 'password' in attrs or 'confirm_password' in attrs:
            if attrs.get('password') != attrs.get('confirm_password'):
                raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    def create(self, validated_data):
        # Remove the confirm_password 
        validated_data.pop('confirm_password')

        # user create 
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''), 
            last_name=validated_data.get('last_name', ''),    
            password=validated_data['password']
        )
        return user
    
    def update(self, instance, validated_data):
        
        password = validated_data.pop('password', None) #pesword delete kora hocce
        validated_data.pop('confirm_password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password) #notun password add kora hocce

        instance.save()
        return instance

class ResistrationSerializer(serializers.ModelSerializer):
    confirm_password=serializers.CharField(required=True)
    class Meta:
        model=User
        fields=['username','first_name','last_name','email','password','confirm_password']
    
    def save(self):
        username=self.validated_data['username']
        email=self.validated_data['email']
        first_name=self.validated_data['first_name']
        last_name=self.validated_data['last_name']
        password1=self.validated_data['password']
        password2=self.validated_data['confirm_password']

        if password1!=password2:
            raise serializers.ValidationError({'error':"password Dosen't matched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': "Email Already Exsits"})
        account=User(username=username,first_name=first_name,last_name=last_name,email=email)
        account.set_password(password1)
        account.is_active=False
        account.save()
        return account

class UserLoginSerializer(serializers.Serializer):
    username=serializers.CharField(required=True)
    password=serializers.CharField(required=True)