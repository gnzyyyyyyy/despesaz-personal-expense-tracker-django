from django.db import models

# Create your models here.
from mongoengine import Document, StringField, DateTimeField
from datetime import datetime

class User(Document):
    username = StringField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    created_at = DateTimeField(default=datetime.now())
    updated_at = DateTimeField(default=datetime.now())

    meta = {
        "collection": "users"
    }