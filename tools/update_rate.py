#!/usr/bin/env python3
"""Actualiza tools/rate.json con el dólar OFICIAL (venta) para la opción "ARS" del switch de precios.

Los precios de los planes son en USD; el peso argentino es solo una comodidad para visitantes de Argentina.
Fuente: https://dolarapi.com/v1/dolares/oficial (requiere permitir dolarapi.com en la red del entorno).
Si falla, se conserva el valor anterior y sale con código 1. Después: python3 tools/build.py
"""
import datetime
import json
import os
import sys
import urllib.request

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rate.json")


def main():
    try:
        req = urllib.request.Request("https://dolarapi.com/v1/dolares/oficial", headers={"User-Agent": "tablero-build"})
        with urllib.request.urlopen(req, timeout=20) as r:
            venta = float(json.load(r)["venta"])
        if not (50 < venta < 100000):
            raise ValueError("valor fuera de rango: %s" % venta)
    except Exception as e:  # noqa
        print("No se pudo actualizar la cotización (%s). Se conserva la anterior." % e)
        return 1
    out = {"fecha": datetime.date.today().isoformat(), "fuente": "dolarapi.com (dólar oficial, venta)", "rates": {"ARS": venta}}
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("Dólar oficial (venta): %s al %s" % (venta, out["fecha"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
