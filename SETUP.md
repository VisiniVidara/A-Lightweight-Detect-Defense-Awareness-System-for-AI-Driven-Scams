# MailSentra: simple setup

## See the website now
1. Open PowerShell in this MailSentra folder.
2. Run `python server.py`.
3. Open http://127.0.0.1:8090 in your browser.

The page displays the US$20/month plan. Visitors can submit early-access requests now. They are stored in the private database table `early_access`; no email, charge, pairing key or download is issued. Do not publish that database. Checkout activates only when the requirements below are complete. Ports 8000–8004 are not used.

## Prepare payments (Sri Lanka)
1. Create a merchant account at https://www.payhere.lk/ . The account owner must complete business/bank verification and select a plan that supports recurring payments and USD. Confirm current fees and eligibility directly with PayHere.
2. Start with the PayHere sandbox. Obtain the merchant ID and the merchant secret for your website. Create an OAuth app with the permissions required for Subscription Manager (Automated Charging API), and configure provider domain/server-IP permissions.
3. Put your real installation package outside public assets, for example `private/packages/MailSentra.xpi`. Never substitute a dummy installer for customer downloads.
4. Publish behind an HTTPS reverse proxy on your own domain. PayHere must reach `/api/payhere/notify`; localhost cannot receive their notifications. Keep the Python service bound to loopback behind the proxy.
5. Set the process environment variables shown in `.env.example`. That file is a reference and is NOT loaded automatically. In PowerShell use `$env:NAME='value'` before running `python server.py`. Do not share secret values. Set PUBLIC_URL to the HTTPS website origin, INSTALLER_PATH to the real package, SUPPORT_EMAIL to your support address, and all four PayHere credentials.
6. Keep MODE=sandbox and LIVE_APPROVED=false. Test checkout, return/cancel, signed notifications, duplicate notifications, renewals, refunds, cancellation and expired access using PayHere sandbox. API payment dates are interpreted in Sri Lanka time; verify this against your merchant's actual sandbox responses before launch.
7. Finalize the seller identity, contact, license, refund/tax policy and privacy/retention process. Then use the approved live credentials, MODE=live and LIVE_APPROVED=true. Restart the service. Sandbox orders cannot grant live access.

The local preview intentionally cannot charge cards. No real payment has been processed by this implementation.

## Customer flow
The customer agrees to US$20 now and automatically every month until cancellation, then pays on PayHere's hosted page using a supported Visa/Mastercard. Card numbers and CVV never enter this website's form or database. A return URL is not payment proof: the server checks signed callbacks and authenticated provider subscription/payment history before granting access.

After returning, select **Check payment** and **Get pairing key**. Save the private subscription management code shown on the page. It is kept only for the current browser session; losing it requires operator support. Paste it into Manage subscription to check access or cancel renewal. Do not share the code. Cancellation stops future renewal and preserves the already-paid period; it is not a refund.

Keys expire within 24 hours, are single-use, and require a current paid period. Reissuing an unused key replaces the old key. Download links last at most 30 minutes. The website does not email keys or verify email addresses.

## Installed product integration
POST `/api/pair` JSON `{ "pairing_key": "MS-...", "device_id": "installation_123" }` exchanges the unused key for a private session token. Your extension/backend must POST `/api/session/verify` with `{ "session_token": "..." }` and enforce a valid paid entitlement before protected operations. Do not trust a cached browser result. This repository cannot enforce licensing in an independently implemented extension until that integration is added. Revoked/expired subscriptions fail verification and downloads.

## Data and operations
Back up `private/server-secret` and the SQLite database together. Changing the secret invalidates access codes/keys/sessions. Protect private files with OS permissions. Billing-linked records are retained for subscription operation; configure and document a lawful retention/deletion process before launch. The existing 30-day cleanup applies only to unlinked registration records. No card details are stored.

Run checks with `python -m unittest discover -s tests -v` from this folder. Tests mock provider responses; passing them is not provider certification or a completed sandbox transaction.

Official references: https://support.payhere.lk/api-&-mobile-sdk/recurring-api and https://support.payhere.lk/api-&-mobile-sdk/subscription-manager-api .

## Viva: demonstrate a purchase without real payments
Open the website on port 8090 and select **Try purchase demo** in the pricing section.
1. Use the fictional customer details supplied.
2. Select **Fill Visa test details**, or enter Mastercard `5555 5555 5555 4444`, expiry `12/30`, code `123`.
3. Select Successful payment or Declined payment, tick the simulation acknowledgement, and select Simulate payment.
4. A successful simulation displays a demo receipt, an example pairing key and the installation journey. The example key cannot activate a real installation. No installer is downloaded.

This is a browser-only demonstration, separate from PayHere sandbox and live billing. It does not call payment APIs, store checkout inputs, create a subscription or grant paid access. Do not enter real card information. Close the dialog to clear its inputs.


## Free download, paid activation
The supplied XPI is copied into `private/packages/mailsentra-unified-thunderbird-fixed.xpi`. `/api/installer` serves that package without payment or registration. The pricing section includes the free download and Thunderbird installation steps. Paid activation is separate: production pairing and session APIs still require verified payment. The product itself must enforce that entitlement; website changes alone do not change the add-on's licensing behavior. The viva checkout continues to display only an example activation key.
