from os import name
from django.urls import path
from donor import views

urlpatterns = [
    path('', views.home , name="home"),
    path('blog', views.blog , name="blog"),
    path('about', views.about , name="about"),
    path('contact', views.contact , name="contact"),
    path('donor', views.donor , name="donor"),
    path('deletednr/<int:id>/', views.delete_dnr, name = "deletednr"),
    path('updataednr/<int:id>/', views.update_dnr, name = "updatednr"),
    path('bloodreq', views.bloodreq , name="bloodreq"),
    path('deletebreq/<int:id>/', views.delete_breq, name = "deletebreq"),
    path('updataebreq/<int:id>/', views.update_breq, name = "updatebreq"),
    path('stock', views.stock , name="stock"),
    path('deletestk/<int:id>/', views.delete_stk, name = "deletestk"),
    path('updataestk/<int:id>/', views.update_stk, name = "updatestk"),
    path('terms', views.terms , name="terms"),
    path('eligible', views.eligible , name="eligible"),
    path('login', views.login , name = "login" ),
    path('logout', views.logout , name = "logout" ),
    path('register', views.register, name = "register" ),
]
