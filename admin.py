from django.contrib import admin
from .models import Ticket, Comment  # Change this line to import from 'tickets'

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_by', 'assigned_to', 'created_at')
    list_filter = ('status', 'created_by', 'assigned_to')
    search_fields = ('title', 'description')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'created_at')
    search_fields = ('content',)
