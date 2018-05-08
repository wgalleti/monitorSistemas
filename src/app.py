import cx_Oracle
from O365 import Message
from decouple import config


class App(object):

    def __init__(self):
        """
        Inicializa classe app recebendo informações do arquivo .env e inicia conexão
        """
        self._host = config('DB_HOST')
        self._port = config('DB_PORT')
        self._service = config('DB_SERVICE')
        self._user = config('DB_USER')
        self._pass = config('DB_PASS')
        self._user_email = config('EMAIL_USER')
        self._pass_email = config('EMAIL_PASS')
        self._to_email = config('EMAIL_TO')

        self.make_connection()

    def _make_tns(self):
        """
        Monta TNS de conexão
        """
        self.tns = cx_Oracle.makedsn(self._host, self._port, service_name=self._service)

    def make_connection(self):
        """
        Inicia conexão com banco de dados ou finaliza aplicação
        """
        self._make_tns()
        try:
            self.connection = cx_Oracle.connect(self._user, self._pass, self.tns, threaded=True)
        except cx_Oracle.DatabaseError as e:
            self.connection = None
            print(e)
            exit(1)

    def disconnect(self):
        """
        Disconecta do banco de dados
        """
        self.connection.close()

    def delete(self, sql, filter):
        """
        Executa comando Delete
        :param sql: comando a ser executado
        :param filter: filtros a serem aplicados no comando
        :return: Quantidade de registros apagados
        """

        if 'delete' not in sql.lower():
            print('Comando DELETE inválido!')
            return 0

        cursor = self.connection.cursor()
        cursor.execute(sql, filter)
        self.connection.commit()

        return cursor.rowcount

    def query(self, sql, filters):
        """
        Executa comando SQL para aplicação
        :param sql: comando a ser executado
        :param filters: filtros a serem aplicados no comando
        :return: lista de dados
        """

        if 'select' not in sql.lower():
            print('Comando SQL inválido!')
            return []

        cursor = self.connection.cursor()
        cursor.execute(sql, filters)
        columns = [col[0].lower() for col in cursor.description]

        data = [dict(zip(columns, row)) for row in cursor.fetchall()]

        for i in enumerate(data):
            for c in columns:
                if type(data[i[0]][c]) == cx_Oracle.LOB:
                    data[i[0]][c] = data[i[0]][c].read()

        return data

    def send_mail(self, subject, body):
        """
        Envia email
        :param subject: titulo de mensagem
        :param body: corpo do email
        :return: objeto de email
        """
        m = Message(auth=(self._user_email, self._pass_email))
        m.setRecipients(self._to_email)
        m.setSubject(subject)
        m.setBodyHTML(body)
        m.sendMessage()

        return m
