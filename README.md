# Needs Market

This project is a backend of online food store (2020). 
Developers team (4 people) used Django Rest Framework (2 people, including me) on backend side and React (2 people) on frontend side.

## Getting Started
Python version: 3.7.5

Clone project:
```
git clone https://github.com/pymaster13/needs_market.git && cd needs_market
```

Create and activate virtual environment:
```
python3 -m venv venv && source venv/bin/activate
```

Install libraries:
```
python3 -m pip install -r requirements.txt
```

Run local Django server:
```
python3 manage.py runserver
```

## Functional

The clients and admin sides are realized.
* Client can register (fully and quickly (only by phone number) modes) and confirm registration, authenticate, reset password, make order and pay it.
* Admin may view all categories, goods, orders, users and statistics on the above.

### Features

Main libraries that are used : 
* Django 3,
* djangorestframework,
* twilio (for sending sms),
* celery and redis (for asynchronous sending sms), 
* yandex-checkout (for payment). 
