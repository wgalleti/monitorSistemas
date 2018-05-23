from django.contrib import admin
from .models import Lock

@admin.register(Lock)
class LockAdmin(admin.ModelAdmin):
    list_display = [
        'segundos',
        'sessionid',
        'maquina',
        'usuario',
        'schema',
        'objeto',
        'tipo',
        'rac',
    ]