import os

from twilio.rest import Client
from celery import shared_task

from foodmarket.settings import  SENDSMS_FROM_NUMBER, SENDSMS_ACCOUNT_SID, SENDSMS_AUTH_TOKEN
from .models import Code

"""
Запуск брокера : "redis-server"
Запуск воркеров CELERY : "celery -A foodmarket worker --loglevel=info --pool=solo"
Запуск логгера FLOWER: "flower -A foodmarket"
"""

@shared_task()
def sms_send(code, number, body):
    try:
        client = Client(SENDSMS_ACCOUNT_SID,SENDSMS_AUTH_TOKEN)
        client.messages.create(
            to=number,
            from_=SENDSMS_FROM_NUMBER,
            body=body
        )
        return {'sended':'True'}
    except:
        return {'sended':'False'}

@shared_task()
def delete_sms(number):
    try:
        user_codes = Code.objects.filter(username = number).delete()
    except:
        return {'success':'False'}
