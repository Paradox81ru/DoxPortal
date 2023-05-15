from django.urls import path
from knox import views as knox_views
from accounts.views import *

app_name = "accounts"
urlpatterns = [
    path('login', LoginView.as_view(), name='knox_login'),
    path('logout', knox_views.LogoutView.as_view(), name='knox_logout'),
    path('logoutall', knox_views.LogoutAllView.as_view(), name='knox_logoutall'),

    path('signup', Signup.as_view()),
    path('confirm-account', ConfirmAccount.as_view(), name='confirm-account'),
    # path('repeated-confirm-account', RepeatedConfirmAccount.as_view(), name='repeated-confirm-account'),
    # path('request-password-reset', RequestPasswordReset.as_view(), name='request-password-reset'),
    # path('confirm-reset-password/<str:token>', confirm_reset_password, name='confirm-reset-password'),
    path("get-all-users", GetAllUsers.as_view()),
    path('get-admin', GetAdmin.as_view()),
    path('get-user', GetUser.as_view())
]
