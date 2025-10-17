from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import CustomUser


def loginPage(request):
    if request.method == "POST":
        identifier = request.POST.get("username")
        password = request.POST.get("password")

        if not identifier or not password:
            messages.error(request, "All fields are required.")
        else:
            user = None

            # Check phone
            try:
                user_obj = CustomUser.objects.get(phone_number=identifier)
                user = authenticate(request, username=user_obj.username, password=password)
            except CustomUser.DoesNotExist:
                # Check email
                try:
                    user_obj = CustomUser.objects.get(email=identifier)
                    user = authenticate(request, username=user_obj.username, password=password)
                except CustomUser.DoesNotExist:
                    # Finally fallback to username
                    user = authenticate(request, username=identifier, password=password)

            if user:
                login(request, user)
                messages.success(request, "Congratulations! You’ve successfully logged in.")
                return redirect('login')  
            else:
                messages.error(request, "Invalid credentials.")

    return render(request, "login.html")

# def loginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         if not username or not password:
#             messages.error(request, "All fields are required.")
#         else:
#             # Try username, email, or phone login
#             user = None
#             try:
#                 # Check if input is phone
#                 user_obj = CustomUser.objects.get(phone_number=username)
#                 user = authenticate(request, username=user_obj.username, password=password)
#             except CustomUser.DoesNotExist:
#                 # Fallback to username/email
#                 user = authenticate(request, username=username, password=password)

#             if user:
#                 login(request, user)
#                 messages.success(request, "🎉 Congratulations! You’ve successfully logged in.")
#                 return redirect('loginPage')  # or dashboard
#             else:
#                 messages.error(request, "Invalid credentials.")

#     return render(request, 'login.html')


from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

def signupPage(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not all([full_name, email, phone, password1, password2]):
            messages.error(request, "All fields are required.")
        elif password1 != password2:
            messages.error(request, "Passwords do not match.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
        else:
            username = email.split('@')[0]
            user = User.objects.create(
                username=username,
                email=email,
                phone_number=phone,
                password=make_password(password1),
                first_name=full_name.split(' ')[0],
                last_name=' '.join(full_name.split(' ')[1:]),
            )
            messages.success(request, "🎉 Congratulations! Your account has been created.")
            return redirect('loginPage')

    return render(request, 'sign-up.html')
