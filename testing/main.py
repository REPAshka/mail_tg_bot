import imaplib
import email
import quopri


imap_server = "imap.mail.ru"
email_server = "timyr4eggg@mail.ru"
email_password = "hzfAj92CVgmYj9qFIgRR"

# imap_server = "imap.mail.ru"
# email_server = "testsurename2000@mail.ru"
# email_password = "mKRXxsHGhkrgHgkaBhs9"

imap = imaplib.IMAP4_SSL(imap_server)
imap.login(email_server, email_password)

imap.select("Inbox")
#imap.select("Sent")

_, msgs = imap.search(None, "ALL")

message_number = 0

print(len(msgs[0].split()))

for msg in msgs[0].split()[::-1]:
    message_number += 1
    if message_number < 5:
        _, data = imap.fetch(msg, "RFC822")

        message = email.message_from_bytes(data[0][1])

        print(message)
        print(f"Message Number: {msg}")
        print(f"From: {message.get('From')}")
        print(f"To: {message.get('To')}")
        print(f"BCC: {message.get('BCC')}")
        print(f"Date: {message.get('Date')}")
        print(f"Subject: {message.get('Subject')}")

        print("Content:")
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                print(part.as_string())

imap.close()

#if __name__ == '__main__':


import email.parser
msg = email.parser.BytesParser().parsebytes(msg_bytes)

# get a bytes object containing the base64-decoded message
textbytes = msg.get_payload(decode=True)

# get the content charset
content_charset = msg.get_content_charset()

# decode the text to obtain a string object
text = textbytes.decode(content_charset)