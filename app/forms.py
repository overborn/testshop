# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import (
    TextField, SelectField, DecimalField
)
from wtforms.validators import Required, NumberRange


class InvoiceForm(Form):
    amount = DecimalField("Amount", validators=[
        NumberRange(min=0)])
    currency = SelectField(choices=[('980', 'uah'), ('643', 'rub')])
    description = TextField('Description', validators=[Required()])
