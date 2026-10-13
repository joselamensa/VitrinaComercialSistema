#!/usr/bin/env python3
"""Autorización de YouTube (se ejecuta UNA VEZ en TU computadora, no en la nube).

Qué hace: abre el navegador para que inicies sesión con la cuenta dueña del canal y aceptes el permiso
de subir videos; recibe el código en http://127.0.0.1:8976/ y lo cambia por un *refresh token*.
Al final imprime el refresh token EN TU TERMINAL. Guardalo en el entorno de la nube como YT_REFRESH_TOKEN.
NUNCA lo pegues en un chat.

Uso:  python3 tools/social/oauth_youtube.py
Pide el Client ID y el Client Secret (el secret se escribe oculto). Solo usa la librería estándar.
"""
import getpass
import http.server
import json
import secrets
import threading
import urllib.parse
import urllib.request
import webbrowser

PORT = 8976
REDIRECT = "http://127.0.0.1:%d/" % PORT
SCOPES = "https://www.googleapis.com/auth/youtube.upload https://www.googleapis.com/auth/youtube.readonly"


def main():
    client_id = input("Client ID de Google: ").strip()
    client_secret = getpass.getpass("Client Secret (no se muestra): ").strip()
    state = secrets.token_urlsafe(16)
    box = {}

    class H(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            if q.get("state", [""])[0] == state and "code" in q:
                box["code"] = q["code"][0]
                msg = "Listo. Ya podés cerrar esta pestaña y volver a la terminal."
            else:
                box["error"] = q.get("error", ["respuesta inválida"])[0]
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
    url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode({
        "client_id": client_id, "redirect_uri": REDIRECT, "response_type": "code", "scope": SCOPES,
        "access_type": "offline", "prompt": "consent", "state": state})
    print("\nSe abre el navegador. Si no, copiá este enlace:\n%s\n" % url)
    webbrowser.open(url)
    t.join(timeout=300)
    srv.server_close()
    if "code" not in box:
        raise SystemExit("No llegó el código (%s)." % box.get("error", "tiempo agotado"))
    data = urllib.parse.urlencode({"code": box["code"], "client_id": client_id, "client_secret": client_secret,
                                   "redirect_uri": REDIRECT, "grant_type": "authorization_code"}).encode()
    with urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=data)) as r:
        tok = json.load(r)
    if "refresh_token" not in tok:
        raise SystemExit("Google no devolvió refresh token. Revocá el acceso de la app en tu cuenta de Google y repetí.")
    print("\n=== REFRESH TOKEN (guardalo en el entorno como YT_REFRESH_TOKEN; no lo compartas) ===")
    print(tok["refresh_token"])
    print("=====================================================================================")


if __name__ == "__main__":
    main()
