from django.contrib import admin
from photos.models import Photo


@admin.register(Photo)
class AdminPhotoView(admin.ModelAdmin):
    pass