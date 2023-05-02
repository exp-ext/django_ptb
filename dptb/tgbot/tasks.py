from celery import Celery
from django.apps import apps as django_apps
from django.contrib.auth import get_user_model

User = get_user_model()
Group = django_apps.get_model(app_label='users', model_name='Group')
GroupConnections = django_apps.get_model(
    app_label='users', model_name='GroupConnections'
)

app = Celery()
