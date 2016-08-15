from datetime import datetime
from sqlalchemy.ext.hybrid import hybrid_property
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

    @hybrid_property
    # @property
    def invoice_id(self):
        # try:
        if self.created:
            return "{}:{}".format(self.id, self.created.strftime("%s"))
        # except AttributeError:
        #     print self

    def __repr__(self):
        return '<Invoice {}: {} {} [{}]>'.format(
            self.id, self.amount, self.currency, self.created)
