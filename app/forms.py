# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import (
    TextField, SelectField, FloatField, IntegerField, DecimalField, HiddenField
)
from wtforms.validators import Required, NumberRange


class DisabledWidget(object):
    def __init__(self, widget):
        self.widget = widget

    def __getattr__(self, name):
        return getattr(self.widget, name)

    def __call__(self, field, **kwargs):
        kwargs.setdefault('disabled', True)
        return self.widget(field, **kwargs)


class InvoiceForm(Form):
    amount = DecimalField("Amount", validators=[
        NumberRange(min=0)])
    currency = SelectField(choices=[('980', 'uah'), ('643', 'rub')])
    description = TextField('Description', validators=[Required()])


class WlForm(Form):
    WMI_MERCHANT_ID = IntegerField()
    WMI_PAYMENT_AMOUNT = FloatField()
    WMI_CURRENCY_ID = IntegerField()
    WMI_PAYMENT_NO = IntegerField()
    WMI_PTENABLED = TextField()
    WMI_SIGNATURE = TextField()
    WMI_FAIL_URL = TextField()
    WMI_SUCCESS_URL = TextField()


class TIPForm(Form):
    amount = FloatField()
    currency = SelectField(choices=[('980', 'uah'), ('643', 'rub')])
    description = TextField()
    shop_id = HiddenField()
    sign = HiddenField()
    shop_invoice_id = HiddenField()

    def __init__(self, *args, **kwargs):
        super(TIPForm, self).__init__(*args, **kwargs)
        for field in self:
            field.widget = DisabledWidget(field.widget)
