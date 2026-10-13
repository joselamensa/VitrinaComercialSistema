#!/usr/bin/env python3
"""Sube (y opcionalmente programa) un video al canal de YouTube autorizado.

Variables de entorno: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN  (nunca se imprimen)
Red: www.googleapis.com y oauth2.googleapis.com

Ejemplos:
  python3 tools/social/youtube_upload.py video.mp4 --title "Título" --description-file desc.txt --tags "a,b,c"
  python3 tools/social/youtube_upload.py video.mp4 --title "T" --description-file d.txt --publish-at 2026-10-20T13:00:00Z
IMPORTANTE: mientras el proyecto de Google Cloud no pase la auditoría de YouTube API, Google deja los videos subidos
por API en PRIVADO. Ver docs/publicacion-automatica.md. Por seguridad el valor por defecto es --privacy private.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def access_token():
    data = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    with urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=data), timeout=30) as r:
        return json.load(r)["access_token"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--title", required=True)
    ap.add_argument("--description-file")
    ap.add_argument("--description", default="")
    ap.add_argument("--tags", default="")
    ap.add_argument("--privacy", default="private", choices=["private", "unlisted", "public"])
    ap.add_argument("--publish-at", help="RFC3339 en UTC, p. ej. 2026-10-20T13:00:00Z (fuerza privacy=private hasta esa hora)")
    ap.add_argument("--category", default="28")
    ap.add_argument("--thumbnail")
    a = ap.parse_args()
    for v in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"):
        if not os.environ.get(v):
            sys.exit("Falta la variable de entorno %s" % v)
    desc = open(a.description_file, encoding="utf-8").read() if a.description_file else a.description
    status = {"privacyStatus": "private" if a.publish_at else a.privacy, "selfDeclaredMadeForKids": False}
    if a.publish_at:
        status["publishAt"] = a.publish_at
    meta = {"snippet": {"title": a.title[:100], "description": desc[:5000], "categoryId": a.category,
                        "tags": [t.strip() for t in a.tags.split(",") if t.strip()]}, "status": status}
    tok = access_token()
    size = os.path.getsize(a.file)
    req = urllib.request.Request(
        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
        data=json.dumps(meta).encode(), method="POST",
        headers={"Authorization": "Bearer " + tok, "Content-Type": "application/json; charset=UTF-8",
                 "X-Upload-Content-Length": str(size), "X-Upload-Content-Type": "video/*"})
    with urllib.request.urlopen(req, timeout=60) as r:
        loc = r.headers["Location"]
    with open(a.file, "rb") as f:
        body = f.read()
    put = urllib.request.Request(loc, data=body, method="PUT", headers={"Authorization": "Bearer " + tok, "Content-Type": "video/*"})
    try:
        with urllib.request.urlopen(put, timeout=900) as r:
            res = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit("Error de YouTube %s: %s" % (e.code, e.read()[:400].decode("utf-8", "replace")))
    vid = res["id"]
    print("Subido: https://www.youtube.com/watch?v=%s (estado: %s)" % (vid, res.get("status", {}).get("privacyStatus")))
    if a.thumbnail:
        t = urllib.request.Request("https://www.googleapis.com/upload/youtube/v3/thumbnails/set?videoId=" + vid,
                                   data=open(a.thumbnail, "rb").read(), method="POST",
                                   headers={"Authorization": "Bearer " + tok, "Content-Type": "image/jpeg"})
        try:
            urllib.request.urlopen(t, timeout=60)
            print("Miniatura cargada.")
        except urllib.error.HTTPError as e:
            print("No se pudo cargar la miniatura (%s). Puede requerir canal verificado." % e.code)


if __name__ == "__main__":
    main()
