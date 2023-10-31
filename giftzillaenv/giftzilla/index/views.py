from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, "index/index.html")

#create logic for randomized gift reg distrobution
    #should include email notification