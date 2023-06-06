import json
from bson import json_util
import Core.MongoDatabase as mdb


def parse_dicom():
    # establishing a connection to the mongodb
    mongoclient = mdb.mongoclient

    print(mongoclient.list_database_names())

    # select the right database
    db = mongoclient['dicom']

    # select the right collection
    collection = db['dicom_header']

    # get all the dicom objects stored in the mongodb and exclude the pixel data array from the query
    cursor = collection.find({}, {'7FE00010': 0})
    header_list = list()

    # loop through all the documents stored in the database
    for document in cursor:
        # convert the object into json // mongodb stores as bson, which must be converted to json
        js = json.loads(json_util.dumps(document))

        # extract the table data for patient form the meta data and store it as own json object
        patient = {}
        patient['PatientID'] = js['00100020']['Value'][0]
        if '00100010' in js and 'Value' in js['00100010']:
            patient['Name'] = js['00100010']['Value'][0]['Alphabetic']
        else:
            patient['Name'] = None
        if '00101010' in js and 'Value' in js['00101010']:
            patient['Age'] = js['00101010']['Value'][0]
        else:
            patient['Age'] = None
        if '0010040' in js and 'Value' in js['0010040']:
            patient['Sex'] = js['00100040']['Value'][0]
        else:
            patient['Sex'] = None
        if '00101020' in js and 'Value' in js['00101020']:
            patient['Size'] = js['00101020']['Value'][0]
        else:
            patient['Size'] = None
        if '00101030' in js and 'Value' in js['00101030']:
            patient['Weight'] = js['00101030']['Value'][0]
        else:
            patient['Weight'] = None
        if '00120062' in js and 'Value' in js['00120062']:
            patient['IDRemoved'] = js['00120062']['Value'][0]
        else:
            patient['IDRemoved'] = None

        # extract the table data for study form the meta data and store it as own json object
        study = {}
        study['StudyInstanceUID'] = js['0020000D']['Value'][0]
        if '00080020' in js and 'Value' in js['00080020']:
            study['StudyDate'] = js['00080020']['Value'][0]
        else:
            study['StudyDate'] = None
        if '00080030' in js and 'Value' in js['00080030']:
            study['StudyTime'] = js['00080030']['Value'][0]
        else:
            study['StudyTime'] = None
        if '00081030' in js and 'Value' in js['00081030']:
            study['StudyDescription'] = js['00081030']['Value'][0]
        else:
            study['StudyDescription'] = None

        # extract the table data for series from the meta data and store it as own json object
        series = {}
        series['SeriesInstanceUID'] = js['0020000E']['Value'][0]
        if '00200011' in js and 'Value' in js['00200011']:
            series['SeriesNumber'] = js['00200011']['Value'][0]
        else:
            series['SeriesNumber'] = None
        if '00080021' in js and 'Value' in js['00080021']:
            series['SeriesDate'] = js['00080021']['Value'][0]
        else:
            series['SeriesDate'] = None
        if '00080031' in js and 'Value' in js['00080031']:
            series['SeriesTime'] = js['00080031']['Value'][0]
        else:
            series['SeriesTime'] = None
        if '00180015' in js and 'Value' in js['00180015']:
            series['BodyPartExamined'] = js['00180015']['Value'][0]
        else:
            series['BodyPartExamined'] = None
        if '00080060' in js and 'Value' in js['00080060']:
            series['Modality'] = js['00080060']['Value'][0]
        else:
            series['Modality'] = None
        if '00080070' in js and 'Value' in js['00080070']:
            series['Manufacturer'] = js['00080070']['Value'][0]
        else:
            series['Manufacturer'] = None
        if '00081090' in js and 'Value' in js['00081090']:
            series['ManufacturerModelName'] = js['00081090']['Value'][0]
        else:
            series['ManufacturerModelName'] = None
        if '00185100' in js and 'Value' in js['00185100']:
            series['PatientPosition'] = js['00185100']['Value'][0]
        else:
            series['PatientPosition'] = None
        if '00180060' in js and 'Value' in js['00180060']:
            series['KVP'] = js['00180060']['Value'][0]
        else:
            series['KVP'] = None
        if '00181150' in js and 'Value' in js['00181150']:
            series['ExposureTime'] = js['00181150']['Value'][0]
        else:
            series['ExposureTime'] = None
        if '00200052' in js and 'Value' in js['00200052']:
            series['FrameOfReferenceUID'] = js['00200052']['Value'][0]
        else:
            series['FrameOfReferenceUID'] = None
        if '0008103E' in js and 'Value' in js['0008103E']:
            series['SeriesDescription'] = js['0008103E']['Value'][0]
        else:
            series['SeriesDescription'] = None

        # extract the table data for image from the meta data and store it as own json object
        image = {}
        image['SOPInstanceUID'] = js['00080018']['Value'][0]
        image['SOPClassUID'] = js['00080016']['Value'][0]
        if '00200013' in js and 'Value' in js['00200013']:
            image['InstanceNumber'] = js['00200013']['Value'][0]
        else:
            image['InstanceNumber'] = None
        if '00080008' in js and 'Value' in js['00080008']:
            image['ImageType'] = js['00080008']['Value']
        else:
            image['ImageType'] = None
        if '00080012' in js and 'Value' in js['00080012']:
            image['ImageCreationDate'] = js['00080012']['Value'][0]
        else:
            image['ImageCreationDate'] = None
        if '00080013' in js and 'Value' in js['00080013']:
            image['ImageCreationTime'] = js['00080013']['Value'][0]
        else:
            image['ImageCreationTime'] = None
        if '00120063' in js and 'Value' in js['00120063']:
            image['De-identificationMethod'] = js['00120063']['Value'][0]
        else:
            image['De-identificationMethod'] = None
        image['SamplesPerPixel'] = js['00280002']['Value'][0]
        if '00280004' in js and 'Value' in js['00280004']:
            image['PhotometricInterpretation'] = js['00280004']['Value'][0]
        else:
            image['PhotometricInterpretation'] = None
        if '00280010' in js and 'Value' in js['00280010']:
            image['BitsAllocated'] = js['00280100']['Value'][0]
        else:
            image['BitsAllocated'] = None
        if '00280101' in js and 'Value' in js['00280101']:
            image['BitsStored'] = js['00280101']['Value'][0]
        else:
            image['BitsStored'] = None
        if '00280102' in js and 'Value' in js['00280102']:
            image['HighBit'] = js['00280102']['Value'][0]
        else:
            image['HighBit'] = None
        if '00280103' in js and 'Value' in js['00280103']:
            image['PixelRepresentation'] = js['00280103']['Value'][0]
        else:
            image['PixelRepresentation'] = None
        if '00281050' in js and 'Value' in js['00281050']:
            image['WindowCenter'] = js['00281050']['Value'][0]
        else:
            image['WindowCenter'] = None
        if '00281051' in js and 'Value' in js['00281051']:
            image['WindowWidth'] = js['00281051']['Value'][0]
        else:
            image['WindowWidth'] = None
        if '00281053' in js and 'Value' in js['00281053']:
            image['RescaleSlope'] = js['00281053']['Value'][0]
        else:
            image['RescaleSlope'] = None
        if '00180050' in js and 'Value' in js['00180050']:
            image['SliceThickness'] = js['00180050']['Value'][0]
        else:
            image['SliceThickness'] = None
        if '00201041' in js and 'Value' in js['00201041']:
            image['SliceLocation'] = js['00201041']['Value'][0]
        else:
            image['SliceLocation'] = None

        # now concatenate the patient, study, series and image objects to one whole json object
        meta_data = {}
        meta_data['Patient'] = patient
        meta_data['Patient']['Study'] = study
        meta_data['Patient']['Study']['Series'] = series
        meta_data['Patient']['Study']['Series']['Image'] = image

        # append the current meta data dict to the list of meta data dicts
        header_list.append(meta_data)

    # printing the meta data list to a file as json object
    header = {'header_data': header_list}
    with open('json.txt', 'w') as file:
        json.dump(header, file)
