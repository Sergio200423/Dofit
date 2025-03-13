from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def signin_view(request):
    return render(request, 'signin.html')

def signup_view(request):
    return render(request, 'signup.html')