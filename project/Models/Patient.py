from sqlalchemy import String, Integer, Column, SmallInteger, Boolean
from sqlalchemy.orm import relationship
from Core.Base import Base


class Patient(Base):
    __tablename__ = "patient"

    patientID = Column(Integer, primary_key=True, index=True)
    patientIDc = Column(String)
    name = Column(String)
    age = Column(String)
    sex = Column(String(1))
    size = Column(SmallInteger)
    weight = Column(SmallInteger)
    idRemoved = Column(Boolean)

    studies = relationship("Study", back_populates="patient")