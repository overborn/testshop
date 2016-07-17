# -*- coding: utf-8 -*-
import hashlib, requests, json

from flask import render_template, redirect, request, url_for

from app import app
from config import SHOP_ID, SHOP_KEY, UAH_INVOICE_URL, TIP_URL
from forms import InvoiceForm, WlForm, TIPForm

INVOICE_KEYS = ("shop_id", "amount", "currency", "payway", "shop_invoice_id")
TIP_KEYS = ('amount', 'currency', 'shop_id', 'shop_invoice_id')


def get_sign(req, keys_required, secret=SHOP_KEY):
    keys_sorted = sorted(keys_required)
    string_to_sign = ":".join([str(req[k]).encode("utf8") for k in keys_sorted]) + secret
    # print string_to_sign
    sign = hashlib.md5(string_to_sign).hexdigest()
    return sign


@app.route("/", methods=('POST', 'GET'))
def index():
    form = InvoiceForm()
    if form.validate_on_submit():
        payload = {
            "shop_id": SHOP_ID,
            "amount": str(form.data['amount']),
            "currency": form.data['currency'],
            'shop_invoice_id': "blah011",
            "description": form.data['description']
        }

        if form.data['currency'] == '980':
            print 'uah'
            payload["payway"] = 'w1_uah'
            sign = get_sign(payload, INVOICE_KEYS)
            payload['sign'] = sign
            resp = requests.post(UAH_INVOICE_URL, json=payload)
            print resp.content
            data = json.loads(resp.content)['data']
            url = data['source']
            data = json.dumps(data['data'])

        elif form.data['currency'] == '643':
            print 'rub'
            sign = get_sign(payload, TIP_KEYS)
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
    print data
    if url == TIP_URL:
        form = TIPForm.from_json(data)
    else:
        form = WlForm.from_json(data)
    return render_template("checkout.html", form=form, url=url)
