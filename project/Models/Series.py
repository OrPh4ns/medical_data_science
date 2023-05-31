from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, SmallInteger
from sqlalchemy.orm import relationship
from Core.MSDatabase import Base


class Series(Base):
    __tablename__ = "series"

    seriesUID = Column(Integer, primary_key=True, index=True)
    seriesUIDc = Column(String)
    seriesNumber = Column(SmallInteger)
    seriesDateTime = Column(DateTime)
    bodyPartExamined = Column(String)
    modality = Column(String)
    manufacturer = Column(String)
    manufacturerModelName = Column(String)
    patientPosition = Column(String)
    kvp = Column(SmallInteger)
    exposureTime = Column(SmallInteger)
    frameOfReferenceUID = Column(String)
    seriesDescription = Column(String)
    study_id = Column(Integer, ForeignKey('study.studyUID'))

    study = relationship("Study", back_populates="series_f")
    images = relationship("Image", back_populates="study")