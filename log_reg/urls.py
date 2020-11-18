from django.urls import path
from . import views

urlpatterns=[
    path('', views.index),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('quotes', views.all_quotes),
    path('add', views.add_quote),
    path('user/<int:poster_id>', views.user_page),
    path('myaccount/<int:user_id>', views.edit_user),
    path('<int:quote_id>/like', views.like),
    path('<int:quote_id>/unlike', views.unlike),
    path('<int:quote_id>/edit_quote', views.edit_quote),
    path('<int:quote_id>/delete_quote', views.delete_quote)
]