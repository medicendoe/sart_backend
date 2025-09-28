from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import GlucoseSample, InsulinSample, Sample, Center, Personnel, Patient, Person
from .serializers import (
    SampleGeneralSerializer, SampleSerializer, InsulinSampleSerializer,
    GlucoseSampleSerializer, CenterSerializer, PersonnelSerializer, PatientSerializer, DeviceSerializer,
    AllSamplesSerializer
)

class SampleCreate(APIView):
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

class SamplesByPatient(APIView):
    def get(self, request, patient_id, *args, **kwargs):
        try:
            patient = Patient.objects.get(id=patient_id)
            samples = Sample.objects.filter(id_device__patient=patient)

            result = []
            for sample in samples:
                sample_data = SampleSerializer(sample).data
                
                # Check if insulin or glucose sample exists for this Sample
                insulin_exists = InsulinSample.objects.filter(sample=sample).exists()
                glucose_exists = GlucoseSample.objects.filter(sample=sample).exists()

                sample_type = "Unknown"
                extra_data = {}

                if insulin_exists:
                    sample_type = "Insulin"
                    insulin = InsulinSample.objects.get(sample=sample)
                    extra_data = InsulinSampleSerializer(insulin).data
                elif glucose_exists:
                    sample_type = "Glucose"
                    glucose = GlucoseSample.objects.get(sample=sample)
                    extra_data = GlucoseSampleSerializer(glucose).data
                
                # Compose combined dict with type and details
                sample_data['type'] = sample_type
                sample_data['details'] = extra_data
                
                result.append(sample_data)

            return Response(result, status=status.HTTP_200_OK)

        except Patient.DoesNotExist:
            return Response(
                {"error": f"Patient with id {patient_id} does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DummyGetLast(APIView):
    def get(self, request, *args, **kwargs):
        try:

            sample = Sample.objects.all().latest("id")
            sampleSerializer = SampleSerializer(sample)

            try:
                insulinSample = InsulinSample.objects.get(sample=sample)
                insulinSerializer = InsulinSampleSerializer(insulinSample)
            except InsulinSample.DoesNotExist:
                insulinSample = None
                print("No insulin data.")

            try:
                glucoseSample = GlucoseSample.objects.get(sample=sample)
                glucoseSerializer = GlucoseSampleSerializer(glucoseSample)
            except GlucoseSample.DoesNotExist:
                glucoseSample = None
                print("No glucose data.")

            return Response({
                "sample": sampleSerializer.data, 
                "insulin": insulinSerializer.data if insulinSample != None else {}, 
                "glucose": glucoseSerializer.data if glucoseSample != None else {}
            }, status.HTTP_200_OK)

        except Sample.DoesNotExist:

            return Response({"detail": "No sample found."}, status=status.HTTP_404_NOT_FOUND)

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

class PersonnelLogin(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            
            # Validación básica
            if not email or not password:
                return Response({'error': 'Email y contraseña son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Buscar persona por email
            try:
                person = Person.objects.get(email=email)
            except Person.DoesNotExist:
                return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Verificar si tiene un perfil de personal asociado
            try:
                personnel = Personnel.objects.get(person=person)
            except Personnel.DoesNotExist:
                return Response({'error': 'Este usuario no es personal médico'}, status=status.HTTP_403_FORBIDDEN)
            
            # Verificar contraseña - autenticación simple
            if personnel.password != password:
                return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
            
            # Retornar éxito y datos básicos (sin token)
            return Response({
                'success': True,
                'user': {
                    'id': personnel.id,
                    'name': f"{person.first_name} {person.first_surname}",
                    'email': person.email,
                    'specialty': personnel.specialty
                }
            })
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class DeviceCreate(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)