from django.db import models

# Create your models here.
from mongoengine import (
    Document,
    StringField,
    DateTimeField,
    FloatField,
    ReferenceField
)
from datetime import datetime
from users.models import User

CATEGORIES = [
    'housing', 'food', 'utilities', 'transportation',
    'entertainment', 'health_care', 'miscellaneous',
    'salary', 'investments', 'gifts', 'refunds', 'other'    
]

TYPE = [
    'income', 'expense'
]

class Transaction(Document):
    user = ReferenceField(User, required=True)

    title = StringField(required=True)
    amount = FloatField(required=True)
    type = StringField(required=True, choices=TYPE, default='expense')
    category = StringField(required=True, choices=CATEGORIES, default='other')
    date = DateTimeField(default=datetime.now)
    createdAt = DateTimeField(default=datetime.now)
    updatedAt = DateTimeField(default=datetime.now)

    meta = {
        "collection": "transactions",
        "indexes": ["user"]
    }