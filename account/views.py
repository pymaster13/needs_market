import random
import datetime

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from yandex_checkout import Configuration, Payment

from .tasks import sms_send, delete_sms
from .models import Code
from market.models import *
from .serializers import *

Configuration.account_id = '712967'
Configuration.secret_key = 'test_sm4w9Xnd6PEP0fmKYGFwPDJ6Rz2FMXwE5EzcXC2EgKU'

class StartRegisterUser(CreateAPIView):
    """
    API function of registration start
    """

    queryset = User.objects.all()
    serializer_class = StartRegisterUserSerializer

    def post(self, request, format=None):
        user_data = self.serializer_class(data=request.data,
                                          context={'request': request})
        if user_data.is_valid():
            valid_user_data = user_data.validated_data
            code = random.randint(1111,9999)
            number = valid_user_data['username']
            body = "Код для регистрации на NeedsMarket: %s." % code
            
            sms_send.delay(code, number, body)
            delete_sms.s(number).apply_async(countdown=60)
            
            code_obj = CodeSerializer(data={'username':valid_user_data['username'], 'code':code})
            
            if code_obj.is_valid():
                code_obj.save()
                return Response({'username':valid_user_data['username'], 'sms':'sended'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': code_obj.errors, 'sms':'not sended'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': user_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class ActivateRegisterUser(APIView):
    """
    API function of registration activation
    """

    queryset = User.objects.all()
    serializer_class = ActivateRegisterUserSerializer

    def post(self, request, format=None):
        user_data = self.serializer_class(data=request.data,
                                          context={'request': request})
        if user_data.is_valid():
            valid_user_data = user_data.validated_data
            code_from_db = Code.objects.filter(username=valid_user_data['username']).order_by('-created').first()

            if(code_from_db.code == valid_user_data['code']):
                first_name = valid_user_data['first_name']
                user_data.save()
                auth_data = AuthenticationSerializer(data=request.data)

                if auth_data.is_valid():
                    valid_auth_data = auth_data.auth(auth_data.validated_data)
                    return Response({'username': valid_auth_data['username'], 
                        'first_name': first_name, 'token': valid_auth_data['token']}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': auth_data.errors}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'success':"False"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': user_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class AuthenticationUser(APIView):
    """
    API function of user authentication
    """

    serializer_class = AuthenticationSerializer

    def post(self, request, format=None):
        user_data = self.serializer_class(data=request.data,
                                          context={'request': request})
        if user_data.is_valid():
            valid_user_data = user_data.auth(user_data.validated_data)
            return Response({'username': valid_user_data['username'], 'first_name': valid_user_data['first_name'], 'token': valid_user_data['token']}, status=status.HTTP_200_OK)
        else:
            return Response({'error': user_data.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': user_data.errors}, status=status.HTTP_400_BAD_REQUEST)

class AuthenticationAdmin(APIView):
    """
    API function of admin authentication
    """

    serializer_class = AdminAuthenticationSerializer

    def post(self, request, format=None):
        user_data = self.serializer_class(data=request.data,
                                          context={'request': request})
        if user_data.is_valid():
            valid_user_data = user_data.auth(user_data.validated_data)
            return Response({'username': valid_user_data['username'], 'first_name': valid_user_data['first_name'], 'admin_token': valid_user_data['admin_token']}, status=status.HTTP_200_OK)
        else:
            return Response({'error': user_data.errors}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': user_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class StartFastRegisterUser(CreateAPIView):
    """
    API function of fast registration start
    """

    queryset = User.objects.all()
    serializer_class = StartFastRegisterUserSerializer

    def post(self, request, format=None):
        user_data = self.serializer_class(data=request.data,
                                          context={'request': request})
        if user_data.is_valid():
            valid_user_data = user_data.validated_data
            
            code = random.randint(1111,9999)
            number = valid_user_data['username']
            password = User.objects.make_random_password()
            valid_user_data['password'] = password
            body = "Ваш пароль: {}. Код для подтверждения быстрой регистрации на NeedsMarket: {}.".format(password,code)
            
            sms_send.delay(code, number, body)
            delete_sms.s(number).apply_async(countdown=60)
            
            code_obj = CodeSerializer(data={'username':valid_user_data['username'],'code':code})
            if code_obj.is_valid():
                code_obj.save()
                return Response({'username':valid_user_data['username'],'password': valid_user_data['password']}, status=status.HTTP_200_OK)
            else:
                return Response({'error': code_obj.errors, 'sms':'not sended'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': user_data.errors}, status=status.HTTP_400_BAD_REQUEST)



class ActivateFastRegisterUser(CreateAPIView):
    """
    API function of fast registration activation
    """

    queryset = User.objects.all()
    serializer_class = ActivateFastRegisterUserSerializer

    def post(self, request, format=None):
        user_data = self.serializer_class(data=request.data,
                                          context={'request': request})
        if user_data.is_valid():
            valid_user_data = user_data.validated_data
            code_from_db = Code.objects.filter(username=valid_user_data['username']).order_by('-created').first()

            if(code_from_db.code == valid_user_data['code']):
                user_data.save()
                data_for_auth = {'username': valid_user_data['username'], 'password': valid_user_data['password'],
                                'first_name': valid_user_data['first_name'], 'code': valid_user_data['code']}
                
                auth_user = AuthenticationSerializer(data=data_for_auth)
                
                if auth_user.is_valid():
                    auth_user_data = auth_user.validated_data
                    auth = auth_user.auth(auth_user_data)
                    return Response({'username': auth_user_data['username'],
                        'first_name': valid_user_data['first_name'], 'token': auth['token']}, status=status.HTTP_200_OK)
                return Response({'success':"False"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'success':"False"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': user_data.errors}, status=status.HTTP_400_BAD_REQUEST)


class StartResetPassword(APIView):
    """
    API function to renew user password
    """

    serializer_class = StartResetPasswordSerializer

    def post(self, request, format=None):
        data = self.serializer_class(data=request.data,
                                     context={'request': request})
        if data.is_valid():
            valid_data = data.validated_data
            code = random.randint(1111,9999)
            number = valid_data['username']
            body = "Код для восстановления пароля на NeedsMarket: {}.".format(code)
            
            sms_send.delay(code, number, body)
            delete_sms.s(number).apply_async(countdown=60)
            
            code_obj = CodeSerializer(data={'username':valid_data['username'], 'code':code})
            if code_obj.is_valid():
                code_obj.save()
                return Response({'username':valid_data['username'], 'sms':'sended'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': code_obj.errors, 'sms':'not sended'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': data.errors}, status=status.HTTP_400_BAD_REQUEST)

class FinishResetPassword(APIView):
    """
    API function to finish renew user password
    """

    serializer_class = FinishResetPasswordSerializer

    def post(self, request, format=None):
        data = self.serializer_class(data=request.data,
                                     context={'request': request})
        if data.is_valid():
            valid_data = data.validated_data
            code = random.randint(1111,9999)
            number = valid_data['username']
            body = "Код для восстановления пароля на NeedsMarket: {}.".format(code)
            
            sms_send.delay(code, number, body)
            delete_sms.s(number).apply_async(countdown=60)
            
            code_obj = CodeSerializer(data={'username':valid_data['username'], 'code':code})
            if code_obj.is_valid():
                code_obj.save()
                return Response({'username':valid_data['username'], 'sms':'sended'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': code_obj.errors, 'sms':'not sended'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': data.errors}, status=status.HTTP_400_BAD_REQUEST)

class FormOrder(APIView):
    """
    API function to creating order
    """

    serializer_class = FormOrderSerializer

    def post(self, request, format=None):
        data = self.serializer_class(data=request.data,
        context={'request': request})
        if data.is_valid():
            valid_data = data.validated_data

            if not valid_data['id']:
                token = valid_data['token']
                user_token = Token.objects.get(key = token)
                user = user_token.user

                total_price = valid_data['cost']
                try:
                    status_order = Status.objects.get(status_name = "Не оплачен")
                except:
                    status_order = Status(status_name = "Не оплачен")
                    status_order.save()

                date = datetime.datetime.strptime(valid_data['date'],'%d.%m.%Y')
                time = datetime.datetime.strptime(valid_data['time'],'%H:%M')

                city = valid_data['city']
                street = valid_data['street']
                house = valid_data['house']
                flat = valid_data['flat']
                adress = Adress(city = city, street = street, house = house, flat = flat)
                adress.save()

                order = Order(user = user, total_price = total_price, status = status_order, date = date,
                time = time, adress = adress)
                order.save()

                goods = valid_data['goods'].split(',')
                goods.pop()

                for id in range(len(goods)):
                    good_and_count = goods[id].split(":")
                    good_name = good_and_count[0]
                    good = Good.objects.get(good_name=good_name)
                    count = good_and_count[1]
                    good_count = GoodCount(good = good, count = count)
                    good_count.save()
                    order.good.add(good_count)

                description = "Заказ №" + str(order.id)

                payment = Payment.create({
                    "amount": {
                        "value": total_price,
                        "currency": "RUB"
                    },
                    "confirmation": {
                        "type": "embedded"
                    },
                    "capture": True,
                    "description": description
                })
                return Response({'order':'created'}, status=status.HTTP_200_OK)

            else:
                id_order = valid_data['id']
                confirmation_token = valid_data['confirmation_token']
                return Response({'id_order':id_order,'confirmation_token': confirmation_token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': data.errors}, status=status.HTTP_400_BAD_REQUEST)
