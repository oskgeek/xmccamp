from django.shortcuts import render, redirect
from django.contrib.auth import authenticate


def login(request):
    
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # the password verified for the user
            if user.is_active:
                
                return redirect('home/')
                
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
    
    return render(request, 'controller/login.html')


def dashboard(request):
    return render(request, 'controller/index.html')


