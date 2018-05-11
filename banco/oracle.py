import cx_Oracle
from decouple import config


class Database:

    def __init__(self):
        self.host = config('DB_HOST')
        self.port = config('DB_PORT')
        self.service = config('DB_SERVICE')
        self.user = config('DB_USER')
        self.pwd = config('DB_PASS')

        self.connection(rac=True)

    def tns(self):
        self.tns = cx_Oracle.makedsn(self.host, self.port, service_name=self.service)

    def connection(self, rac=False):
        self.tns()
        try:
            self.connection = cx_Oracle.connect(self.user, self.pwd, self.tns, threaded=rac)
        except cx_Oracle.DatabaseError as e:
            self.connection = None
            print(e)
            exit(1)

    def disconnect(self):
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
