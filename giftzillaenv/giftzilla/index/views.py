from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "index/index.html")

def custom_404_view(request,exception):
    return render(request, 'index/404.html', status=404)

def custom_500_view(request,exception):
    return render(request, 'index/404.html', status=500)
#create logic for randomized gift reg distrobution
    #should include email notification