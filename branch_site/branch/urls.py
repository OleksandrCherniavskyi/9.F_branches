from django.urls import path
from . import views

urlpatterns = [
    #path("",  views.main, name="main"),
    path('', views.search, name='search'),
    #path('person_info.html', views.search_person, name='person_info')
]