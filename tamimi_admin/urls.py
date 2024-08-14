from django.urls import path
from tamimi_admin import views
from django.conf.urls.static import static
from django.conf import settings
from .views import UpdateFCMTokenView

urlpatterns = [
    # home page
    path('home/', views.home_view, name='homepage'),
    path('', views.home_view, name='home_page'),

    # Device List and create
    path('devicesorder/', views.device_order_view, name='devices_order'),

    # Section List and create
    path('sectionsorder/', views.section_order_view, name='sections_order'),

    # Device List and create
    path('devices/', views.all_devices_view, name='show_all_devices'),

    # Section List and create
    path('sections/', views.all_sections_view, name='show_all_sections'),

    # Parent Section List and create
    path('parentsections/', views.all_parent_sections_view, name='show_all_parent_sections'),

    # Section list of parent
    path('childsections/<pk>', views.child_section_view, name='child_page'),

    # Push notification
    path('pushnotification/', views.pushnotification_view, name='push_notification_page'),

    # User sign in/ sign up
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    # apis
    path('mdevice/', views.getDeviceData),
    path('msection/', views.getSectionData),
    path('mparent/', views.getParentData),
    path('mdorder/', views.getDeviceOrderData),
    path('msorder/', views.getSectionOrderData),
    path('update-fcm-token/', UpdateFCMTokenView.as_view(), name='update_fcm_token'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

