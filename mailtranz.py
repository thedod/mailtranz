#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mtconfig import *
import os,cgi
from mysender import send
import pystache
stache = pystache.Renderer(
    search_dirs=TEMPLATE_FOLDER,file_encoding='utf-8',string_encoding='utf-8',file_extension=False)

def make_multipart_mail(headers, text=None, html=None):
    """Construct a multipart mail message with text and HTML parts.
    @param headers {dict} A mapping with, at least: "To", "Subject" and
        "From", header values. "To", "Cc" and "Bcc" values must be *lists*,
        if given.
    @param text {str} The text email content.
    @param html {str} The HTML email content.
    
    Derived from <http://code.activestate.com/recipes/576931-send-a-multipart-email/>
    """
    from email.MIMEMultipart import MIMEMultipart
    from email.MIMEText import MIMEText
    import smtplib
    
    if text is None and html is None:
        raise ValueError("neither `text` nor `html` content was given for "
            "sending the email")
    if not ("To" in headers and "From" in headers and "Subject" in headers):
        raise ValueError("`headers` dict must include at least all of "
            "'To', 'From' and 'Subject' keys")

    # Create the root message and fill in the from, to, and subject headers
    msg_root = MIMEMultipart('related')
    for name, value in headers.items():
        msg_root[name] = isinstance(value, list) and ', '.join(value) or value
    msg_root.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want
    # to display.
    msg_alternative = MIMEMultipart('alternative')
    msg_root.attach(msg_alternative)

    # Attach HTML and text alternatives.
    if text:
        msg_text = MIMEText(text.encode('utf-8'), 'plain', 'utf-8')
        msg_alternative.attach(msg_text)
    if html:
        msg_text = MIMEText(html.encode('utf-8'), 'html', 'utf-8')
        msg_alternative.attach(msg_text)
    return msg_root

def is_ssl(env):
    return env.get('HTTPS','').lower()=='on' or env.get('HTTP_HTTPS','').lower()=='on'

def main():
    try:
        scriptname=os.environ['SCRIPT_NAME']
    except: 
        raise Exception,'Program should run as a cgi'
    if DEBUG:
        import cgitb; cgitb.enable()
    else: # should be POST and SSL (unless DEBUG)
        if os.environ['REQUEST_METHOD']=='GET':
            print 'Content-type: text/html; charset=utf-8\n'
            print stache.render(stache.load_template('error.html'),{ 'message':MSG_ERROR_NOT_POST }).encode('utf-8')
            return
        if not is_ssl(os.environ):
            print 'Content-type: text/html; charset=utf-8\n'
            print stache.render(stache.load_template('error.html'),{ 'message':MSG_ERROR_NOT_SSL }).encode('utf-8')
            return
    try:
        basescriptname=scriptname.rsplit('/',1)[-1]
        scriptname_map = SCRIPTNAME_MAPS[basescriptname]
    except Exception,e:
        print 'Content-type: text/html; charset=utf-8\n'
        print stache.render(stache.load_template('error.html'),{
            'message': DEBUG and str(e) or str(type(e))
        }).encode('utf-8')
        return
    fields = []
    ref = '???'
    form = cgi.FieldStorage()
    for fielddef  in TRANZFIELDS:
        val = unicode(form.getvalue(fielddef['id'],''),'utf-8')
        if val:
            field = {'value':val}
            field.update(fielddef)
            fields.append(field)
            if fielddef['id']==scriptname_map['ref']:
                ref = val

    subject = '{0}: {1}'.format(scriptname_map['subject'],ref)
    text = stache.render(stache.load_template('message.txt'),{ 'fields': fields })
    html = stache.render(stache.load_template('message.html'),{ 'fields': fields })
    msg = make_multipart_mail({'From':[SMTP_FROM], 'To':SMTP_TOS, 'Subject':subject}, text, html)
    try:
        send(msg, SMTP_HOST, SMTP_PORT, SMTP_KEYFILE, SMTP_CERTFILE, SMTP_USERNAME, SMTP_PASSWORD)
    except Exception,e:
        print 'Content-type: text/html; charset=utf-8\n'
        print stache.render(stache.load_template('error.html'),{
            'message': DEBUG and str(e) or str(type(e))
        }).encode('utf-8')
        return
    print 'Location: {0}\n'.format(scriptname_map['redirect'])    

if __name__ == '__main__':
    main()
