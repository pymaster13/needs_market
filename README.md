# Needs Market

This project is a backend of online food store (2020). 
A team (4 people) project that was implemented on Django Rest Framework (2 people, including me) and React (2 people).

## Getting Started

Clone project:
```
mkdir project && cd project
git clone https://github.com/pymaster13/needs_market.git
cd needs_market
```

Create and activate virtual environment:
```
python3.7 -m venv venv
source venv/bin/activate
```

Install libraries:
```
python3.7 -m pip install -r requirements.txt
```

Run local Django server:
```
python3.7 manage.py runserver
```

## Functional

The clients and admin sides are realized.
Client can register (fully and quickly (only by phone number) modes) and confirm registration, authenticate, reset_password, make order.
Admin may view all categories, goods, orders, users and statistics on the above.

### Features

There are used: Django3, djangorestframework, twilio (for sending sms), celery and redis (for asynchronous sending sms). 
