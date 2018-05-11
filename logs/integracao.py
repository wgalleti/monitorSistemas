from banco.oracle import Database
from message.office365 import Email365

db = Database()
mail = Email365()

sql = "SELECT * FROM DB_INTEGRACAO.GATEC_LOG_INTEGRACAO ORDER BY DATA DESC"
dsql = "DELETE FROM DB_INTEGRACAO.GATEC_LOG_INTEGRACAO WHERE DESCRICAO = :descricao"
body = """
    <h1>Erros encontrados na integração</h1>
    Foram encontrados {erros} erros na integração do Gatec. Verifique os erros abaixo:
    <br>
"""
message = """
    <h3> Motivo {motivo}</h3>
    <br>
    <small>Hora {hora}</small>
    <br>
    <small>Departamento {departamento}</small>
    <p>{log}</p>
    <hr>
    <br>
"""
err = 0

for i in db.query(sql, dict()):
    err += 1
    key = dict(descricao=i['descricao'])
    body += message.format(motivo=i['motivo'],
                           hora=i['data'],
                           departamento=i['departamento'],
                           log=i['descricao'])
    db.delete(dsql, key)

subject = 'Erros na integração'
db.disconnect()

if err > 0:
    mail.send(subject, body.format(erros=err))
