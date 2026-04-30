from django.urls import path
from .views import TransactionView, TransactionDetailView

urlpatterns = [
    path('', TransactionView.as_view()),
    path('<str:id>/', TransactionDetailView.as_view()),
]