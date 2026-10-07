#!/usr/bin/env python3
"""Avisa a los buscadores que usan IndexNow (Bing, Yandex, Naver, Seznam...) de URLs nuevas o modificadas.

Google NO usa IndexNow: para Google valen el sitemap y los enlaces internos.
La clave es pública por diseño: el archivo /<clave>.txt de la raíz prueba que el sitio es tuyo.

Uso:
  python3 tools/indexnow.py            # envía todas las URLs del sitemap
  python3 tools/indexnow.py --changed  # solo las páginas tocadas en el último commit
  python3 tools/indexnow.py --changed --since HEAD~3
  python3 tools/indexnow.py URL [URL ...]
Requiere acceso de red a api.indexnow.org.
"""
import json
import os
import re
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from content import SITE_URL, INDEXNOW_KEY  # noqa

HOST = SITE_URL.split("//")[1]


def sitemap_urls():
    return re.findall(r"<loc>(.*?)</loc>", open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read())


def changed_urls(since):
    out = subprocess.run(["git", "diff", "--name-only", since, "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    urls = set()
    for f in out:
        if f == "index.html":
            urls.add(SITE_URL + "/")
        elif f.endswith("/index.html"):
            urls.add("%s/%s/" % (SITE_URL, f[: -len("/index.html")]))
        elif f in ("sitemap.xml", "robots.txt"):
            continue
    # si cambia el CSS o el generador compartido, no se reenvía todo: solo lo que realmente cambió en HTML
    return sorted(u for u in urls if u in set(sitemap_urls()))


def main(argv):
    args = argv[1:]
    if "--changed" in args:
        since = args[args.index("--since") + 1] if "--since" in args else "HEAD~1"
        urls = changed_urls(since)
    elif args and not args[0].startswith("--"):
        urls = args
    else:
        urls = sitemap_urls()
    if not urls:
        print("Nada para enviar.")
        return 0
    body = json.dumps({"host": HOST, "key": INDEXNOW_KEY, "keyLocation": "%s/%s.txt" % (SITE_URL, INDEXNOW_KEY), "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/IndexNow", data=body, headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print("IndexNow: HTTP %s — %d URLs enviadas" % (r.status, len(urls)))
    except urllib.error.HTTPError as e:
        # 200/202 = aceptado; 403 = clave no verificada aún; 422 = URL fuera del host; 429 = demasiados pedidos
        print("IndexNow: HTTP %s %s" % (e.code, e.reason))
        return 1
    except Exception as e:  # noqa
        print("IndexNow: no se pudo conectar (%s). ¿Está permitido api.indexnow.org en la red del entorno?" % e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
