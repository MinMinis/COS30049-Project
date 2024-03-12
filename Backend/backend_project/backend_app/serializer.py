from rest_framework import serializers, validators
from django.contrib.auth.models import User
from backend_app.models import *

import re

class UserInfoSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length= 68 , min_length= 6)
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name','phoneNumber' , 'otp')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_password(self, value):
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Passwords must have at least one special character")

        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Passwords must have at least one number")

        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Passwords must have at least one upper character")

        if any(char.isspace() for char in value):
            raise serializers.ValidationError("Passwords cannot have spaces" )
        if not value :
            raise serializers.ValidationError("Passwords cannot be empty") 
        return value

    def validate_email(self, value):
        if not (re.search(r'[^@]*@[^@]*$' , value) ):
            raise serializers.ValidationError("Invalid email format. Please include the @ symbol.")

        if value == "": 
            raise serializers.ValidationError("Email cannot empty")
        
        return value
    
    def validate_username(self, value) :
        if not value : 
            raise serializers.ValidationError("Username cannot be empty")
        return value
    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        phoneNumber = validated_data.get('phoneNumber')
        otp = validated_data.get('otp')
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phoneNumber=phoneNumber ,
            otp = otp 
        )

        return user

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length= 255) 
    password = serializers.CharField(max_length= 60)
    access_token = serializers.CharField(max_length= 255 , read_only=True)
    refresh_token = serializers.CharField(max_length= 255 , read_only=True)
    class Meta:
        model = User
        fields = ('username', 'password', 'access_token', 'refresh_token')
        extra_kwargs = {
            'password': {'write_only': True}
        }

class SearchUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username', 'email', 'first_name', 'last_name','phoneNumber')

class HistoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoryModel
        fields = '__all__'