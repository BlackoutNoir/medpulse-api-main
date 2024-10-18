import datetime
from enum import Enum
import uuid
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String , DateTime, Table
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

class Gender(Base):
    __tablename__ = 'gender'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    gender = Column(String, unique=True, nullable=False)

    users = relationship("User", back_populates="gender")

class AuthTypeEnum(enum.Enum):
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

    auth_type = Column(Enum(AuthTypeEnum), nullable=False)


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