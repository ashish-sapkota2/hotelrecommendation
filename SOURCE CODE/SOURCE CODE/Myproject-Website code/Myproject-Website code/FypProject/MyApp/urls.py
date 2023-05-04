from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login_try, name='login_try'),
    path('types', views.types, name='types'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('allhotels/(<id>)/', views.hotel_types, name='hotel_types'),
    path('info/(<id>)/', views.hotel_info, name='hotel_info'),
    path('searchresults/', views.search, name='search'),
    path('(<id>)/favourite/', views.favourite, name='favourite'),
    path('favourites/', views.favourite_list, name='favourites'),
    path('token/', views.token_send, name= 'token_send'),
    path('success/', views.success, name= 'success'),
    path('verify/<auth_token>', views.verify, name= 'verify'),
    path('error/', views.error_page, name= 'error'),
]