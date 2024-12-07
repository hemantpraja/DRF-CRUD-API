from django.shortcuts import render
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .models import Transactions
from .serializers import TransactionSerializer


# Function-Based View
@api_view(["GET"])
def get_transactions(request):
    queryset = Transactions.objects.all()
    serializer = TransactionSerializer(queryset, many=True)
    
    return Response({
        "data": serializer.data,
        "total": queryset.aggregate(total=Sum('amount'))['total'] or 0
    })


# Class-Based View
class TransactionAPI(APIView):
    def get(self, request):
        print("Hiii")
        queryset = Transactions.objects.all()
        serializer = TransactionSerializer(queryset, many=True)
        
        return Response({
            "data": serializer.data,
            "total": queryset.aggregate(total=Sum('amount'))['total'] or 0
        })

    def post(self, request):
        data = request.data
        serializer = TransactionSerializer(data=data)
        
        if not serializer.is_valid():
            return Response({
                "message": "Data not saved",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
            "message": "Data saved",
            "data": serializer.data,
        }, status=status.HTTP_201_CREATED)

    def put(self, request):
        return Response({
            "message": "This is a PUT method",
        })

    def patch(self, request):
        data = request.data
        transaction_id = data.get('id')
        
        if not transaction_id:
            return Response({
                "message": "Data not updated",
                "errors": "ID is required",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            transaction = Transactions.objects.get(id=transaction_id)
        except Transactions.DoesNotExist:
            return Response({
                "message": "Transaction not found",
            }, status=status.HTTP_404_NOT_FOUND)
        
        serializer = TransactionSerializer(instance=transaction, data=data, partial=True)
        
        if not serializer.is_valid():
            return Response({
                "message": "Data not saved",
                "errors": serializer.errors,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()
        return Response({
            "message": "Data updated",
            "data": serializer.data,
        })

    def delete(self, request):
        data = request.data
        transaction_id = data.get('id')
        
        if not transaction_id:
            return Response({
                "message": "Data not deleted",
                "errors": "ID is required",
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            transaction = Transactions.objects.get(id=transaction_id)
        except Transactions.DoesNotExist:
            return Response({
                "message": "Transaction not found",
            }, status=status.HTTP_404_NOT_FOUND)
        
        transaction.delete()
        return Response({
            "message": "Data deleted",
        }, status=status.HTTP_204_NO_CONTENT)
