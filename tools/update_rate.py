#!/usr/bin/env python3
"""Actualiza tools/rate.json con el dólar oficial (venta) para el switch USD/ARS de los planes.

Fuente: https://dolarapi.com/v1/dolares/oficial  (requiere permitir el dominio dolarapi.com en la red del entorno).
Si falla, NO modifica el archivo anterior y sale con código 1.
Después de actualizar: python3 tools/build.py
"""
import datetime
import json
import os
import sys
import urllib.request

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rate.json")
URL = "https://dolarapi.com/v1/dolares/oficial"


def main():
    try:
        with urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "tablero-build"}), timeout=20) as r:
            d = json.load(r)
        venta = float(d["venta"])
        if not (50 < venta < 100000):
            raise ValueError("valor fuera de rango: %s" % venta)
    except Exception as e:  # noqa
        print("No se pudo actualizar la cotización (%s). Se conserva la anterior." % e)
        return 1
    out = {"venta": venta, "fecha": datetime.date.today().isoformat(), "fuente": "dolarapi.com — dólar oficial (venta)"}
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("Cotización oficial (venta): %s al %s" % (venta, out["fecha"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
