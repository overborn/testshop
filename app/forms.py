from flask_wtf import Form
from wtforms import DecimalField, TextField, SelectField, FloatField, IntegerField
from wtforms.validators import Required, NumberRange, URL


class InvoiceForm(Form):
    currency = SelectField(choices=[('980', 'uah'), ('643', 'rub')])
    amount = FloatField("Amount", validators=[Required(), NumberRange(min=0)])
    description = TextField('Description', validators=[Required()])


class CheckoutForm(Form):
    WMI_MERCHANT_ID = IntegerField(validators=[Required()])
    WMI_PAYMENT_AMOUNT = FloatField(validators=[Required(), NumberRange(min=0)])
    WMI_CURRENCY_ID = IntegerField(validators=[Required()])
    WMI_PAYMENT_NO = IntegerField(validators=[Required()])
    WMI_PTENABLED = TextField(validators=[Required()])
    WMI_SIGNATURE = TextField(validators=[Required()])
    WMI_FAIL_URL = TextField(validators=[Required(), URL()])
    WMI_SUCCESS_URL = TextField(validators=[Required(), URL()])

"""
<input name="WMI_MERCHANT_ID" value="194260758738"/>
<input name="WMI_PAYMENT_AMOUNT" value="10.00"/>
<input name="WMI_CURRENCY_ID" value="980"/>
<input name="WMI_PAYMENT_NO" value="39"/>
<input name="WMI_PTENABLED" value="WalletOneUAH"/>
<input name="WMI_SIGNATURE" value=" ThBrO9NKIjxtIzvuqYcCyA=="/>
"""
