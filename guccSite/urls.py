from django.urls import path
from guccSite import views

app_name = 'guccSite'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery, name='gallery'),
    path('borrow-gear/', views.category_menu, name='find-gear'),
    path('gear/<gear_name_slug>', views.view_gear, name='view-gear'),
    path('category/<category_name_slug>', views.view_category, name='view-category'),
    path('account/', views.account, name='account'),
    path('logout/', views.process_logout, name='logout'),
    path('admin-error/', views.admin_error, name='admin-error'),
    path('booking/<booking_id>/', views.booking, name='booking'),
    path('user/<user>/', views.user, name='user')
]