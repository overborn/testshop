# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import TextField, SelectField, FloatField, IntegerField
from wtforms.validators import Required, NumberRange, URL


class InvoiceForm(Form):
    amount = FloatField("Amount", validators=[Required(), NumberRange(min=0)])
    currency = SelectField(choices=[('980', 'uah'), ('643', 'rub')])
    description = TextField('Description', validators=[Required()])


class WlForm(Form):
    WMI_MERCHANT_ID = IntegerField(validators=[Required()])
    WMI_PAYMENT_AMOUNT = FloatField(validators=[Required(), NumberRange(min=0)])
    WMI_CURRENCY_ID = IntegerField(validators=[Required()])
    WMI_PAYMENT_NO = IntegerField(validators=[Required()])
    WMI_PTENABLED = TextField(validators=[Required()])
    WMI_SIGNATURE = TextField(validators=[Required()])
    WMI_FAIL_URL = TextField(validators=[Required(), URL()])
    WMI_SUCCESS_URL = TextField(validators=[Required(), URL()])


class TIPForm(Form):
    amount = FloatField("Amount", validators=[Required(), NumberRange(min=0)])
    currency = SelectField(choices=[('980', 'uah'), ('643', 'rub')])
    shopId = TextField(validators=[Required()])
    sign = TextField(validators=[Required()])
    shop_invoice_id = TextField(validators=[Required()])
    description = TextField('Description', validators=[Required()])

"""
Добрый день, Виталий.
Вы были правы, в документации указано верно.
я поначалу смотрел список параметров для запроса pre_invoice, который, насколько я понял, мне использовать при выполнении тестового задания не нужно.

появились еще вопросы.
написано, что сервис должен состоять из одной страницы.
в то же время мне предлагается генерировать форму, и подтверждать ее.
потому хотел уточнить
сейчас моя реализация предусматривает, что при получении успшного ответа от https://central.pay-trio.com/invoice 
приложение перенаправляет на страницу с формой, содержащей данные из ответа, которую должен подтвердить пользователь.
это нормально?
стоит ли это переписывать, чтоб форма подтягивалась например аяксом на ту же страницу?
"""