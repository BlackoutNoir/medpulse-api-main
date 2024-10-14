from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base

class TableName(Base):
    __tablename__ = "table_name"

    id = Column(Integer, primary_key=True, index=True)