from django.shortcuts import render, redirect
import Core.Controller
from django.contrib.auth import login, authenticate, logout


class UserController(Core.Controller.Controller):
    def login(self,request):
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
        logout(request)
        return redirect('/login')
