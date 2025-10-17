from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.db.models import Q 


CustomUser = get_user_model()

from django.contrib.auth import authenticate, login
from django.contrib import messages
from MARTHA.models import CustomUser  

def loginPage(request):
    if request.method == 'POST':
        identifier = request.POST.get('username')
        password = request.POST.get('password')

        if not identifier or not password:
            messages.error(request, "All fields are required.")
        else:
            user = authenticate(request, username=identifier, password=password)
            if user:
                login(request, user)
                messages.success(request, "Successfully logged in.")
                return redirect('dashboard') 
            else:
                messages.error(request, "Invalid credentials.")

    return render(request, 'login.html')



def signupPage(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([full_name, email, phone, password, confirm_password]):
            messages.error(request, "All fields are required.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match.")
        elif CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        elif CustomUser.objects.filter(phone_number=phone).exists():
            messages.error(request, "Phone number already exists.")
        else:
            username = email.split('@')[0] 
            
            
            CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone_number=phone,
                full_name=full_name 
            )
            
            messages.success(request, "Congratulations! Your account has been created. Please log in.")
            return redirect('loginPage')

    return render(request, 'sign-up.html')