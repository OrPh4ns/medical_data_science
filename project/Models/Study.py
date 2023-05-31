from sqlalchemy import String, Integer, Column, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from Core.MSDatabase import Base


class Study(Base):
    __tablename__ = "study"

    studyUID = Column(Integer, primary_key=True, index=True)
    studyUIDc = Column(String)
    studyDateTime = Column(DateTime)
    studyDescription = Column(String)
    patient_id = Column(Integer, ForeignKey('patient.patientID'))

    patient = relationship("Patient", back_populates="studies")
    series_f = relationship("Series", back_populates="study")