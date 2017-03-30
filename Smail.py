#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#python3
import sys
import os
import smtplib
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.text import MIMEText
from email.header import Header
from email import encoders

class Smail():

    def __init__(self):
        self.set_mail_type()
        self.set_charset()
        self.server_from_addr=None
        self.server_to_addrs=[]
        self.to_addr=[]
        self.cc_addr=[]
        self.bcc_addr=[]
        self.attachment_list=[]
        self.attachment_num=0


    def set_server(self,server,port,smtp_user,smtp_pass,time_out=600,try_time=3):
        self.smtp_server=server
        self.smtp_port=port
        self.smtp_user=smtp_user
        self.smtp_pass=smtp_pass
        self.try_time=try_time
        self.time_out=time_out
        if self.server_from_addr == None:
            self.server_from_addr = self.smtp_user

    def set_mail_type(self,mail_type='plain'):
        self.mail_type=mail_type
    def set_charset(self,charset='utf-8'):
        self.charset=charset



    def set_subject(self,subject):
        self.subject=subject.encode(self.charset)
    def set_content(self,content):
        self.content=content.encode(self.charset)
    def set_server_from_addr(self,from_addr):
        self.server_from_addr=from_addr

    def add_to_addr(self,to_addr):
        self.to_addr.append(to_addr)
        self.server_to_addrs.append(to_addr)
    def add_cc_addr(self,cc_addr):
        self.cc_addr.append(cc_addr)
        self.server_to_addrs.append(cc_addr)
    def add_bcc_addr(self,bcc_addr):
        self.bcc_addr.append(bcc_addr)
        self.server_to_addrs.append(bcc_addr)

    def add_attachment(self,filepath,filename=None):
        if filename == None:
            filename=os.path.basename(filepath)

        with open(filepath,'rb') as f:
            file=f.read()

        ctype, encoding = mimetypes.guess_type(filepath)
        if ctype is None or encoding is not None:ctype = "application/octet-stream"
        maintype, subtype = ctype.split('/', 1)

        if maintype == "text":
            with open(filepath) as f:file=f.read()
            attachment = MIMEText(file, _subtype=subtype)
        elif maintype == "image":
            with open(filepath,'rb') as f:file=f.read()
            attachment = MIMEImage(file, _subtype=subtype)
        elif maintype == "audio":
                with open(filepath,'rb') as f:file=f.read()
                attachment = MIMEAudio(file, _subtype=subtype)
        else:
                with open(filepath,'rb') as f:file=f.read()
                attachment = MIMEBase(maintype,subtype)
                attachment.set_payload(file)
                attachment.add_header('Content-Disposition', 'attachment', filename=filename)
                encoders.encode_base64(attachment)

        attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        attachment.add_header('Content-ID',str(self.attachment_num))
        self.attachment_num+=1

        self.attachment_list.append(attachment)

    def create_only_img_mail(self):
        html=''
        for attachment_id in range(self.attachment_num):
            html=html + '<p><img src="cid:{}"></p>'.format(attachment_id)
        html='<html><body>' + html + '</body></html>'
        self.mail_type='html'
        self.content=html


    def send(self):
        if len(self.attachment_list) == 0:
            self.msg = MIMEText(self.content, self.mail_type, self.charset)
        else:
            self.msg = MIMEMultipart()
            self.msg.attach(MIMEText(self.content, self.mail_type, self.charset))
            for attachment in self.attachment_list:
                self.msg.attach(attachment)

        self.msg['Subject'] =Header(self.subject,self.charset)
        self.msg['From'] = self.server_from_addr
        self.msg['To'] = ",".join(self.to_addr)
        if self.cc_addr:
            self.msg['cc'] = ",".join(self.cc_addr)
        if self.bcc_addr:
            self.msg['bcc'] = ",".join(self.bcc_addr)

        #send
        for a in range(self.try_time):
            try:
                if self.smtp_port == 25:
                    server = smtplib.SMTP(self.smtp_server, self.smtp_port,timeout=self.time_out)
                else:
                    server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port,timeout=self.time_out)
                #server.set_debuglevel(1)
                server.login(self.smtp_user,self.smtp_pass)
                server.sendmail(self.server_from_addr,self.server_to_addrs,self.msg.as_string())
                server.quit()
                break
            except Exception as e:
                print(e)

