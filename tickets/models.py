from django.db import models
from django.contrib.auth.models import User

class Ticket(models.Model):
    id = models.BigAutoField(primary_key=True)  # הגדרת סוג המפתח הראשי
    STATUSES = (
        ('open', 'פתוח'),
        ('in_progress', 'בטיפול'),
        ('closed', 'סגור'),
    )
    
    title = models.CharField(max_length=200, verbose_name="כותרת")
    description = models.TextField(verbose_name="תיאור")
    status = models.CharField(max_length=20, choices=STATUSES, default='open', verbose_name="סטטוס")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets', verbose_name="נוצר על ידי")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets', verbose_name="משויך ל")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="נוצר ב")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="עודכן ב")
    is_general = models.BooleanField(default=False, verbose_name="קריאה כללית")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "קריאה"
        verbose_name_plural = "קריאות"


class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)  # הגדרת סוג המפתח הראשי
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments', verbose_name="קריאה")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="משתמש")
    content = models.TextField(verbose_name="תוכן")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="נוצר ב")

    def __str__(self):
        return f'תגובה מאת {self.user.username} על קריאה {self.ticket.id}'

    class Meta:
        verbose_name = "תגובה"
        verbose_name_plural = "תגובות"
