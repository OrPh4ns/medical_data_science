from django.shortcuts import render, redirect
import Core.Controller
from django.contrib.auth import login, authenticate, logout


class UserController(Core.Controller.Controller):
    def login(self,request):
        """
        Handles the login functionality.

       If the request method is POST, it attempts to authenticate the user with the provided username and password.
       If authentication is successful, the user is logged in and redirected to the homepage.
       If authentication fails, the login page is rendered again with an error message.

       If the request method is GET, it renders the login page.

        Args:
        self: The instance of the UserController class.
        request: The HTTP request object.

        Returns:
        If the request method is POST and authentication is successful, redirects to the homepage.
        If the request method is POST and authentication fails, renders the login page with an error message.
        If the request method is GET, renders the login page.
        """
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                return render(request, 'login.html', {'error': 'Bitte prüfen Sie Ihre Daten nochmal'})
        else:
            return render(request, 'login.html')
    
    
    
    def logout(self,request):
        """
        Handles the logout functionality.

        Logs out the currently authenticated user and redirects to the login page.

        Args:
        self: The instance of the UserController class.
        request: The HTTP request object.

        Returns:
        Redirects to the login page.
        """
        logout(request)
        return redirect('/login')
