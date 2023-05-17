from django.contrib import admin
from ratings.models import MatchGroup


@admin.register(MatchGroup)
class AdminMatchGroupView(admin.ModelAdmin):
    pass
