from django.urls import path
from knox import views as knox_views
from accounts.views import *

app_name = "accounts"
urlpatterns = [
    path('login', LoginView.as_view(), name='knox_login'),
    path('logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),

    path("get-all-users", GetAllUsers.as_view()),
    path('get-admin', GetAdmin.as_view()),
    path('get-user', GetUser.as_view())
]
