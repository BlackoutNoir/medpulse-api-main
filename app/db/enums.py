from enum import Enum
from sqlalchemy.dialects.postgresql import ENUM
from app.db.main import engine
from sqlalchemy.ext.asyncio import AsyncConnection

class user_type(str, Enum):
    admin = "admin"
    patient = "patient"
    staff = "staff"
    user = "user"


class auth_type(str, Enum):
    email = "email"
    sms = "sms"
    none = "none"

class gender_type(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class entity_type(str, Enum):
    user = "user"
    chat = "chat"
    admin = "admin"
    staff = "staff"
    patient = "patient"
    page = "page"
    department = "department"
    bill = "bill"
    appointment = "appointment"
    labtest = "labtest"
    prescription = "prescription"
    medication = "medication"
    allergies = "allergies"
    diagnosis = "diagnosis"

class action_type(str, Enum):
    create = "create"
    update = "update"
    delete = "delete"
    get = "get"

class treatment_type(str, Enum):
    APPOINTMENT = "APPOINTMENT"
    PRESCRIPTION = "PRESCRIPTION"
    LABTEST = "LABTEST"
    OTHER = "OTHER"

class insured_status_type(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    NOT_COVERED = "NOT_COVERED"

class payment_status_type(str, Enum):
    PAYED = "PAYED"
    UNPAYED = "UNPAYED"
    PENDING = "PENDING"

class lab_test_status(str, Enum):
    PENDING = "PENDING"   
    PREFORMED = "PREFORMED" 
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class lab_test_type(str, Enum):
    BLOOD_TEST = "BLOOD_TEST"
    URINE_TEST = "URINE_TEST"
    XRAY = "XRAY"
    MRI = "MRI"

class order_status_type(str, Enum):
    PENDING = "PENDING"
    READY = "READY"
    NOT_ACTIVE = "NOT_ACTIVE"


class blood_type(str, Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"

class appointment_status_type(str, Enum):
    SCHEDULED = "SCHEDULED"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"
    PENDING = "PENDING"





# async def create_enums() -> None:
#     async with engine.begin() as conn:        
#         await create_enum_type(conn, user_type)
#         await create_enum_type(conn, auth_type)
#         await create_enum_type(conn, gender_type)


# async def create_enum_type(conn : AsyncConnection, enum_type : ENUM):

#     try:
#         await conn.run_sync(enum_type.create) 
#         print(f"Created ENUM type '{enum_type.name}' in the database.")
#     except Exception as e:
#         if 'already exists' in str(e):
#             print(f"ENUM type '{enum_type.name}' already exists in the database.")
#         else:
#             raise  
