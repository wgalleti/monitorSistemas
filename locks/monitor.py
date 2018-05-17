from banco.oracle import Database
from message.office365 import Email365
from datetime import timedelta
from .config import SQL_LOCKS, SQL_SQLID, EMAIL_BODY, EMAIL_MESSAGE, EMAIL_FOOTER

import sqlparse

db = Database()
mail = Email365()

sql = SQL_LOCKS
sql_id = SQL_SQLID

body = EMAIL_BODY
message = EMAIL_MESSAGE
locks = 0

for i in db.query(sql, dict()):
    locks += 1
    run_sql = None
    if i['sql_address'] is not None:
        for s in db.query(sql_id, dict(sql_id=i['prev_sql_id'])):
            run_sql = sqlparse.format(s['sql_fulltext'].lower(), reindent=True, keyword_case='upper')
    body += message.format(maquina=i['maquina'],
                           usuario=i['usuario'],
                           objeto=i['objetos'],
                           sessao=i['sid'],
                           tempo=str(timedelta(seconds=i['tempo'])),
                           banco=i['oracledb'],
                           rac=i['rac'],
                           comando=i['comando'],
                           sql=run_sql)

subject = 'Locks no banco de dados'
db.disconnect()

body += EMAIL_FOOTER

if locks > 0:
    try:
        mail.send(subject, body.format(locks=locks))
    except:
        print(f'Erro ao enviar o email {mail.error}')
        exit(1)
