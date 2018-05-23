from smtplib import SMTPException
from django.core.mail import EmailMessage
from django.template.loader import get_template
from threading import Thread
from api.monitor import settings


class SendEmail(Thread):

    def __init__(self, email_to, nome_destinatario, title, template, context=None):
        self.email_to = email_to
        self.nome_destinatario = nome_destinatario
        self.context = dict(data=context)
        self.title = title
        self.template = template
        Thread.__init__(self)

    def run(self):
        template = get_template(self.template)
        message_html = template.render(self.context)

        email = EmailMessage(self.title, message_html, settings.DEFAULT_FROM_EMAIL, [self.email_to])
        email.content_subtype = 'html'

        try:
            email.send()
        except SMTPException as e:
            # por log
            pass