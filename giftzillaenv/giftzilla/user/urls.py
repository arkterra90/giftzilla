from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [

        path("createRegistry", views.createRegistry, name="createRegistry"),
        path("<int:userID>/regJoin", views.regJoin, name="regJoin"),
        path("<int:userID>/viewreg", views.viewReg, name="viewReg"),
        path("<str:groupPin>/adminReg", views.adminReg, name="adminReg"),
        path("<str:groupPin>/<int:userID>/userGifts", views.userGifts, name="userGifts")
]