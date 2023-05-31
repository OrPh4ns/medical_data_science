from django.shortcuts import render

import project.Core.Controller


class HomeController(project.Core.Controller.Controller):

    def index(self, request):
        return render(request, 'home.html', {"data": "change later"})