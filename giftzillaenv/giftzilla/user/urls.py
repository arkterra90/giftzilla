from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [

        path("createRegistry", views.createRegistry, name="createRegistry"),
        path("<int:userID>/regJoin", views.regJoin, name="regJoin"),
        path("<int:userID>/viewreg", views.viewReg, name="viewReg"),
        path("<str:groupPin>/adminReg", views.adminReg, name="adminReg"),
        path("<str:groupPin>/<int:userID>/userGifts", views.userGifts, name="userGifts"),
        path("<str:groupPin>/<int:userID>/viewWishList", views.viewWishList, name="viewWishList"),
        path("<str:groupPin>/<int:userID>/adminWishListView", views.adminWishListView, name="adminWishListView"),
        path("<str:groupPin>/regPair", views.regPair, name="regPair"),
        path("<str:groupPin>/regDelete", views.regDelete, name="regDelete"),
        path("<str:wishID>/wishEdit", views.wishEdit, name="wishEdit"),
        path("<str:groupPin>/<int:userID>/userRegDelete", views.userRegDelete, name="userRegDelete"),
        path("<str:groupPin>/createPairs", views.createPairs, name="createPairs"),
        path("<str:groupPin>/noPairs", views.noPairs, name="noPairs")






]