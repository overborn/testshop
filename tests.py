#!venv/bin/python
import os
import app
import json
import unittest
import tempfile
from app import db
from flask import url_for
from config import basedir
from app.models import Invoice

GOOD_REQUEST = json.loads('''{
    "client_price": 10.0,
    "created": "2015-08-18 18:58:54",
    "description": "description",
    "invoice_id": 1,
    "payway": "w1_uah",
    "processed": "2015-08-24 00:30:34",
    "ps_currency": 980,
    "ps_data": null,
    "shop_amount": 10.0,
    "shop_currency": 980,
    "shop_id": 300000,
    "shop_invoice_id": "1",
    "shop_refund": 9.8,
    "sign": "e63152bc42c86ab3033ff2a943812f5f",
    "status": 3,
    "test_add_on": "test!"
}''')

BAD_SIGN_REQUEST = json.loads('''{
    "client_price": 10.0,
    "created": "2015-08-18 18:58:54",
    "description": null,
    "invoice_id": 3,
    "payway": "w1_uah",
    "processed": "2015-08-24 00:30:34",
    "ps_currency": 980,
    "ps_data": null,
    "shop_amount": 10.0,
    "shop_currency": 980,
    "shop_id": 300000,
    "shop_invoice_id": "1",
    "shop_refund": 9.8,
    "sign": "182fb4f514bcbc86b70a90b66f116b0b",
    "status": 3,
    "test_add_on": "test!"
}''')

HEADERS = {
    'content-type': 'application/x-www-form-urlencoded'
}


class NotifyTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        app.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
            os.path.join(basedir, 'test.db')
        app.app.config['SERVER_NAME'] = 'myapp.test:5000'
        db.create_all()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])
        db.session.remove()
        db.drop_all()

    def test_bad_sign(self):
        """
        notify returns error when request is made with wrong sign
        """
        with app.app.app_context():
            rv = self.app.post(
                url_for("notify"), data=BAD_SIGN_REQUEST, headers=HEADERS)
            print rv.data
            assert 'WRONG SIGN' == rv.data

    def test_no_invoice(self):
        """
        notify returns error when no invoice for certain id found
        """
        with app.app.app_context():
            rv = self.app.post(
                url_for("notify"), data=GOOD_REQUEST, headers=HEADERS)
            assert 'ERROR' == rv.data

    def test_bad_invoice(self):
        """
        notify returns error when invoice params don't match request
        """
        inv = Invoice(10, '980', 'bad')
        db.session.add(inv)
        db.session.commit()
        with app.app.app_context():
            rv = self.app.post(
                url_for("notify"), data=GOOD_REQUEST, headers=HEADERS)
            assert 'ERROR' == rv.data

    def test_good_invoice(self):
        """
        notify returns OK when invoice matches request
        """
        inv = Invoice(10, '980', 'description')
        db.session.add(inv)
        db.session.commit()
        with app.app.app_context():
            rv = self.app.post(
                url_for("notify"), data=GOOD_REQUEST, headers=HEADERS)
            print rv.data
            assert 'OK' == rv.data

if __name__ == '__main__':
    unittest.main()
