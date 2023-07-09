from django.shortcuts import render, redirect
from Core import MongoDatabase as mdb
import Core.Controller


class HomeController(Core.Controller.Controller):

    def index(self, request):
        """
        Renders the home page with relevant information based on the user's authentication status.

        Args:

        self: The instance of the view class.
        request: An HttpRequest object representing the client's request.

        Returns:
        
        If the user is authenticated, renders the 'home.html' template with the count of documents
        in the 'mdb.collection' and server information.
        If the user is not authenticated, redirects the user to the login page.
        """
        if request.user.is_authenticated:
            documents_count = mdb.collection.count_documents({})
            import platform
            server = {
                "System": platform.system(),
                "NodeName": platform.node(),
                "Release": platform.release(),
                "Version": platform.version(),
                "Machine": platform.machine(),
                "Processor": platform.processor()
            }
            return render(request, 'home.html', {"documents_count": documents_count, "server":server})
        else:
            return redirect('/login')