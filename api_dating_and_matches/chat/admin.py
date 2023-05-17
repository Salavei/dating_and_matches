from django.contrib import admin
from chat.models import ChatName

@admin.register(ChatName)
class ChatNameAdminView(admin.ModelAdmin):
    pass

