from banco.oracle import Database
from message.office365 import Email365
from datetime import timedelta
from locks.config import SQL_LOCKS, SQL_SQLID, EMAIL_BODY, EMAIL_MESSAGE, EMAIL_FOOTER

import sqlparse


class Monitor:
    sql = SQL_LOCKS
    sql_id = SQL_SQLID

    def __init__(self, subject):
        self.mail = Email365()
        self.db = Database()

        self.body = EMAIL_BODY
        self.message = EMAIL_MESSAGE
        self.footer = EMAIL_FOOTER
        self.subject = subject
        self.locks = 0

    def run(self):
        self.body += ''.join(list(self.load_locks()))
        self.body = self.body.format(locks=self.locks) + self.footer

        if self.locks > 0:
            try:
                self.mail.send(self.subject, self.body)
            except Exception as e:
                print(f'Erro ao enviar o email {self.mail.error}. Erro: {e}')

    def load_locks(self):
        return (self.mount_message(self.parse_lock(i)) for i in self.db.query(self.sql, dict()))

    def parse_lock(self, lock):
        self.locks += 1
        lock['run_sql'] = None
        if lock['sql_address'] is not None:
            for s in self.db.query(self.sql_id, dict(sql_id=lock['prev_sql_id'])):
                lock['run_sql'] = sqlparse.format(s['sql_fulltext'].lower(), reindent=True, keyword_case='upper')
        return lock

    def mount_message(self, data):
        return self.message.format(maquina=data.get('maquina', None),
                                   usuario=data.get('usuario', None),
                                   objeto=data.get('objetos', None),
                                   sessao=data.get('sid', None),
                                   tempo=str(timedelta(seconds=data.get('tempo', 90))),
                                   banco=data.get('oracledb', None),
                                   rac=data.get('rac', None),
                                   comando=data.get('comando', None),
                                   sql=data.get('run_sql', None))


if __name__ == '__main__':
    monitor = Monitor('Locks no banco de dados')
    monitor.run()
