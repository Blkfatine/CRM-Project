from django.urls import path
from .views import notifications_view, mark_notification_as_read, unread_count, mark_all_notifications_as_read
from . import views
urlpatterns = [
    path('', notifications_view, name='notifications'),
    path('mark_all_as_read/', mark_all_notifications_as_read, name='mark_all_as_read'),
    path('unread_count/', unread_count, name='unread_count'),
]
