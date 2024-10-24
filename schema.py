from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date
import uuid
import enum



class UserBase(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    phone_no: Optional[str] = None
    date_of_birth: Optional[date] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: uuid.UUID
    gender: str

    class Config:
        orm_mode = True


class GenderBase(BaseModel):
    gender: str

class GenderResponse(GenderBase):
    id: uuid.UUID

    class Config:
        orm_mode = True


class SettingsBase(BaseModel):
    font_size: Optional[int] = None
    screen_reader: bool = False
    on_screen_keyboard: bool = False
    email_notifications: bool = True
    sms_notifications: bool = False
    email_reminders: bool = False
    sms_reminders: bool = False

class SettingsResponse(SettingsBase):
    settings_id: uuid.UUID

    class Config:
        orm_mode = True


class LogBase(BaseModel):
    timestamp: datetime
    action_id: uuid.UUID

class LogResponse(LogBase):
    log_id: uuid.UUID

    class Config:
        orm_mode = True


class ActionBase(BaseModel):
    description: str

class ActionResponse(ActionBase):
    action_id: uuid.UUID

    class Config:
        orm_mode = True


class ChatBase(BaseModel):
    name: str

class ChatResponse(ChatBase):
    chat_id: uuid.UUID
    creation_date: datetime

    class Config:
        orm_mode = True


class MessageBase(BaseModel):
    message_content: str
    is_read: bool = False

class MessageResponse(MessageBase):
    message_id: uuid.UUID
    timestamp: datetime

    class Config:
        orm_mode = True


class AdminBase(UserBase):
    pass

class AdminResponse(AdminBase):
    admin_id: uuid.UUID

    class Config:
        orm_mode = True


class PageBase(BaseModel):
    title: str
    created_by: str

class PageResponse(PageBase):
    page_id: uuid.UUID
    created_date: datetime
    last_modified: datetime

    class Config:
        orm_mode = True


class PageContentBase(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    paragraph: Optional[str] = None
    image_url: Optional[str] = None

class PageContentResponse(PageContentBase):
    content_id: uuid.UUID

    class Config:
        orm_mode = True


class StaffBase(UserBase):
    employment_date: date
    employed_until: date

class StaffResponse(StaffBase):
    staff_id: uuid.UUID
    role_id: uuid.UUID
    department_id: uuid.UUID

    class Config:
        orm_mode = True


class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = None
    default_appointment_time: int

class DepartmentResponse(DepartmentBase):
    dept_id: uuid.UUID

    class Config:
        orm_mode = True


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleResponse(RoleBase):
    role_id: uuid.UUID

    class Config:
        orm_mode = True


class PermissionBase(BaseModel):
    description: str

class PermissionResponse(PermissionBase):
    permission_id: uuid.UUID

    class Config:
        orm_mode = True


class DoctorBase(StaffBase):
    specializations: Optional[str] = None
    qualifications: Optional[str] = None
    years_of_experience: int
    enable_online_appointments: bool = True

class DoctorResponse(DoctorBase):
    doctor_id: uuid.UUID

    class Config:
        orm_mode = True


class PatientBase(UserBase):
    address: Optional[str] = None

class PatientResponse(PatientBase):
    patient_id: uuid.UUID

    class Config:
        orm_mode = True


class InsuranceBase(BaseModel):
    company: str
    details: Optional[str] = None
    policy_no: int

class InsuranceResponse(InsuranceBase):
    insurance_id: uuid.UUID

    class Config:
        orm_mode = True


class TreatmentBase(BaseModel):
    description: str
    cost: float
    discount: Optional[float] = None
    treatment_type: str
    insured_status: str

class TreatmentResponse(TreatmentBase):
    treatment_id: uuid.UUID

    class Config:
        orm_mode = True


class BillBase(BaseModel):
    amount: float
    description: str
    status_type: str

class BillResponse(BillBase):
    bill_id: uuid.UUID
    date_issued: datetime

    class Config:
        orm_mode = True


class PaymentBase(BaseModel):
    amount_paid: float
    status: str

class PaymentResponse(PaymentBase):
    payment_id: uuid.UUID
    date: datetime

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    start_date: datetime
    end_date: datetime
    reason_for_visit: Optional[str] = None

class AppointmentResponse(AppointmentBase):
    appointment_id: uuid.UUID
    status: str

    class Config:
        orm_mode = True


class LabTestBase(BaseModel):
    test_kind: str
    test_status: str
    date_issued: datetime

class LabTestResponse(LabTestBase):
    test_id: uuid.UUID

    class Config:
        orm_mode = True


class LabResultBase(BaseModel):
    parameter: str
    value: str
    unit: Optional[str] = None

class LabResultResponse(LabResultBase):
    result_id: uuid.UUID

    class Config:
        orm_mode = True


class MedicationBase(BaseModel):
    name: str
    company: str
    stock: int
    price: float
    active_ingredients: str

class MedicationResponse(MedicationBase):
    medication_id: uuid.UUID

    class Config:
        orm_mode = True


class PrescriptionBase(BaseModel):
    date_prescribed: datetime
    order_status: str

class PrescriptionResponse(PrescriptionBase):
    prescription_id: uuid.UUID

    class Config:
        orm_mode = True


class PrescribedMedicationBase(BaseModel):
    dosage: str
    quantity: str
    frequency: str
    duration: str
    instruction_details: Optional[str] = None

class PrescribedMedicationResponse(PrescribedMedicationBase):
    prescribed_medication_id: uuid.UUID

    class Config:
        orm_mode = True


class BloodType(enum.Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"


class DiagnosisBase(BaseModel):
    name: str

class DiagnosisResponse(DiagnosisBase):
    diagnosis_id: uuid.UUID

    class Config:
        orm_mode = True


class AllergyBase(BaseModel):
    name: str

class AllergyResponse(AllergyBase):
    allergy_id: uuid.UUID

    class Config:
        orm_mode = True


class MedicalHistoryBase(BaseModel):
    blood_type: Optional[BloodType] = None
    height: Optional[float] = None
    weight: Optional[float] = None

class MedicalHistoryResponse(MedicalHistoryBase):
    medical_history_id: uuid.UUID
    diagnoses: List[DiagnosisResponse] = []
    medications: List[MedicationResponse] = []
    allergies: List[AllergyResponse] = []

    class Config:
        orm_mode = True