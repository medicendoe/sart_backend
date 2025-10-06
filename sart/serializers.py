from rest_framework import serializers

from django.contrib.auth import authenticate
from .models import Sample, InsulinSample, Treatment, GlucoseSample, Center, Personnel, Patient, Person, Device

class PersonnelLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            person = Person.objects.get(email=email)
            personnel = Personnel.objects.get(person=person)
            
            if personnel.check_password(password):
                return {
                    'personnel': personnel,
                    'person': person
                }
            else:
                raise serializers.ValidationError('Credenciales inválidas')
                
        except (Person.DoesNotExist, Personnel.DoesNotExist):
            raise serializers.ValidationError('Credenciales inválidas')

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

class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = "__all__"

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'

class PersonnelSerializer(serializers.ModelSerializer):
    person = PersonSerializer(required=False)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = Personnel
        fields = '__all__'
    
    def create(self, validated_data):
        person_data = validated_data.pop('person', None)
        center_data = validated_data.pop('centers', None)
        password = validated_data.pop('password', None)
        
        # Create the Person instance if person data is provided
        if person_data:
            person = Person.objects.create(**person_data)
            validated_data['person'] = person
        
        # Create the Personnel instance
        personnel = Personnel.objects.create(**validated_data)
        
        # Set password if provided
        if password:
            personnel.set_password(password)
            personnel.save()
        
        if center_data:
            personnel.centers.set(center_data)
                
        return personnel

class PatientSerializer(serializers.ModelSerializer):
    person = PersonSerializer(required=False)
    treatments = TreatmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'
    
    def create(self, validated_data):
        person_data = validated_data.pop('person', None)
        personels_data = validated_data.pop('personnels', None)
        
        # Create the Person instance if person data is provided
        if person_data:
            person = Person.objects.create(**person_data)
            validated_data['person'] = person
        
        # Create the Patient instance
        patient = Patient.objects.create(**validated_data)

        # Create the Personnel instances if provided
        if personels_data:
            patient.personnels.set(personels_data)
        return patient

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

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'
