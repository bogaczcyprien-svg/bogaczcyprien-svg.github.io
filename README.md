# Météo

Script Python qui affiche la météo actuelle d'une ville donnée en argument, via l'API gratuite [wttr.in](https://wttr.in) (aucune clé API requise).

## Prérequis

- Python 3.10+

## Usage

```
python meteo.py <ville>
```

Exemple :

```
python meteo.py Paris
```

### Unité de température

Par défaut, la température est affichée en Celsius. L'unité peut être choisie selon l'ordre de priorité suivant :

1. Option `--unit` en ligne de commande (`C` ou `F`)
2. Variable d'environnement `METEO_UNIT`
3. Celsius par défaut

Exemples :

```
python meteo.py Paris --unit F
```

```
$env:METEO_UNIT="F"
python meteo.py Paris
```

## Sortie

```
Météo actuelle à Saint-Merri, France
  Condition       : Partly Cloudy
  Température     : 32 °C (ressenti 32 °C)
  Humidité        : 34 %
  Vent            : 7 km/h
```
