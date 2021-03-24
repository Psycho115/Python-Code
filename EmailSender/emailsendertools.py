#-*- coding: gb18030 -*-

import smtplib
from email.MIMEText import MIMEText
from email.mime.multipart import MIMEMultipart
from email.Header import Header


class EmailSenderBase:

    def __init__(self):        
        self.mail_receivers = []
        self.mail_attachments = []

    def AddReceiver(self, receiver):        
        self.mail_receivers.extend(receiver)
        print self.mail_receivers

    def AddAttachment(self, attachment):
        self.mail_attachments.extend(attachment)
        print self.mail_attachments
    
    def SetMessage(self, text_type, subject, message):
        self.message = MIMEMultipart()
        self.message["From"] = self.mail_sender
        self.message["To"] = ",".join(self.mail_receivers)
        self.message["Subject"] = subject
        if text_type == "text":
            self.message.attach(MIMEText(message, 'plain', 'gb18030'))
        elif text_type == "html":
            self.message.attach(MIMEText(message, 'html', 'gb18030'))
        else: 
            print "type not found, use 'text' instead"
            self.message.attach(MIMEText(message, 'plain', 'gb18030'))

    def SetAttachment(self):
        for filepath in self.mail_attachments:
            att = MIMEText(open(filepath,'rb').read(), 'base64', 'gb18030')
            filename = filepath.split("/")[0]
            att["Content-Type"] = 'application/octet-stream'
            # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
            att["Content-Disposition"] = 'attachment; filename="{0}"'.format(filename)
            self.message.attach(att)


class EmailSender_126(EmailSenderBase):

    mail_host = "smtp.126.com"
    mail_port = 25
    mail_user = "tangjingzhe_@126.com"
    mail_pass = "ivan+901206"
    mail_sender = "tangjingzhe_@126.com"

    def __init__(self):        
        EmailSenderBase.__init__(self)

    def SendEmail(self):
        if len(self.mail_attachments):
            self.SetAttachment()  
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.mail_host, self.mail_port)
            smtpObj.login(self.mail_user,self.mail_pass) 
            smtpObj.sendmail(self.mail_sender, self.mail_receivers, self.message.as_string())
            print "Email sent!"
        except smtplib.SMTPException as error:
            print "Failed with error {0}".format(error)
        
    

