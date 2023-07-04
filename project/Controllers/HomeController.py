from django.shortcuts import render, redirect
from Core import MongoDatabase as mdb
import Core.Controller
import datetime
from django.contrib.auth import login, authenticate, logout


class HomeController(Core.Controller.Controller):

    def index(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            documents_count = mdb.collection.count_documents({})
            import platform
            # Retrieve system information
            server = {
                "System": platform.system(),
                "NodeName": platform.node(),
                "Release": platform.release(),
                "Version": platform.version(),
                "Machine": platform.machine(),
                "Processor": platform.processor()
            }
            # Render the home.html template with the documents count and values
            return render(request, 'home.html', {"documents_count": documents_count, "server":server})
        else:
            # Redirect the user to the login page if not authenticated
            return redirect('/login')