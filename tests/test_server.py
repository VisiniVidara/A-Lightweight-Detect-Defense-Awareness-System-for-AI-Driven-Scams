import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import time
import unittest
import uuid
from datetime import datetime, timezone, timedelta
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import server as app
import billing

class BillingTests(unittest.TestCase):
 def setUp(self):
  self.root=app.ROOT/'private'/('test_'+uuid.uuid4().hex);self.root.mkdir(parents=True)
  self.old=app.DATA;app.DATA=self.root/'data';self.package=self.root/'package.xpi';self.package.write_bytes(b'test fixture only')
  self.env=patch.dict(os.environ,{'MAILSENTRA_SERVER_SECRET':'test','MAILSENTRA_PAYHERE_MODE':'sandbox','MAILSENTRA_PAYHERE_MERCHANT_ID':'123','MAILSENTRA_PAYHERE_MERCHANT_SECRET':'secret','MAILSENTRA_INSTALLER_PATH':str(self.package)})
  self.env.start();app.initialize();self.ctx=app.billing_context();self.ctx.PUBLIC_URL='https://shop.example';self.config=patch.object(billing,'configured',return_value=True);self.config.start()
  self.values=dict(username='Test User',email='test@example.com',phone='+94771234567',consent=True,subscription_consent=True,first_name='Test',last_name='User',address='Test Street',city='Colombo',country='Sri Lanka')
 def tearDown(self):
  self.config.stop();self.env.stop();app.DATA=self.old;assert self.root.resolve().is_relative_to((app.ROOT/'private').resolve());shutil.rmtree(self.root)
 def checkout(self):
  self.order=billing.create_checkout(self.ctx,self.values);return self.order
 def notify(self,state='RECEIVED'):
  order=self.order['fields']['order_id'];v=dict(merchant_id='123',order_id=order,payhere_amount='20.00',payhere_currency='USD',status_code='2',subscription_id='789')
  v['md5sig']=billing.md5('123'+order+'20.00USD2'+billing.md5('secret'))
  subscription=dict(order_id=order,subscription_id=789,currency='USD',amount=20,status='ACTIVE')
  date=datetime.now(timezone(timedelta(hours=5,minutes=30))).strftime('%Y-%m-%d %H:%M:%S')
  payment=dict(order_id=order,payment_id=456,currency='USD',amount=20,date=date,status=state)
  with patch.object(billing,'api',side_effect=[subscription,[payment]]):return billing.notification(self.ctx,v)
 def test_checkout_cannot_issue_free_key(self):
  d=self.checkout();self.assertNotIn('pairing_key',d);self.assertEqual(d['fields']['amount'],'20.00');self.assertEqual(d['fields']['recurrence'],'1 Month')
  with self.assertRaises(billing.BillingError) as e:billing.claim(self.ctx,{'access_token':d['access_token']})
  self.assertEqual(e.exception.status,402)
 def test_verified_payment_claim_and_replay(self):
  d=self.checkout();self.notify();before=billing.status(self.ctx,{'access_token':d['access_token']});self.notify();after=billing.status(self.ctx,{'access_token':d['access_token']});self.assertEqual(before['paid_until'],after['paid_until']);self.assertTrue(after['paid'])
  key=billing.claim(self.ctx,{'access_token':d['access_token']});self.assertRegex(key['pairing_key'],r'^MS-[A-Za-z0-9_-]{32}$');self.assertIn('download_url',key)
  with app.database() as con:self.assertEqual(con.execute('SELECT COUNT(*) FROM billing_payments').fetchone()[0],1);self.assertNotIn(key['pairing_key'],dict(con.execute('SELECT * FROM registrations').fetchone()).values())
 def test_refund_revokes_access(self):
  d=self.checkout();self.notify();self.notify('REFUNDED');self.assertFalse(billing.status(self.ctx,{'access_token':d['access_token']})['paid'])
 def test_cancellation_preserves_paid_period(self):
  d=self.checkout();self.notify();v={'access_token':d['access_token']}
  with patch.object(billing,'api',return_value=None) as api:billing.cancel(self.ctx,v);billing.cancel(self.ctx,v);self.assertEqual(api.call_count,1)
  self.assertTrue(billing.status(self.ctx,v)['paid']);self.assertEqual(billing.status(self.ctx,v)['status'],'cancelled')
 def test_expired_and_wrong_mode_denied(self):
  d=self.checkout();self.notify()
  with app.database() as con:con.execute('UPDATE billing_orders SET paid_until=?',(int(time.time())-1,))
  self.assertFalse(billing.status(self.ctx,{'access_token':d['access_token']})['paid'])
  with patch.dict(os.environ,{'MAILSENTRA_PAYHERE_MODE':'live'}):
   with self.assertRaises(billing.BillingError):billing.status(self.ctx,{'access_token':d['access_token']})
 def test_forged_webhook_denied(self):
  self.checkout()
  with self.assertRaises(billing.BillingError):billing.notification(self.ctx,dict(merchant_id='123',order_id=self.order['fields']['order_id'],payhere_amount='20.00',payhere_currency='USD',status_code='2',subscription_id='789',md5sig='forged'))
 def test_no_setup_no_order(self):
  with patch.object(billing,'configured',return_value=False):
   with self.assertRaises(billing.BillingError):self.checkout()
  with app.database() as con:self.assertEqual(con.execute('SELECT COUNT(*) FROM registrations').fetchone()[0],0)
 def test_consent_required(self):
  self.values['subscription_consent']=False
  with self.assertRaises(billing.BillingError):self.checkout()
 def test_access_code_not_stored_plaintext(self):
  d=self.checkout()
  with app.database() as con:self.assertNotIn(d['access_token'],dict(con.execute('SELECT * FROM billing_orders').fetchone()).values())
 def test_early_access_http_validation_and_duplicate(self):
  import threading
  from urllib.request import Request, urlopen
  from urllib.error import HTTPError
  http=app.ThreadingHTTPServer(('127.0.0.1',0),app.Handler)
  thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start()
  base='http://127.0.0.1:'+str(http.server_port)
  def post(values,csrf):
   request=Request(base+'/api/early-access',data=json.dumps(values).encode(),headers={'Content-Type':'application/json','X-CSRF-Token':csrf})
   try:response=urlopen(request)
   except HTTPError as error:response=error
   with response:return response.status,json.load(response)
  try:
   with urlopen(base+'/api/status') as response:csrf=json.load(response)['csrf_token']
   self.assertEqual(post(self.values,'invalid')[0],403)
   self.assertEqual(post({**self.values,'consent':False},csrf)[0],400)
   code,result=post(self.values,csrf);self.assertEqual(code,201);self.assertEqual(result['status'],'early_access_saved');self.assertNotIn('pairing_key',result)
   self.assertEqual(post(self.values,csrf)[0],201)
   with app.database() as con:
    self.assertEqual(con.execute('SELECT COUNT(*) FROM early_access').fetchone()[0],1)
    self.assertEqual(con.execute('SELECT COUNT(*) FROM billing_orders').fetchone()[0],0)
  finally:http.shutdown();http.server_close();thread.join()
 def test_month_end(self):
  start=datetime(2026,1,31,tzinfo=timezone.utc);self.assertEqual(datetime.fromtimestamp(billing.next_month(start.timestamp()),timezone.utc).day,28)

if __name__=='__main__':unittest.main()
