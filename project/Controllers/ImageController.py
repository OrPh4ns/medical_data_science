import base64
import math
from io import BytesIO
from PIL import Image
import matplotlib.pyplot as plt
import pydicom
from django.shortcuts import render, redirect

from Core import Controller
from Core import MSDatabase as ms
from Core import MongoDatabase as mds
from Models.Image import Image


class ImageController(Controller.Controller):
    
    def get_image(self, db: ms.Session, image_id: int):
        """
        Retrieves an image from the database based on the provided image_id.

        Args:

        self: The instance of the ImageController class.
        db: The database session object.
        image_id: The ID of the image to retrieve.

        Returns:

        The first Image object from the database where the imageUID matches the provided image_id.
        """
        return db.query(Image).filter(Image.imageUID == image_id).first()

    def show_images(self, request, page_id=1):
        """
        Renders the 'images.html' template with a paginated list of images.

        Args:

        self: The instance of the ImageController class.
        request: An HttpRequest object representing the client's request.
        page_id: The ID of the page to display (default is 1).

        Returns:

        If the user is authenticated, renders the 'images.html' template with a paginated list of images
        and related information.
        If the user is not authenticated, redirects the user to the login page.
        """
        if request.user.is_authenticated:
            page_size = 10
            skip = (page_id - 1) * page_size
            mongo_documents = mds.collection.find().skip(skip).limit(page_size)
            objects_count = mds.collection.count_documents({})
            max = math.ceil(objects_count / page_size)
            documents = []
            for doc in mongo_documents:
                sop = doc['0020000E']['Value'][0][-10:]
                study_date = doc['00080020']['Value'][0]
                name = doc['00100010']['Value'][0]['Alphabetic']
                documents.append([sop,study_date,doc['file']['filename'], name])
            return render(request, 'images.html', {"documents": documents, "page_id": page_id, "max":max, "objects_count":objects_count})
        else:
            return redirect('/login')

    def show_image(self, request, image_id):
        """
        Renders the 'image.html' template with detailed information about a specific image.

        Args:
        self: The instance of the ImageController class.
        request: An HttpRequest object representing the client's request.
        image_id: The ID of the image to display.

        Returns:
        If the user is authenticated, renders the 'image.html' template with detailed information
        about the specified image.
        If the user is not authenticated, redirects the user to the login page.
        """
        if request.user.is_authenticated:
            docs = mds.collection.find()
            for i in docs:
                if str(image_id) in i['file']['filename']:
                    ds = pydicom.dcmread(i['file']['filename'])
                    srNumber = ds.SeriesNumber
                    mod = ds.Modality
                    id = ds.SeriesInstanceUID[-10:]
                    date = ds.SeriesDate
                    sex = ds.PatientSex
                    gb= ds.PatientBirthDate
                    filename = i['file']['filename']
                    pixel_array = ds.pixel_array
                    png_image_stream = BytesIO()
                    plt.imsave(png_image_stream, pixel_array, format='png')
                    png_image_stream.seek(0)
                    encoded_png = base64.b64encode(png_image_stream.getvalue()).decode('utf-8')
        else:
            return redirect('/login')
        return render(request, 'image.html', {"srNumber":srNumber, "sex": sex, "birthdate":gb, "mod":mod, "id":id, "date":date, "image":encoded_png, "filename":filename})

    def search_images(self, request):
        """
        Handles the search functionality for images.

        Args:
        self: The instance of the ImageController class.
        request: An HttpRequest object representing the client's request.

        Returns:
        If the user is authenticated and the request method is POST, renders the 'search.html' template
        with the search results based on the provided search criteria.
        If the user is authenticated and the request method is not POST, renders the 'search.html' template
        to display the search form.
        If the user is not authenticated, redirects the user to the login page.
        """
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
                return render(request, 'search.html', {"documents": documents})
            else:
                return render(request, 'search.html')
        else:
            return redirect('/login')
