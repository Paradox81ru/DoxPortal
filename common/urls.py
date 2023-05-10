from django.urls import path
from .views import *

app_name = "common"
urlpatterns = [
    path("begin-data", get_begin_data),
    path("get-login-form-data", get_login_form_data),
    path("get-contact-form-data", get_contact_form_data),
    path("get-register-form-data", get_register_form_data),
    path("get-about-page", AboutPageView.as_view()),
    path('contact', ContactView.as_view())
]