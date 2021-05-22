from rest_framework.views import APIView
from rest_framework import viewsets, status, parsers
from rest_framework.response import Response
from .models import Admin
from .models import AdminRegister
from .models import Document
from party_register.models import Party
from .serializers import AdminSerializer
from .serializers import DocumentSerializer
from pyexcel_xlsx import get_data
import datetime
import json

# from .serializers import PartyRegisterSerializer
from django.db import transaction
from rest_framework.exceptions import ParseError

class AdminAPIView(APIView):

    def get(self, request):
        try:
            if 'admin_id' in request.query_params and request.query_params["admin_id"] != "":
                admin_id = request.query_params["admin_id"]
                admin = Admin.objects.get(admin_id=admin_id)
                serializer = AdminSerializer(admin)

                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                admins = Admin.objects.all()
                serializer = AdminSerializer(admins, many=True)
                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
                
        except:
            return Response({
                    'success': False,
                    'message': 'INTERNAL_SERVER_ERROR'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            if request.data.get('name') is not None and request.data.get('username') is not None and request.data.get('password') is not None and request.data.get('contact_number') is not None:
                admin = Admin(name=request.data.get('name'), contact_number=request.data.get('contact_number'), description=request.data.get('description'))
                admin.save()

                adminRegister = AdminRegister(username=request.data.get('username'), password=request.data.get('password'), admin=admin)
                adminRegister.save()

                serializer = AdminSerializer(admin)

                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'success': False,
                    'message': 'Invalid Request'
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                    'success': False,
                    'message': 'INTERNAL_SERVER_ERROR'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
              
    @transaction.atomic
    def patch(self, request, *args, **kwargs):
        try:
            admin_id = request.query_params["admin_id"]
            if admin_id is not None and admin_id != "":
                admin = Admin.objects.get(admin_id=admin_id)

                data = request.data

                admin.name = data.get("name", admin.name)
                admin.contact_number = data.get("contact_number", admin.contact_number)
                admin.description = data.get("description", admin.description)
                admin.status = data.get("status", admin.status)

                admin.save()

                serializer = AdminSerializer(admin)

                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_202_ACCEPTED)

            else:
                return Response({
                    'success': False,
                    'message': 'Invalid Request'
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                    'success': False,
                    'message': 'INTERNAL_SERVER_ERROR'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        try:
            admin_id = request.query_params["admin_id"]
            if admin_id is not None and admin_id != "":
                admin = Admin.objects.get(admin_id=admin_id)

                admin.delete()

                return Response({
                    'success': True,
                    'message': ""+admin_id+" deleted successfully !!"
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'success': False,
                    'message': 'Invalid Request'
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                    'success': False,
                    'message': 'INTERNAL_SERVER_ERROR'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.
##############################################################################

class DocumentAPIView(APIView):

    def get(self, request):  
        try:
            if 'admin_id' in request.query_params and request.query_params["admin_id"] != "" and 'party_id' in request.query_params and request.query_params["party_id"] != "":
                admin_id = request.query_params["admin_id"]
                party_id = request.query_params["party_id"]
                admin = Admin.objects.get(admin_id=admin_id)
                party = Party.objects.get(party_id=party_id)
                documents = Document.objects.all().filter(valid_to_date__isnull=True).filter(party=party).filter(admin=admin)
                serializer = DocumentSerializer(documents, many=True)

                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            elif 'admin_id' in request.query_params and request.query_params["admin_id"] != "":
                admin_id = request.query_params["admin_id"]
                admin = Admin.objects.get(admin_id=admin_id)
                documents = Document.objects.all().filter(valid_to_date__isnull=True).filter(admin=admin)
                serializer = DocumentSerializer(documents, many=True)

                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            elif 'party_id' in request.query_params and request.query_params["party_id"] != "":
                party_id = request.query_params["party_id"]
                party = Party.objects.get(party_id=party_id)
                documents = Document.objects.all().filter(valid_to_date__isnull=True).filter(party=party)
                serializer = DocumentSerializer(documents, many=True)

                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                documents = Document.objects.all().filter(valid_to_date__isnull=True)
                serializer = DocumentSerializer(documents, many=True)
                return Response({
                    'success': True,
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
                
        except:
            return Response({
                    'success': False,
                    'message': 'INTERNAL_SERVER_ERROR'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            if 'admin_id' in request.query_params and request.query_params["admin_id"] != "" and 'party_id' in request.query_params and request.query_params["party_id"] != "":
                admin_id = request.query_params["admin_id"]
                party_id = request.query_params["party_id"]

                admin = Admin.objects.get(admin_id=admin_id)
                party = Party.objects.get(party_id=party_id)

                file_obj = request.data["document"]
                data = get_data(file_obj)
                
                json_object = json.loads(json.dumps(data))

                index = -1
                for row in json_object['final']:
                    if index == -1:
                        for colum in row:
                            index = index + 1
                            if colum.lower() == 'item':
                                item_index = index
                            elif colum.lower() == 'counts':
                                counts_index = index
                            elif colum.lower() == 'category':
                                category_index = index
                            elif colum.lower() == 'description':
                                description_index = index

                    else:
                        size = len(row)
                        if size > item_index:
                            item = row[item_index]
                        if size > counts_index:
                            counts = row[counts_index]
                        if size > category_index:
                            category = row[category_index]
                        if size > description_index:
                            description = row[description_index]

                        countStr = str(counts)
                        document = Document(item=item, counts=countStr, category=category, description=description, party=party, admin=admin)
                        document.save()
                        
                return Response({
                    'success': True,
                    'data': "Document uploaded successfully !!"
                }, status=status.HTTP_201_CREATED)

            else:
                return Response({
                    'success': False,
                    'message': 'Invalid Request'
                }, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({
                    'success': False,
                    'message': 'INTERNAL_SERVER_ERROR'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @transaction.atomic
    def delete(self, request, format=None):
        try:
            if 'admin_id' in request.query_params and request.query_params["admin_id"] != "" and 'party_id' in request.query_params and request.query_params["party_id"] != "":
                admin_id = request.query_params["admin_id"]
                party_id = request.query_params["party_id"]
                
                admin = Admin.objects.get(admin_id=admin_id)
                party = Party.objects.get(party_id=party_id)
                documents = Document.objects.all().filter(valid_to_date__isnull=True).filter(party=party).filter(admin=admin)

                documents.update(valid_to_date=datetime.datetime.now())

                return Response({
                    'success': True,
                    'message': "Documents deleted successfully !!"
                }, status=status.HTTP_200_OK)

            else:
                return Response({
                    'success': False,
                    'message': 'Invalid Request'
                }, status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response({
                    'success': False,
                    'message': 'INTERNAL_SERVER_ERROR'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
