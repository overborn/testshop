# -*- coding: utf-8 -*-
import hashlib, requests, json

from flask import (
    render_template, request, jsonify
)

from app import app, db
from models import Invoice
from config import SHOP_ID, SHOP_KEY, UAH_INVOICE_URL, TIP_URL
from forms import InvoiceForm


INVOICE_KEYS = ("shop_id", "amount", "currency", "payway", "shop_invoice_id")
TIP_KEYS = ('amount', 'currency', 'shop_id', 'shop_invoice_id')


def _get_sign(req, keys_required, secret=SHOP_KEY):
    keys_sorted = sorted(keys_required)
    string_to_sign = ":".join(
        [str(req[k]).encode("utf8") for k in keys_sorted]) + secret
    app.logger.info("string_to_sign: {}".format(string_to_sign))
    sign = hashlib.md5(string_to_sign).hexdigest()
    return sign


@app.route("/", methods=('GET',))
def index():
    form = InvoiceForm()
    return render_template("index.html", form=form)


@app.route("/check", methods=('POST', ))
def check():
    form = InvoiceForm()
    if form.validate_on_submit():
        invoice = Invoice(
            form.data['amount'],
            form.data['currency'],
            form.data['description']
        )
        db.session.add(invoice)
        db.session.commit()
        app.logger.info(u"invoice created: {}".format(invoice))

        payload = {
            "shop_id": SHOP_ID,
            "amount": invoice.amount,
            "currency": invoice.currency,
            'shop_invoice_id': invoice.id,
            "description": invoice.description
        }
        if invoice.currency == '980':
            payload["payway"] = 'w1_uah'
            sign = _get_sign(payload, INVOICE_KEYS)
            payload['sign'] = sign
            resp = requests.post(UAH_INVOICE_URL, json=payload)
            data = json.loads(resp.content)['data']
            app.logger.info("data: {}".format(data))
            if not data:
                return jsonify(json.loads(resp.content))
            url = data['source']
            data = data['data']

        elif invoice.currency == '643':
            sign = _get_sign(payload, TIP_KEYS)
            payload['sign'] = sign
            data = payload
            url = TIP_URL

        return jsonify({'result': 'ok', 'data': data, 'url': url})
    return jsonify({'result': 'error', 'message': 'Form validation error'})


@app.route("/notify", methods=('POST',))
def notify():
    app.logger.info(request.values)
    keys = [key for key in request.values if (
        request.values[key] not in ['null', None] and key != 'sign')]
    sign = _get_sign(request.values, keys)
    if sign != request.values.get('sign', ''):
        return 'WRONG SIGN'
    shop_invoice_id = request.values.get('shop_invoice_id', '')
    invoice = Invoice.query.get(shop_invoice_id)
    app.logger.info("invoice: {}".format(invoice))
    if (
        invoice and
        invoice.amount == float(request.values.get('shop_amount')) and
        invoice.currency == request.values.get('shop_currency') and
        invoice.description == request.values.get('description')
    ):
        return 'OK'
    return "ERROR"
