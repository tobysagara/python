from django.urls import path     
from . import views

urlpatterns = [
     path('', views.index),
     path('register', views.register),
     path('login', views.login),
     path('wishes', views.wishes),
     path('logout', views.logout),
     path('wishes/new', views.new_wish),
     path('create_wish', views.create_wish),
     path('wishes/edit/<int:id>', views.edit),
     path('wishes/update/<int:id>', views.update),
     path('delete/<int:id>', views.delete),
     path('wishes/granted/<int:id>', views.granted),
]