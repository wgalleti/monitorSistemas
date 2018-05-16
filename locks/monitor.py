from banco.oracle import Database
from message.office365 import Email365
from datetime import timedelta

import sqlparse

db = Database()
mail = Email365()

sql = """
    SELECT C.SECONDS_IN_WAIT AS TEMPO,
           A.SESSION_ID || ',' || SERIAL# || ',@' || C.INST_ID AS SESSIONID,
           B.OBJECT_NAME AS OBJETO,
           C.MACHINE || ' - ' || A.OS_USER_NAME AS MAQUINA,
           A.ORACLE_USERNAME AS ORACLEDB,
           NVL(C.LOCKWAIT, 'Active') AS TIPOESPERA,
           DECODE(A.LOCKED_MODE,
                  2, 'Registro Compartilhado',
                  3, 'Registro Exclusivo',
                  4, 'Compartilhado',
                  5, 'Compartilhando registro Exclusivo',
                  6, 'Exclusivo',
                  'Desconhecido') AS LOCKMODO,
           B.OBJECT_TYPE AS OBJETOTIPO,
           C.PROCESS AS PROCESSO,
           C.INST_ID AS INSTANCIA,
           'ALTER SYSTEM KILL SESSION ''' || A.SESSION_ID || ',' || SERIAL# || ',@' || C.INST_ID || ''' IMMEDIATE' AS KILL_COMMAND,
           C.PREV_SQL_ADDR AS SQL_ADDRESS
      FROM SYS.GV_$LOCKED_OBJECT A,
           SYS.ALL_OBJECTS B,
           SYS.GV_$SESSION C
     WHERE A.OBJECT_ID = B.OBJECT_ID
       AND C.SID = A.SESSION_ID
       AND C.SECONDS_IN_WAIT >= 90
     ORDER BY SECONDS_IN_WAIT DESC, 5 DESC
"""
sql_id = """
    SELECT SQL_TEXT, 
           SQL_FULLTEXT 
      FROM SYS.GV_$SQL 
     WHERE ADDRESS = :sql_address
"""
body = """
    <h1Locks no banco de dados</h1>
    Foram encontrados {locks} locks no banco de dados:
"""
message = """
    <h3> Maquina / Usuário {usuario}</h3>
    <br>
    <small>Banco {banco}</small>
    <br>
    <small>Tempo em execução {tempo}</small>
    <br>
    <small>Para encessar essa sessão, execute o comando <b>{comando}</b></small>
    <br>
    <pre>{sql}</pre>
    <hr>
"""
locks = 0

for i in db.query(sql, dict()):
    locks += 1
    run_sql = None
    if i['sql_address'] is not None:
        for s in db.query(sql_id, dict(sql_address=i['sql_address'])):
            run_sql = sqlparse.format(s['sql_fulltext'].lower(), reindent=True, keyword_case='upper')
    body += message.format(usuario=i['maquina'],
                           tempo=str(timedelta(seconds=i['tempo'])),
                           banco=i['oracledb'],
                           comando=i['kill_command'],
                           sql=run_sql)

subject = 'Locks no banco de dados'
db.disconnect()

body += """
    <h3>Utilidade</h3>
    Para encessar essa sessão, siga os passos abaixo
    <br>
    <pre>
      1. Abra o Terminal.
      2. Execute o aplicativo SQLPlus conectando com um usuário DBA: sqlplus system@producao
      3. Rode o comando: ALTER SYSTEM KILL SESSION '123,123,@1' IMMEDIATE;
      4. Saia do SQLPlus: exit
    </pre>
    <br>
"""

if locks > 0:
    try:
        mail.send(subject, body.format(locks=locks))
    except:
        print(f'Erro ao enviar o email {mail.error}')
        exit(1)

