from rest_framework import serializers
from .models import Party
from .models import File
# from .models import PartyRegister

class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = ["party_id","name","contact_number","status","description"]

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'

# class PartyRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = PartyRegister
#         fields = '__all__'