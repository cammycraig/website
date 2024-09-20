from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from gearstore_app import views

app_name = 'gearstore_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('borrow-gear/', views.category_menu, name='find-gear'),
    path('gear/<gear_name_slug>', views.view_gear, name='view-gear'),
    path('category/<category_name_slug>', views.view_category, name='view-category'),
    path('account/', views.account, name='account'),
    path('logout/', views.process_logout, name='logout'),
    path('admin-error/', views.admin_error, name='admin-error'),
    path('booking/<booking_id>/', views.booking, name='booking'),
    path('user/<user>/', views.user, name='user')
]
#
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
