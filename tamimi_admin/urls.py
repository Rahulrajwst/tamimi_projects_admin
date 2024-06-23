from django.urls import path
from tamimi_admin import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/', views.home_view, name='homepage'),
    path('', views.home_view, name='home_page'),
    path('devices/', views.all_devices_view, name='show_all_devices'),
    path('sections/', views.all_sections_view, name='show_all_sections'),
    path('parentsections/', views.all_parent_sections_view, name='show_all_parent_sections'),
    path('childsections/<pk>', views.child_section_view, name='child_page'),
    path('mdevice/', views.getDeviceData),
    path('msection/', views.getSectionData),
    path('mparent/', views.getParentData),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns = [
#     path('home/', views.home_view, name='homepage'),
#     path('', views.home_view, name='home_page'),
#     path('categories/', views.all_categories_view, name='show_all_category'),
#     path('edit/<pk>', views.edit_view, name='edit_page'),
#     path('sections/', views.all_sections_view, name='show_all_section'),
#     path('createcategory/', views.create_category_view, name='create_category'),
#     path('createsection/', views.create_section_view, name='create_section'),
#     path('device/', views.getDeviceData)
# ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)