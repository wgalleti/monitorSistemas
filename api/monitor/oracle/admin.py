from django.contrib import admin
from .models import Lock

@admin.register(Lock)
class LockAdmin(admin.ModelAdmin):
    list_display = [
        'tempo',
        'session_id',
        'usuario',
        'maquina',
        'objetos',
        'processo',
        'locks',
        'killed_user',
        'killed_in'
    ]