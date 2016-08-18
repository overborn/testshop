# -*- coding: utf-8 -*-
from datetime import datetime
from app import db


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3))
    description = db.Column(db.String(120))
    amount = db.Column(db.Float)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, amount, currency, description=''):
        self.amount = amount
        self.currency = currency
        self.description = description

    def __repr__(self):
        return u'<Invoice {}: {} {} {} [{}]>'.format(
            self.id, self.amount, self.currency, self.description, self.created
        )
