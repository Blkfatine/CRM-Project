from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification
from conversations.models import Conversation, Message 
@login_required

def notifications_view(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

    context = {
        'notifications': notifications,
        'notifications_count': notifications.count(), 
        'unread_count': unread_count 
    }
    
    return render(request, 'notifications.html', context)



from django.contrib.auth.models import User

@login_required
def create_notification(user=None, notification_type='announcement', **kwargs):
    if notification_type == 'lead':
        lead = kwargs.get('lead')
        message = f"Nouveau lead ajouté : {lead.Prénom} {lead.Nom} le {lead.crée.strftime('%Y-%m-%d %H:%M:%S')}"
        users = User.objects.all()  
    elif notification_type == 'announcement':
        title = kwargs.get('title')
        updated = kwargs.get('updated', False)
        if updated:
            message = f"L'annonce '{title}' a été mise à jour."
        else:
            message = f"Nouvelle annonce : {title}"
        users = User.objects.all()  
    else:
        message = "Vous avez une nouvelle notification"
        users = [user]

    for user in users:
        Notification.objects.create(
            user=user,
            message=message,
            type=notification_type,
            is_read=False
        )



from django.http import JsonResponse
from django.shortcuts import get_object_or_404

@login_required
def mark_notification_as_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success'})


@login_required
def unread_count(request):
    count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'unread_count': count})


@login_required
def mark_all_notifications_as_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
