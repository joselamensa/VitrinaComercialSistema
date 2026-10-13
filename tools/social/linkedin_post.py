#!/usr/bin/env python3
"""Publica en la PÁGINA DE EMPRESA de LinkedIn (texto, con enlace opcional a un artículo).

Variables de entorno: LI_ACCESS_TOKEN, LI_ORG_ID (número de la página), opcional LI_API_VERSION (AAAAMM, default 202510),
y para renovar el token: LI_CLIENT_ID, LI_CLIENT_SECRET, LI_REFRESH_TOKEN. Red: api.linkedin.com, www.linkedin.com.

Uso:
  python3 tools/social/linkedin_post.py --text-file post.txt [--link URL --link-title "T" --link-description "D"]
  python3 tools/social/linkedin_post.py --check          # verifica que el token y la página funcionen, sin publicar
"""
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request


def little_text(s):
    # LinkedIn "little text": estos caracteres se escapan con barra invertida.
    return re.sub(r"([\\|{}@\[\]()<>#*_~])", r"\\\1", s)


def headers():
    return {"Authorization": "Bearer " + os.environ["LI_ACCESS_TOKEN"], "X-Restli-Protocol-Version": "2.0.0",
            "LinkedIn-Version": os.environ.get("LI_API_VERSION", "202510"), "Content-Type": "application/json"}


def refresh():
    if not (os.environ.get("LI_REFRESH_TOKEN") and os.environ.get("LI_CLIENT_ID") and os.environ.get("LI_CLIENT_SECRET")):
        return False
    data = urllib.parse.urlencode({"grant_type": "refresh_token", "refresh_token": os.environ["LI_REFRESH_TOKEN"],
                                   "client_id": os.environ["LI_CLIENT_ID"], "client_secret": os.environ["LI_CLIENT_SECRET"]}).encode()
    with urllib.request.urlopen(urllib.request.Request("https://www.linkedin.com/oauth/v2/accessToken", data=data), timeout=30) as r:
        os.environ["LI_ACCESS_TOKEN"] = json.load(r)["access_token"]
    return True


def call(req_factory):
    try:
        return urllib.request.urlopen(req_factory(), timeout=60)
    except urllib.error.HTTPError as e:
        if e.code == 401 and refresh():
            return urllib.request.urlopen(req_factory(), timeout=60)
        sys.exit("Error de LinkedIn %s: %s" % (e.code, e.read()[:400].decode("utf-8", "replace")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text-file")
    ap.add_argument("--text")
    ap.add_argument("--link")
    ap.add_argument("--link-title", default="")
    ap.add_argument("--link-description", default="")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    for v in ("LI_ACCESS_TOKEN", "LI_ORG_ID"):
        if not os.environ.get(v):
            sys.exit("Falta la variable de entorno %s" % v)
    org = "urn:li:organization:%s" % os.environ["LI_ORG_ID"]
    if a.check:
        url = "https://api.linkedin.com/rest/posts?author=%s&q=author&count=1" % urllib.parse.quote(org, safe="")
        with call(lambda: urllib.request.Request(url, headers={**headers(), "X-RestLi-Method": "FINDER"})) as r:
            print("OK: el token puede leer las publicaciones de la página (HTTP %s)." % r.status)
        return
    text = open(a.text_file, encoding="utf-8").read().strip() if a.text_file else (a.text or "")
    if not text:
        sys.exit("Falta el texto (--text o --text-file)")
    body = {"author": org, "commentary": little_text(text), "visibility": "PUBLIC",
            "distribution": {"feedDistribution": "MAIN_FEED", "targetEntities": [], "thirdPartyDistributionChannels": []},
            "lifecycleState": "PUBLISHED", "isReshareDisabledByAuthor": False}
    if a.link:
        body["content"] = {"article": {"source": a.link, "title": a.link_title or a.link, "description": a.link_description}}
    payload = json.dumps(body).encode()
    with call(lambda: urllib.request.Request("https://api.linkedin.com/rest/posts", data=payload, method="POST", headers=headers())) as r:
        print("Publicado. ID: %s" % r.headers.get("x-restli-id"))


if __name__ == "__main__":
    main()
