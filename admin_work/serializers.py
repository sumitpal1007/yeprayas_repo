from rest_framework import serializers
from .models import Admin
from .models import Document

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ["admin_id","name","contact_number","status","description"]


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["item","counts","category","description","created_at","updated_at"]
