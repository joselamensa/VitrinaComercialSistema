#!/usr/bin/env python3
"""Actualiza tools/rate.json con las cotizaciones para el switch de moneda de los planes.

- ARS: dólar OFICIAL (venta) de https://dolarapi.com/v1/dolares/oficial
- UYU, CLP, MXN, COP, PEN, BRL, EUR: tipo de cambio de referencia de https://open.er-api.com/v6/latest/USD
Si una fuente falla, se conserva el último valor conocido de esas monedas. Sale con 1 si no se actualizó nada.
Requiere permitir en la red del entorno: dolarapi.com y open.er-api.com.
Después: python3 tools/build.py
"""
import datetime
import json
import os
import sys
import urllib.request

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rate.json")
OTHERS = ["UYU", "CLP", "MXN", "COP", "PEN", "BRL", "EUR"]


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "tablero-build"}), timeout=20) as r:
        return json.load(r)


def main():
    try:
        prev = json.load(open(PATH, encoding="utf-8"))
    except Exception:
        prev = {}
    rates = {k: float(v) for k, v in prev.get("rates", {}).items()}
    if "venta" in prev and "ARS" not in rates:
        rates["ARS"] = float(prev["venta"])
    updated = []
    try:
        v = float(get("https://dolarapi.com/v1/dolares/oficial")["venta"])
        if 50 < v < 100000:
            rates["ARS"] = v
            updated.append("ARS")
    except Exception as e:  # noqa
        print("ARS: no se pudo actualizar (%s); se conserva el valor anterior." % e)
    try:
        d = get("https://open.er-api.com/v6/latest/USD")
        if d.get("result") == "success":
            for c in OTHERS:
                if c in d["rates"] and float(d["rates"][c]) > 0:
                    rates[c] = float(d["rates"][c])
                    updated.append(c)
    except Exception as e:  # noqa
        print("Otras monedas: no se pudieron actualizar (%s); se conservan las anteriores." % e)
    if not updated:
        print("No se actualizó ninguna cotización.")
        return 1
    out = {"fecha": datetime.date.today().isoformat(),
           "fuente": "ARS: dolarapi.com (dólar oficial, venta). Resto: open.er-api.com (referencia)",
           "rates": {k: round(v, 4) for k, v in sorted(rates.items())}}
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("Actualizado: %s" % ", ".join(updated))
    return 0


if __name__ == "__main__":
    sys.exit(main())
