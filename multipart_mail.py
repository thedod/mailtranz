#!/usr/bin/env python
# -*- coding: utf-8 -*-
def make_multipart_mail(headers, text=None, html=None):
    """Send an email -- with text and HTML parts.
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

def testmsg():
    thetext = u'זה עברית and English יחד'
    thehtml = u'<div dir="rtl">{0}</div>'.format(thetext)
    theheaders = {
        'From':['sari@calltext.co.il'],
        'To':['unclezzzen@gmail.com'],
        'cc':['dod_zzzen@f-m.fm'],
        'Subject':'Testing multipart'}
    m=make_multipart_mail(theheaders,thetext,thehtml)
    return m

if __name__ == '__main__':
    print testmsg().as_string()
