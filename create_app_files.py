import os

files = {
    r'd:/Django/myvenv/A/User/views.py': '''from django.shortcuts import render

def home(request):
    return render(request, 'User/home.html')

def login_view(request):
    return render(request, 'User/login.html')

def registration(request):
    return render(request, 'User/registration.html')
''',
    r'd:/Django/myvenv/A/User/urls.py': '''from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration, name='registration'),
]
''',
    r'd:/Django/myvenv/A/User/templates/User/home.html': '''<!DOCTYPE html>
<html>
<head><title>Home</title></head>
<body>
    <h1>Home Page</h1>
</body>
</html>''',
    r'd:/Django/myvenv/A/User/templates/User/login.html': '''<!DOCTYPE html>
<html>
<head><title>Login</title></head>
<body>
    <h1>Login Page</h1>
</body>
</html>''',
    r'd:/Django/myvenv/A/User/templates/User/registration.html': '''<!DOCTYPE html>
<html>
<head><title>Registration</title></head>
<body>
    <h1>Registration Page</h1>
</body>
</html>'''
}

for path, content in files.items():
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        print(f'Created {path}')
    except Exception as e:
        print(f'Error creating {path}: {e}')
