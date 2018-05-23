from django.db import models
from .managers import LockManager


class Lock(models.Model):
    """
    Modelo de Locks
    """

    objects = LockManager()

    segundos = models.TimeField()
    sessionid = models.CharField(max_length=100)
    maquina = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100)
    schema = models.CharField(max_length=100)
    objeto = models.TextField()
    tipo = models.CharField(max_length=50)
    rac = models.IntegerField(default=1)
    sqlid = models.CharField(max_length=100)
    sql = models.TextField()
    killed_user = models.ForeignKey('auth.User', null=True, blank=True)
    killed_in = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sessionid}'
