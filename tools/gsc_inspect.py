#!/usr/bin/env python3
"""Inspección de URLs en Google Search Console (solo lectura).

Revisa, para cada URL del sitemap (más variantes http/sin-www de la home), cómo la ve Google:
estado de cobertura, canónica elegida por Google, último rastreo, etc.
Útil para entender avisos como «Página con redirección» o «Rastreada: actualmente sin indexar».

Requiere:  pip install google-auth requests
Variables: GSC_SERVICE_ACCOUNT_JSON, GSC_SITE   (nunca se imprimen)
Uso:  python3 tools/gsc_inspect.py [--extra URL ...]
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    raw, site = os.environ.get("GSC_SERVICE_ACCOUNT_JSON"), os.environ.get("GSC_SITE")
    if not raw or not site:
        print("SIN_DATOS: faltan GSC_SERVICE_ACCOUNT_JSON o GSC_SITE.")
        return 0
    from google.oauth2 import service_account
    from google.auth.transport.requests import AuthorizedSession
    creds = service_account.Credentials.from_service_account_info(
        json.loads(raw), scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    s = AuthorizedSession(creds)
    sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
    urls = re.findall(r"<loc>(.*?)</loc>", sm)
    extra = ["http://tablero.uno/", "https://tablero.uno/", "http://www.tablero.uno/", "https://www.tablero.uno/index.html"]
    if "--extra" in sys.argv:
        extra += sys.argv[sys.argv.index("--extra") + 1:]
    seen = set()
    print("| URL | Veredicto | Cobertura | Canónica de Google | Último rastreo |\n|---|---|---|---|---|")
    for u in extra + urls:
        if u in seen:
            continue
        seen.add(u)
        r = s.post("https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                   json={"inspectionUrl": u, "siteUrl": site, "languageCode": "es-419"})
        if r.status_code != 200:
            print("| %s | ERROR %s | %s | | |" % (u, r.status_code, r.text[:120].replace("\n", " ")))
            continue
        x = r.json().get("inspectionResult", {}).get("indexStatusResult", {})
        print("| %s | %s | %s | %s | %s |" % (u, x.get("verdict", "?"), x.get("coverageState", "?"),
              x.get("googleCanonical", "-"), x.get("lastCrawlTime", "-")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
