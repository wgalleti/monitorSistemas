from banco.oracle import Database
from message.office365 import Email365
from datetime import timedelta

import sqlparse

db = Database()
mail = Email365()

sql = """
    SELECT C.SECONDS_IN_WAIT AS TEMPO,
           C.SID,
           A.SESSION_ID || ',' || SERIAL# || ',@' || C.INST_ID AS SESSIONID,
           B.OBJECT_NAME AS OBJETO,
           C.MACHINE AS MAQUINA,
           A.OS_USER_NAME AS USUARIO,
           A.ORACLE_USERNAME AS ORACLEDB,
           B.OBJECT_NAME AS OBJETO,
           B.OBJECT_TYPE AS OBJETOTIPO,
           C.PROCESS AS PROCESSO,
           C.INST_ID AS RAC,
           C.SQL_ADDRESS,
           C.PREV_SQL_ID,
           'ALTER SYSTEM KILL SESSION ''' || A.SESSION_ID || ',' || SERIAL# || ',@' || C.INST_ID || ''' IMMEDIATE' AS COMANDO
      FROM SYS.GV_$LOCKED_OBJECT A,
           SYS.ALL_OBJECTS B,
           SYS.GV_$SESSION C
     WHERE A.OBJECT_ID = B.OBJECT_ID
       AND A.INST_ID = C.INST_ID
       AND C.SID = A.SESSION_ID   
       AND C.SECONDS_IN_WAIT >= 90
     ORDER BY SECONDS_IN_WAIT DESC, 5 DESC
"""
sql_id = """
    SELECT SQL_TEXT, 
           SQL_FULLTEXT 
      FROM SYS.GV_$SQL 
     WHERE SQL_ID = :sql_id
"""
body = """
    <h1Locks no banco de dados</h1>
    Foram encontrados {locks} locks no banco de dados:
"""
message = """
    <br>
    <h3>Sessão {sessao} em {maquina} para {usuario}</h3>
    <table border="1" cellpadding="1" cellspacing="0" class="body" style="border-collapse: separate; mso-table-lspace: 0pt; mso-table-rspace: 0pt; width: 80%;">
        <tbody>
            <tr>
                <td>Objeto</td>
                <td>Tempo em Execução</td>
                <td>Banco de Dados</td>
                <td>Rac</td>
            </tr>
            <tr>
                <td>{objeto}</td>
                <td>{tempo}</td>
                <td>{banco}</td>
                <td>{rac}</td>
            </tr>
        </tbody>
    </table>
    <br>
    <small>Para encessar essa sessão, execute o comando <b>{comando}</b></small>
    <br>
    SQL em execução:
    <pre>{sql}</pre>
    <hr>
"""
locks = 0

for i in db.query(sql, dict()):
    locks += 1
    run_sql = None
    if i['sql_address'] is not None:
        for s in db.query(sql_id, dict(sql_id=i['prev_sql_id'])):
            run_sql = sqlparse.format(s['sql_fulltext'].lower(), reindent=True, keyword_case='upper')
    body += message.format(maquina=i['maquina'],
                              usuario=i['usuario'],
                              objeto=i['objeto'],
                              sessao=i['sid'],
                              tempo=str(timedelta(seconds=i['tempo'])),
                              banco=i['oracledb'],
                              rac=i['rac'],
                              comando=i['comando'],
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
