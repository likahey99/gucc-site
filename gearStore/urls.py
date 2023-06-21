from django.urls import path
from gearStore import views

app_name = 'gearStore'

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
    path('category/<slug:category_name_slug>/add-gear/', views.add_gear, name='add-gear'),
    path('add-category/', views.add_category, name='add-category'),
    path('edit-category/<slug:category_name_slug>', views.edit_category, name='edit-category'),
    path('category/<slug:category_name_slug>/edit-gear/<slug:gear_name_slug>/', views.edit_gear, name='edit-gear'),
    path('category/<slug:category_name_slug>/delete-gear/<slug:gear_name_slug>/', views.delete_gear, name='delete-gear'),
    path('delete-category/<slug:category_name_slug>', views.delete_category, name='delete-category'),
    path('edit-home/', views.edit_home, name='edit-home'),
    path('edit-about/', views.edit_about, name='edit-about'),
    path('edit-contact', views.edit_contact, name='edit-contact'),
    path('booking/<booking_id>/', views.booking, name='booking'),
    path('user/<user>/', views.user, name='user')
]