from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import GlucoseSample, InsulinSample, Sample
from .serializers import SampleGeneralSerializer, SampleSerializer, InsulinSampleSerializer, GlucoseSampleSerializer

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
