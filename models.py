import enum
import uuid
from datetime import datetime
from sqlalchemy import Boolean, Column, Date, Float, ForeignKey, Integer, String , DateTime, Table, Enum
from sqlalchemy.orm import relationship
from database import Base


chat_participants = Table(
    'chat_participant', Base.metadata,
    Column('chat_id', String, ForeignKey('chat.chat_id', ondelete="CASCADE"), primary_key=True),
    Column('user_id', String, ForeignKey('medplus_user.user_id', ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = 'medplus_user'

    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    settings_id = Column(String, ForeignKey('settings.settings_id'), nullable=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone_no = Column(String, nullable=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)

    logs = relationship("Log", back_populates="user", cascade="all, delete-orphan")
    
    settings = relationship("Settings", back_populates="user", uselist=False)

    chats = relationship("Chat", secondary=chat_participants, back_populates="participants")

    gender_id = Column(String, ForeignKey('gender.id'), nullable=False)
    gender = relationship("Gender", back_populates="users")

    messages = relationship("Message", back_populates="sender", cascade="all, delete-orphan")
    
    user_type = Column(String, nullable=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',  
        'polymorphic_on': user_type      
    }


class Gender(Base):
    __tablename__ = 'gender'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    gender = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="gender")

class AuthType(enum.Enum):
    email = "email"
    sms = "sms"
    none = "none"

class Settings(Base):
    __tablename__ = 'settings'

    settings_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    font_size = Column(Integer, nullable=True)
    screen_reader = Column(Boolean, default=False)
    on_screen_keyboard = Column(Boolean, default=False)
    email_notifications = Column(Boolean, default=True)
    sms_notifications = Column(Boolean, default=False)
    email_reminders = Column(Boolean, default=False)
    sms_reminders = Column(Boolean, default=False)

    auth_type = Column(Enum(AuthType), nullable=False)


    user_id = Column(String, ForeignKey('medplus_user.user_id', ondelete="CASCADE"), unique=True, nullable=False)
    user = relationship("User", back_populates="settings")


class Log(Base):
    __tablename__ = 'log'

    log_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    action_id = Column(String, ForeignKey('action.action_id', ondelete="CASCADE"), nullable=False)

    user_id = Column(String, ForeignKey('medplus_user.user_id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="logs")

class Action(Base):
    __tablename__ = 'action'

    action_id = Column(String, primary_key=True)
    description = Column(String, nullable=False)

    logs = relationship("Log", back_populates="action")


class Chat(Base):
    __tablename__ = 'chat'

    chat_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    participants = relationship("User", secondary=chat_participants, back_populates="chats")

class Message(Base):
    __tablename__ = 'message'

    message_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    message_content = Column(String, nullable=False)

    sender_id = Column(String, ForeignKey('medplus_user.user_id', ondelete="CASCADE"), nullable=False)

    chat_id = Column(String, ForeignKey('chat.chat_id', ondelete="CASCADE"), nullable=False)

    sender = relationship("User", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")



class Admin(User):
    __tablename__ = 'admin' 

    admin_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey('medplus_user.user_id', ondelete="CASCADE"), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',  
    }

class Page(Base):
    __tablename__ = 'page'

    page_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, nullable=False)
    created_by = Column(String, nullable=False)  
    created_date = Column(DateTime, default=datetime.utcnow)
    last_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_visible = Column(Boolean, default=True)
    
    contents = relationship("PageContent", back_populates="page", cascade="all, delete-orphan")

class PageContent(Base):
    __tablename__ = 'page_content'

    content_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, nullable=True)
    subtitle = Column(String, nullable=True)
    paragraph = Column(String, nullable=True)
    image_url = Column(String, nullable=True)


    page_id = Column(String, ForeignKey('page.page_id', ondelete="CASCADE"), nullable=False)

    page = relationship("Page", back_populates="contents")

class Staff(User):
    __tablename__ = 'staff'

    staff_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey('medplus_user.user_id', ondelete="CASCADE"), nullable=False)
    

    employment_date = Column(Date, nullable=False)
    employed_until = Column(Date, nullable=False)

    role_id = Column(String, ForeignKey('role.role_id'), nullable=False)
    department_id = Column(String, ForeignKey('department.dept_id', ondelete="RESTRICT"), nullable=False)
    
    role = relationship("Role", back_populates="staff")
    department = relationship("Department", back_populates="staff")

    __mapper_args__ = {
        'polymorphic_identity': 'staff',  
    }
    @property
    def is_working(self):
        if self.employed_until is None:
            return True 
        return datetime.utcnow().date() <= self.employed_until

class Department(Base):
    __tablename__ = 'department'

    dept_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    default_appointment_time = Column(Integer, nullable=False)

    staff = relationship("Staff", back_populates="department")

role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', String, ForeignKey('role.role_id', ondelete="CASCADE"), primary_key=True),
    Column('permission_id', String, ForeignKey('permission.permission_id', ondelete="CASCADE"), primary_key=True)
)

class Role(Base):
    __tablename__ = 'role'

    role_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    
    staff = relationship("Staff", back_populates="role")

    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

class Permission(Base):
    __tablename__ = 'permission'

    permission_id = Column(String, primary_key=True, index=True)
    description = Column(String, nullable=True)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")


class Doctor(Staff):
    __tablename__ = 'doctor'

    doctor_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    staff_id = Column(String, ForeignKey('staff.staff_id', ondelete="CASCADE"), nullable=False)


    specializations = Column(String, nullable=True)  
    qualifications = Column(String, nullable=True)

    years_of_experience = Column(Integer, nullable=False)
    enable_online_appointments = Column(Boolean, default=True)

    appointments = relationship("Appointment", back_populates="doctor")

    __mapper_args__ = {
        'polymorphic_identity': 'doctor', 
    }

class Patient(User):
    __tablename__ = 'patient'

    patient_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey('medplus_user.user_id', ondelete="CASCADE"), nullable=False)
    address = Column(String, nullable=True)

    medical_history = relationship("MedicalHistory", back_populates="patient", uselist=False)


    insurance = relationship("Insurance", back_populates="patients")
    appointments = relationship("Appointment", back_populates="patient")
    lab_tests = relationship("LabTest", back_populates="patient", cascade="all, delete-orphan")
    prescriptions = relationship("Prescription", back_populates="patient", cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'patient',  
    }

class Insurance(Base):
    __tablename__ = 'insurance'

    insurance_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    company = Column(String, nullable=False)
    details = Column(String, nullable=True)
    policy_no = Column(Integer, nullable=False)
    patient_id = Column(String, ForeignKey('patient.patient_id', ondelete="CASCADE"), unique=True, nullable=False)

    patient = relationship("Patient", back_populates="insurance")

class TreatmentType(enum.Enum):
    APPOINTMENT = "APPOINTMENT"
    PRESCRIPTION = "PRESCRIPTION"
    LABTEST = "LABTEST"
    OTHER = "OTHER"

class InsuredStatus(enum.Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    NOT_COVERED = "NOT_COVERED"

class Treatment(Base):
    __tablename__ = 'treatment'

    treatment_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    description = Column(String(255), nullable=False)
    cost = Column(Float, nullable=False)
    discount = Column(Float, nullable=True)
    treatment_type = Column(Enum(TreatmentType), nullable=False)
    insured_status = Column(Enum(InsuredStatus), nullable=False, default=InsuredStatus.NOT_COVERED)

    appointment_id = Column(String, ForeignKey('appointment.appointment_id'), nullable=True)
    prescription_id = Column(String, ForeignKey('prescription.prescription_id'), nullable=True)
    labtest_id = Column(String, ForeignKey('lab_test.test_id'), nullable=True)
    bill_id = Column(String, ForeignKey('bill.bill_id', ondelete="CASCADE"), nullable=True)
  
    appointment = relationship("Appointment")
    prescription = relationship("Prescription")
    labtest = relationship("LabTest")
    bill = relationship("Bill", back_populates="treatments")


class Bill(Base):
    __tablename__ = 'bill'

    bill_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    status_type = Column(String, nullable=False)
    date_issued = Column(DateTime, default=datetime.utcnow, nullable=False)
    

    patient_id = Column(String, ForeignKey('patient.patient_id', ondelete="CASCADE"), nullable=False)
    
    treatments = relationship("Treatment", back_populates="bill")
    payments = relationship("Payment", back_populates="bill")


class PaymentStatusType(enum.Enum):
    PAYED = "PAYED"
    UNPAYED = "UNPAYED"
    PENDING = "PENDING"

class Payment(Base):
    __tablename__ = 'payment'

    payment_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    amount_paid = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(PaymentStatusType), nullable=False, default=PaymentStatusType.PENDING)
    transaction_id = Column(String, nullable=True)
    description = Column(String, nullable=True)
    status_type = Column(String, nullable=True)

    bill_id = Column(String, ForeignKey('bill.bill_id', ondelete="CASCADE"), nullable=False)

    bill = relationship("Bill", back_populates="payments")

class AppointmentStatusType(enum.Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"

class Appointment(Base):
    __tablename__ = 'appointment'

    appointment_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    is_checked_in = Column(Boolean, default=False)
    status = Column(Enum(AppointmentStatusType), nullable=False, default=AppointmentStatusType.SCHEDULED)
    reason_for_visit = Column(String, nullable=True)
    location = Column(String, nullable=True)
    is_virtual = Column(Boolean, default=False)
    details = Column(String, nullable=True)

    patient_id = Column(String, ForeignKey('patient.patient_id', ondelete="CASCADE"), nullable=False)
    doctor_id = Column(String, ForeignKey('doctor.doctor_id', ondelete="CASCADE"), nullable=False)

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")


class LabTestStatus(enum.Enum):
    PENDING = "PENDING"   
    PREFORMED = "PREFORMED" 
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class LabTestType(enum.Enum):
    BLOOD_TEST = "BLOOD_TEST"
    URINE_TEST = "URINE_TEST"
    XRAY = "XRAY"
    MRI = "MRI"

class LabTest(Base):
    __tablename__ = 'lab_test'

    test_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    date_issued = Column(DateTime, default=datetime.utcnow, nullable=False)
    date_performed = Column(DateTime, nullable=True) 
    test_status = Column(Enum(LabTestStatus), nullable=False, default=LabTestStatus.PENDING)
    test_kind = Column(Enum(LabTestType), nullable=False)

    patient_id = Column(String, ForeignKey('patient.patient_id', ondelete="CASCADE"), nullable=False)
    doctor_id = Column(String, ForeignKey('doctor.doctor_id', ondelete="CASCADE"), nullable=False)

    patient = relationship("Patient", back_populates="lab_tests")
    doctor = relationship("Doctor")
    results = relationship("LabResult", back_populates="lab_test", cascade="all, delete-orphan")

class LabResult(Base):
    __tablename__ = 'lab_result'

    result_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    parameter = Column(String, nullable=False)
    value = Column(String, nullable=False)
    unit = Column(String, nullable=True)
    file_attachment = Column(String, nullable=True)

    test_id = Column(String, ForeignKey('lab_test.test_id', ondelete="CASCADE"), nullable=False)

    lab_test = relationship("LabTest", back_populates="results")


class Medication(Base):
    __tablename__ = 'medication'

    medication_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    standard_dose = Column(String, nullable=True)
    form = Column(String, nullable=True)
    route = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    active_ingredients = Column(String, nullable=False)

class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    READY = "READY"
    NOT_ACTIVE = "NOT_ACTIVE"

class Prescription(Base):
    __tablename__ = 'prescription'

    prescription_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    date_prescribed = Column(DateTime, default=datetime.utcnow, nullable=False)
    order_status = Column(Enum(OrderStatus), default=OrderStatus.NOT_ACTIVE, nullable=False)
    
    patient_id = Column(String, ForeignKey('patient.patient_id', ondelete="CASCADE"), nullable=False)
    doctor_id = Column(String, ForeignKey('doctor.doctor_id', ondelete="CASCADE"), nullable=False)

    patient = relationship("Patient", back_populates="prescriptions")  
    doctor = relationship("Doctor")
    prescribed_medications = relationship("PrescribedMedication", back_populates="prescription", cascade="all, delete-orphan")

class PrescribedMedication(Base):
    __tablename__ = 'prescribed_medication'

    prescribed_medication_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    dosage = Column(String, nullable=False)
    quantity = Column(String, nullable=False)  
    frequency = Column(String, nullable=False)
    duration = Column(String, nullable=False) 
    instruction_details = Column(String, nullable=True)

    prescription_id = Column(String, ForeignKey('prescription.prescription_id', ondelete="CASCADE"), nullable=False)
    medication_id = Column(String, ForeignKey('medication.medication_id', ondelete="CASCADE"), nullable=False)


    prescription = relationship("Prescription", back_populates="prescribed_medications")
    medication = relationship("Medication")

class BloodType(enum.Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

class Diagnosis(Base):
    __tablename__ = 'diagnosis'  

    diagnosis_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)

class Allergy(Base):
    __tablename__ = 'allergy' 

    allergy_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)

medical_history_medications = Table(
    'medical_history_medications', Base.metadata,
    Column('medical_history_id', String, ForeignKey('medical_history.medical_history_id',ondelete="CASCADE"), primary_key=True),
    Column('medication_id', String, ForeignKey('medication.medication_id',ondelete="CASCADE"), primary_key=True)
)

medical_history_diagnoses = Table(
    'medical_history_diagnoses', Base.metadata,
    Column('medical_history_id', String, ForeignKey('medical_history.medical_history_id',ondelete="CASCADE"), primary_key=True),
    Column('diagnosis_id', String, ForeignKey('diagnosis.diagnosis_id',ondelete="CASCADE"), primary_key=True)
)

medical_history_allergies = Table(
    'medical_history_allergies', Base.metadata,
    Column('medical_history_id', String, ForeignKey('medical_history.medical_history_id',ondelete="CASCADE"), primary_key=True),
    Column('allergy_id', String, ForeignKey('allergy.allergy_id',ondelete="CASCADE"), primary_key=True)
)

class MedicalHistory(Base):
    __tablename__ = 'medical_history'

    medical_history_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    

    blood_type = Column(Enum(BloodType), nullable=True)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)

    patient_id = Column(String, ForeignKey('patient.patient_id', ondelete="CASCADE"), unique=True, nullable=False)
    
    medications = relationship("Medication", secondary=medical_history_medications)
    diagnoses = relationship("Diagnosis", secondary=medical_history_diagnoses)
    allergies = relationship("Allergy", secondary=medical_history_allergies)

   


    
