from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Center, Personnel, Patient
from .serializers import (
    SampleGeneralSerializer, CenterSerializer, PersonnelSerializer, PatientSerializer, DeviceSerializer, PersonnelLoginSerializer
)

class PersonnelLoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = PersonnelLoginSerializer(data=request.data)
        if serializer.is_valid():
            personnel = serializer.validated_data['personnel']
            person = serializer.validated_data['person']
            
            # Generate JWT tokens
            refresh = RefreshToken.for_user(personnel)
            refresh['email'] = person.email
            refresh['name'] = f"{person.first_name} {person.first_surname}"
            refresh['specialty'] = personnel.specialty
            refresh['personnel_id'] = personnel.id
            
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': {
                    'id': personnel.id,
                    'email': person.email,
                    'name': f"{person.first_name} {person.first_surname}",
                    'specialty': personnel.specialty
                }
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SampleCreate(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):

        data = {}
        sample_data = {}

        try:
            sample_data['version'] = request.data['version']
            sample_data['id_device'] = request.data['id_device']
            sample_data['geolocation'] = request.data['geolocation']
            sample_data['send_data'] = request.data['send_data']

            data['sample'] = sample_data

            data['insulin'] = request.data['data-insulin']
            data['glucose'] = request.data['data-glucose']
        except KeyError:
            print('Missing Data on the request')

        serializer = SampleGeneralSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CenterCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CenterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CenterList(APIView):
    def get(self, request, *args, **kwargs):
        centers = Center.objects.all()
        serializer = CenterSerializer(centers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PersonnelCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PersonnelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonnelList(APIView):
    def get(self, request, *args, **kwargs):
        personnels = Personnel.objects.all()
        serializer = PersonnelSerializer(personnels, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PatientList(APIView):
    def get(self, request, *args, **kwargs):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class PatientsByPersonnel(APIView):
    def get(self, request, personnel_id, *args, **kwargs):
        try:
            # Verify if the personnel exists
            personnel = Personnel.objects.get(id=personnel_id)
            
            # Get all patients assigned to this personnel
            patients = Patient.objects.filter(personnels=personnel)
            
            # Serialize the patients
            serializer = PatientSerializer(patients, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Personnel.DoesNotExist:
            return Response(
                {"error": f"Personnel with id {personnel_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PersonnelByCenter(APIView):
    def get(self, request, center_id, *args, **kwargs):
        try:
            # Verify if the center exists
            center = Center.objects.get(id=center_id)
            
            # Get all personnel from this center
            personnel = Personnel.objects.filter(centers=center)
            
            # Serialize the personnel
            serializer = PersonnelSerializer(personnel, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Center.DoesNotExist:
            return Response(
                {"error": f"Center with id {center_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DeviceCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)