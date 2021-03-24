#-*- coding: gb18030 -*-

from emailsendertools import EmailSender_126


if __name__=='__main__':
    
    emailsender = EmailSender_126()
    message = """
    sffhfhhghsghjs
    dasdgasdgfaerg
    rgarg
    """

#    f = open("大米.m4a", "rb")
#    f.close()
    emailsender.AddReceiver(["393942656@qq.com"])
    #emailsender.AddAttachment(["大米.m4a"])
    emailsender.SetMessage("text", "Python Try", message)
    emailsender.SendEmail()