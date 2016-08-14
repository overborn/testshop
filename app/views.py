# -*- coding: utf-8 -*-
import hashlib, requests, json

from flask import render_template, redirect, request, url_for, flash

from app import app, db
from models import Invoice
from config import SHOP_ID, SHOP_KEY, UAH_INVOICE_URL, TIP_URL
from forms import InvoiceForm, WlForm, TIPForm


INVOICE_KEYS = ("shop_id", "amount", "currency", "payway", "shop_invoice_id")
TIP_KEYS = ('amount', 'currency', 'shop_id', 'shop_invoice_id')


def _get_sign(req, keys_required, secret=SHOP_KEY):
    keys_sorted = sorted(keys_required)
    string_to_sign = ":".join(
        [str(req[k]).encode("utf8") for k in keys_sorted]) + secret
    app.logger.info("string_to_sign: {}".format(string_to_sign))
    sign = hashlib.md5(string_to_sign).hexdigest()
    return sign


@app.route("/", methods=('POST', 'GET'))
def index():
    form = InvoiceForm()
    if form.validate_on_submit():
        invoice = Invoice(
            str(form.data['amount']),
            form.data['currency'],
            form.data['description']
        )
        db.session.add(invoice)
        db.session.commit()
        app.logger.info("invoice created: {}".format(invoice))

        payload = {
            "shop_id": SHOP_ID,
            "amount": invoice.amount,
            "currency": invoice.currency,
            'shop_invoice_id': "blah011",
            "description": invoice.description
        }

        if form.data['currency'] == '980':
            payload["payway"] = 'w1_uah'
            sign = _get_sign(payload, INVOICE_KEYS)
            payload['sign'] = sign
            resp = requests.post(UAH_INVOICE_URL, json=payload)
            # print resp.content
            data = json.loads(resp.content)['data']
            app.logger.info("data: {}".format(data))
            if not data:
                flash(json.loads(resp.content)['message'])
                return render_template("index.html", form=form)
            url = data['source']
            data = json.dumps(data['data'])

        elif form.data['currency'] == '643':
            sign = _get_sign(payload, TIP_KEYS)
            payload['sign'] = sign
            url = TIP_URL
            data = json.dumps(payload)

        return redirect(url_for(
            'checkout',
            data=data,
            url=url)
        )
    return render_template("index.html", form=form)


@app.route("/checkout", methods=('GET',))
def checkout():
    url = request.args['url']
    data = json.loads(request.args["data"])
    # print data
    app.logger.info("data got: {}".format(data))
    if url == TIP_URL:
        form = TIPForm.from_json(data)
    else:
        form = WlForm.from_json(data)
    return render_template("checkout.html", form=form, url=url)
