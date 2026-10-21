"""PayHere hosted monthly checkout. No PAN, CVV, card expiry or cardholder data is stored."""
import base64
import calendar
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
import hashlib
import hmac
import json
import os
import re
import secrets
import time
import threading
RECONCILE_LOCK = threading.Lock()
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

AMOUNT = "20.00"
CURRENCY = "USD"


class BillingError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


def sandbox():
    return os.environ.get("MAILSENTRA_PAYHERE_MODE", "sandbox") == "sandbox"


def base_url():
    return "https://sandbox.payhere.lk" if sandbox() else "https://www.payhere.lk"


def configured(app):
    origin = urlsplit(app.PUBLIC_URL)
    public = origin.scheme == "https" and bool(origin.hostname) and origin.hostname not in {"localhost", "127.0.0.1"} and origin.path in {"", "/"} and not origin.query and not origin.fragment
    credentials = all(os.environ.get(k, "").strip() for k in ("MAILSENTRA_PAYHERE_MERCHANT_ID", "MAILSENTRA_PAYHERE_MERCHANT_SECRET", "MAILSENTRA_PAYHERE_APP_ID", "MAILSENTRA_PAYHERE_APP_SECRET", "MAILSENTRA_SUPPORT_EMAIL"))
    approved = sandbox() or os.environ.get("MAILSENTRA_BILLING_LIVE_APPROVED") == "true"
    return bool(public and credentials and app.installer() and approved and os.environ.get("MAILSENTRA_PAYHERE_MODE", "sandbox") in {"sandbox", "live"})


def initialize(con):
    con.executescript("""
    CREATE TABLE IF NOT EXISTS billing_orders (
        id TEXT PRIMARY KEY, registration_id TEXT UNIQUE NOT NULL,
        access_hash TEXT UNIQUE NOT NULL, mode TEXT NOT NULL,
        state TEXT NOT NULL DEFAULT 'pending', created INTEGER NOT NULL,
        subscription_id TEXT UNIQUE, paid_until INTEGER NOT NULL DEFAULT 0,
        cancel_requested INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS billing_payments (
        payment_id TEXT PRIMARY KEY, order_id TEXT NOT NULL,
        state TEXT NOT NULL, payment_date TEXT NOT NULL
    );
    """)


def md5(value):
    return hashlib.md5(value.encode()).hexdigest().upper()


def api(path, body=None):
    """Use OAuth and authenticated provider snapshots in addition to callback signatures."""
    try:
        credentials = os.environ["MAILSENTRA_PAYHERE_APP_ID"] + ":" + os.environ["MAILSENTRA_PAYHERE_APP_SECRET"]
        auth = base64.b64encode(credentials.encode()).decode()
        token_request = Request(base_url() + "/merchant/v1/oauth/token", data=b"grant_type=client_credentials", headers={"Authorization": "Basic " + auth, "Content-Type": "application/x-www-form-urlencoded"})
        with urlopen(token_request, timeout=15) as response:
            token = json.load(response)["access_token"]
        request = Request(base_url() + "/merchant/v1/" + path, data=json.dumps(body).encode() if body is not None else None, headers={"Authorization": "Bearer " + token, "Content-Type": "application/json"})
        with urlopen(request, timeout=15) as response:
            result = json.load(response)
        if result.get("status") != 1:
            raise ValueError("Provider did not confirm the request")
        return result.get("data")
    except Exception as error:
        raise BillingError("The payment provider could not confirm this request. Please retry later.", 503) from error


def get_order(app, values):
    token = values.get("access_token", "")
    if not isinstance(token, str) or not 30 <= len(token) <= 100:
        raise BillingError("A valid subscription access code is required.", 401)
    with app.database() as con:
        order = con.execute("SELECT * FROM billing_orders WHERE access_hash=? AND mode=?", (app.digest(token), "sandbox" if sandbox() else "live")).fetchone()
    if not order:
        raise BillingError("This subscription access code is invalid.", 401)
    return order


def is_paid(order):
    return order["paid_until"] > int(time.time()) and order["state"] in {"active", "cancelled", "past_due"}


def registration_entitled(con, registration_id):
    order = con.execute("SELECT * FROM billing_orders WHERE registration_id=? AND mode=?", (registration_id, "sandbox" if sandbox() else "live")).fetchone()
    return order if order and is_paid(order) else None


def create_checkout(app, values):
    if not configured(app):
        raise BillingError("Checkout is not open yet. No payment has been taken and no pairing key has been issued.", 503)
    for key in ("first_name", "last_name", "address", "city", "country"):
        value = values.get(key, "")
        if not isinstance(value, str) or not 1 <= len(value.strip()) <= 150 or any(ord(c) < 32 for c in value):
            raise BillingError("Please complete your name and billing address.")
    if values.get("subscription_consent") is not True:
        raise BillingError("Please accept the US$20 monthly recurring subscription before continuing.")
    now = int(time.time())
    username, email, phone = values["username"], values["email"], values["phone"]
    order_id, registration_id, access_token = "MS-" + secrets.token_hex(16), secrets.token_hex(16), secrets.token_urlsafe(32)
    with app.database() as con:
        recent = con.execute("SELECT COUNT(*) FROM registrations WHERE email=? AND created>?", (email, now - 3600)).fetchone()[0]
        if recent >= 3:
            raise BillingError("Too many recent checkout attempts. Resume the existing checkout or try again later.", 429)
        con.execute("INSERT INTO registrations (id,username,email,phone,consent_version,created,download_hash,download_expires,pairing_hash,pairing_expires,key_issued) VALUES (?,?,?,?,?,?,?,?,?,?,0)", (registration_id, username, email, phone, "monthly-usd20-v1", now, app.digest(secrets.token_urlsafe(32)), 0, app.digest(secrets.token_urlsafe(32)), 0))
        con.execute("INSERT INTO billing_orders (id,registration_id,access_hash,mode,created) VALUES (?,?,?,?,?)", (order_id, registration_id, app.digest(access_token), "sandbox" if sandbox() else "live", now))
    merchant = os.environ["MAILSENTRA_PAYHERE_MERCHANT_ID"]
    fields = {"merchant_id": merchant, "return_url": app.PUBLIC_URL + "/?payment=return#get-started", "cancel_url": app.PUBLIC_URL + "/?payment=cancel#get-started", "notify_url": app.PUBLIC_URL + "/api/payhere/notify", "order_id": order_id, "items": "MailSentra Monthly Subscription", "currency": CURRENCY, "amount": AMOUNT, "recurrence": "1 Month", "duration": "Forever", "first_name": values["first_name"].strip(), "last_name": values["last_name"].strip(), "email": email, "phone": phone, "address": values["address"].strip(), "city": values["city"].strip(), "country": values["country"].strip()}
    fields["hash"] = md5(merchant + order_id + AMOUNT + CURRENCY + md5(os.environ["MAILSENTRA_PAYHERE_MERCHANT_SECRET"]))
    return {"status": "checkout_required", "action": base_url() + "/pay/checkout", "fields": fields, "access_token": access_token, "sandbox": sandbox()}


def next_month(timestamp):
    value = datetime.fromtimestamp(timestamp, timezone.utc)
    month = value.month % 12 + 1
    year = value.year + (1 if value.month == 12 else 0)
    return int(value.replace(year=year, month=month, day=min(value.day, calendar.monthrange(year, month)[1])).timestamp())


def notification(app, values):
    with RECONCILE_LOCK:
        return _notification(app, values)


def _notification(app, values):
    merchant = os.environ.get("MAILSENTRA_PAYHERE_MERCHANT_ID", "")
    secret = os.environ.get("MAILSENTRA_PAYHERE_MERCHANT_SECRET", "")
    if not merchant or not secret:
        raise BillingError("Payment notifications are not configured.", 503)
    required = ("merchant_id", "order_id", "payhere_amount", "payhere_currency", "status_code", "md5sig", "subscription_id")
    if any(not isinstance(values.get(k), str) or not values[k] for k in required):
        raise BillingError("Invalid payment notification.")
    signature = md5(values["merchant_id"] + values["order_id"] + values["payhere_amount"] + values["payhere_currency"] + values["status_code"] + md5(secret))
    if values["merchant_id"] != merchant or not hmac.compare_digest(signature, values["md5sig"].upper()):
        raise BillingError("Invalid payment signature.", 403)
    try:
        correct_amount = Decimal(values["payhere_amount"]) == Decimal(AMOUNT)
    except InvalidOperation:
        correct_amount = False
    if not correct_amount or values["payhere_currency"] != CURRENCY:
        raise BillingError("Payment amount or currency does not match the subscription.", 400)
    subscription_id = values["subscription_id"]
    if not re.fullmatch(r"[0-9]{1,30}", subscription_id):
        raise BillingError("Invalid subscription reference.")
    with app.database() as con:
        order = con.execute("SELECT * FROM billing_orders WHERE id=? AND mode=?", (values["order_id"], "sandbox" if sandbox() else "live")).fetchone()
    if not order or (order["subscription_id"] and order["subscription_id"] != subscription_id):
        raise BillingError("Unknown subscription order.", 404)
    # Fetch provider truth: message type, payment ID and dates are not covered by the callback checksum.
    subscription = api("subscription/" + subscription_id)
    payments = api("subscription/" + subscription_id + "/payments")
    if not isinstance(subscription, dict) or subscription.get("order_id") != order["id"] or str(subscription.get("subscription_id")) != subscription_id or subscription.get("currency") != CURRENCY or str(subscription.get("amount", "")) not in {"20", "20.0", "20.00"}:
        raise BillingError("Provider subscription does not match this order.", 403)
    if not isinstance(payments, list):
        raise BillingError("Payment history could not be verified.", 503)
    verified = []
    for payment in payments:
        if not isinstance(payment, dict):
            raise BillingError("Invalid provider payment history.", 503)
        if payment.get("order_id") != order["id"] or payment.get("currency") != CURRENCY or str(payment.get("amount", "")) not in {"20", "20.0", "20.00"}:
            continue
        # PayHere API date strings are interpreted in the merchant's Sri Lanka timezone.
        try:
            date = datetime.strptime(payment["date"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone(timedelta(hours=5, minutes=30)))
            timestamp = int(date.timestamp())
            payment_id = str(payment["payment_id"])
            state = str(payment["status"])
        except (KeyError, ValueError):
            raise BillingError("Provider returned an invalid payment record.", 503)
        if not re.fullmatch(r"[0-9]{1,30}", payment_id) or timestamp > int(time.time()) + 300:
            raise BillingError("Provider returned an invalid payment record.", 503)
        verified.append((timestamp, payment_id, state))
    latest = max(verified, default=None)
    paid_until = next_month(latest[0]) if latest and latest[2] == "RECEIVED" else 0
    provider_state = str(subscription.get("status", ""))
    state = "active" if provider_state == "ACTIVE" else "cancelled"
    if not paid_until:
        state = "revoked" if verified else "pending"
    with app.database() as con:
        con.execute("BEGIN IMMEDIATE")
        for timestamp, payment_id, payment_state in verified:
            existing = con.execute("SELECT order_id FROM billing_payments WHERE payment_id=?", (payment_id,)).fetchone()
            if existing and existing[0] != order["id"]:
                raise BillingError("Payment already belongs to a different order.", 409)
            con.execute("INSERT INTO billing_payments (payment_id,order_id,state,payment_date) VALUES (?,?,?,?) ON CONFLICT(payment_id) DO UPDATE SET state=excluded.state", (payment_id, order["id"], payment_state, str(timestamp)))
        current = con.execute("SELECT cancel_requested FROM billing_orders WHERE id=?", (order["id"],)).fetchone()
        if current[0] and state == "active":
            state = "cancelled"
        con.execute("UPDATE billing_orders SET subscription_id=?,state=?,paid_until=? WHERE id=?", (subscription_id, state, paid_until, order["id"]))
    return {"received": True}


def status(app, values):
    order = get_order(app, values)
    return {"status": order["state"], "paid": is_paid(order), "paid_until": order["paid_until"], "sandbox": order["mode"] == "sandbox", "order_id": order["id"]}


def claim(app, values):
    order = get_order(app, values)
    key, download = "MS-" + secrets.token_urlsafe(24), secrets.token_urlsafe(32)
    now = int(time.time())
    with app.database() as con:
        con.execute("BEGIN IMMEDIATE")
        order = con.execute("SELECT * FROM billing_orders WHERE id=?", (order["id"],)).fetchone()
        if not is_paid(order):
            raise BillingError("A verified active payment is required before access can be issued.", 402)
        registration = con.execute("SELECT paired_at FROM registrations WHERE id=?", (order["registration_id"],)).fetchone()
        if registration[0]:
            raise BillingError("This subscription is already paired to an installation. Use your existing installation.", 409)
        expires = min(now + 86400, order["paid_until"])
        con.execute("UPDATE registrations SET key_issued=1,pairing_hash=?,pairing_expires=?,download_hash=?,download_expires=? WHERE id=?", (app.digest(key), expires, app.digest(download), min(now + 1800, order["paid_until"]), order["registration_id"]))
    result = {"status": "key_issued", "pairing_key": key, "pairing_expires_at": expires, "key_delivery": "screen", "paid_until": order["paid_until"], "email_verified": False}
    if app.installer():
        result.update(download_url="/api/download?token=" + download, expires_in=1800)
    return result


def cancel(app, values):
    order = get_order(app, values)
    if not order["subscription_id"]:
        raise BillingError("No authorized subscription is available to cancel.", 409)
    if not order["cancel_requested"]:
        api("subscription/cancel", {"subscription_id": int(order["subscription_id"])})
        with app.database() as con:
            con.execute("UPDATE billing_orders SET state='cancelled',cancel_requested=1 WHERE id=?", (order["id"],))
    return {"cancelled": True, "paid_until": order["paid_until"]}
