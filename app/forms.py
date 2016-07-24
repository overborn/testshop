# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import (
    TextField, SelectField, FloatField, DecimalField, HiddenField, IntegerField
)
from wtforms.validators import Required, NumberRange
from wtforms_components import read_only


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


class ReadonlyForm(Form):
    def __init__(self, *args, **kwargs):
        super(ReadonlyForm, self).__init__(*args, **kwargs)
        for field in self:
            read_only(field)
        self.currency_name.widget = DisabledWidget(self.currency_name.widget)


class WlForm(ReadonlyForm):
    WMI_MERCHANT_ID = HiddenField()
    WMI_PAYMENT_AMOUNT = FloatField('Amount')
    WMI_CURRENCY_ID = HiddenField()
    currency_name = SelectField('Currency', choices=[
        ('980', 'uah'), ('643', 'rub')], default='980')
    WMI_PAYMENT_NO = HiddenField()
    WMI_PTENABLED = HiddenField()
    WMI_SIGNATURE = HiddenField()
    WMI_FAIL_URL = HiddenField()
    WMI_SUCCESS_URL = HiddenField()


class TIPForm(ReadonlyForm):
    amount = FloatField()
    currency_name = SelectField(choices=[('980', 'uah'), ('643', 'rub')])
    currency = HiddenField()
    description = TextField()
    shop_id = HiddenField()
    sign = HiddenField()
    shop_invoice_id = HiddenField()
