from django.urls import path
from . import views
app_name ='app_book'
urlpatterns = [
    path('lasya/',views.display_page),
     
    path('exam/',views.exam, name='exam')
   
    ]