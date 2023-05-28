from django.contrib import admin
from django.urls import path
# from Controllers import ImageController, PatientController, StudyController, SeriesController, HomeController
from Controllers import HomeController
# image = ImageController.ImageController()
# patient = PatientController.PatientController()
# study = StudyController.StudyController()
# series = SeriesController.SeriesController()
home = HomeController.HomeController()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home.index)
]