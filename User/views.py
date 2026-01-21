from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Ensure home is protected if used, but we are redirecting to landing now
@login_required(login_url='login')
def home(request):
    return render(request, 'User/home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                # Redirect to 'landing' (Main Hotel Page) instead of 'home' (User Portal)
                return redirect('landing')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'User/login.html', {'form': form})

def registration(request):
    form = UserCreationForm()
    return render(request, 'User/registration.html', {'form': form})

def doRegistration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
          
            user.is_staff = False
            user.is_superuser = False
            user.save()
            
            login(request, user)
            messages.success(request, "Registration successful.")
        
            return redirect('landing')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            return render(request, 'User/registration.html', {'form': form})
    else:
        return redirect('registration')

def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('login')

def contact(request):
    return render(request, 'User/contact.html')

