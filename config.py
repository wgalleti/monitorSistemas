import cx_Oracle
from O365 import Message
from decouple import config


class Config(object):

    def __init__(self):
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
        self.tns = cx_Oracle.makedsn(self._host, self._port, service_name=self._service)

    def make_connection(self):
        self._make_tns()
        try:
            self.connection = cx_Oracle.connect(self._user, self._pass, self.tns, threaded=True)
        except:
            self.connection = None

    def delete(self, sql, filter):
        cursor = self.connection.cursor()
        cursor.execute(sql, filter)
        self.connection.commit()

        return cursor.rowcount

    def query(self, sql, filters):
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
        m = Message(auth=(self._user_email, self._pass_email))
        m.setRecipients(self._to_email)
        m.setSubject(subject)
        m.setBodyHTML(body)
        m.sendMessage()

        return m
