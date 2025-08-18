from django.db import models


class Sample(models.Model):
    version = models.CharField(max_length=5)
    id_device = models.ForeignKey('Device', on_delete=models.CASCADE, related_name='samples')
    geolocation = models.CharField(max_length=100)
    send_data = models.DateTimeField()

class InsulinSample(models.Model):
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE)
    stop_buzzer = models.DateTimeField()
    confirm_type = models.DateTimeField()
    mount_syringe = models.DateTimeField()
    start_dose = models.DateTimeField()
    confirm_dose = models.DateTimeField()
    confirm_insulin_admin = models.DateTimeField()
    insulin_dose = models.IntegerField()
    insulin_type = models.CharField(max_length=50)

class Device(models.Model):
    id_device = models.CharField(max_length=100, primary_key=True)
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='devices', null=True)

class GlucoseSample(models.Model):
    sample = models.OneToOneField(Sample, on_delete=models.CASCADE)
    confirm_glucose_test = models.DateTimeField()
    index = models.DecimalField(max_digits=4, decimal_places=2)

class Center(models.Model):
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    mobile = models.BigIntegerField()
    opening_hours = models.TimeField()
    closing_hours = models.TimeField()
    open_24hrs = models.BooleanField(default=False)

class Treatment(models.Model):
    beginning_date = models.DateTimeField()
    type = models.CharField(max_length=50, default='NPH')
    quantity = models.IntegerField()
    first_administration = models.TimeField()
    second_administration = models.TimeField()
    patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='treatments')

class Person(models.Model):
    rut = models.CharField(max_length=9)
    dv = models.CharField(max_length=1)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    first_surname = models.CharField(max_length=100)
    second_surname = models.CharField(max_length=100)
    birthdate = models.DateField(auto_now=False, auto_now_add=False)
    gender = models.CharField(max_length=1)
    address = models.CharField(max_length=200)
    mobile = models.PositiveIntegerField()
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name

class Personnel(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    centers = models.ManyToManyField('Center', related_name='centers')

    def __str__(self):
        return self.person.first_name

class Patient(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    emergency_contact = models.CharField(max_length=200)
    emergency_email = models.CharField(max_length=200)
    emergency_mobile = models.PositiveIntegerField()
    medical_care = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=4, decimal_places=2)
    last_hba1c = models.PositiveIntegerField()
    stroke_suffered = models.BooleanField(default=False)
    blood_preassure = models.PositiveIntegerField()
    adherence = models.CharField(max_length=5)
    nph = models.CharField(max_length=5)
    insulin_type = models.CharField(max_length=5)
    glucose = models.CharField(max_length=5)
    personnels = models.ManyToManyField('Personnel', related_name='patients')

    def __str__(self):
        return self.person.first_name
