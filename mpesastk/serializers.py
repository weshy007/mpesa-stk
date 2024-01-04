from rest_framework import serializers

from .validators import validate_possible_number
from .utils import MpesaGateWay
from .models import ResponseBody, Transacton

pay = MpesaGateWay()


class SendSTKPushSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    amount = serializers.CharField()


    def validate_amount(self, attrs):
        amount = int(attrs)

        if amount <= 0:
            raise serializers.ValidationError(detail="Amount must be greater than 0")
        return amount
    

    def validate_phone_number(self, attrs):
        phone_number = attrs

        try:
            validate_possible_number(phone_number, 'KE')
            return phone_number
        except:
            raise serializers.ValidationError(detail="Invalid Phone Number")
        
    
    def create(self, validate_data):
        phone_number = validate_data['phone_number']
        amount = validate_data['amount']

        if str(phone_number)[0] == '+':
            phone_number = phone_number[1:]
        elif str(phone_number)[0] == '0':
            phone_number = '254' + phone_number[1:]

        callback_url = ''
        payment = pay.stk_push(phone_number=phone_number, amount=amount, callback_url=callback_url)

        res = payment.json()

        return res
    
class MpesaResponseBodySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseBody
        fields = '__all__'

    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transacton
        fields = '__all__'