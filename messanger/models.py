from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Message(models.Model):
    subject = models.CharField(("Subject"), max_length=120)
    sender = models.ForeignKey(User,on_delete=models.CASCADE, related_name='sent_messages', verbose_name=("Sender"),blank=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,related_name='received_messages', verbose_name=("Recipient"))
    is_read = models.BooleanField(default=False)
    message = models.TextField(("Message"))
    sent_at = models.DateTimeField(("Sent at"), auto_now_add=True, blank=True)
 
    class Meta:
        verbose_name = ("message")
        verbose_name_plural = ("messages")
        ordering = ['-sent_at', '-id']
 
    def __str__(self):
        return self.message
