import base64
import io
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
        return db.query(Image).filter(Image.imageUID == image_id).first()

    def show_images(self, request, page_id=1):
        if request.user.is_authenticated:
            page_size = 10
            skip = (page_id - 1) * page_size
            mongo_documents = mds.collection.find().skip(skip).limit(page_size)
            objects_count = mds.collection.count_documents({})
            max = math.ceil(objects_count / page_size)
            documents = []
            for doc in mongo_documents:
                image = pydicom.dcmread(doc['file']['filename'])
                documents.append([image.SOPInstanceUID[-10:],image.StudyDate,doc['file']['filename'], image.PatientName])
            return render(request, 'images.html', {"documents": documents, "page_id": page_id, "max":max, "objects_count":objects_count})
        else:
            return redirect('/login')

    def show_image(self, request, image_id):
        if request.user.is_authenticated:
            docs = mds.collection.find()
            for i in docs:
                if str(image_id) in i['file']['filename']:
                    ds = pydicom.dcmread(i['file']['filename'])
                    name = ds.PatientName
                    mod = ds.Modality
                    id = ds.SeriesInstanceUID[-10:]
                    date = ds.SeriesDate
                    sex = ds.PatientSex
                    filename = i['file']['filename']
                    pixel_array = ds.pixel_array
                    png_image_stream = BytesIO()
                    plt.imsave(png_image_stream, pixel_array, format='png')
                    png_image_stream.seek(0)
                    encoded_png = base64.b64encode(png_image_stream.getvalue()).decode('utf-8')
        else:
            return redirect('/login')
        return render(request, 'image.html', {"name":name, "sex": sex, "mod":mod, "id":id, "date":date, "image":encoded_png, "filename":filename})

