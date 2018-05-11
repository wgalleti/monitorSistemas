from datetime import timedelta

from banco.oracle import Database
from message.office365 import Email365

db = Database()
email = Email365()


sql = "SELECT * FROM E000LPA ORDER BY DATINI, HORINI"
dsql = 'DELETE E000LPA WHERE CODPRA = :regra AND SEQLOG = :seq'
body = """
    <h1>Erros no processo automático</h1>
    Foram encontrados {erros} erros na execução do processo automático. Verifique os erros abaixo:
    <br>
"""
message = """
    <h3> Processo {seqlog}</h3>
    <br>
    <small>Iniciado as {inicio} e finalizado as {fim}</small>
    <p>{log}</p>
    <hr>
    <br>
"""
err = 0

for i in db.query(sql, dict()):
    key = dict(regra=i['codpra'], seq=i['seqlog'])
    if (i['tiplor'] != 'E'):
        db.delete(dsql, key)
    else:
        err += 1
        body += message.format(seqlog=i['seqlog'],
                               inicio=i['datini'] + timedelta(minutes=i['horini']),
                               fim=i['datfim'] + timedelta(minutes=i['horfim']),
                               log=i['msglg1'])
        db.delete(dsql, key)

subject = 'Erro ao executar processo automático'
db.disconnect()

if err > 0:
    email.send(subject, body.format(erros=err))
