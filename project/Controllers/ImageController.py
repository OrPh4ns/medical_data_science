from django.shortcuts import render
from Core import Controller
from Core import MSDatabase as ms
from Models.Image import Image


class ImageController(Controller.Controller):
    def get_image(self, db: ms.Session, image_id: int):
        return db.query(Image.Image).filter(Image.Image.imageUID == image_id).first()

    def index(self, request):
            pass
            # return render(request, 'home.html', {"patient": "xxxxxxx"})