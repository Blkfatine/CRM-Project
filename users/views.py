
from itertools import count
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from appointments.models import Appointment
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from notifications.views import create_notification  
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Announcement
from .forms import CustomUserCreationForm
from leads.models import Lead
from django.db.models import Count
from django.views.generic import ListView
from notifications.models import Notification 
from .forms import AnnouncementForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = True
            user.save()
            messages.success(request, 'Compte créé avec succès! Vous pouvez maintenant vous connecter.')
            return redirect('login')
        else:
            # Pass errors to the template
            return render(request, 'login.html', {'signup_form': form, 'show_signup': True})
    else:
        signup_form = CustomUserCreationForm()
    return render(request, 'login.html', {'signup_form': signup_form, 'show_signup': True})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Rediriger l'admin vers son tableau de bord spécifique
            if user.is_staff or user.is_superuser:
                return redirect('admin_dashboard')  
            else:
                # Rediriger les utilisateurs normaux vers la liste des leads
                return redirect('lead_list')  
    else:
        form = AuthenticationForm()
    
    # Initialize signup form for template context
    signup_form = CustomUserCreationForm()
    return render(request, 'login.html', {'form': form, 'signup_form': signup_form})


def custom_logout(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(lambda u: u.is_staff or u.is_superuser)
def admin_dashboard(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.is_active = True
            user.save()
            messages.success(request, 'Utilisateur ajouté avec succès! L\'utilisateur peut maintenant se connecter.')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Erreur lors de l\'ajout de l\'utilisateur.')
    else:
        form = CustomUserCreationForm()

    
    leads = Lead.objects.all()
    leads_count = leads.count()
    converted_leads_count = leads.filter(statut='converti').count()
    conversion_rate = (converted_leads_count / leads_count * 100) if leads_count > 0 else 0
    appointments = Appointment.objects.all()
    appointments_count = appointments.count()
    leads_pending_followup = leads.filter(Assigné__isnull=True).count()
    lead_sources = leads.values('source').annotate(count=Count('source')).order_by('source')
    sources = [source['source'] for source in lead_sources]
    counts = [source['count'] for source in lead_sources]
    new_leads_count = leads.filter(statut='nouveau').count()
    lost_leads_count = leads.filter(statut='perdu').count()

    
    utilisateurs = User.objects.filter(is_staff=False, is_superuser=False)
    leads_counts = [leads.filter(Assigné=user).count() for user in utilisateurs]
    recent_leads = leads.order_by('-crée')[:10]

    
    performances_utilisateurs = []
    labels = []
    conversion_rates = []
    for utilisateur in utilisateurs:
        user_leads = leads.filter(Assigné=utilisateur)
        user_leads_count = user_leads.count()
        user_converted_leads_count = user_leads.filter(statut='converti').count()
        conversion_rate_user = (user_converted_leads_count / user_leads_count * 100) if user_leads_count > 0 else 0
        performances_utilisateurs.append({
            'utilisateur': utilisateur.username,
            'conversion_rate': conversion_rate_user
        })
        labels.append(utilisateur.username)
        conversion_rates.append(conversion_rate_user)

    
    return render(request, 'admin_dashboard.html', {
        'form': form,
        'leads_count': leads_count,
        'appointments_count': appointments_count,
        'taux_conversion_global': conversion_rate,
        'leads_pending_followup': leads_pending_followup,
        'sources': sources,
        'counts': counts,
        'utilisateurs': [user.username for user in utilisateurs],
        'leads_counts': leads_counts,
        'new_leads_count': new_leads_count,
        'lost_leads_count': lost_leads_count,
        'recent_leads': recent_leads,
        'performances_utilisateurs': performances_utilisateurs,
        'labels': labels,
        'conversion_rates': conversion_rates,
    })








class AppointmentsListView(ListView):
    model = Appointment
    template_name = 'appointments_list.html'


class LeadActionsView(ListView):
    model = Lead
    template_name = 'lead_actions.html'


def is_admin(user):
    return user.is_staff  
@login_required
@user_passes_test(is_admin)
def create_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.author = request.user
            announcement.save()

            
            users = User.objects.all()
            for user in users:
                Notification.objects.create(
                    user=user,
                    message=f'Une nouvelle annonce "{announcement.title}" a été ajoutée.',
                    type='announcement' 
                )
            return redirect('announcements_list')
    else:
        form = AnnouncementForm()
    return render(request, 'create_announcement.html', {'form': form})





@login_required
def announcements_list(request):
    announcements = Announcement.objects.all().order_by('-updated_at', '-created_at')
    
    user_announcements = []
    for announcement in announcements:
        user_announcements.append({
            'announcement': announcement,
            'is_modified_by_user': announcement.is_modified
        })

    is_admin = request.user.is_superuser

    return render(request, 'announcements_list.html', {
        'user_announcements': user_announcements,
        'is_admin': is_admin 
    })



def edit_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            announcement.is_modified = True
            announcement.save()
            
            create_notification(request, notification_type='announcement', title=announcement.title, updated=True)
            
            messages.success(request, "Annonce mise à jour avec succès.")
            return redirect('announcements_list')
    else:
        form = AnnouncementForm(instance=announcement)
    
    return render(request, 'edit_announcement.html', {'form': form, 'announcement': announcement})


def delete_announcement(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    if request.method == 'POST':
        announcement.delete()
        return redirect('announcements_list')
    return render(request, 'delete_announcement.html', {'announcement': announcement})
@login_required
def user_management(request):
    users = User.objects.all()
    return render(request, 'user_management.html', {'users': users})


@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if old_password and not check_password(old_password, user.password):
            messages.error(request, "L'ancien mot de passe est incorrect.")
        else:
            if username:
                user.username = username
            if email:
                user.email = email

            if new_password:
                if new_password == confirm_password:
                    user.set_password(new_password)  
                    update_session_auth_hash(request, user)  
                else:
                    messages.error(request, "Les nouveaux mots de passe ne correspondent pas.")
            
            if not messages.get_messages(request): 
                user.save()
                messages.success(request, 'Informations modifiées avec succès.')
                return redirect('user_management')

    return render(request, 'edit_user.html', {'user': user})

@login_required
def change_user_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        if new_password:
            user.password = make_password(new_password)
            user.save()
            messages.success(request, 'Mot de passe modifié avec succès.')
        return redirect('user_management')
    return render(request, 'change_user_password.html', {'user': user})
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Utilisateur supprimé avec succès.')
        return redirect('user_management')
    return render(request, 'confirm_delete_user.html', {'user': user})
