from django.urls import path
from query_app import views


urlpatterns = [
    path('index/', views.index, name="index"),
    path('login/', views.login_page, name="login"),
    path('about/', views.about, name="about"),
    path('service/', views.service, name="service"),
    path('contact/', views.contact, name="contact"),
    path('signup/' , views.signup, name="signup"),
    path('Results/', views.Results, name="Results"),

]

