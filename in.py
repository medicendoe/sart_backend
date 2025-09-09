from sart.models import Patient, Person, Personnel

superuser = Personnel.objects.create_superuser(
    email='admin@example.com',
    password='admin_password',
    specialty='Administración',
    person_data={
        'rut': '87654321',
        'dv': '0',
        'first_name': 'Admin',
        'middle_name': '',
        'first_surname': 'Sistema',
        'second_surname': '',
        'birthdate': '1975-01-01',
        'gender': 'M',
        'address': 'Oficina Central',
        'mobile': 123456789,
    }
)

# Paciente 1
patient1 = Patient.objects.create(
    person=Person.objects.create(
        rut='12345678',
        dv='9',
        first_name='María',
        middle_name='Carmen',
        first_surname='González',
        second_surname='Rodríguez',
        birthdate='1985-03-15',
        gender='F',
        address='Av. Libertador 1234',
        mobile=987654321,
        email='maria.gonzalez@email.com'
    ),
    emergency_contact='Carlos González',
    emergency_email='carlos.gonzalez@email.com',
    emergency_mobile=956789123,
    medical_care='Fonasa',
    weight=65.50,
    last_hba1c=6,
    stroke_suffered=False,
    blood_preassure=120
)

# Paciente 2
patient2 = Patient.objects.create(
    person=Person.objects.create(
        rut='23456789',
        dv='1',
        first_name='José',
        middle_name='Luis',
        first_surname='Martínez',
        second_surname='Silva',
        birthdate='1978-11-22',
        gender='M',
        address='Calle Principal 567',
        mobile=912345678,
        email='jose.martinez@email.com'
    ),
    emergency_contact='Ana Martínez',
    emergency_email='ana.martinez@email.com',
    emergency_mobile=945678912,
    medical_care='Isapre',
    weight=78.20,
    last_hba1c=7,
    stroke_suffered=True,
    blood_preassure=140
)

# Paciente 3
patient3 = Patient.objects.create(
    person=Person.objects.create(
        rut='34567890',
        dv='2',
        first_name='Patricia',
        middle_name='Elena',
        first_surname='Sánchez',
        second_surname='Morales',
        birthdate='1992-07-08',
        gender='F',
        address='Pasaje Los Robles 890',
        mobile=923456789,
        email='patricia.sanchez@email.com'
    ),
    emergency_contact='Roberto Sánchez',
    emergency_email='roberto.sanchez@email.com',
    emergency_mobile=934567891,
    medical_care='Fonasa',
    weight=59.80,
    last_hba1c=5,
    stroke_suffered=False,
    blood_preassure=110
)

# Paciente 4
patient4 = Patient.objects.create(
    person=Person.objects.create(
        rut='45678901',
        dv='3',
        first_name='Roberto',
        middle_name='Antonio',
        first_surname='Herrera',
        second_surname='Castro',
        birthdate='1970-12-03',
        gender='M',
        address='Boulevard Central 456',
        mobile=934567890,
        email='roberto.herrera@email.com'
    ),
    emergency_contact='Carmen Herrera',
    emergency_email='carmen.herrera@email.com',
    emergency_mobile=923456780,
    medical_care='Particular',
    weight=82.10,
    last_hba1c=8,
    stroke_suffered=False,
    blood_preassure=135
)

# Paciente 5
patient5 = Patient.objects.create(
    person=Person.objects.create(
        rut='56789012',
        dv='4',
        first_name='Claudia',
        middle_name='Beatriz',
        first_surname='López',
        second_surname='Fernández',
        birthdate='1988-09-17',
        gender='F',
        address='Villa Las Flores 123',
        mobile=945678901,
        email='claudia.lopez@email.com'
    ),
    emergency_contact='Pedro López',
    emergency_email='pedro.lopez@email.com',
    emergency_mobile=912345679,
    medical_care='Isapre',
    weight=72.30,
    last_hba1c=6,
    stroke_suffered=False,
    blood_preassure=125
)

print("5 pacientes creados exitosamente:")
print(f"1. {patient1.person.first_name} {patient1.person.first_surname}")
print(f"2. {patient2.person.first_name} {patient2.person.first_surname}")
print(f"3. {patient3.person.first_name} {patient3.person.first_surname}")
print(f"4. {patient4.person.first_name} {patient4.person.first_surname}")
print(f"5. {patient5.person.first_name} {patient5.person.first_surname}")

device_codes = [
    'u9ao3eeA2xczFDTk',  # Dispositivo 1
    'npZAF7UYom8waWR8',  # Dispositivo 2
    'c4XCyLVx8Vkfnjwf',  # Dispositivo 3
    'gqPENhHp4SJrd7Zq',  # Dispositivo 4
    'UeugrALEq3YNLyRA'   # Dispositivo 5
]

patients = [patient1, patient2, patient3, patient4, patient5]

devices = []
for i, (patient, device_code) in enumerate(zip(patients, device_codes), 1):
    device = Device.objects.create(
        id_device=device_code,
        patient=patient
    )
    devices.append(device)
    print(f"Dispositivo {i} creado: {device_code} -> {patient.person.first_name} {patient.person.first_surname}")