from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, SmallInteger, Float
from sqlalchemy.orm import relationship
from Core.MSDatabase import Base


class Image(Base):
    __tablename__ = "image"

    imageUID = Column(Integer, primary_key=True, index=True)
    imageUIDc = Column(String)
    classUID = Column(String)
    creationDateTime = Column(DateTime)
    imageType = Column(String)
    instanceNumber = Column(SmallInteger)
    de_idMethod = Column(String)
    samplesPerPixel = Column(SmallInteger)
    photometricInterpretation = Column(String)
    bitsAllocated = Column(SmallInteger)
    bitsStored = Column(SmallInteger)
    highBit = Column(SmallInteger)
    pixelRepresentation = Column(SmallInteger)
    windowCenter = Column(Float)
    windowWidth = Column(Float)
    rescaleSlope = Column(Float)
    sliceThickness = Column(Float)
    sliceLocation = Column(Float)
    series_id = Column(Integer, ForeignKey('series.seriesUID'))

    study = relationship("Series", back_populates="images")