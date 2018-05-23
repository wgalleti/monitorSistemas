from django.db import models, connection
from .helpers import custom_query
from .queries import SQL_LOCKS, SQL_SQLID
from datetime import timedelta
import sqlparse


class LockManager(models.Manager):

    def _load_sql(self, data):
        for d in data:
            data[d]['sql'] = ''
            data[d]['segundos'] = str(timedelta(seconds=data[d]['segundos']))
            if data[d]['sqlid'] is not None:
                sql = custom_query(SQL_SQLID, [data[d]['sqlid'], data[d]['rac']])
                data[d]['sql'] = [sqlparse.format(s['sql_fulltext'].lower(), reindent=True, keyword_case='upper') for s in sql][0] if len(sql) > 0 else ''
            yield data[d]

    def locks(self):
        db = custom_query(SQL_LOCKS, [])

        data = dict()
        for i in db:
            try:
                if data[i['sessionid']]:
                    data[i['sessionid']]['objeto'] += ', ' + i['objeto']
            except KeyError:
                data[i['sessionid']] = i

        return list(self._load_sql(data))

    def locked(self, sessionid):
        for lock in self.locks():
            if lock['sessionid'] == sessionid:
                return lock
        return dict()

    def kill(self, session):
        with connection.cursor() as cursor:
            cursor.execute(f"ALTER SYSTEM KILL SESSION '{session}' IMMEDIATE")
