from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from myapp import views

app_name = 'myapp'

urlpatterns = [path(r'', views.index, name='index'),
               path(r'about', views.about, name='about'),
               path(r'<int:topic_id>', views.detail, name='detail'),
               path(r'findcourses', views.findcourses, name='findcourses'),
               path(r'place_order', views.place_order, name='place_order'),
               path(r'review', views.review, name='review'),
               path(r'login', views.user_login, name='user_login'),
               path(r'logout', views.user_logout, name='user_logout'),
               path(r'myaccount', views.myaccount, name='myaccount'),
               path(r'myorders', views.myorders, name='myorders'),
               path(r'register', views.register, name='register'),
               ]

