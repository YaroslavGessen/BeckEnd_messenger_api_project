from django.contrib import admin
from .models import *


class MessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject', 'sender', 'recipient', 'is_read', 'message',]
    list_display_links = ['id']

    search_fields = ['recipient']
    fields = ['sender', 'recipient','subject','message','is_read']

admin.site.register(Message, MessageAdmin)