from django.db import models

# Create your models here.


class Justificatif(models.Model):
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]

    STATUS_CHOICES = [
        ('En attente', 'En attente'),
        ('Accepté', 'Accepté'),
        ('Refusé', 'Refusé'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    sender_id = models.IntegerField(help_text="ID of the sender from Auth service")
    target_user_id = models.IntegerField(help_text="ID of the reviewer (teacher or department head)")
    session_id = models.IntegerField(help_text="ID of the session from Presences service")
    
    file = models.FileField(upload_to='justificatifs_files/', help_text="Justification file (PDF or image)")
    submission_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='En attente')
    admin_comment = models.TextField(blank=True, null=True, help_text="Comment from the reviewer")

    def str(self):
        return f"[{self.user_type.upper()}] Justificatif #{self.id} - Sender ID: {self.sender_id}"