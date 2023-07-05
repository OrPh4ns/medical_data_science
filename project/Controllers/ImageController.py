import base64
import io
import json
import math
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import pydicom
from bson import json_util
from django.shortcuts import render, redirect

from Core import Controller
from Core import MSDatabase as ms
from Core import MongoDatabase as mds
from Models.Image import Image


class ImageController(Controller.Controller):
    def get_image(self, db: ms.Session, image_id: int):
        return db.query(Image).filter(Image.imageUID == image_id).first()

    # This method is used to show a paginated list of images
    def show_images(self, request, page_id=1):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Set the number of images per page
            page_size = 10
            # Calculate the number of images to skip based on the page_id
            skip = (page_id - 1) * page_size
            # Retrieve a subset of documents from the collection
            mongo_documents = mds.collection.find().skip(skip).limit(page_size)
            # Count the total number of documents in the collection
            objects_count = mds.collection.count_documents({})
            # Calculate the maximum number of pages
            max = math.ceil(objects_count / page_size)
            # Create an empty list to store image details
            documents = []
            # Iterate through each document
            for doc in mongo_documents:
                # Read the DICOM image file
                # Extract relevant information from the image
                sop = doc['0020000E']['Value'][0][-10:]
                study_date = doc['00080020']['Value'][0]
                name = doc['00100010']['Value'][0]['Alphabetic']
                documents.append([sop,study_date,doc['file']['filename'], name])
            # Render the images.html template with the retrieved documents and pagination details
            return render(request, 'images.html', {"documents": documents, "page_id": page_id, "max":max, "objects_count":objects_count})
        # Redirect the user to the login page if not authenticated
        else:
            return redirect('/login')

    # This method is used to show a single image
    def show_image(self, request, image_id):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Retrieve all documents from the collection
            docs = mds.collection.find()
            # Iterate through each document
            for i in docs:
                # Check whether the image_id is present in the filename
                if str(image_id) in i['file']['filename']:
                    # Read the DICOM image file
                    ds = pydicom.dcmread(i['file']['filename'])
                    # Extract relevant information from the image
                    srNumber = ds.SeriesNumber
                    mod = ds.Modality
                    id = ds.SeriesInstanceUID[-10:]
                    date = ds.SeriesDate
                    sex = ds.PatientSex
                    gb= ds.PatientBirthDate
                    filename = i['file']['filename']
                    pixel_array = ds.pixel_array
                    # Convert the pixel array to a PNG image
                    png_image_stream = BytesIO()
                    plt.imsave(png_image_stream, pixel_array, format='png')
                    png_image_stream.seek(0)
                    # Encode the PNG image to base64 format
                    encoded_png = base64.b64encode(png_image_stream.getvalue()).decode('utf-8')
        # Redirect user to the login page if not authenticated
        else:
            return redirect('/login')
        # Render the image.html template with the extracted image details
        return render(request, 'image.html', {"srNumber":srNumber, "sex": sex, "birthdate":gb, "mod":mod, "id":id, "date":date, "image":encoded_png, "filename":filename})



    def search_images(self, request):
        if request.user.is_authenticated:
            if request.method == 'POST':
                req_type = request.POST['req_type']
                search = request.POST['search']
                query = {""+req_type+"": ""+search+""}
                results = mds.collection.find(query).limit(30)
                documents = []
                for i in results:
                    patient_id = i['00100020']['Value'][0]
                    name = i['00100010']['Value'][0]['Alphabetic']
                    sex = i['00100040']['Value'][0]
                    study_date = i['00080020']['Value'][0]
                    study_nr = i['00080050']['Value'][0]
                    series_date = i['00080021']['Value'][0]
                    modality = i['00080060']['Value'][0]
                    filename = i['file']['filename']
                    doc = [patient_id, name, sex, study_date, study_nr, series_date, modality, filename]
                    documents.append(doc)
                # Render the images.html template with the retrieved documents and pagination details
                return render(request, 'search.html', {"documents": documents})
            else:
                return render(request, 'search.html')
        else:
            return redirect('/login')
