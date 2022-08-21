import re
import configparser
from imbox import Imbox
from html2text import html2text

config = configparser.ConfigParser()
config.read('config_mail_bot.ini', encoding='utf-8-sig')


class Reader(object):
    """ Reads the email and stuff. """

    def __init__(self, userName, userPassword):
        self.inbox = Imbox("imap.mail.ru", username=userName, password=userPassword, ssl=True)
        self.getMessages()

    def getMessages(self):
        self.all_inbox_messages = self.inbox.messages()
        return self.all_inbox_messages

    def listMessageIds(self,msg_count):
        """ More or less debug. """
        for uid, message in self.all_inbox_messages[:-msg_count:-1]:
            # print('sent_from_name', message.sent_from[0]['name'])
            # print('sent_from_mail', message.sent_from[0]['email'])
            # print('sent_to_name', message.sent_to[0]['name'])
            # print('sent_to_email', message.sent_to[0]['email'])
            print('subject', message.subject)
            # print('date', message.date)
            # print('body_plain', message.body['plain'])
            # print('attachments', message.attachments)
            if len(message.body['html']) > 0:
                phrase1 = " ".join(re.sub(r'\||\---|\[|\]', '', message.body['html'][0]).split())
                print(" ".join((html2text(phrase1)).split()))
                print(re.sub(r'- ', '-', phrase1))
                phrase1 = re.sub(r'http\S+', '', phrase1, flags=re.MULTILINE)
                print(re.sub(r'!«\w+».|!\w+|\\-', '', phrase1))
                # phrase = re.sub(r'http\S+', '', html2text(message.body['html'][0]), flags=re.MULTILINE)
                # phrase = " ".join(re.sub(r'\||\---|\[|\]', '', phrase).split())
                # print(re.sub(r'!«\w+».|!\w+|\\-', '', phrase))
                # print("##########################################################################")
            elif len(message.body['plain']) > 0:
                phrase1 = " ".join(re.sub(r'\||\---|\[|\]', '', message.body['plain'][0]).split())
                print(" ".join((html2text(phrase1)).split()))
                print(re.sub(r'- ', '-', phrase1))
                phrase1 = re.sub(r'http\S+', '', phrase1, flags=re.MULTILINE)
                print(re.sub(r'!«\w+».|!\w+|\\-', '', phrase1))
                # phrase = re.sub(r'http\S+', '', html2text(message.body['plain'][0]), flags=re.MULTILINE)
                # phrase = " ".join(re.sub(r'\||\---|\[|\]', '', phrase).split())
                # print(re.sub(r'!«\w+».|!\w+|\\-', '', phrase))
                # print("##########################################################################")


Me = Reader(userName=config.get('mail_ru', 'user'), userPassword=config.get('mail_ru', 'password'))
Me.listMessageIds(5)