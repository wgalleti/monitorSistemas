from banco.oracle import Database
from message.office365 import Email365
from pluma.config import *


class Boletim:

    def __init__(self):
        self.db = Database()
        self.mail = Email365()
        self.db_resumo = []
        self.db_detalhe = []
        self.data_resumo = []
        self.data_detalhe = []
        self.total_resumo = dict()
        self.total_detalhe = dict()
        self.template_resumo = ''
        self.template_detalhe = ''

        self.send_mail()

    def _load_db_data(self):
        self.db_resumo = self.db.query(SQL_RESUMO, [])
        self.db_detalhe = self.db.query(SQL_DETALHES, [])

    def _parse_db_resumo(self, row):
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

        return row_item

    def _parse_db_detalhe(self, row):
        row_item = dict(
            beneficiadora=row['beneficiadora'],
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

        return row_item

    def _format_resumo(self, item):
        row_item = item.copy()
        row_item['peso_algodao'] = format_number(row_item['peso_algodao'])
        row_item['peso_pluma'] = format_number(row_item['peso_pluma'])
        row_item['fardinhos'] = format_number(row_item['fardinhos'], 0)
        row_item['fardoes'] = format_number(row_item['fardoes'], 0)
        row_item['rendimento'] = format_number(row_item['rendimento'])
        row_item['peso_medio'] = format_number(row_item['peso_medio'])

        return row_item

    def _total_resumo(self):
        self.total_resumo = dict(fardoes=0,
                                 peso_algodao=0,
                                 peso_pluma=0,
                                 fardos_produzido=0,
                                 rendimento=0,
                                 peso_medio=0)

        for i in self.data_resumo:
            self.total_resumo['fardoes'] += i['fardoes']
            self.total_resumo['peso_algodao'] += i['peso_algodao']
            self.total_resumo['peso_pluma'] += i['peso_pluma']
            self.total_resumo['fardos_produzido'] += i['fardinhos']

        self.total_resumo['rendimento'] = (self.total_resumo['peso_pluma'] / self.total_resumo['peso_algodao']) * 100
        self.total_resumo['peso_medio'] = self.total_resumo['peso_pluma'] / self.total_resumo['fardos_produzido']

        self.total_resumo['fardoes'] = format_number(self.total_resumo['fardoes'], 0)
        self.total_resumo['peso_algodao'] = format_number(self.total_resumo['peso_algodao'])
        self.total_resumo['peso_pluma'] = format_number(self.total_resumo['peso_pluma'])
        self.total_resumo['fardos_produzido'] = format_number(self.total_resumo['fardos_produzido'], 0)
        self.total_resumo['rendimento'] = format_number(self.total_resumo['rendimento'])
        self.total_resumo['peso_medio'] = format_number(self.total_resumo['peso_medio'])

    def _template_resumo(self):
        tb_item = []
        for item in self.data_resumo:
            tb_item.append(tb_resumo_row.format(**self._format_resumo(item)))

        itens = ''.join(tb_item)
        self._total_resumo()
        totais = tb_resumo_footer.format(**self.total_resumo)

        self.template_resumo = tb_resumo_header.format(itens=itens,
                                                       totais=totais)

    def _template_detalhe(self):
        algodoeira = ''
        algodoeira_old = ''
        tabelas = []
        itens = []

        for i in self.data_detalhe:

            if algodoeira == '':
                algodoeira = i['beneficiadora']
                algodoeira_old = algodoeira

            algodoeira = i['beneficiadora']

            if algodoeira != algodoeira_old:
                tabelas.append(tb_detalhe_header.format(algodoeira=algodoeira_old,
                                                        itens=''.join(itens)))
                algodoeira_old = algodoeira
                itens = []

            itens.append(tb_detalhe_row.format(**i))

        if len(itens):
            tabelas.append(tb_detalhe_header.format(algodoeira=algodoeira_old, itens=''.join(itens)))

        self.template_detalhe = ''.join(tabelas)

    def load_data(self):
        self._load_db_data()
        self.data_resumo = [self._parse_db_resumo(row) for row in self.db_resumo]
        self.data_detalhe = [self._parse_db_detalhe(row) for row in self.db_detalhe]

    def send_mail(self):
        self.load_data()
        self._template_resumo()
        self._template_detalhe()

        conteudo = body.format(tabela_resumo=self.template_resumo,
                               tabela_detalhes=self.template_detalhe)
        to = 'rogerio.cardoso@scheffer.agr.br;celio.sampaio@scheffer.agr.br;william.galleti@scheffer.agr.br'
        # to = 'william.galleti@scheffer.agr.br'
        subject = 'Qualidade de Beneficiamento - Boletim Diario'

        try:
            self.mail.send(subject, conteudo, to=to)
        except Exception as e:
            print(f"Erro ao enviar email para {to}. \n Erro: {e}")


boletim = Boletim()
