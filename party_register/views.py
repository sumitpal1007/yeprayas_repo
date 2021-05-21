from rest_framework.views import APIView
from rest_framework import viewsets, status, parsers
from rest_framework.response import Response
from .models import Party
from .models import PartyRegister
from .serializers import PartySerializer
from .models import File
from .serializers import FileSerializer
# from .serializers import PartyRegisterSerializer
from django.db import transaction
from rest_framework.exceptions import ParseError

class PartyAPIView(APIView):

    def get(self, request):
        parties = Party.objects.all()
        serializer = PartySerializer(parties, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        }, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            if request.data.get('name') is not None and request.data.get('username') is not None and request.data.get('password') is not None and request.data.get('contact_number') is not None:
                party = Party(name=request.data.get('name'), contact_number=request.data.get('contact_number'), description=request.data.get('description'))
                party.save()

                partyRegister = PartyRegister(username=request.data.get('username'), password=request.data.get('password'), party=party)
                partyRegister.save()

                serializer = PartySerializer(party)

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
            party_id = request.query_params["party_id"]
            if party_id is not None and party_id != "":
                party = Party.objects.get(party_id=party_id)

                data = request.data

                party.name = data.get("name", party.name)
                party.contact_number = data.get("contact_number", party.contact_number)
                party.description = data.get("description", party.description)
                party.status = data.get("status", party.status)

                party.save()

                serializer = PartySerializer(party)

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
            party_id = request.query_params["party_id"]
            if party_id is not None and party_id != "":
                party = Party.objects.get(party_id=party_id)

                party.delete()

                return Response({
                    'success': True,
                    'message': ""+party_id+" deleted successfully !!"
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


# class PartyRegisterViewSets(viewsets.ModelViewSet):
#     queryset = PartyRegister.objects.all()
#     serializer_class = PartyRegisterSerializer




########################################################################
########################################################################

class FileAPIView(APIView):
    parser_class = (parsers.FileUploadParser,)

    def get(self, request):
        try:
            if request.query_params["party_id"] != "":
                party_id = request.query_params["party_id"]
                party = Party.objects.get(party_id=party_id)
                files = File.objects.all().filter(party=party)
                serializer = FileSerializer(files, many=True)

                return Response({
                    'success': True,
                    'data': serializer.data
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

                

    @transaction.atomic
    def post(self, request, format=None):
        try:
            party_id = request.query_params["party_id"]
            if party_id is not None and party_id != "" and request.data['file'] is not None :
                party = Party.objects.get(party_id=party_id)

                fileData = request.data['file']

                uploadedFile = File(title=fileData.name, document=fileData, party=party)
                
                uploadedFile.save()

                return Response({
                    'success': True,
                    'message': "File uploaded successfully !!"
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
            party_id = request.query_params["party_id"]
            if party_id is not None and party_id != "":
                party = Party.objects.get(party_id=party_id)

                files = File.objects.all().filter(party=party)

                files.delete()

                return Response({
                    'success': True,
                    'message': "Files deleted successfully !!"
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
