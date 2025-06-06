from django.urls import path, include
from . import views

app_name='library'
urlpatterns = [
    path('', views.generate_xml, name='generate_xml'),
    path('view_xml/', views.view_xml, name="view_xml"),
    path('recent_book/', views.recent_book, name="recent_book"),
    path('add_book/', views.add_book, name="add_book"),
    path('edit_book/', views.edit_book, name="edit_book"),
]