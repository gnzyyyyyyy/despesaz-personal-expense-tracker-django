from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from.models import Transaction
from datetime import datetime

class TransactionView(APIView):
    def post(self, request):
        try:
            user = request.user
            data = request.data

            transaction = Transaction(
                user=user,
                title=data.get("title"),
                amount=float(data.get("amount")),
                type=data.get("type"),
                category=data.get("category", "other"),
                date=datetime.fromisoformat(data.get("date")) if data.get("date") else datetime.now()
            )

            transaction.save()

            return Response({
                "message": "Transaction created",
                "transaction": {
                    "id": str(transaction.id),
                    "title": transaction.title,
                    "amount": transaction.amount,
                    "type": transaction.type,
                    "category": transaction.category,
                    "date": transaction.date
                }
            }, status=201)

        except Exception as e:
            return Response({
                "message": "Error creating transaction",
                "error": str(e)
            }, status=500)

    def get(self, request):
        try:
            user = request.user

            transactions = Transaction.objects(user=user).order_by("-createdAt")

            data = []
            for t in transactions:
                data.append({
                    "id": str(t.id),
                    "title": t.title,
                    "amount": t.amount,
                    "type": t.type,
                    "category": t.category,
                    "date": t.date,
                })

            return Response({
                "transactions": data
            }, status=200)

        except Exception as e:
            return Response({
                "message": "Error fetching transactions",
                "error": str(e)
            }, status=500)

class TransactionDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            user = request.user
            data = request.data

            transaction = Transaction.objects(id=id, user=user.id).first()

            if not transaction:
                return Response({
                    "message": "Transaction not found"
                }, status=404)

            transaction.title = data.get("title", transaction.title)
            transaction.amount = float(data.get("amount", transaction.amount))
            transaction.type = data.get("type", transaction.type)
            transaction.category = data.get("category", transaction.category)

            transaction.updatedAt = datetime.now()

            transaction.save()

            transaction.reload()

            return Response({
                "message": "Updated",
                "transaction": {
                    "id": str(transaction.id),
                    "title": transaction.title,
                    "amount": transaction.amount,
                    "type": transaction.type,
                    "category": transaction.category,
                    "date": transaction.date
                }
            })
        
        except Exception as e:
            return Response({
                "message": "Error updating transaction",
                "error": str(e)
            }, status=500)
        

    def delete(self, request, id):
        try:
            user = request.user

            transaction = Transaction.objects(id=id, user=user.id).first()

            if not transaction:
                return Response({
                    "message": "Transaction not found"
                }, status=404)

            transaction.delete()

            return Response({
                "message": "Transaction deleted"
            }, status=200)

        except Exception as e:
            return Response({
                "message": "Error deleting transaction",
                "error": str(e)
            }, status=500)