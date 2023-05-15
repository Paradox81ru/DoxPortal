from django.urls import path
from my_admin.views import *


app_name = "my_admin"
urlpatterns = [
    path('begin-data', begin_data, name='begin-data'),
]