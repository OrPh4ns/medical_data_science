from django.shortcuts import render

import Core.Controller


class HomeController(Core.Controller.Controller):

    def index(self, request):
        return render(request, 'home.html', {"data": "change later"})