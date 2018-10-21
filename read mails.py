import imaplib
import base64
import os
import sys
import quopri
from html.parser import HTMLParser
import email
import collections
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import mimetypes
import email.mime.application

email_user = input('Email: ')
email_pass = input('Password: ')

mail = imaplib.IMAP4_SSL("imap.gmail.com",993)

mail.login(email_user, email_pass)

#select label from all the labels fetched
type, data = mail.list()
labels = []
for label in data:
    labels.append(label.decode('utf-8').split()[2].strip('\"'))
mail.select(labels[labels.index('INBOX')])

#get ids of all the mails in selected mailbox
searchQuery = '(FROM "Flipkart")'
type, data = mail.uid('search', None, 'ALL')   # mail.uid('search', None, searchQuery) if searching for given condition
mail_ids = data[0]
id_list = mail_ids.split()


#print headers
group = collections.Counter()
for num in data[0].split():
    typ, data = mail.uid('fetch',num, '(RFC822)' )
    try:
        msg = email.message_from_string(data[0][1].decode('utf-8'))
        email_subject = msg['subject']
        email_from = msg['from']
        group[email_from] += 1
        print ('From : ' + email_from + '\n')
        print ('Subject : ' + email_subject + '\n')
        print('Date : '+ msg['date']+'\n')
        move_from_old_label_to_new(num, new_label)
        download_attachment(msg)
        get_urls(msg)
    except Exception as e:
        print(e)
mail.close()
mail.logout()

#rename label
def rename_label(old_label_name,new_label_name):
    mail.rename(old_label_name, new_label_name)
 
# create new label
def create_label(label_name):
    mail.create(label_name)


def download_attachment(email_message):
    # downloading attachments
    for part in email_message.walk():
        # this part comes from the snipped I don't understand yet... 
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()

        if bool(fileName):
            filePath = os.path.join('/Users/sanketdoshi/python/attachments/', fileName)
            if not os.path.isfile(filePath) :
                fp = open(filePath, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()

        subject = str(email_message).split("Subject: ", 1)[1].split("\nTo:", 1)[0]
        print('Downloaded "{file}" from email titled "{subject}" with UID {uid}.'.format(file=fileName, subject=subject, uid=latest_email_uid.decode('utf-8')))


#get any html tags links 
class parseLinks(HTMLParser):
    def handle_starttag(self, tag, attrs):
        global global_futures_fair_value
        if tag == 'a':
            for name, value in attrs:
                if name == 'href':
                    print(name)
                    print(value)
def get_urls(msg):
    msg = str(msg.get_payload()[0])
    msg = quopri.decodestring(msg)
    linkParser = parseLinks()
    linkParser.feed(msg.decode('utf-8'))


#move from one label to another
def move_from_old_label_to_new(uid, new_label):
    result = mail.uid('COPY',uid, new_label)
    if result[0] == 'OK':
        #deletes mail from previous label
        mov, data = mail.uid('STORE', uid , '+FLAGS', '(\Deleted)')
        mail.expunge()


# send mail
def send_mail():
    smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
    smtp_ssl_port = 465
    s = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
    s.login(email_user, email_pass)

    msg = MIMEMultipart()
    msg['Subject'] = 'I have a picture'
    msg['From'] = email_user
    msg['To'] = email_user

    txt = MIMEText('I just bought a new camera.')
    msg.attach(txt)

    filename = 'introduction-to-algorithms-3rd-edition-sep-2010.pdf' #path to file
    fo=open(filename,'rb')
    attach = email.mime.application.MIMEApplication(fo.read(),_subtype="pdf")
    fo.close()
    attach.add_header('Content-Disposition','attachment',filename=filename)
    msg.attach(attach)
    s.send_message(msg)
    s.quit()

