from pydicom import dcmread
import json
import project.Core.MongoDatabase as mdb


def insert_into_mongodb():
    # establish a connection the the mongodb
    mongoclient = mdb.mongoclient

    print(mongoclient.list_database_names())

    # select the right database
    db = mongoclient['dicom']

    # select the right collection
    collection = db['dicom_header']

    for i in range(0, 50):
        if i < 10:
            # formatting the right dicom file name // --> needs to be changed
            file_string = 'dicoms/{}_00000{}.dcm'.format(i, i)
            ds = dcmread(file_string).to_json()
            # the object still needs to be converted to json, because it is still a string
            json_obj = json.loads(ds)
            # write the json object into the collection
            collection.insert_one(json_obj)
        else:
            # --> needs to be changes to the right dicom file path
            file_string = 'dicoms/{}_0000{}.dcm'.format(i, i)
            ds = dcmread(file_string).to_json()
            json_obj = json.loads(ds)
            collection.insert_one(json_obj)

