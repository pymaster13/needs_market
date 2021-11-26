import re

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import *


class StartRegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializer of registration start
    """

    class Meta:
        model = User
        fields = ['username', 'password', 'first_name']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.set_password(validated_data['password'])
        user.first_name = validated_data['first_name']
        user.is_active = False
        user.save()
        return user

    def validate_username(self,username):
        user = list(username)
        if user[0] == '8':
            user.pop(0)
            user.insert(0,'7')
            user.insert(0,'+')
        elif user[0] == '7':
            user.insert(0,'+')

        return "".join(user)

    def validate_first_name(self, first_name):
         error = ''
         if (len(first_name) > 20):
             raise serializers.ValidationError("Invalid length of first_name.")
         
         substr = re.compile('^[А-ЯЁа-яё]+$')
         result = re.match(substr, first_name)
         
         try:
             res = result.group(0)
         except:
             res = ''
         if (res == ''):
            raise serializers.ValidationError("Invalid symbols in first_name.")
         
         return first_name

    def validate_password(self, password):
         error = ''
         if (len(password) < 6):
             raise serializers.ValidationError("Minimal length of password is 6 numbers.")
         substr = re.compile('[А-ЯЁа-яё]+')
         result = re.search(substr, password)
         
         try:
             res = result.group(0)
         except:
             res = ''
         
         if (res):
            raise serializers.ValidationError("Password must be consists of latin symbols.")
         
         return password


class ActivateRegisterUserSerializer(serializers.Serializer):
    """
    Serializer of registration activation
    """

    username = serializers.CharField(required=True,allow_blank=True, write_only=True, label="Username")
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True, max_length=20)
    code = serializers.CharField(max_length=4)

    def create(self, validated_data):
        data = {'username':validated_data['username'], 'password':validated_data['password'],
            'first_name':validated_data['first_name']}
        user = User.objects.create(**data)
        user.set_password(validated_data['password'])
        user.first_name = validated_data['first_name']
        user.is_active = True
        user.save()
        return user

    def validate_username(self,username):
        user = list(username)
        if user[0] == '8':
            user.pop(0)
            user.insert(0,'7')
            user.insert(0,'+')
        elif user[0] == '7':
            user.insert(0,'+')

        return "".join(user)

    def validate_first_name(self, first_name):
         error = ''
         if (len(first_name) > 20):
             raise serializers.ValidationError("Maximal length of first_name is 20 letters.")
         
         substr = re.compile('^[А-ЯЁа-яё]+$')
         result = re.match(substr, first_name)
         
         try:
             res = result.group(0)
         except:
             res = ''
         if (res == ''):
            raise serializers.ValidationError("First_name must consists of russian letters only.")
         return first_name

    def validate_password(self, password):
         password = password
         error = ''
         if (len(password) < 6):
             raise serializers.ValidationError("Minimal length of password is 6 numbers.")
         substr = re.compile('[А-ЯЁа-яё]+')
         result = re.search(substr, password)
         
         try:
             res = result.group(0)
         except:
             res = ''
         if (res):
            raise serializers.ValidationError("Password must be consists of latin symbols")
         
         return password


class CodeSerializer(serializers.ModelSerializer):
    """
    Serializer of sms-code
    """

    class Meta:
        model = Code
        fields = ['username', 'code']

    def create(self, validated_data):
        code = Code.objects.create(**validated_data)
        code.save()
        return code

    def validate_username(self,username):
        user = list(username)
        if user[0] == '8':
            user.pop(0)
            user.insert(0,'7')
            user.insert(0,'+')
        elif user[0] == '7':
            user.insert(0,'+')

        return "".join(user)

class AuthenticationSerializer(serializers.Serializer):
    """
    Serializer of user authentication
    """

    username = serializers.CharField(required=True,allow_blank=True, write_only=True, label="Username")
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    token = serializers.CharField(allow_blank=True, read_only=True)

    def validate_password(self, password):
        if not password:
            raise serializers.ValidationError("Please enter password to login.")
        error = ''

        if (len(password) < 6):
            raise serializers.ValidationError("Minimal length of password is 6 numbers.")

        substr = re.compile('[А-ЯЁа-яё]+')
        result = re.search(substr, password)

        try:
            res = result.group(0)
        except:
             res = ''
        if (res):
           raise serializers.ValidationError("Password must be consists of latin symbols'")

        return password

    def auth(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']

        name_list = list(username)
        if name_list[0] == '8':
            name_list.pop(0)
            name_list.insert(0,'7')
            name_list.insert(0,'+')
            str = ""
            username = str.join(name_list)

        elif name_list[0] == '7':
            name_list.insert(0,'+')
            str = ""
            username = str.join(name_list)

        try:
            user = User.objects.get(username=username)
        except:
            raise serializers.ValidationError("User not exists.")

        if user:
            result = user.check_password(password)
            if not user.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        if user.is_active:
            token, created = Token.objects.get_or_create(user=user)
            validated_data['token'] = token.key
            validated_data['first_name'] = user.first_name
            return validated_data
        else:
            raise serializers.ValidationError("User not active.")


class AdminAuthenticationSerializer(serializers.Serializer):
    """
    Serializer of admin authentication
    """

    username = serializers.CharField(required=True,allow_blank=True, write_only=True, label="Username")
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    token = serializers.CharField(allow_blank=True, read_only=True)

    def validate_password(self, password):
        if not password:
            raise serializers.ValidationError("Please enter password to login.")
        error = ''

        substr = re.compile('[А-ЯЁа-яё]+')
        result = re.search(substr, password)

        try:
            res = result.group(0)
        except:
             res = ''
        if (res):
           raise serializers.ValidationError("Password must be consists of latin symbols'")

        return password

    def auth(self, validated_data):
        try:
            username = validated_data['username']
            password = validated_data['password']
            user = User.objects.get(username=username)
        except:
            raise serializers.ValidationError("Admin not exists.")

        if user:
            result = user.check_password(password)
            if not user.check_password(password):
                raise serializers.ValidationError("Invalid credentials.")

        if user.is_staff:
            token = Token.objects.get(user=user)
            validated_data['admin_token'] = token.key
            validated_data['first_name'] = user.first_name
            return validated_data
        else:
            raise serializers.ValidationError("You are not admin!")


class StartFastRegisterUserSerializer(serializers.ModelSerializer):
    """
    Serializer of fast user registration
    """

    class Meta:
        model = User
        fields = ['username', 'first_name']

    def validate_username(self,username):
        user = list(username)
        if user[0] == '8':
            user.pop(0)
            user.insert(0,'7')
            user.insert(0,'+')
        elif user[0] == '7':
            user.insert(0,'+')

        return "".join(user)

    def validate_first_name(self, first_name):
         error = ''
         if (len(first_name) > 20):
             raise serializers.ValidationError("Maximal length of first_name is 20 letters.")

         substr = re.compile('^[А-ЯЁа-яё]+$')
         result = re.match(substr, first_name)

         try:
             res = result.group(0)
         except:
             res = ''
         if (res == ''):
            raise serializers.ValidationError("First name must consists of russian letters only.")

         return first_name


class ActivateFastRegisterUserSerializer(serializers.Serializer):
    """
    Serializer of fast registration activation
    """

    username = serializers.CharField(required=True,allow_blank=True, write_only=True, label="Username")
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True, max_length=20)
    code = serializers.CharField(max_length=4)

    def create(self, validated_data):
        data = {'username':validated_data['username'], 'password':validated_data['password'],
            'first_name':validated_data['first_name']}
        user = list(data['username'])

        if user[0] == '8':
            user.pop(0)
            user.insert(0,'7')
            user.insert(0,'+')
            data['username'] = "".join(user)

        elif user[0] == '7':
            user.insert(0,'+')
            str = ""
            user_str = str.join(user)
            data['username'] = user_str

        user = User.objects.create(**data)
        user.set_password(validated_data['password'])
        user.first_name = validated_data['first_name']
        user.is_active = True
        user.save()

        return user

    def validate_first_name(self, first_name):
         error = ''
         if (len(first_name) > 20):
             raise serializers.ValidationError("Maximal length of first_name is 20 letters.")
         
         substr = re.compile('^[А-ЯЁа-яё]+$')
         result = re.match(substr, first_name)
         
         try:
             res = result.group(0)
         except:
             res = ''
         if (res == ''):
            raise serializers.ValidationError("First name must consists of russian letters only.")
         
         return first_name

    def validate_password(self, password):
         error = ''
         if (len(password) < 6):
             raise serializers.ValidationError("Minimal length of password is 6 numbers.")
         
         substr = re.compile('[А-ЯЁа-яё]+')
         result = re.search(substr, password)
         
         try:
             res = result.group(0)
         except:
             res = ''
         if (res):
            raise serializers.ValidationError("Password must be consists of latin symbols.")
         
         return password

class StartResetPasswordSerializer(serializers.Serializer):
    """
    Serializer of start password reset
    """
    
    username = serializers.CharField(required=True,allow_blank=True, write_only=True, label="Username")

    class Meta:
        model = User
        fields = ['username']

    def validate_username(self,username):
        user = list(username)
        if user[0] == '8':
            user.pop(0)
            user.insert(0,'7')
            user.insert(0,'+')
        elif user[0] == '7':
            user.insert(0,'+')

        return "".join(user)

class FinishResetPasswordSerializer(serializers.Serializer):
    """
    Serializer of activate password reset
    """

    username = serializers.CharField(required=True,allow_blank=True, write_only=True, label="Username")
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    code = serializers.CharField(max_length=4)

    class Meta:
        model = User
        fields = ['username', 'password', 'code']

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        user.save()
        return user

    def validate_username(self,username):
        user = list(username)
        if user[0] == '8':
            user.pop(0)
            user.insert(0,'7')
            user.insert(0,'+')
        elif user[0] == '7':
            user.insert(0,'+')

        return "".join(user)

    def update(self, validated_data):
        data = {'username':validated_data['username'], 'password':validated_data['password']}
        user = User.objects.get(username = data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_password(self, password):
         error = ''
         if (len(password) < 6):
             raise serializers.ValidationError("Minimal length of password is 6 numbers.")

         substr = re.compile('[А-ЯЁа-яё]+')
         result = re.search(substr, password)

         try:
             res = result.group(0)
         except:
             res = ''
         if (res):
            raise serializers.ValidationError("Password must be consists of latin symbols")

         return password

class FormOrderSerializer(serializers.Serializer):

    id = serializers.CharField(allow_blank=True, write_only=True, label="Id")
    confirmation_token = serializers.CharField(allow_blank=True, write_only=True, label="Confirmation Token")
    token = serializers.CharField(required=True,allow_blank=True, write_only=True, label="Token")
    goods = serializers.CharField(required=True,allow_blank=True, write_only=True, label="Goods")
    cost = serializers.CharField(required=True,allow_blank=True, write_only=True, label="Cost")
    city = serializers.CharField(required=True,allow_blank=True, write_only=True, label="City")
    street = serializers.CharField(required=True,allow_blank=True, write_only=True, label="Street")
    house = serializers.CharField(required=True,allow_blank=True, write_only=True, label="House")
    flat = serializers.CharField(required=True,allow_blank=True, write_only=True, label="Flat")
    date = serializers.CharField(required=True,allow_blank=True, write_only=True, label="Date")
    time = serializers.CharField(required=True,allow_blank=True, write_only=True, label="Time")