from django.db import models
from django.utils import timezone

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_modified = models.BooleanField(default=False)  # Champ pour marquer si l'annonce a été modifiée

    def save(self, *args, **kwargs):
        # Marquer l'annonce comme modifiée si la date de mise à jour est plus récente
        if self.pk and self.updated_at > self.created_at:
            self.is_modified = True
        super().save(*args, **kwargs)
