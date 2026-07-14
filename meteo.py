#!/usr/bin/env python3
"""Affiche la météo actuelle d'une ville donnée en argument."""

import argparse
import sys
import io
import os
import urllib.request
import urllib.parse
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def get_weather(ville: str) -> dict:
    url = "https://wttr.in/" + urllib.parse.quote(ville) + "?format=j1"
    with urllib.request.urlopen(url, timeout=10) as response:
        return json.loads(response.read().decode())


def unite_preferee(unite_cli: str | None) -> str:
    """CLI > variable d'environnement METEO_UNIT > Celsius par défaut."""
    if unite_cli:
        return unite_cli.upper()
    return os.environ.get("METEO_UNIT", "C").upper()


def main():
    parser = argparse.ArgumentParser(description="Affiche la météo actuelle d'une ville.")
    parser.add_argument("ville")
    parser.add_argument(
        "--unit", choices=["C", "F", "c", "f"], default=None,
        help="Unité de température (C ou F). Sinon, utilise la variable "
             "d'environnement METEO_UNIT, sinon Celsius par défaut.",
    )
    args = parser.parse_args()

    unite = unite_preferee(args.unit)
    if unite not in ("C", "F"):
        print(f"Unité inconnue « {unite} », utilisation de Celsius par défaut.")
        unite = "C"

    try:
        data = get_weather(args.ville)
    except Exception as e:
        print(f"Erreur lors de la récupération de la météo : {e}")
        sys.exit(1)

    current = data["current_condition"][0]
    zone = data["nearest_area"][0]

    nom_ville = zone["areaName"][0]["value"]
    pays = zone["country"][0]["value"]
    description = current["weatherDesc"][0]["value"]
    humidite = current["humidity"]
    vent_kmh = current["windspeedKmph"]

    if unite == "F":
        temp = current["temp_F"]
        ressenti = current["FeelsLikeF"]
        symbole = "°F"
    else:
        temp = current["temp_C"]
        ressenti = current["FeelsLikeC"]
        symbole = "°C"

    print(f"Météo actuelle à {nom_ville}, {pays}")
    print(f"  Condition       : {description}")
    print(f"  Température     : {temp} {symbole} (ressenti {ressenti} {symbole})")
    print(f"  Humidité        : {humidite} %")
    print(f"  Vent            : {vent_kmh} km/h")


if __name__ == "__main__":
    main()
