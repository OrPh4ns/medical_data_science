import Core.MongoDatabase as Mdb


def get_document(doc_id):
    """
    finds a document by its id and returns it without the pixel data if it was found
    """
    doc = Mdb.collection.find_one({'00080018.Value': doc_id}, {'7FE00010': 0})
    return doc


def get_all_documents_without_pixel_data():
    """
    gets all documents stored in the mongodb and returns them without the pixel data
    """
    docs = Mdb.collection.find({}, {'7FE00010': 0})
    return docs


def get_document_metadata(doc_id):
    """
    gets a document by its id and returns it with some of its metadata
    the returned metadata contains information about the following fields:
    PatientID, Patient Sex, ID Removed Boolean, StudyID, Study Date, SeriesID and Series Date
    """
    doc = Mdb.collection.find_one({'00080018.Value': doc_id}, {'0010020': 1, '0010040': 1, '00120062': 1, '0020000D': 1,
                                                               '00080020': 1, '0020000E': 1, '00080021': 1})
    return doc


def get_document_with_pixel_data(doc_id):
    """
    gets a document by its id and returns its pixel data array for showing its associated dicom image
    """
    doc = Mdb.collection.find_one({'00080018.Value': doc_id}, {'7FE00010': 1})
    return doc
