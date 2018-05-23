from django.db import models, connection
from .helpers import custom_query
from .queries import SQL_LOCKS
from datetime import timedelta


class LockManager(models.Manager):

    def locks(self, time=90):
        return custom_query(SQL_LOCKS, [time])

    def locked(self, sessionid):
        for lock in custom_query(SQL_LOCKS, [1]):
            if lock['sessionid'] == sessionid:
                return dict(tempo=str(timedelta(seconds=lock['tempo'])),
                            session_id=lock['sessionid'],
                            maquina=lock['maquina'],
                            usuario=lock['usuario'],
                            objetos=lock['objetos'],
                            processo=lock['processo'],
                            locks=lock['qtd_locked'])
        return dict()

    def kill(self, session):
        with connection.cursor() as cursor:
            cursor.execute(f"ALTER SYSTEM KILL SESSION '{session}' IMMEDIATE")
