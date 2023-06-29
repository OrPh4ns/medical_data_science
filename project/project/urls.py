from django.contrib import admin
from django.urls import path
# from Controllers import , PatientController, StudyController, SeriesController, HomeController
from Controllers import HomeController, UserController,ImageController

image = ImageController.ImageController()
# patient = PatientController.PatientController()
# study = StudyController.StudyController()
# series = SeriesController.SeriesController()
home = HomeController.HomeController()
user = UserController.UserController()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.index),
    path('login', user.login),
    path('logout', user.logout),
    path('images', image.show_images),
    path('images/<int:page_id>/', image.show_images),
    path('image/<int:image_id>/', image.show_image)
]