"""Paste your Unsplash access key into a local page:  python3 _build/unsplash_key.py

Opens a form on http://127.0.0.1:8899 (this computer only). The key is written to
_build/.secrets/unsplash (owner read/write only, never committed or published) and the
server stops. `python3 _build/unsplash.py --forget` deletes the file after it has run.
"""
import html
import http.server
import os
import threading
import urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
SECRETS = os.path.join(HERE, ".secrets")
KEY_FILE = os.path.join(SECRETS, "unsplash")

PAGE = """<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><title>Unsplash key</title>
<style>body{font:16px/1.5 -apple-system,system-ui,sans-serif;background:#faf2ee;color:#3a2a33;display:grid;place-items:center;min-height:100vh;margin:0}
form{background:#fff;padding:2rem;border-radius:1rem;max-width:30rem;box-shadow:0 20px 40px -30px #55203f}
h1{font:600 1.4rem Georgia,serif;color:#55203f;margin:0 0 .5rem}input{width:100%;box-sizing:border-box;padding:.8rem;border:1px solid #e2c6ba;border-radius:.5rem;font:inherit;margin:1rem 0}
button{background:#55203f;color:#fff;border:0;padding:.8rem 1.4rem;border-radius:999px;font:inherit;cursor:pointer}small{color:#76656d}</style></head>
<body><form method="post"><h1>Unsplash access key</h1>{msg}
<p><small>Stays on this computer in a private file, is never published, and is deleted after the photos are fetched.</small></p>
<input name="key" type="password" autocomplete="off" required placeholder="Access key"><button>Save key</button></form></body></html>"""


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, body):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body.encode())

    def do_GET(self):
        self._send(PAGE.replace("{msg}", ""))

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        key = urllib.parse.parse_qs(self.rfile.read(n).decode()).get("key", [""])[0].strip()
        if not key:
            return self._send(PAGE.replace("{msg}", "<p>Please paste a key.</p>"))
        os.makedirs(SECRETS, mode=0o700, exist_ok=True)
        fd = os.open(KEY_FILE, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(fd, "w") as f:
            f.write(key)
        self._send("<!doctype html><meta charset=utf-8><body style='font:16px system-ui;padding:3rem'>"
                   "<h1>Saved</h1><p>You can close this tab. Next: <code>python3 _build/unsplash.py --forget</code></p>")
        threading.Thread(target=self.server.shutdown).start()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    srv = http.server.HTTPServer(("127.0.0.1", 8899), Handler)
    print("Open http://127.0.0.1:8899 and paste your Unsplash access key.")
    srv.serve_forever()
    print("Key saved to", html.escape(KEY_FILE))
