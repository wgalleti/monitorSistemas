from O365 import Message
from decouple import config

class Email365:

    def __init__(self):
        """
        Inicializa classe app recebendo informações do arquivo .env e inicia conexão
        """
        self.user = config('EMAIL_USER')
        self.pwd = config('EMAIL_PASS')
        self.to_email = config('EMAIL_TO')

    def send(self, subject, body):
        """
        Envia email
        :param subject: titulo de mensagem
        :param body: corpo do email
        :return: objeto de email
        """
        m = Message(auth=(self.user, self.pwd))
        m.setRecipients(self.to_email)
        m.setSubject(subject)
        m.setBodyHTML(body)
        m.sendMessage()

        return m
