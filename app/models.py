from app import db


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency = db.Column(db.String(3))
    description = db.Column(db.String(120))
    amount = db.Column(db.Integer)

    def __repr__(self):
        return '<Invoice %s %s>' % (self.id, self.amount)
