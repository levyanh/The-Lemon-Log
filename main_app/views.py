from django.shortcuts import render


# Add home view:
def home(request):
    return render(request, 'home.html')
# Add about view:
def about(request):
    return render(request,'about.html')