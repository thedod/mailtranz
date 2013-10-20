# -*- coding: utf-8 -*-
DEBUG = False
TEMPLATE_FOLDER = 'templates'
SMTP_HOST = 'mail.example.com'
SMTP_PORT = 465
SMTP_KEY = None # [if relevant] file path
SMTP_CERT = None # ditto
SMTP_USERNAME = 'me@example.com'
SMTP_PASSWORD = '*******'

SMTP_FROM = 'me@example.com'
SMTP_TOS = ['me@example.com','accounting@example.com']

MSG_ERROR_NOT_POST = 'שימוש לא נכון במערכת.'
MSG_ERROR_NO_SSL = 'גישה לא מאובטחת למערכת.'

SCRIPTNAME_MAPS = {
    'success.cgi': {'subject':'[Transaction] Success','title':'פרטי עיסקה שבוצעה','ref':'Tempref','redirect':'http://example.com/shop-thankyou'},
    'fail.cgi': {'subject':'[Transaction] Failure','title':'פרטי עיסקה שנכשלה','ref':'Tempref','redirect':'http://example.com/shop-error'}
}

TRANZFIELDS = [
    {u'id':u'Tempref', u'name':u'אסמכתא', u'default':u'???'},
    {u'id':u'Response', u'name':u'קוד תגובה', u'default':u'???'},
    {u'id':u'Confirmation', u'name':u'קוד אישור', u'default':u'???'},
    {u'id':u'pdesc', u'name':u'מוצר', u'default':u'???',u'hexencoded': True},
    {u'id':u'sum', u'name':u'סכום', u'default':u'???'},
    {u'id':u'contact', u'name':u'שם', u'default':u'???', u'rtl':True},
    {u'id':u'email', u'name':u'דואל', u'default':u'???'},
    {u'id':u'phone', u'name':u'טלפון'},
    {u'id':u'address', u'name':u'כתובת', u'rtl':True},
    {u'id':u'city', u'name':u'עיר', u'rtl':True},
    {u'id':u'remarks', u'name':u'הערות', u'rtl':True}
]
