from rest_framework import serializers
from .models import Sample, InsulinSample, GlucoseSample

class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = "__all__"

class InsulinSampleSerializer(serializers.ModelSerializer):
    sample = SampleSerializer(required=False)

    class Meta:
        model = InsulinSample
        fields = "__all__"

class GlucoseSampleSerializer(serializers.ModelSerializer):
    sample = SampleSerializer(required=False)

    class Meta:
        model = GlucoseSample
        fields = "__all__"

class SampleGeneralSerializer(serializers.Serializer):
    sample = SampleSerializer()
    insulin = InsulinSampleSerializer(required=False)
    glucose = GlucoseSampleSerializer(required=False)

    def create(self, validated_data):

        response = {}

        try:
            sample = Sample.objects.create(**validated_data['sample'])
            response['sample'] = sample
        except KeyError:
            print('Missing sample data')

        if 'insulin' in validated_data:
            try:
                insulin = InsulinSample.objects.create(sample=sample, **validated_data['insulin'])
                response['insulin'] = insulin
            except KeyError:
                print('Incomplete insulin data')

        if 'glucose' in validated_data:
            try:
                glucose = GlucoseSample.objects.create(sample=sample, **validated_data['glucose'])
                response['glucose'] = glucose
            except KeyError:
                print('Incomplete glucose data')


        return response
