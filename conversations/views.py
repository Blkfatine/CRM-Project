
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone

from django.http import JsonResponse
from django.http import HttpResponseForbidden

def make_aware_if_naive(dt):
    if timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt
@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user).prefetch_related('messages')
    users = User.objects.exclude(id=request.user.id) 

    conversation_data = []
    for conversation in conversations:
        other_participants = conversation.participants.exclude(id=request.user.id)
        if other_participants.exists():
            participant = other_participants.first()
            last_message = conversation.messages.last() if conversation.messages.exists() else None
            conversation_data.append({
                'conversation': conversation,
                'participant': participant,
                'last_message': last_message
            })
    now = timezone.now()   

    conversation_data.sort(
        key=lambda x: make_aware_if_naive(x['last_message'].timestamp) if x['last_message'] else now,
        reverse=True
    )
    return render(request, 'conversations/conversation_list.html', {
        'conversations': conversation_data,
        'users': users
    })

from django.shortcuts import redirect

@login_required
def conversation_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)

    conversation = Conversation.objects.filter(
        participants=request.user
    ).filter(
        participants=other_user
    ).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    if request.method == 'POST':
        content = request.POST.get('content')
        file = request.FILES.get('file')

        if content or file:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content,
                file=file
            )
        return redirect('conversation_detail', user_id=user_id)

    messages = conversation.messages.order_by('timestamp')

    return render(request, 'conversations/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages
    })

    
@login_required
def start_conversation(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    conversation, created = Conversation.objects.get_or_create(participants__in=[request.user, other_user])
    conversation.participants.add(request.user, other_user)
    return redirect('conversation_detail', conversation_id=conversation.id)
@login_required
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    if request.user not in conversation.participants.all():
        return HttpResponseForbidden("You are not authorized to delete this conversation.")

    if request.method == 'POST':
        conversation.delete()
        return redirect('conversation_list')  

    return render(request, 'conversations/conversation_confirm_delete.html', {'conversation':conversation})


