from django.contrib import admin
from .models import Report, File, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_admin']
    list_editable = ['is_admin']
    list_filter = ['is_admin']

admin.site.register(Report)
admin.site.register(File)
admin.site.register(Profile, ProfileAdmin)