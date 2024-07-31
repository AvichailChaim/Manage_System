from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Ticket, Comment
from .forms import TicketForm, CommentForm

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(assigned_to=request.user) | Ticket.objects.filter(is_general=True)
    return render(request, 'tickets/ticket_list.html', {'tickets': tickets})

@login_required
def ticket_detail(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.ticket = ticket
            comment.user = request.user
            comment.save()
            return redirect('ticket_detail', pk=pk)
    else:
        form = CommentForm()
    return render(request, 'tickets/ticket_detail.html', {'ticket': ticket, 'form': form})

@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            send_ticket_notification(ticket, 'created')
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html', {'form': form})

@login_required
def ticket_update(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            ticket = form.save()
            send_ticket_notification(ticket, 'updated')
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm(instance=ticket)
    return render(request, 'tickets/ticket_form.html', {'form': form})

def send_ticket_notification(ticket, action):
    subject = f'עדכון בקריאה: {ticket.title}'
    if action == 'created':
        message = f'קריאה חדשה נוצרה: {ticket.title}\n\nתיאור: {ticket.description}'
    elif action == 'updated':
        message = f'הקריאה עודכנה: {ticket.title}\n\nסטטוס חדש: {ticket.get_status_display()}'
    else:
        return

    recipients = [ticket.assigned_to.email] if ticket.assigned_to else [user.email for user in User.objects.filter(is_staff=True)]
    
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipients,
        fail_silently=False,
    )
