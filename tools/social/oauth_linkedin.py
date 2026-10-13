#!/usr/bin/env python3
"""Autorización de LinkedIn para publicar en la PÁGINA DE EMPRESA (se ejecuta UNA VEZ en TU computadora).

Requisitos previos (ver docs/publicacion-automatica.md): app en linkedin.com/developers asociada a la página,
producto "Community Management API" aprobado, y esta URL registrada en Auth > Redirect URLs:
    http://127.0.0.1:8977/callback
Imprime el access token (y el refresh token, si LinkedIn lo entrega) EN TU TERMINAL. No los pegues en un chat.
Uso:  python3 tools/social/oauth_linkedin.py
"""
import getpass
import http.server
import json
import secrets
import threading
import urllib.parse
import urllib.request
import webbrowser

PORT = 8977
REDIRECT = "http://127.0.0.1:%d/callback" % PORT
SCOPES = "w_organization_social r_organization_social"


def main():
    cid = input("Client ID de LinkedIn: ").strip()
    secret = getpass.getpass("Client Secret (no se muestra): ").strip()
    state = secrets.token_urlsafe(16)
    box = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if q.get("state", [""])[0] == state and "code" in q:
                box["code"] = q["code"][0]
                msg = "Listo. Ya podés cerrar esta pestaña y volver a la terminal."
            else:
                box["error"] = q.get("error_description", q.get("error", ["respuesta inválida"]))[0]
                msg = "No se pudo autorizar: %s" % box["error"]
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(msg.encode())

        def log_message(self, *a):
            pass

    srv = http.server.HTTPServer(("127.0.0.1", PORT), H)
    t = threading.Thread(target=srv.handle_request)
    t.start()
    url = "https://www.linkedin.com/oauth/v2/authorization?" + urllib.parse.urlencode({
        "response_type": "code", "client_id": cid, "redirect_uri": REDIRECT, "state": state, "scope": SCOPES})
    print("\nSe abre el navegador. Si no, copiá este enlace:\n%s\n" % url)
    webbrowser.open(url)
    t.join(timeout=300)
    srv.server_close()
    if "code" not in box:
        raise SystemExit("No llegó el código (%s)." % box.get("error", "tiempo agotado"))
    data = urllib.parse.urlencode({"grant_type": "authorization_code", "code": box["code"], "redirect_uri": REDIRECT,
                                   "client_id": cid, "client_secret": secret}).encode()
    with urllib.request.urlopen(urllib.request.Request("https://www.linkedin.com/oauth/v2/accessToken", data=data)) as r:
        tok = json.load(r)
    print("\n=== Guardá estos valores en el entorno (no los compartas) ===")
    print("LI_ACCESS_TOKEN=%s" % tok.get("access_token"))
    print("(vence en %s días aprox.)" % (int(tok.get("expires_in", 0)) // 86400))
    if tok.get("refresh_token"):
        print("LI_REFRESH_TOKEN=%s" % tok["refresh_token"])
    else:
        print("LinkedIn no entregó refresh token: habrá que repetir esta autorización cuando venza el access token.")
    print("==============================================================")


if __name__ == "__main__":
    main()
