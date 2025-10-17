from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.db.models import Q 


CustomUser = get_user_model()


def loginPage(request):
    if request.method == 'POST':
        identifier = request.POST.get('username') 
        password = request.POST.get('password')

        if not identifier or not password:
            messages.error(request, "All fields are required.")
            return render(request, 'login.html') 

       
        try:
            user_obj = CustomUser.objects.get(
                Q(username=identifier) |
                Q(email=identifier) |
                Q(phone_number=identifier)
            )
            
            
            django_username = user_obj.username 
            
            
            user = authenticate(request, username=django_username, password=password)

        except CustomUser.DoesNotExist:
            user = None
        except Exception:
            user = None
        
        if user:
            login(request, user)
            messages.success(request, "Congratulations! You’ve successfully logged in.")
            return redirect('loginPage') 
        else:

            messages.error(request, "Invalid credentials (user not found or bad password).") 

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