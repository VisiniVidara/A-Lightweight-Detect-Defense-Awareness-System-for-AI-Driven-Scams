"""MailSentra local website server. Run: python server.py. See SETUP.md before deployment."""
import hashlib
import billing
from types import SimpleNamespace
from contextlib import contextmanager
import hmac
import json
import logging
import os
from pathlib import Path
import re
import secrets
import sqlite3
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, unquote, urlsplit
import mimetypes

ROOT = Path(__file__).resolve().parent
DATA = Path(os.environ.get("MAILSENTRA_DATA_DIR", str(ROOT / "private"))).resolve()
PUBLIC_URL = os.environ.get("MAILSENTRA_PUBLIC_URL", "http://127.0.0.1:8090").rstrip("/")
SECRET = ""
PORT = int(os.environ.get("PORT", "8090"))
HOST = os.environ.get("MAILSENTRA_HOST", "127.0.0.1")
LIMIT_LOCK = threading.Lock()
LIMITS = {}
RETENTION_DAYS = max(1, int(os.environ.get("MAILSENTRA_RETENTION_DAYS", "30")))


@contextmanager
def database():
    con = sqlite3.connect(DATA / "registrations.sqlite3", timeout=15)
    con.row_factory = sqlite3.Row
    try:
        with con:
            yield con
    finally:
        con.close()


def initialize():
    global SECRET
    DATA.mkdir(parents=True, exist_ok=True)
    SECRET = os.environ.get("MAILSENTRA_SERVER_SECRET", "")
    if not SECRET:
        secret_file = DATA / "server-secret"
        try:
            with secret_file.open("x", encoding="ascii") as stream:
                stream.write(secrets.token_hex(48))
        except FileExistsError:
            pass
        SECRET = secret_file.read_text(encoding="ascii").strip()
        if len(SECRET) < 32:
            raise RuntimeError("The private server secret is invalid. Restore it from a backup.")
    with database() as con:
        con.executescript("""
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS registrations (
            id TEXT PRIMARY KEY, username TEXT NOT NULL, email TEXT NOT NULL,
            phone TEXT NOT NULL, consent_version TEXT NOT NULL, created INTEGER NOT NULL,
            download_hash TEXT UNIQUE NOT NULL, download_expires INTEGER NOT NULL,
            pairing_hash TEXT UNIQUE NOT NULL, pairing_expires INTEGER NOT NULL,
            emailed INTEGER NOT NULL DEFAULT 0, paired_at INTEGER, device_id TEXT,
            session_hash TEXT UNIQUE, session_expires INTEGER
        );
        """)
        columns = {row[1] for row in con.execute("PRAGMA table_info(registrations)")}
        if "key_issued" not in columns:
            con.execute("ALTER TABLE registrations ADD COLUMN key_issued INTEGER NOT NULL DEFAULT 0")
        # Previously emailed keys remain usable; old pending registrations never issued a key.
        con.execute("UPDATE registrations SET key_issued=1 WHERE emailed=1")
        con.execute("CREATE TABLE IF NOT EXISTS early_access (id TEXT PRIMARY KEY, username TEXT NOT NULL, email TEXT UNIQUE NOT NULL, phone TEXT NOT NULL, consent_version TEXT NOT NULL, created INTEGER NOT NULL)")
        con.execute("DELETE FROM early_access WHERE created < ?", (int(time.time()) - RETENTION_DAYS * 86400,))
        billing.initialize(con)
        # Keep billing-linked registrations: deleting one would break paid subscription access.
        con.execute("DELETE FROM registrations WHERE created < ? AND id NOT IN (SELECT registration_id FROM billing_orders)", (int(time.time()) - RETENTION_DAYS * 86400,))


def digest(value):
    return hmac.new(SECRET.encode(), value.encode(), hashlib.sha256).hexdigest()


def installer():
    value = os.environ.get("MAILSENTRA_INSTALLER_PATH", str(ROOT / "private" / "packages" / "mailsentra-unified-thunderbird-fixed.xpi"))
    if not value:
        return None
    path = Path(value).expanduser().resolve()
    return path if path.is_file() and path.suffix.lower() in {".exe", ".msi", ".xpi", ".zip"} else None


def billing_context():
    return SimpleNamespace(PUBLIC_URL=PUBLIC_URL, installer=installer, database=database, digest=digest)


def ready():
    return billing.configured(billing_context())


class Handler(BaseHTTPRequestHandler):
    server_version = "MailSentra"
    sys_version = ""

    def log_message(self, fmt, *args):
        # Do not log paths: download query strings contain bearer tokens.
        logging.info("HTTP response completed")

    def headers_common(self):
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self' https://sandbox.payhere.lk https://www.payhere.lk")

    def respond(self, status, payload):
        content = json.dumps(payload).encode()
        self.send_response(status)
        self.headers_common()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def limited(self, bucket, maximum, window=3600):
        # Direct client address only. A production reverse proxy must enforce its own limits.
        key = (bucket, self.client_address[0])
        now = time.time()
        with LIMIT_LOCK:
            for old_key in list(LIMITS):
                if not LIMITS[old_key] or LIMITS[old_key][-1] < now - window:
                    del LIMITS[old_key]
            items = [t for t in LIMITS.get(key, []) if t > now - window]
            if len(items) >= maximum:
                return True
            if len(LIMITS) >= 10000 and key not in LIMITS:
                return True
            items.append(now)
            LIMITS[key] = items
        return False

    def do_GET(self):
        request = urlsplit(self.path)
        if request.path == "/api/status":
            stamp = str(int(time.time()) // 3600)
            self.respond(200, {"ready": ready(), "registration_ready": True, "key_delivery": "screen", "payment_required": True, "checkout_ready": ready(), "sandbox": billing.sandbox(), "price": "20.00", "currency": "USD", "support_email": os.environ.get("MAILSENTRA_SUPPORT_EMAIL", ""), "csrf_token": stamp + "." + digest("csrf:" + stamp)})
            return
        if request.path in {"/api/installer", "/api/demo/download"}:
            # The package is public; activation keys still require verified payment.
            if self.limited("installer", 60):
                return self.respond(429, {"error": "Too many download requests. Please try again later."})
            package = installer()
            if not package:
                return self.respond(503, {"error": "The installation package is unavailable."})
            try:
                with package.open("rb") as stream:
                    self.send_response(200)
                    self.headers_common()
                    self.send_header("Content-Type", "application/octet-stream")
                    self.send_header("Content-Disposition", 'attachment; filename="MailSentra-Thunderbird.xpi"')
                    self.send_header("Cache-Control", "no-store")
                    self.send_header("Content-Length", str(package.stat().st_size))
                    self.end_headers()
                    while chunk := stream.read(65536):
                        self.wfile.write(chunk)
            except (BrokenPipeError, ConnectionResetError):
                pass
            return
        if request.path == "/api/download":
            if self.limited("download", 60):
                return self.respond(429, {"error": "Too many requests. Please try later."})
            token = parse_qs(request.query).get("token", [""])[0]
            with database() as con:
                row = con.execute("SELECT id FROM registrations WHERE download_hash=? AND download_expires>? AND key_issued=1", (digest(token), int(time.time()))).fetchone()
                if row and not billing.registration_entitled(con, row["id"]):
                    row = None
            package = installer()
            if not row:
                return self.respond(403, {"error": "This download link is invalid or expired. Please register again."})
            if not package:
                return self.respond(503, {"error": "The installation package is currently unavailable."})
            filename = "MailSentra-Setup" + package.suffix.lower()
            try:
                with package.open("rb") as stream:
                    self.send_response(200)
                    self.headers_common()
                    self.send_header("Content-Type", "application/octet-stream")
                    self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
                    self.send_header("Cache-Control", "no-store")
                    self.send_header("Content-Length", str(package.stat().st_size))
                    self.end_headers()
                    while chunk := stream.read(65536):
                        self.wfile.write(chunk)
            except (BrokenPipeError, ConnectionResetError):
                pass
            return
        if request.path.startswith("/api/"):
            return self.respond(404, {"error": "Endpoint not found."})
        target = (ROOT / unquote(request.path).lstrip("/")).resolve()
        if target == ROOT:
            target = ROOT / "index.html"
        if target.is_dir():
            target = target / "index.html"
        # Serve only explicit public files, never configuration, database or installers.
        allowed_root = target.parent == ROOT and target.name in {"index.html", "privacy.html", "terms.html", "research.html"}
        allowed_asset = any(target.is_relative_to(ROOT / folder) for folder in ("assets", "css", "js", "product", "prototype")) and target.suffix.lower() in {".html", ".css", ".js", ".png", ".jpg", ".jpeg"}
        allowed_document = target.parent == ROOT / "documents" and target.name in {
            "full-system-overview.pdf", "ai-detector.pdf", "defense-and-awareness.pdf",
            "steganography-detection.pdf", "thesis.pdf",
        }
        allowed_milestone = target.parent == ROOT / "milestones" and target.name in {
            "project-proposal.pptx", "progress-presentation-01.pptx",
            "progress-presentation-02.pptx", "final-presentation.pptx",
            "topic-assessment-form.pdf", "checklist-01.pdf", "checklist-02.pdf",
        }
        if not (allowed_root or allowed_asset or allowed_document or allowed_milestone) or not target.is_file():
            return self.respond(404, {"error": "Page not found."})
        content = target.read_bytes()
        self.send_response(200)
        self.headers_common()
        self.send_header("Content-Type", (mimetypes.guess_type(target.name)[0] or "application/octet-stream") + ("; charset=utf-8" if target.suffix in {".html", ".css", ".js"} else ""))
        self.send_header("Content-Length", str(len(content)))
        self.send_header("Cache-Control", "no-cache")
        if allowed_milestone:
            disposition = "inline" if target.suffix == ".pdf" and parse_qs(request.query).get("download") != ["1"] else "attachment"
            self.send_header("Content-Disposition", f'{disposition}; filename="MailSentra-{target.name}"')
        if allowed_document:
            disposition = "attachment" if parse_qs(request.query).get("download") == ["1"] else "inline"
            self.send_header("Content-Disposition", f'{disposition}; filename="MailSentra-{target.name}"')
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        if urlsplit(self.path).path == "/api/payhere/notify":
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 16384 or self.headers.get("Content-Type", "").split(";")[0] != "application/x-www-form-urlencoded":
                    return self.respond(400, {"error": "Invalid payment notification."})
                fields = parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True, max_num_fields=80)
                if any(len(v) != 1 for v in fields.values()):
                    return self.respond(400, {"error": "Duplicate notification fields."})
                return self.respond(200, billing.notification(billing_context(), {k: v[0] for k, v in fields.items()}))
            except billing.BillingError as error:
                return self.respond(error.status, {"error": str(error)})
            except (ValueError, UnicodeDecodeError):
                return self.respond(400, {"error": "Invalid payment notification."})
        origin_allowed = self.headers.get("Origin") in (None, PUBLIC_URL)
        path = urlsplit(self.path).path
        if path not in {"/api/register", "/api/early-access", "/api/pair", "/api/session/verify", "/api/billing/status", "/api/billing/claim", "/api/billing/cancel"}:
            return self.respond(404, {"error": "Endpoint not found."})
        if self.limited(path, 5 if path in {"/api/register", "/api/early-access"} else (360 if path == "/api/billing/status" else 30)):
            return self.respond(429, {"error": "Too many attempts. Please try again later."})
        if self.headers.get("Content-Type", "").split(";")[0] != "application/json":
            return self.respond(415, {"error": "JSON is required."})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 4096:
                raise ValueError()
            values = json.loads(self.rfile.read(length))
            if not isinstance(values, dict):
                raise ValueError()
        except (ValueError, UnicodeDecodeError):
            return self.respond(400, {"error": "Invalid request."})
        if not origin_allowed:
            return self.respond(403, {"error": "Request origin is not allowed."})
        if path.startswith("/api/billing/"):
            if path != "/api/billing/status" and not self.csrf_valid():
                return self.respond(403, {"error": "Refresh the page and try again."})
            try:
                action = {"/api/billing/status": billing.status, "/api/billing/claim": billing.claim, "/api/billing/cancel": billing.cancel}[path]
                return self.respond(200, action(billing_context(), values))
            except billing.BillingError as error:
                return self.respond(error.status, {"error": str(error)})
        if path == "/api/early-access":
            return self.early_access(values)
        if path == "/api/register":
            return self.register(values)
        if path == "/api/pair":
            return self.pair(values)
        session = values.get("session_token", "")
        if not isinstance(session, str) or len(session) > 200:
            return self.respond(400, {"error": "Invalid session."})
        with database() as con:
            row = con.execute("SELECT id FROM registrations WHERE session_hash=? AND session_expires>? AND key_issued=1", (digest(session), int(time.time()))).fetchone()
            entitlement = billing.registration_entitled(con, row["id"]) if row else None
        self.respond(200 if entitlement else 401, {"valid": bool(entitlement), "paid_until": entitlement["paid_until"] if entitlement else None})

    def csrf_valid(self):
        token = self.headers.get("X-CSRF-Token", "")
        return any(hmac.compare_digest(token, str(t) + "." + digest("csrf:" + str(t))) for t in (int(time.time()) // 3600, int(time.time()) // 3600 - 1))

    def early_access(self, values):
        if not self.csrf_valid():
            return self.respond(403, {"error": "Please refresh the page and try again."})
        username, email, phone = (values.get(k, "") for k in ("username", "email", "phone"))
        if not all(isinstance(v, str) for v in (username, email, phone)):
            return self.respond(400, {"error": "Please check your contact details."})
        username, email, phone = username.strip(), email.strip().lower(), phone.strip()
        if (not 2 <= len(username) <= 60 or any(ord(c) < 32 for c in username) or
            len(email) > 254 or not re.fullmatch(r"[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+", email) or
            not re.fullmatch(r"\+?[0-9 ()-]{7,30}", phone) or len(re.sub(r"\D", "", phone)) < 7 or values.get("consent") is not True):
            return self.respond(400, {"error": "Enter a valid name, email and phone number, and accept the early-access notice."})
        now = int(time.time())
        with database() as con:
            con.execute("DELETE FROM early_access WHERE created < ?", (now - RETENTION_DAYS * 86400,))
            # Email uniqueness makes retries idempotent; do not expose whether somebody else registered.
            con.execute("INSERT OR IGNORE INTO early_access (id,username,email,phone,consent_version,created) VALUES (?,?,?,?,?,?)", (secrets.token_hex(16), username, email, phone, "early-access-v1", now))
        return self.respond(201, {"status": "early_access_saved"})

    def register(self, values):
        if not self.csrf_valid():
            return self.respond(403, {"error": "Please refresh the page and try again."})
        username, email, phone = (values.get(k, "") for k in ("username", "email", "phone"))
        if not all(isinstance(v, str) for v in (username, email, phone)):
            return self.respond(400, {"error": "Please check your registration details."})
        username, email, phone = username.strip(), email.strip().lower(), phone.strip()
        if (not 2 <= len(username) <= 60 or any(ord(c) < 32 for c in username) or
            not re.fullmatch(r"[^\s@<>]+@[^\s@<>]+\.[^\s@<>]+", email) or len(email) > 254 or
            not re.fullmatch(r"\+?[0-9 ()-]{7,30}", phone) or len(re.sub(r"\D", "", phone)) < 7 or
            values.get("consent") is not True):
            return self.respond(400, {"error": "Enter a valid username, email and phone number, and accept the registration terms."})
        try:
            values.update(username=username, email=email, phone=phone)
            return self.respond(201, billing.create_checkout(billing_context(), values))
        except billing.BillingError as error:
            return self.respond(error.status, {"error": str(error)})

    def pair(self, values):
        key, device = values.get("pairing_key", ""), values.get("device_id", "")
        if not isinstance(key, str) or not 10 <= len(key) <= 100 or not isinstance(device, str) or not re.fullmatch(r"[A-Za-z0-9_-]{8,128}", device):
            return self.respond(400, {"error": "A pairing key and an installation ID are required."})
        session, now = secrets.token_urlsafe(32), int(time.time())
        with database() as con:
            con.execute("BEGIN IMMEDIATE")
            row = con.execute("SELECT id FROM registrations WHERE pairing_hash=? AND pairing_expires>? AND paired_at IS NULL AND key_issued=1", (digest(key), now)).fetchone()
            entitlement = billing.registration_entitled(con, row["id"]) if row else None
            if not entitlement:
                return self.respond(401, {"error": "A valid unused pairing key and active paid subscription are required."})
            updated = con.execute("UPDATE registrations SET paired_at=?, device_id=?, session_hash=?, session_expires=? WHERE id=? AND paired_at IS NULL", (now, device, digest(session), now + 86400 * 365, row["id"])).rowcount
        if not updated:
            return self.respond(401, {"error": "The pairing key is invalid, expired, or already used."})
        self.respond(200, {"paired": True, "session_token": session, "expires_in": entitlement["paid_until"] - now, "paid_until": entitlement["paid_until"]})


if __name__ == "__main__":
    if PUBLIC_URL.startswith("https://") is False and urlsplit(PUBLIC_URL).hostname not in {"127.0.0.1", "localhost"}:
        raise SystemExit("A public deployment requires an HTTPS MAILSENTRA_PUBLIC_URL.")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    initialize()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    server.daemon_threads = True
    print(f"MailSentra preview: http://{HOST}:{PORT}", flush=True)
    print("US$20/month checkout configured." if ready() else "US$20/month subscription preview. Checkout disabled until merchant setup, public HTTPS and installer are configured.", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
