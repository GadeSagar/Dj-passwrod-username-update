from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Account
from django.contrib.auth.hashers import make_password



def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        mobile_number = request.POST.get('mobile_number')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        country = request.POST.get('country')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')

        # Check if username or email already exists
        if Account.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
        elif Account.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
        else:
            user = Account.objects.create(
                username=username,
                password=make_password(password),  # Hash the password manually
                email=email,
                mobile_number=mobile_number,
                age=age,
                gender=gender,
                city=city,
                country=country,
                birth_date=birth_date,
                address=address
            )
            messages.success(request, "Account created successfully!")
            return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password!")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


def home_view(request):
    return render(request, 'home.html')


from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import get_user_model


def update_profile_view(request):
    user = request.user

    if request.method == 'POST':
        # Update Username
        new_username = request.POST.get('username')
        if new_username and new_username != user.username:
            if get_user_model().objects.filter(username=new_username).exists():
                messages.error(request, "Username already exists!")
            else:
                user.username = new_username

        # Update Password
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 and password1 != password2:
            messages.error(request, "Passwords do not match!")
        elif password1:
            user.set_password(password1)  # Hashes the password
            update_session_auth_hash(request, user)  # Keeps the user logged in after password change

        # Save the user
        user.save()
        messages.success(request, "Profile updated successfully!")
        return redirect('home')

    return render(request, 'update_profile.html')
