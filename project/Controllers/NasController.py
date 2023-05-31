import json
import re
import time
from datetime import datetime
from pydicom import dcmread
from webdav3.client import Client
from dotenv import dotenv_values
import project.Core.MongoDatabase as mdb
import project.Core.MSDatabase as msdb
from project.Models.Image import Image
from project.Models.Patient import Patient
from project.Controllers import PatientController
from project.Controllers import StudyController
from project.Controllers import ImageController
from project.Controllers import SeriesController
from project.Models.Series import Series
from project.Models.Study import Study


class NasController:
    def __init__(self):
        env = dotenv_values()
        self.nas_host = env['NASHOST']
        self.nas_user = env['NASUSER']
        self.nas_pass = env['NASPASS']
        self.remote_path = []
        self.found = False
        self.counter = 0
        self.org = {
            'webdav_hostname': self.nas_host,
            'webdav_login': self.nas_user,
            'webdav_password': self.nas_pass,
        }

    def download_start(self, option):
        client = Client(option)
        files = client.list()
        for i in range(1, len(files)):
            if "/" in files[i]:
                print("\033[0m Folder Found ][ " + ''.join(self.remote_path) + files[i] + "\n")
                if self.found:
                    self.remote_path.pop()
                    self.found = False
                self.remote_path.append(files[i])
                options = {
                    'webdav_hostname': self.nas_host + "/" + '/'.join(self.remote_path),
                    'webdav_login': self.nas_user,
                    'webdav_password': self.nas_pass,
                }
                self.download_start(options)
            elif ".dcm" in files[i]:
                local_file_path = 'uploads/' + str(int(time.time())) + "_" + str(self.counter) + "_" + files[i]
                client2 = Client(self.org)
                print("\033[92m DICOM Found ][ " + ''.join(self.remote_path) + files[i])
                client2.download(''.join(self.remote_path) + files[i], local_file_path)
                self.counter += 1
                self.found = True
                # formatting the right dicom file name // --> needs to be changed
                ds = dcmread(local_file_path).to_json()
                # the object still needs to be converted to json, because it is still a string
                json_obj = json.loads(ds)
                # append file path to the json object
                json_obj['file'] = {"filename":local_file_path}
                # extract the image unique id to query its existence
                val = json_obj['00080018']['Value'][0]
                # write the json object into the collection if its not already there
                try:
                    # if the object already exists, the query will return the corresponding document
                    cursor = mdb.collection.find({'00080018.Value': val}, {'7FE00010': 0})
                    if cursor:
                        mdb.collection.insert_one(json_obj)
                        print("Image inserted into object database \n 2 seconds sleep ...")
                        # small break
                        time.sleep(1)
                except:
                    pass

            # Check if the current file is the last file in the current folder
            if i == len(files) - 1 and self.remote_path:
                self.remote_path.pop()
                print("\033[91m Back to Folder ][ " + ''.join(self.remote_path))
                self.found = False

    def insert_into_msdb(self):
            """"
            function for inserting the from the mongodb extracted and parsed dicom files into the statistics database
            """
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
                    patient_obj = PatientController.PatientController()
                    patient = patient_obj.get_patient(msdb.db, cleaned_id)
                    if not patient:
                        pat_json = obj['Patient']
                        # check for ID removed value if its true or false
                        id_rem = False
                        if pat_json['IDRemoved'] == 'YES':
                            id_rem = True
                        new_patient = Patient.Patient(patientID=cleaned_id, patientIDc=pat_json['PatientID'],
                                                      name=pat_json['Name'], age=pat_json['Age'], sex=pat_json['Sex'],
                                                      size=pat_json['Size'], weight=pat_json['Weight'],
                                                      idRemoved=id_rem)
                        msdb.db.add(new_patient)
                        # now get the patient from the db
                        patient_obj = PatientController.PatientController()
                        patient = patient_obj.get_patient(msdb.db, cleaned_id)

                    # check if the current study already exists and if not insert the study into db
                    study_obj = StudyController.StudyController()
                    study = study_obj.get_study(msdb.db, obj['Patient']['Study']['StudyInstanceUID'][-8:])
                    if not study:
                        stu_json = obj['Patient']['Study']
                        # making an DateTime object out of the StudyDate and StudyTime integer series
                        date = stu_json['StudyDate'] + stu_json['StudyTime']
                        # formatting the combined integer series
                        temp = date[:4] + '-' + date[4:6] + '-' + date[6:8] + 'T' + date[8:10] + ':' + date[
                                                                                                       10:12] + ':' + date[
                                                                                                                      12:14]
                        # get the DateTime object from the formatted string
                        timestamp = datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S")
                        new_study = Study.Study(studyUID=stu_json['StudyInstanceUID'][-8:],
                                                studyUIDc=stu_json['StudyInstanceUID'],
                                                studyDescription=stu_json['StudyDescription'],
                                                studyDateTime=timestamp, patient_id=patient.patientID)
                        msdb.db.add(new_study)
                        # now get the patient from the db
                        study = study_obj.get_study(msdb.db, obj['Patient']['Study']['StudyInstanceUID'][-8:])

                    # check if the current series already exists and if not insert the series into db
                    series_obj = SeriesController.SeriesController()
                    series = series_obj.get_series(msdb.db, obj['Patient']['Study']['Series']['SeriesInstanceUID'][-8:])
                    if not series:
                        ser_json = obj['Patient']['Study']['Series']
                        # making an DateTime object out of the SeriesDate and SeriesTime integer series
                        date = ser_json['SeriesDate'] + ser_json['SeriesTime']
                        # formatting the combined integer series
                        temp = date[:4] + '-' + date[4:6] + '-' + date[6:8] + 'T' + date[8:10] + ':' + date[
                                                                                                       10:12] + ':' + date[
                                                                                                                      12:14]
                        # get the DateTime object from the formatted string
                        timestamp = datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S")
                        new_series = Series.Series(seriesUID=ser_json['SeriesInstanceUID'][-8:]
                                                   , seriesUIDc=ser_json['SeriesInstanceUID'],
                                                   seriesNumber=ser_json['SeriesNumber'], seriesDateTime=timestamp,
                                                   bodyPartExamined=ser_json['BodyPartExamined']
                                                   , modality=ser_json['Modality'],
                                                   manufacturer=ser_json['Manufacturer']
                                                   , manufacturerModelName=ser_json['ManufacturerModelName'],
                                                   patientPosition=ser_json['PatientPosition'],
                                                   kvp=ser_json['KVP'], exposureTime=ser_json['ExposureTime'],
                                                   frameOfReferenceUID=ser_json['FrameOfReferenceUID'],
                                                   seriesDescription=ser_json['SeriesDescription'],
                                                   study_id=study.studyUID)
                        msdb.db.add(new_series)
                        # now get the patient from the db
                        serObj = SeriesController.SeriesController()
                        series = serObj.get_series(msdb.db, obj['Patient']['Study']['Series']['SeriesInstanceUID'][-8:])

                    # check if the current image already exists and if not insert the image into db
                    imgObj = ImageController.ImageController()
                    image = imgObj.get_image(msdb.db, obj['Patient']['Study']['Series']['Image']['SOPInstanceUID'][-8:])
                    if not image:
                        img_json = obj['Patient']['Study']['Series']['Image']
                        # making an DateTime object out of the ImageDate and ImageTime integer series
                        date = img_json['ImageCreationDate'] + img_json['ImageCreationTime']
                        # formatting the combined integer series
                        temp = date[:4] + '-' + date[4:6] + '-' + date[6:8] + 'T' + date[8:10] + ':' + date[
                                                                                                       10:12] + ':' + date[
                                                                                                                      12:14]
                        # get the DateTime object from the formatted string
                        timestamp = datetime.strptime(temp, "%Y-%m-%dT%H:%M:%S")
                        # concat the image type array
                        im_type = ' '.join(img_json['ImageType'])
                        new_im = Image.Image(imageUID=img_json['SOPInstanceUID'][-8:],
                                             imageUIDc=img_json['SOPInstanceUID'],
                                             classUID=img_json['SOPClassUID'], creationDateTime=timestamp,
                                             imageType=im_type, instanceNumber=img_json['InstanceNumber'],
                                             de_idMethod=img_json['De-identificationMethod'],
                                             samplesPerPixel=img_json['SamplesPerPixel'],
                                             photometricInterpretation=img_json['PhotometricInterpretation'],
                                             bitsAllocated=img_json['BitsAllocated'], bitsStored=img_json['BitsStored'],
                                             highBit=img_json['HighBit'],
                                             pixelRepresentation=img_json['PixelRepresentation'],
                                             windowCenter=img_json['WindowCenter'], windowWidth=img_json['WindowWidth'],
                                             rescaleSlope=img_json['RescaleSlope'],
                                             sliceThickness=img_json['SliceThickness'],
                                             sliceLocation=img_json['SliceLocation'], series_id=series.seriesUID)
                        img_objects.append(new_im)
                    counter += 1
                    if counter % 50 == 0:
                        msdb.db.commit()
                        # after committing the patient, study and series data to the db, also bulk load the images
                        msdb.db.bulk_save_objects(img_objects)
                        msdb.db.commit()
                        print('Inserted 50 rows of data.')
                        # reset the bulk array
                        img_objects = []
