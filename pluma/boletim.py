from banco.oracle import Database
from message.office365 import Email365
from pluma.config import *

db = Database()
mail = Email365()

to = 'rogerio.cardoso@scheffer.agr.br;celio.sampaio@scheffer.agr.br;william.galleti@scheffer.agr.br'
subject = 'Qualidade de Beneficiamento - Boletim Diario'


def parse_resumo(row):
    row_item = dict(
        beneficiadora=row['beneficiadora'],
        fardoes=row['fardoes'],
        fardinhos=row['fardinhos'],
        talhoes=row['talhoes'],
        variedades=row['variedades'],
        peso_algodao=row['peso_algodao'],
        peso_pluma=row['peso_pluma'],
    )

    row_item['rendimento'] = (row_item['peso_pluma'] / row_item['peso_algodao']) * 100
    row_item['peso_medio'] = row_item['peso_pluma'] / row_item['fardinhos']

    row_item['peso_algodao'] = format_number(row_item['peso_algodao'])
    row_item['peso_pluma'] = format_number(row_item['peso_pluma'])
    row_item['fardinhos'] = format_number(row_item['fardinhos'], 0)
    row_item['fardoes'] = format_number(row_item['fardoes'], 0)
    row_item['rendimento'] = format_number(row_item['rendimento'])
    row_item['peso_medio'] = format_number(row_item['peso_medio'])

    return row_item


def parse_item(row):
    row_item = dict(
        produtora=row['produtora'],
        fardao_id=row['fardao_id'],
        tipo_fardao=row['tipo_fardao'],
        talhao=row['talhao'],
        variedade=row['variedade'],
        peso_algodao=row['peso_algodao'],
        peso_pluma=row['peso_pluma'],
        primeiro_fardo=row['primeiro_fardo'].strftime('%d/%m/%Y %H:%M'),
        ultimo_fardo=row['ultimo_fardo'].strftime('%d/%m/%Y %H:%M'),
        fardinhos=row['fardinhos'],
    )
    row_item['rendimento'] = (row_item['peso_pluma'] / row_item['peso_algodao']) * 100
    row_item['peso_medio'] = row_item['peso_pluma'] / row_item['fardinhos']

    row_item['peso_algodao'] = format_number(row_item['peso_algodao'])
    row_item['peso_pluma'] = format_number(row_item['peso_pluma'])
    row_item['fardinhos'] = format_number(row_item['fardinhos'], 0)
    row_item['rendimento'] = format_number(row_item['rendimento'])
    row_item['peso_medio'] = format_number(row_item['peso_medio'])


    return tb_detalhe_row.format(**row_item)


resumos_itens = []
resumos = []
for i in db.query(SQL_RESUMO, []):
    resumos_itens.append(tb_resumo_row.format(**parse_resumo(i)))

resumos.append(tb_resumo_header.format(itens=''.join(resumos_itens)))

itens = []
algodoeira = ''
algodoeira_old = ''
tabelas = []
for i in db.query(SQL_DETALHES, []):

    if algodoeira == '':
        algodoeira = i['beneficiadora']
        algodoeira_old = algodoeira

    algodoeira = i['beneficiadora']

    if algodoeira != algodoeira_old:
        tabelas.append(tb_detalhe_header.format(algodoeira=algodoeira_old, itens=''.join(itens)))
        algodoeira_old = algodoeira
        itens = []

    itens.append(parse_item(i))

if len(itens):
    tabelas.append(tb_detalhe_header.format(algodoeira=algodoeira_old, itens=''.join(itens)))

conteudo = body.format(tabela_resumo=''.join(resumos), tabela_detalhes=''.join(tabelas))

try:
    mail.send(subject, conteudo, to=to)
except Exception as e:
    print(f"Erro ao enviar email para {to}. \n Erro: {e}")
