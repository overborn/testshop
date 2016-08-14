# -*- coding: utf8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

CSRF_ENABLED = True
SECRET_KEY = '4p((iuz0xcp8_1q3e*qfwn3*=60_83(etr_7+2*pvx)i(xc&34'

# shop config
SHOP_KEY = '0PtrdGkiMB9jGcDUJkrIJwQRwPVl0HOkT'
SHOP_ID = '301155'

UAH_INVOICE_URL = 'https://central.pay-trio.com/invoice'
TIP_URL = "https://tip.pay-trio.com/ru/"
