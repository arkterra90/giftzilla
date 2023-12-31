from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'register'

urlpatterns = [

    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:userID>/profileView", views.profileView, name="profileView")

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)