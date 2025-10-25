from django.shortcuts import render, get_object_or_404, redirect
from .forms import AppointmentForm
from .models import Appointment
from leads.models import Lead
from django.utils import timezone
from django.contrib import messages
from datetime import timedelta
from django.contrib.auth.decorators import login_required
import calendar

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            
            conflicting_appointments = Appointment.objects.filter(date=appointment.date)
            if conflicting_appointments.exists():
                form.add_error(None, "Un autre rendez-vous existe déjà à cette date et heure.")
            else:
                appointment.save()
                return redirect('appointments_list') 
    else:
        form = AppointmentForm()
    
    form.fields['lead'].queryset = Lead.objects.filter(Assigné=request.user)
    
    return render(request, 'book_appointment.html', {'form': form})

from django.shortcuts import render, redirect
from datetime import datetime

from django.shortcuts import render
from .utils import get_calendar_weeks
  
import random

def random_color():
    return "#{:06x}".format(random.randint(0, 0xFFFFFF))
    
@login_required
def appointments_list(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('appointments_list')
    else:
        form = AppointmentForm()

    today = datetime.now()
    month = request.GET.get('month')
    year = request.GET.get('year')

    if not month:
        month = today.month
    else:
        month = int(month)

    if not year:
        year = today.year
    else:
        year = int(year)

    if month == 1:
        previous_month = 12
        previous_year = year - 1
    else:
        previous_month = month - 1
        previous_year = year

    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year

    appointments = Appointment.objects.filter(date__year=year, date__month=month).order_by('date')

    
    appointment_counts = {day: [] for day in range(1, calendar.monthrange(year, month)[1] + 1)} 
    for appointment in appointments:
        day = appointment.date.day
        if day in appointment_counts:
            appointment_counts[day].append(appointment)

    
    months_fr = [
        "Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
        "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"
    ]
    current_month_name = months_fr[month - 1]

    
    calendar_weeks = get_calendar_weeks(year, month)

    context = {
        'form': form,
        'appointments': appointments,
        'appointment_counts': appointment_counts,
        'year': year,
        'month': month,
        'current_month_name': current_month_name,
        'previous_month': previous_month,
        'previous_year': previous_year,
        'next_month': next_month,
        'next_year': next_year,
        'today': today,
        'calendar_weeks': calendar_weeks,
    }

    return render(request, 'appointments_list.html', context)

@login_required
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'appointment_detail.html', {'appointment': appointment})

@login_required
def appointment_delete(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    if request.method == 'POST':
        appointment.delete()
        return redirect('appointments_list')   
    return render(request, 'appointment_confirm_delete.html', {'appointment': appointment})



@login_required
def appointment_edit(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Le rendez-vous a été modifié avec succès.')
            return redirect('appointments_list')
        else:
            messages.error(request, 'Veuillez corriger les erreurs ci-dessous.')
    else:
        form = AppointmentForm(instance=appointment)
    
    return render(request, 'book_appointment.html', {'form': form, 'appointment':appointment})
