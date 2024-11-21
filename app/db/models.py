from sqlmodel import  SQLModel, Field, Column, Relationship
import uuid
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime, date, timezone
from typing import Optional, List
from app.db.enums import (
    user_type as UserType, 
    auth_type as AuthType, 
    gender_type, 
    entity_type, 
    action_type,
    treatment_type,
    insured_status_type,
    payment_status_type,
    appointment_status_type,
    lab_test_status,
    lab_test_type,
    order_status_type,
    blood_type as BloodType
)


class ChatParticipant(SQLModel, table=True):
    __tablename__ = "chat_participant"
    chat_uid: uuid.UUID = Field(foreign_key="chat.uid", ondelete="CASCADE", primary_key=True)
    user_uid: uuid.UUID = Field(foreign_key="medpulse_user.uid", ondelete="CASCADE", primary_key=True)


class User(SQLModel, table=True):
    __tablename__ = "medpulse_user"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    username: str  = Field(unique=True)
    email: str = Field(unique=True)
    firstname: str
    lastname: str
    phone_no: Optional[str] = Field(default=None, nullable=True)
    date_of_birth:  Optional[date] = Field(default=None, nullable=True)
    is_verified: bool = Field(default=False)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(timezone.utc)))
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(timezone.utc)))  
    last_login: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(timezone.utc)))
    password_hash: str = Field(exclude=True)
    image_url: str = Field(default=None, nullable=True)

    user_type: UserType = Field(
        nullable=False
    )

    gender: Optional[gender_type] = Field(default=None, nullable=True) 


    settings: Optional["Settings"] = Relationship(
        back_populates="user", 
        sa_relationship_kwargs={"lazy": "selectin","cascade": "all, delete-orphan"}
        
    )

    logs: List["Log"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin","cascade": "all, delete-orphan"}
    )

    chats: List["Chat"] = Relationship(
        back_populates="participants", link_model=ChatParticipant,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    patient: Optional["Patient"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin","cascade": "all, delete-orphan"}
    )

    staff: Optional["Staff"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"lazy": "selectin","cascade": "all, delete-orphan"}
    )
    



class Settings(SQLModel, table=True):
    __tablename__ = "settings"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    user_uid : uuid.UUID = Field(foreign_key="medpulse_user.uid", nullable=False, unique=True)

    font_size: int = Field(default=14)
    screen_reader: bool = Field(default=False)
    on_screen_keyboard: bool = Field(default=False)
    email_notifications: bool = Field(default=True)
    sms_notifications: bool = Field(default=False)
    email_reminders: bool = Field(default=False)
    sms_reminders: bool = Field(default=False)
    auth_type: AuthType = Field(nullable=False, default=AuthType.none)

    user: User = Relationship(
        back_populates="settings", sa_relationship_kwargs={"lazy": "selectin"}
    )

class Log (SQLModel, table=True):
    __tablename__ = "log"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    user_uid : uuid.UUID = Field(foreign_key="medpulse_user.uid", nullable=False)

    action: action_type
    entity: entity_type
    description: str 
    timestamp: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(timezone.utc)))

    user: User = Relationship(
        back_populates="logs",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

class Chat(SQLModel, table=True):
    __tablename__ = "chat"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    name: str
    creation_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(timezone.utc)))

    messages: List["Message"] = Relationship(
        back_populates="chat",
        sa_relationship_kwargs={"lazy": "selectin","cascade": "all, delete-orphan"}
    )
    
    participants: List[User] = Relationship(
        link_model=ChatParticipant,
        back_populates="chats",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

class Message(SQLModel, table=True):
    __tablename__ = "message"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    timestamp: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(timezone.utc)))
    is_read: bool = Field(default=False)
    message_content: str

    sender_uid: uuid.UUID = Field(foreign_key="medpulse_user.uid",ondelete="CASCADE", nullable=False)
    chat_uid: uuid.UUID = Field(foreign_key="chat.uid", nullable=False)

    chat: Chat = Relationship(
        back_populates="messages",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Page(SQLModel, table=True):
    __tablename__ = "page"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    title: str
    created_by: str
    created_date: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(timezone.utc)))
    last_modified: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)) )
    is_visible: bool = Field(default=True)

    contents: List["PageContent"] = Relationship(
        back_populates="page",
        sa_relationship_kwargs={"lazy": "selectin","cascade": "all, delete-orphan"},
        
    )

class PageContent(SQLModel, table=True):
    __tablename__ = "page_content"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    title: Optional[str] = None
    subtitle: Optional[str] = None
    paragraph: Optional[str] = None
    image_url: Optional[str] = None

    
    page_uid : uuid.UUID = Field(foreign_key="page.uid", nullable=False)

    page: Optional[Page] = Relationship(
        back_populates="contents",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class Schedule(SQLModel, table=True):
    __tablename__ = "schedule"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    staff_uid: uuid.UUID = Field(foreign_key="staff.uid")

    shift_start: datetime
    shift_end: datetime
    day_of_week: str  
    location: Optional[str] = Field(default=None)  
    notes: Optional[str] = Field(default=None)  
    # Relationships
    staff: Optional["Staff"] = Relationship(
        back_populates="schedules",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class Staff(SQLModel, table=True):
    __tablename__ = "staff"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    user_uid: uuid.UUID = Field(foreign_key="medpulse_user.uid", nullable=False)

    employment_date: date
    employed_until: Optional[date] = None

    role_uid: uuid.UUID = Field(foreign_key="role.uid", nullable=False)
    department_uid: uuid.UUID = Field(foreign_key="department.uid", nullable=False)

    role: Optional["Role"] = Relationship(back_populates="staff",sa_relationship_kwargs={"lazy": "selectin"})
    department: Optional["Department"] = Relationship(back_populates="staff",sa_relationship_kwargs={"lazy": "selectin"})
    user: Optional["User"] = Relationship(back_populates="staff",sa_relationship_kwargs={"lazy": "selectin"})

    doctor: Optional["Doctor"] = Relationship(back_populates="staff", sa_relationship_kwargs={"lazy": "selectin"})

    schedules: List["Schedule"] = Relationship(
        back_populates="staff",
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"}
    )

class Department(SQLModel, table=True):
    __tablename__ = "department"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    name: str
    description: Optional[str] = None
    default_appointment_time: int #in minutes

    staff: List["Staff"] = Relationship(back_populates="department",sa_relationship_kwargs={"lazy": "selectin"})
    

class RolePermission(SQLModel, table=True):
    role_uid: uuid.UUID  = Field(foreign_key="role.uid",ondelete="CASCADE", primary_key=True)
    permission_uid: uuid.UUID = Field(foreign_key="permission.uid",ondelete="CASCADE", primary_key=True)


class Role(SQLModel, table=True):
    __tablename__ = 'role'

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    name: str = Field(unique=True, nullable=False)
    description: Optional[str] = None

    staff: List["Staff"] = Relationship(
        back_populates="role",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    permissions: List["Permission"] = Relationship(
        back_populates="roles",
        link_model=RolePermission,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class Permission(SQLModel, table=True):
    __tablename__ = 'permission'

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    description: Optional[str] = None

    roles: List[Role] = Relationship(
        back_populates="permissions",
        link_model=RolePermission,
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class Doctor(SQLModel, table=True):
    __tablename__ = 'doctor'

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    staff_uid: uuid.UUID = Field(foreign_key="staff.uid", nullable=False)


    specializations: List[str] = Field(
        sa_column=Column(pg.JSON, nullable=True)  
    )
    qualifications: List[str] = Field(
        sa_column=Column(pg.JSON, nullable=True)  
    )

    years_of_experience: int
    enable_online_appointments : bool

    staff: Staff = Relationship(
        back_populates="doctor",
        sa_relationship_kwargs={"lazy": "selectin"}
    )   

    
    appointments: Optional[List["Appointment"]] = Relationship(
        back_populates="doctor",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Patient(SQLModel, table=True):
    __tablename__ = "patient"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    user_uid: uuid.UUID = Field(foreign_key="medpulse_user.uid", nullable=False, unique=True)

    
    address: Optional[str] = Field(default=None)

    # Relationships


    user: Optional["User"] = Relationship(
        back_populates="patient",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    medical_history: Optional["MedicalHistory"] = Relationship(
        back_populates="patient", 
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"}
    )

    insurance: Optional["Insurance"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin", "cascade": "all, delete-orphan"}
    )

    appointments: Optional[List["Appointment"]] = Relationship(
        back_populates="patient",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    lab_tests: Optional[List["LabTest"]] = Relationship(
        back_populates="patient",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    prescriptions: Optional[List["Prescription"]] = Relationship(
        back_populates="patient",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    bills: Optional[List["Bill"]] = Relationship(
        back_populates="patient",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Insurance(SQLModel, table=True):
    __tablename__ = "insurance"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    company: str = Field(nullable=False)
    details: Optional[str] = Field(default=None)
    policy_no: int = Field(nullable=False)

    patient_uid: uuid.UUID = Field(
        foreign_key="patient.uid", nullable=False, unique=True, ondelete="CASCADE"
    )

class Treatment(SQLModel, table=True):
    __tablename__ = "treatment"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    description: str
    cost: float = Field(nullable=False)
    discount: Optional[float] = Field(default=0.0)
    type: treatment_type = Field(nullable=False)
    insured_status: insured_status_type = Field(
        default=insured_status_type.NOT_COVERED
    
    )

    bill_uid: uuid.UUID = Field(
        foreign_key="bill.uid",
        ondelete="CASCADE"
    )


    appointment_uid: Optional[uuid.UUID] = Field(foreign_key="appointment.uid", default=None)
    prescription_uid: Optional[uuid.UUID] = Field(foreign_key="prescription.uid", default=None)
    labtest_uid: Optional[uuid.UUID] = Field(foreign_key="lab_test.uid", default=None)
    

    # Relationships
    appointment: Optional["Appointment"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    prescription: Optional["Prescription"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    labtest: Optional["LabTest"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    bill: Optional["Bill"] = Relationship(
        back_populates="treatments",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

class Bill(SQLModel, table=True):
    __tablename__ = "bill"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    amount: float 
    description: str
    payed: bool
    date_issued:  datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(timezone.utc)))

    patient_uid: uuid.UUID = Field(
        foreign_key="patient.uid", nullable=False, ondelete="CASCADE"
    )

    # Relationships
    treatments: List[Treatment] = Relationship(back_populates="bill", sa_relationship_kwargs={"lazy": "selectin"})
    payments: List["Payment"] = Relationship(back_populates="bill", sa_relationship_kwargs={"lazy": "selectin"})
    patient: Patient = Relationship(back_populates="bills", sa_relationship_kwargs={"lazy": "selectin"})

class Payment(SQLModel, table=True):
    __tablename__ = "payment"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    amount_paid: float = Field(nullable=False)
    date:  datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(timezone.utc)))
    status: payment_status_type = Field(default=payment_status_type.UNPAYED)
    transaction_id: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    status_type: Optional[str] = Field(default=None)

    bill_uid: uuid.UUID = Field(
        foreign_key="bill.uid", ondelete="CASCADE"
    )

    # Relationship
    bill: Optional[Bill] = Relationship(
        back_populates="payments",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Appointment(SQLModel, table=True):
    __tablename__ = "appointment"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    start_date: datetime 

    duration: int # in minutes 


    is_checked_in: bool = Field(default=False)


    status: appointment_status_type = Field(
        default=appointment_status_type.PENDING,
    )
    reason_for_visit: Optional[str] = Field(default=None)
    location: str
    is_virtual: bool = Field(default=False)
    details: Optional[str] = Field(default=None)

    patient_uid: uuid.UUID = Field(
        foreign_key="patient.uid",
        ondelete="CASCADE"
    )
    doctor_uid: uuid.UUID = Field(
        foreign_key="doctor.uid",
        ondelete="CASCADE"
    )

    # Relationships
    patient: Optional["Patient"] = Relationship(
        back_populates="appointments",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    doctor: Optional["Doctor"] = Relationship(
        back_populates="appointments",
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class LabTest(SQLModel, table=True):
    __tablename__ = "lab_test"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    date_issued:  datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(timezone.utc)))
    date_performed: Optional[datetime] = Field(default=None)
    test_status: lab_test_status = Field(
        default=lab_test_status.PENDING
    )
    test_type: lab_test_type 

    patient_uid: uuid.UUID = Field(
        foreign_key="patient.uid", nullable=False, ondelete="CASCADE"
    )
    doctor_uid: uuid.UUID = Field(
        foreign_key="doctor.uid", nullable=False, ondelete="CASCADE"
    )

    # Relationships
    patient: Optional["Patient"] = Relationship(
        back_populates="lab_tests",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    issued_by: Optional["Doctor"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    results: List["LabResult"] = Relationship(
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"}
    )


class LabResult(SQLModel, table=True):
    __tablename__ = "lab_result"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    parameter: Optional[str] 
    value: Optional[str]
    unit: Optional[str] 
    file_attachment: Optional[str] 

    test_uid: uuid.UUID = Field(
        foreign_key="lab_test.uid", ondelete="CASCADE"
    )


class Medication(SQLModel, table=True):
    __tablename__ = "medication"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    name: str 
    company: str 
    stock: int 
    standard_dose: Optional[str] 
    form: Optional[str] 
    route: Optional[str] 
    price: float 
    active_ingredients: str 


class Prescription(SQLModel, table=True):
    __tablename__ = "prescription"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    date_prescribed: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now(timezone.utc)))
    order_status: order_status_type = Field(
        default=order_status_type.NOT_ACTIVE
    )

    patient_uid: uuid.UUID = Field(
        foreign_key="patient.uid", ondelete="CASCADE"
    )
    doctor_uid: uuid.UUID = Field(
        foreign_key="doctor.uid", ondelete="CASCADE"
    )

    # Relationships
    patient: Optional["Patient"] = Relationship(
        back_populates="prescriptions",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    
    doctor: Optional["Doctor"] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    prescribed_medications: List["PrescribedMedication"] = Relationship(
        back_populates="prescription",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "lazy": "selectin"},
        
    )


class PrescribedMedication(SQLModel, table=True):
    __tablename__ = "prescribed_medication"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    dosage: str 
    quantity: str 
    frequency: str 
    duration: str 
    instruction_details: Optional[str] = Field(default=None)

    prescription_uid: uuid.UUID = Field(
        foreign_key="prescription.uid", ondelete="CASCADE"
    )

    medication_uid: uuid.UUID = Field(
        foreign_key="medication.uid", ondelete="CASCADE"
    )

    # Relationships
    prescription: Optional[Prescription] = Relationship(
        back_populates="prescribed_medications",
        sa_relationship_kwargs={"lazy": "selectin"}

    )
    medication: Optional[Medication] = Relationship(
        sa_relationship_kwargs={"lazy": "selectin"}
    )


class Diagnosis(SQLModel, table=True):
    __tablename__ = "diagnosis"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str 


class Allergy(SQLModel, table=True):
    __tablename__ = "allergy"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    name: str 


class MedicalHistoryMedications(SQLModel, table=True):
    __tablename__ = "medical_history_medications"

    medical_history_uid: uuid.UUID = Field(foreign_key="medical_history.uid", ondelete="CASCADE", primary_key=True)
    medication_uid: uuid.UUID = Field(foreign_key="medication.uid", ondelete="CASCADE", primary_key=True)


class MedicalHistoryAllergies(SQLModel, table=True):
    __tablename__ = "medical_history_allergies"

    medical_history_uid: uuid.UUID = Field(foreign_key="medical_history.uid", ondelete="CASCADE", primary_key=True)
    allergy_uid: uuid.UUID = Field(foreign_key="allergy.uid", ondelete="CASCADE", primary_key=True)


class MedicalHistoryDiagnosis(SQLModel, table=True):
    __tablename__ = "medical_history_diagnosis"

    medical_history_uid: uuid.UUID = Field(foreign_key="medical_history.uid", ondelete="CASCADE", primary_key=True)
    diagnosis_uid: uuid.UUID = Field(foreign_key="diagnosis.uid", ondelete="CASCADE", primary_key=True)
  

class MedicalHistory(SQLModel, table=True):
    __tablename__ = "medical_history"

    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )

    blood_type: Optional[BloodType] = Field(default=None)
    height: Optional[float] = Field(default=None)
    weight: Optional[float] = Field(default=None)

    patient_uid: uuid.UUID = Field(
        foreign_key="patient.uid", nullable=False, unique=True, ondelete="CASCADE"
    )

    # Relationships

    patient: Patient = Relationship(
        back_populates="medical_history",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    medications: List["Medication"] = Relationship(
        link_model= MedicalHistoryMedications,
        sa_relationship_kwargs={ "lazy": "selectin"}
    )
    diagnoses: List["Diagnosis"] = Relationship(
        link_model= MedicalHistoryDiagnosis,
        sa_relationship_kwargs={"lazy": "selectin"}
    )
    allergies: List["Allergy"] = Relationship(
        link_model= MedicalHistoryAllergies,
        sa_relationship_kwargs={"lazy": "selectin"}
    )