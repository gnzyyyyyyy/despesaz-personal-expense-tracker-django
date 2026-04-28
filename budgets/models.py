from django.db import models

# Create your models here.
from mongoengine import (
    Document, StringField, FloatField,
    DateTimeField, ReferenceField
)
from datetime import datetime
from users.models import User

CATEGORY_CHOICES = [
    'housing', 'food', 'utilities', 'transportation',
    'entertainment', 'health_care', 'miscellaneous',
    'salary', 'investments', 'gifts', 'refunds', 'other'
]

class Budget(Document):
    userId = ReferenceField(User, required=True)
    category = StringField(required=True, choices=CATEGORY_CHOICES, default='other')
    limitAmount = FloatField(required=True, min_value=0)
    month = DateTimeField(required=True)
    notes = StringField()
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)

    meta = {
        "collection": "budgets",
        "indexes": [
            {
                "fields": ["userId", "category", "month"],
                "unique": True
            }
        ]
    }