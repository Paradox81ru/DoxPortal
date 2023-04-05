from django.urls import path
from .views import *

app_name = "common"
urlpatterns = [
    path("begin-data", get_begin_data),
    path("get-login-form-data", get_login_form_data)
]