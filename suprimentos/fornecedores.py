from banco.oracle import Database
from message.office365 import Email365
from suprimentos.config import *

db = Database()
mail = Email365()

sql = """
SELECT FRN.CODFOR AS FORNECEDOR_ID,
       INITCAP(TRIM(FRN.NOMFOR)) AS FORNECEDOR,
       LOWER(FRN.INTNET) AS EMAIL,
       INITCAP(FIL.SIGFIL) AS FILIAL,
       IPO.NUMOCP AS ORDEM,
       IPO.CODPRO AS PRODUTO,
       INITCAP(IPO.CPLIPO) AS DESCRICAO,
       IPO.UNIMED AS UNIDADE_MEDIDA,
       IPO.QTDPED AS PEDIDO,
       IPO.QTDREC AS ENTREGUE,
       IPO.QTDPED - IPO.QTDREC AS PENDENTE,
       IPO.DATENT AS PREVISAO,
       TRUNC(SYSDATE) - IPO.DATENT AS DIAS
  FROM E420IPO IPO,
       E420OCP OCP,
       E095FOR FRN,
       E070FIL FIL
 WHERE IPO.CODEMP = OCP.CODEMP
   AND IPO.CODFIL = OCP.CODFIL
   AND IPO.NUMOCP = OCP.NUMOCP
   AND OCP.CODFOR = FRN.CODFOR
   AND IPO.CODEMP = FIL.CODEMP
   AND IPO.CODFIL = FIL.CODFIL
   AND IPO.CODEMP = 1
   AND IPO.SITIPO NOT IN (4, 5, 9)
   AND IPO.DATENT < TRUNC(SYSDATE) 
   AND NVL(TRIM(FRN.INTNET), ' ') <> ' '
   AND IPO.USUGER IN (464,396,212,532,109,562)
 ORDER BY 1, 2, 4, 5, 7
"""

fornecedor = dict()
for i in db.query(sql, []):
    try:
        if fornecedor[f"{i['fornecedor']} - {i['fornecedor_id']}"]:
            fornecedor[f"{i['fornecedor']} - {i['fornecedor_id']}"].append(i)
    except KeyError:
        fornecedor[f"{i['fornecedor']} - {i['fornecedor_id']}"] = []
        fornecedor[f"{i['fornecedor']} - {i['fornecedor_id']}"].append(i)

db.disconnect()

for f in fornecedor:
    conteudo = body.format(fornecedor=f, pendencias=len(fornecedor[f]))
    conteudo += table_header
    to = f"{fornecedor[f][0]['email']};gilberto.bonfim@gruposcheffer.com.br"
    for i in fornecedor[f]:
        i['pedido'] = format_number(i['pedido'])
        i['entregue'] = format_number(i['entregue'])
        i['pendente'] = format_number(i['pendente'])
        i['previsao'] = i['previsao'].strftime('%d/%m/%Y')

        conteudo += table_items.format(**i)

    conteudo += table_end
    subject = 'Pendências de Entrega'
    try:
        mail.send(subject, conteudo, to=to)
    except Exception:
        print(f"Erro ao enviar email para {f}-{fornecedor[f][0]['email']};gilberto.bonfim@gruposcheffer.com.br")