import re
from configparser import ConfigParser
from imbox import Imbox
from html2text import html2text

config = ConfigParser()
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
        def clear_msg(msg):
            phrase = html2text(msg[0])
            phrase = " ".join(re.sub(r'\||\---|\[|\]|', '', phrase).split())  # чистка от скобок
            phrase = " ".join(re.sub(r'- ', '-', phrase).split())  # чиним ломанные ссылки
            phrase = re.sub(r'http://image', '', phrase, flags=re.MULTILINE)  # удаляем картинки
            phrase = re.sub(r'\.png|\.jpg', '', phrase)  # удаляем оставшиеся картинки
            phrase = re.sub(r'!«\w+».|!\w+|\\-', '', phrase)  # чистим от мусора
            for val in phrase.split():
                if len(re.findall(r'http\S+', val)) > 0:
                    #print(val)
                    for link_val in re.split(r'[\(,\)]', val):
                        if (re.match(r'https\S+|http\S+', link_val)) and len(link_val) > 70:
                            # print('VAAAAAAAL', link_val, len(link_val))
                            phrase = phrase.replace(val, '')  # удалить длинные ссылки
            print(phrase)
            print("##########################################################################")

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
                clear_msg(message.body['html'])
            elif len(message.body['plain']) > 0:
                clear_msg(message.body['plain'])



Me = Reader(userName=config.get('mail_ru', 'user'), userPassword=config.get('mail_ru', 'password'))
Me.listMessageIds(5)
