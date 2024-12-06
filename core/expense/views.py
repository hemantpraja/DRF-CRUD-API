from django.shortcuts import render
from .models import Transactions
from rest_framework.response import Response
from .serializers import TransactionSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.db.models import Sum

@api_view("GET")
def get_transactions(request):
    queryset = Transactions.objects.all()
    serializer = TransactionSerializer(queryset, many=True)
    
    return Response({
        "data":serializer.data,
        "total": queryset.aggregate(total=Sum('amount'))['total'] or 0
    })
    
class TransactionAPI(APIView):
    def get(self, request):
        queryset = Transactions.objects.all()
        serializer = TransactionSerializer(queryset, many=True)
        
        return Response({
            "data":serializer.data,
            "total": queryset.aggregate(total=Sum('amount'))['total'] or 0
        })
        
    def post(self, request):
        data = request.data
        print(data)
        serializer = TransactionSerializer(data=data)
        if not serializer.is_valid():
            return Response({
                "message" : "data not saved",
                "errors":serializer.errors,
            })
        
        serializer.save()
        return Response({
            "message" : "data saved",
            "data":serializer.data
        })
        
    def put(self, request):
        return Response({
            "message" : "this is a put method"
        })
        
    def patch(self, request):
        data = request.data
        
        if not data.get('id'):
            return Response({
                "message" : "data not updated",
                "errors":"id is required"
            })
        transactions = Transactions.objects.get(id=id)
        serializer = TransactionSerializer(instance=transactions, data=data, partial=True)
        if not serializer.is_valid():
            return Response({
                "message" : "data not saved",
                "errors":serializer.errors,
            })
        
        serializer.save()
        return Response({
            "message" : "data saved",
            "data":serializer.data
        })
       
    def delete(self, request):
        data = request.data
        if not data.get('id'):
            return Response({
                "message" : "data not deleted",
                "errors":"id is required"
            })
        
        transaction = Transactions.objects.get(id=data.get('id')).delete()
        
        return  Response({
            "message" : "data deleted",
            "data":{}
        })