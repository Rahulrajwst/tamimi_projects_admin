from django.urls import path
from admin_app import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/', views.home_page, name='homepage'),
    path('', views.home_page),
    path('new/', views.create_page,name='create_new'),
    path('homedata/', views.getData)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)