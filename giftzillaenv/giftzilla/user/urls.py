from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [

        path("createRegistry", views.createRegistry, name="createRegistry")
]