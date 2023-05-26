import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from project.Models import Patient, Image, Series, Study
from project.Core.MSDatabase import engine, Base
import json
from datetime import datetime
import re
# Base.metadata.create_all(bind=engine)


def insert_into_msdb():
    # establish a connection to the database
    session_local = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    con = engine.connect()
    print(con)
    ins = sqlalchemy.inspect(engine)
    print(ins.get_table_names())

    # get and create a session object for interacting with the db
    db = next(get_db(session_local))
    with open('json.txt') as file:
        data = json.load(file)
        # create a array of image objects for bulk loading them into db
        img_objects = []
        counter = 0
        for obj in data['header_data']:
            # extract just the numbers from the patient ID field
            p_id = re.findall(r"\d+", obj['Patient']['PatientID'])
            # concatenate all the found ID parts to just one
            cleaned_id = ''
            for id_part in p_id:
                cleaned_id = cleaned_id + id_part
            # check if the current patient already exists and if not insert the patient into db
            patient = get_patient(db, cleaned_id)
            if not patient:
                pat_json = obj['Patient']
                # check for ID removed value if its true or false
                id_rem = False
                if pat_json['IDRemoved'] == 'YES':
                    id_rem = True
                new_patient = Patient.Patient(patientID=cleaned_id, patientIDc=pat_json['PatientID'],
                                                    name=pat_json['Name'], age=pat_json['Age'], sex=pat_json['Sex'],
                                                    size=pat_json['Size'], weight=pat_json['Weight'], idRemoved=id_rem)
                db.add(new_patient)
                # now get the patient from the db
                patient = get_patient(db, cleaned_id)

            # check if the current study already exists and if not insert the study into db
            study = get_study(db, obj['Patient']['Study']['StudyInstanceUID'][-8:])
            if not study:
                stu_json = obj['Patient']['Study']
                # making an DateTime object out of the StudyDate and StudyTime integer series
                date = stu_json['StudyDate'] + stu_json['StudyTime']
                # formatting the combined integer series
                temp = date[:4] + '-' + date[4:6] + '-' + date[6:8] + 'T' + date[8:10] + ':' + date[10:12] + ':' + date[
                                                                                                                   12:14]
                # get the DateTime object from the formatted string
                timestamp = datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S")
                new_study = Study.Study(studyUID=stu_json['StudyInstanceUID'][-8:], studyUIDc=stu_json['StudyInstanceUID'],
                                                studyDescription=stu_json['StudyDescription'],
                                                studyDateTime=timestamp, patient_id=patient.patientID)
                db.add(new_study)
                # now get the patient from the db
                study = get_study(db, obj['Patient']['Study']['StudyInstanceUID'][-8:])

            # check if the current series already exists and if not insert the series into db
            series = get_series(db, obj['Patient']['Study']['Series']['SeriesInstanceUID'][-8:])
            if not series:
                ser_json = obj['Patient']['Study']['Series']
                # making an DateTime object out of the SeriesDate and SeriesTime integer series
                date = ser_json['SeriesDate'] + ser_json['SeriesTime']
                # formatting the combined integer series
                temp = date[:4] + '-' + date[4:6] + '-' + date[6:8] + 'T' + date[8:10] + ':' + date[10:12] + ':' + date[
                                                                                                                   12:14]
                # get the DateTime object from the formatted string
                timestamp = datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S")
                new_series = Series.Series(seriesUID=ser_json['SeriesInstanceUID'][-8:]
                                                  , seriesUIDc=ser_json['SeriesInstanceUID'],
                                                  seriesNumber=ser_json['SeriesNumber'], seriesDateTime=timestamp,
                                                  bodyPartExamined=ser_json['BodyPartExamined']
                                                  , modality=ser_json['Modality'], manufacturer=ser_json['Manufacturer']
                                                  , manufacturerModelName=ser_json['ManufacturerModelName'],
                                                  patientPosition=ser_json['PatientPosition'],
                                                  kvp=ser_json['KVP'], exposureTime=ser_json['ExposureTime'],
                                                  frameOfReferenceUID=ser_json['FrameOfReferenceUID'],
                                                  seriesDescription=ser_json['SeriesDescription'], study_id=study.studyUID)
                db.add(new_series)
                # now get the patient from the db
                series = get_series(db, obj['Patient']['Study']['Series']['SeriesInstanceUID'][-8:])

            # check if the current image already exists and if not insert the image into db
            image = get_image(db, obj['Patient']['Study']['Series']['Image']['SOPInstanceUID'][-8:])
            if not image:
                img_json = obj['Patient']['Study']['Series']['Image']
                # making an DateTime object out of the ImageDate and ImageTime integer series
                date = img_json['ImageCreationDate'] + img_json['ImageCreationTime']
                # formatting the combined integer series
                temp = date[:4] + '-' + date[4:6] + '-' + date[6:8] + 'T' + date[8:10] + ':' + date[10:12] + ':' + date[
                                                                                                                   12:14]
                # get the DateTime object from the formatted string
                timestamp = datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S")
                # concat the image type array
                im_type = ' '.join(img_json['ImageType'])
                new_im = Image.Image(imageUID=img_json['SOPInstanceUID'][-8:], imageUIDc=img_json['SOPInstanceUID'],
                                             classUID=img_json['SOPClassUID'], creationDateTime=timestamp,
                                             imageType=im_type, instanceNumber=img_json['InstanceNumber'],
                                             de_idMethod=img_json['De-identificationMethod'],
                                             samplesPerPixel=img_json['SamplesPerPixel'],
                                             photometricInterpretation=img_json['PhotometricInterpretation'],
                                             bitsAllocated=img_json['BitsAllocated'], bitsStored=img_json['BitsStored'],
                                             highBit=img_json['HighBit'], pixelRepresentation=img_json['PixelRepresentation'],
                                             windowCenter=img_json['WindowCenter'], windowWidth=img_json['WindowWidth'],
                                             rescaleSlope=img_json['RescaleSlope'], sliceThickness=img_json['SliceThickness'],
                                             sliceLocation=img_json['SliceLocation'], series_id=series.seriesUID)
                img_objects.append(new_im)
            counter += 1
            if counter % 25 == 0:
                db.commit()
                # after committing the patient, study and series data to the db, also bulk load the images
                db.bulk_save_objects(img_objects)
                db.commit()
                print('Inserted the 25 rows of data.')
                # reset the bulk array
                img_objects = []


# define helper functions for checking if the database already contains a specified patient, study, series or image
def get_patient(db: Session, patient_id: int):
    return db.query(Patient.Patient).filter(Patient.Patient.patientID == patient_id).first()


def get_study(db: Session, study_id: int):
    return db.query(Study.Study).filter(Study.Study.studyUID == study_id).first()


def get_series(db: Session, series_id: int):
    return db.query(Series.Series).filter(Series.Series.seriesUID == series_id).first()


def get_image(db: Session, image_id: int):
    return db.query(Image.Image).filter(Image.Image.imageUID == image_id).first()


def get_db(session):
    """
    this functions obtains a session object for querying the database
    :return:
    """
    database = session()
    try:
        yield database
    finally:
        database.close()


if __name__ == '__main__':
    insert_into_msdb()
