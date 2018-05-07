from datetime import timedelta
from src.app import App

app = App()

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

for i in app.query(sql, dict()):
    key = dict(descricao=i['descricao'])
    err += 1
    body += message.format(motivo=i['motivo'],
                           hora=i['data'],
                           departamento=i['departamento'],
                           log=i['descricao'])
    app.delete(dsql, key)

subject = 'Erros na integração'
app.send_mail(subject, body.format(erros=err))
