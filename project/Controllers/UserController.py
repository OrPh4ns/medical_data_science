from django.shortcuts import render, redirect
import Core.Controller
from django.contrib.auth import login, authenticate, logout


class UserController(Core.Controller.Controller):
    def login(self,request):
        if request.method == 'POST':
            # Retrieve the username and password from the POST request
            username = request.POST['username']
            password = request.POST['password']
            # Authenticate the user using the provided credentials
            user = authenticate(username=username, password=password)
            # Check if the user is authenticated
            if user is not None:
                # Log in the user
                login(request, user)
                # Redirect to the home page
                return redirect('/')
            # Otherwise render the login.html template with an error message
            else:
                return render(request, 'login.html', {'error': 'Bitte prüfen Sie Ihre Daten nochmal'})
        # Render the login.html template for GET requests
        else:
            return render(request, 'login.html')
    
    
    
    def logout(self,request):
        # Log out the user
        logout(request)
        # Redirect to the login page
        return redirect('/login')
