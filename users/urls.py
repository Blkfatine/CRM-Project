# users/urls.py
from django.urls import path
from .views import (login_view, signup_view, custom_logout, admin_dashboard,
                    LeadActionsView, AppointmentsListView, announcements_list,
                    create_announcement, edit_announcement, delete_announcement)
from users import views
from .views import user_management, change_user_password, edit_user

urlpatterns = [
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', custom_logout, name='logout'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('gestion-utilisateurs/', views.user_management, name='user_management'),
    path('modifier-utilisateur/<int:user_id>/', views.edit_user, name='edit_user'),
    path('changer-mot-de-passe/<int:user_id>/', views.change_user_password, name='change_user_password'),
    path('supprimer-utilisateur/<int:user_id>/', views.delete_user, name='delete_user'),  # Assurez-vous que ce chemin est bien défini

    path('appointments/', AppointmentsListView.as_view(), name='appointments_list'),
    path('announcements/', views.announcements_list, name='announcements_list'),
    path('announcements/new/', views.create_announcement, name='create_announcement'),
    path('edit-announcement/<int:id>/', views.edit_announcement, name='edit_announcement'),
    path('annonce/supprimer/<int:id>/', views.delete_announcement, name='delete_announcement'),
]

