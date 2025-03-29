from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def login_view(request):
    #Comprueba si el usuario ha iniciado sesion
    if request.user.is_authenticated:
        return redirect('main')
    else:
        return render(request, 'login.html')
    
@login_required(login_url='/')
def main_view(request):
    #Comprueba si el usuario ha iniciado sesion
    if request.user.is_authenticated:
        return render(request, 'main.html')
    else:
        return redirect('login')
