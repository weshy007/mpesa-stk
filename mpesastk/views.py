from django.shortcuts import render
from rest_framework import views, response, status


from .serializers import *
from .models import *


# Create your views here.
class SendSTKPushView(views.APIView):
    def post(self, request, format=None):
        serializer = SendSTKPushSerializer(data=request.data)
        if serializer.is_valid():
            res = serializer.save()
            return response.Response(res, status=status.HTTP_200_OK)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class MpesaCallbackView(views.APIView):
    def post(self, request, format=None):
        body = request.data

        if body:
            mpesa = ResponseBody.objects.create(body=body)

            mpesa_body = mpesa.body

            if mpesa_body['stkCallback']['resultCode'] == 0:
                transaction = Transacton.objects.create(
                    amount = mpesa_body['Body']['stkCallback']['CallbackMetadata']['Item'][0]["Value"],
                    receipt_no=mpesa_body['Body']['stkCallback']['CallbackMetadata']['Item'][1]["Value"],
                    phonenumber=mpesa_body['Body']['stkCallback']['CallbackMetadata']['Item'][-1]["Value"],
                )

            return response.Response({"message": 'Callback received and processed successfully.'})
        return response.Response({"failed": "No Callback Received"}, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, format=None):
        response_bodies = ResponseBody.objects.all()
        serializer = MpesaResponseBodySerializer(response_bodies, many=True)

        return response.Response({'responses': serializer.data})
    

class TransactionView(views.APIView):
    def get(self, request, format=None):
        transactions = Transacton.objects.all()
        serializer = TransactionSerializer(transactions, many=True)

        return response.Response({'transactions': serializer.data})