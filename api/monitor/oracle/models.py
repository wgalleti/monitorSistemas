from django.db import models
from .managers import LockManager


class Lock(models.Model):
    """
    Modelo de Locks
    """

    objects = LockManager()

    tempo = models.TimeField()
    session_id = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    maquina = models.CharField(max_length=100)
    objetos = models.TextField()
    processo = models.CharField(max_length=100)
    locks = models.IntegerField(default=1)
    killed_user = models.ForeignKey('auth.User', null=True, blank=True)
    killed_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.session_id}'
