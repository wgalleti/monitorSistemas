from django.shortcuts import render
from rest_framework import viewsets, response
from .serializers import *


class LockViewSet(viewsets.ModelViewSet):
    queryset = Lock.objects.all()
    serializer_class = LockSerializer

    def list(self, request, *args, **kwargs):
        locks = Lock.objects.locks()
        return response.Response(locks, status=200)

    def create(self, request, *args, **kwargs):
        sessionid = request.data.get('sessionid', None)

        if sessionid is None:
            return response.Response(dict(error='Sid,Session,Instance is required'), status=400)

        try:
            data = Lock.objects.locked(sessionid)

            if len(data) == 0:
                return response.Response(dict(success='Sessão não existe ou já foi desconectada!'))

            log = Lock(**data)
            log.killed_user_id = request.user.id
            log.save()

            Lock.objects.kill(sessionid)

        except Exception as e:
            return response.Response(dict(error=f'{e}'), status=400)

        return response.Response(dict(success='Sessão eliminada!', log=LockSerializer(log).data), status=201)
