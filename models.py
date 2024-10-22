import datetime
import enum
import uuid
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String , DateTime, Table, Enum
from sqlalchemy.orm import relationship
from database import Base


chat_participants = Table(
    'chat_participants', Base.metadata,
    Column('chat_id', String, ForeignKey('chats.chat_id', ondelete="CASCADE"), primary_key=True),
    Column('user_id', String, ForeignKey('users.user_id', ondelete="CASCADE"), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    settings_id = Column(String, ForeignKey('settings.id'), nullable=True)
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

    gender = Column(String, ForeignKey('gender.id'), nullable=False)
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


    user_id = Column(String, ForeignKey('users.user_id', ondelete="CASCADE"), unique=True, nullable=False)
    user = relationship("User", back_populates="settings")


class Log(Base):
    __tablename__ = 'logs'

    log_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)

    action_id = Column(String, ForeignKey('actions.action_id', ondelete="CASCADE"), nullable=False)

    user_id = Column(String, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="logs")

class Action(Base):
    __tablename__ = 'actions'

    action_id = Column(String, primary_key=True)
    description = Column(String, nullable=False)

    logs = relationship("Log", back_populates="action")


class Chat(Base):
    __tablename__ = 'chats'

    chat_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    creation_date = Column(DateTime, default=datetime.utcnow)

    messages = relationship("Message", back_populates="chat", cascade="all, delete-orphan")
    participants = relationship("User", secondary=chat_participants, back_populates="chats")

class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_read = Column(Boolean, default=False)
    message_content = Column(String, nullable=False)

    sender_id = Column(String, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)

    chat_id = Column(String, ForeignKey('chats.chat_id', ondelete="CASCADE"), nullable=False)

    sender = relationship("User", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")



class Admin(User):
    __tablename__ = 'admins' 

    admin_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'admin',  
    }

class Page(Base):
    __tablename__ = 'pages'

    page_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, nullable=False)
    created_by = Column(String, nullable=False)  
    created_date = Column(DateTime, default=datetime.utcnow)
    last_modified = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_visible = Column(Boolean, default=True)
    
    content = relationship("PageContent", back_populates="page", cascade="all, delete-orphan")

class PageContent(Base):
    __tablename__ = 'page_content'

    content_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    title = Column(String, nullable=True)
    subtitle = Column(String, nullable=True)
    paragraph = Column(String, nullable=True)
    image_url = Column(String, nullable=True)


    page_id = Column(String, ForeignKey('pages.page_id', ondelete="CASCADE"), nullable=False)

    page = relationship("Page", back_populates="contents")

class Staff(User):
    __tablename__ = 'staff'

    staff_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)
    

    employment_date = Column(Date, nullable=False)
    employment_until = Column(Date, nullable=False)

    role_id = Column(String, ForeignKey('roles.role_id'), nullable=False)
    department_id = Column(String, ForeignKey('departments.dept_id', ondelete="RESTRICT"), nullable=False)
    
    role = relationship("Role", back_populates="staff")
    department = relationship("Department", back_populates="staff")

    __mapper_args__ = {
        'polymorphic_identity': 'staff',  
    }

    def is_working(self):
        if self.employed_until is None:
            return True 
        return datetime.utcnow().date() <= self.employed_until

class Department(Base):
    __tablename__ = 'departments'

    dept_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    default_appointment_time = Column(Integer, nullable=False)

    staff = relationship("Staff", back_populates="department")

role_permissions = Table(
    'role_permissions', Base.metadata,
    Column('role_id', String, ForeignKey('roles.role_id', ondelete="CASCADE"), primary_key=True),
    Column('permission_id', String, ForeignKey('permissions.permission_id', ondelete="CASCADE"), primary_key=True)
)

class Role(Base):
    __tablename__ = 'roles'

    role_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    
    staff = relationship("Staff", back_populates="role")

    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

class Permission(Base):
    __tablename__ = 'permissions'

    permission_id = Column(String, primary_key=True, index=True)
    description = Column(String, nullable=True)

    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")


class Doctor(Staff):
    __tablename__ = 'doctors'

    doctor_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    staff_id = Column(String, ForeignKey('staff.staff_id', ondelete="CASCADE"), nullable=False)


    specializations = Column(String, nullable=True)  
    qualifications = Column(String, nullable=True)

    years_of_experience = Column(Integer, nullable=False)
    enable_online_appointments = Column(Boolean, default=True)

    __mapper_args__ = {
        'polymorphic_identity': 'doctor', 
    }

class Patient(User):
    __tablename__ = 'patients'

    patient_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, ForeignKey('users.user_id', ondelete="CASCADE"), nullable=False)

    address = Column(String, nullable=True)
    insurance_id = Column(String, ForeignKey('insurance.insurance_id'), nullable=True)
    medical_history_id = Column(String, ForeignKey('medical_history.medical_history_id'), nullable=True)


    insurance = relationship("Insurance", back_populates="patients")
    medical_history = relationship("MedicalHistory", back_populates="patients")

    __mapper_args__ = {
        'polymorphic_identity': 'patient',  
    }