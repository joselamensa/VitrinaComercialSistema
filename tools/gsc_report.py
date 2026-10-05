#!/usr/bin/env python3
"""Reporte de Google Search Console (solo lectura) para el agente SEO.

Requiere:  pip install google-auth requests
Variables de entorno:
  GSC_SERVICE_ACCOUNT_JSON  contenido del JSON de la cuenta de servicio
  GSC_SITE                  p. ej. sc-domain:tablero.uno  o  https://www.tablero.uno/
Si faltan, imprime un aviso y sale con código 0 (el agente sigue con los chequeos técnicos).
Nunca imprime credenciales.
"""
import datetime as dt
import json
import os
import sys
import urllib.parse


def main():
    raw, site = os.environ.get("GSC_SERVICE_ACCOUNT_JSON"), os.environ.get("GSC_SITE")
    if not raw or not site:
        print("SIN_DATOS: faltan GSC_SERVICE_ACCOUNT_JSON o GSC_SITE. Seguí solo con chequeos técnicos.")
        return 0
    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import AuthorizedSession
    except ImportError:
        print("SIN_DATOS: instalá dependencias: pip install google-auth requests")
        return 0
    creds = service_account.Credentials.from_service_account_info(
        json.loads(raw), scopes=["https://www.googleapis.com/auth/webmasters.readonly"])
    s = AuthorizedSession(creds)
    base = "https://searchconsole.googleapis.com/webmasters/v3/sites/%s/searchAnalytics/query" % urllib.parse.quote(site, safe="")
    end = dt.date.today() - dt.timedelta(days=3)  # GSC tiene ~2-3 días de demora

    def q(start, stop, dims, limit=25):
        r = s.post(base, json={"startDate": str(start), "endDate": str(stop), "dimensions": dims, "rowLimit": limit})
        if r.status_code != 200:
            print("ERROR API %s: %s" % (r.status_code, r.text[:300]))
            sys.exit(0)
        return r.json().get("rows", [])

    cur_s, prev_e = end - dt.timedelta(days=27), end - dt.timedelta(days=28)
    prev_s = prev_e - dt.timedelta(days=27)

    def tot(a, b):
        rows = q(a, b, [], 1)
        return rows[0] if rows else {"clicks": 0, "impressions": 0, "ctr": 0, "position": 0}

    c, p = tot(cur_s, end), tot(prev_s, prev_e)
    print("# Search Console — %s a %s (vs. 28 días previos)\n" % (cur_s, end))
    print("| Métrica | Actual | Previo |\n|---|---|---|")
    print("| Clics | %d | %d |" % (c["clicks"], p["clicks"]))
    print("| Impresiones | %d | %d |" % (c["impressions"], p["impressions"]))
    print("| CTR | %.1f%% | %.1f%% |" % (c["ctr"] * 100, p["ctr"] * 100))
    print("| Posición media | %.1f | %.1f |\n" % (c["position"], p["position"]))

    qs = q(cur_s, end, ["query"], 250)
    print("## Top consultas")
    for r in sorted(qs, key=lambda r: -r["impressions"])[:15]:
        print("- %s — imp %d, clics %d, pos %.1f" % (r["keys"][0], r["impressions"], r["clicks"], r["position"]))
    print("\n## Oportunidades (posición 8–30 con impresiones): candidatas a artículo o mejora")
    for r in sorted([r for r in qs if 8 <= r["position"] <= 30], key=lambda r: -r["impressions"])[:15]:
        print("- %s — imp %d, pos %.1f" % (r["keys"][0], r["impressions"], r["position"]))
    print("\n## Páginas con muchas impresiones y CTR bajo (mejorar title/description)")
    pg = q(cur_s, end, ["page"], 100)
    for r in sorted([r for r in pg if r["impressions"] >= 20 and r["ctr"] < 0.02], key=lambda r: -r["impressions"])[:10]:
        print("- %s — imp %d, CTR %.1f%%, pos %.1f" % (r["keys"][0], r["impressions"], r["ctr"] * 100, r["position"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
