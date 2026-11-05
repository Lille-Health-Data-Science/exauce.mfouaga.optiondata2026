"""TP séance 2 · Construire le flux FHIR quotidien des glycémies (20 min).

extraire (API FHIR, pagination) → aplatir (Parquet) → valider (Pandera) → charger (DuckDB, idempotent)

Avant de commencer :
  - copier ce fichier dans dags/ ;
  - créer le pool api_fhir : Admin › Pools › + , nom api_fhir, 3 places.
Étapes :
  1. compléter extraire avec le code de pagination de la séance 1 ;
  2. écrire aplatir vers Parquet ;
  3. ajouter la validation (unités autorisées : g/L, mg/dL, mmol/L) ;
  4. charger dans DuckDB de façon idempotente (DELETE + INSERT du jour) ;
  5. provoquer une panne (mauvaise URL dans BASE) et observer les retries.
"""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path

from airflow.sdk import Asset, dag, task
from airflow.timetables.trigger import CronTriggerTimetable

DONNEES = Path(__file__).resolve().parents[1] / "donnees"
BASE = os.environ.get("FHIR_BASE", "https://hapi.fhir.org/baseR4")   # étape 5 : mettre une mauvaise URL
UNITES = ["g/L", "mg/dL", "mmol/L"]
glycemies = Asset("glycemies")


def jour(data_interval_start) -> str:
    """Le jour traité, au format AAAA-MM-JJ."""
    return (data_interval_start or datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


@dag(schedule=CronTriggerTimetable("0 6 * * *", timezone="Europe/Paris", interval=timedelta(days=1)),
     start_date=datetime(2026, 11, 1), catchup=False, tags=["fhir", "tp"])
def fhir_glycemies_quotidien():

    @task(pool="api_fhir", retries=5, retry_delay=timedelta(minutes=2))
    def extraire(data_interval_start=None) -> str:
        """Étape 1 : glycémies (LOINC 2345-7) modifiées depuis le début de l'intervalle, toutes pages."""
        import requests

        url = f"{BASE}/Observation"
        params = {"code": "http://loinc.org|2345-7", "_count": 100,
                  "_lastUpdated": f"ge{jour(data_interval_start)}"}
        ressources = []
        # À COMPLÉTER : boucle de pagination (séance 1) qui remplit `ressources`
        #   - requests.get(url, params=params, headers={"Accept": "application/fhir+json"}, timeout=30)
        #   - r.raise_for_status() : une erreur HTTP fait échouer la tâche, donc déclenche un retry
        #   - suivre le lien « next » ; params = None ensuite
        ...
        chemin = DONNEES / "brut" / f"glycemies_{jour(data_interval_start)}.ndjson"
        chemin.parent.mkdir(parents=True, exist_ok=True)
        chemin.write_text("".join(json.dumps(o) + "\n" for o in ressources))
        return str(chemin)                            # XCom : un chemin, pas les données

    @task
    def aplatir(chemin: str) -> str:
        """Étape 2 : une ligne par Observation (id, patient, date, statut, valeur, unite), en Parquet."""
        import pandas as pd

        # À COMPLÉTER : lire le NDJSON ligne par ligne, construire un DataFrame,
        # l'écrire avec df.to_parquet(...) et renvoyer le chemin du fichier Parquet
        ...

    @task
    def valider(chemin: str) -> str:
        """Étape 3 : schéma Pandera ; que faire des lignes invalides ?"""
        import pandas as pd
        import pandera.pandas as pa

        # À COMPLÉTER : schéma avec unite dans UNITES, valeur > 0, patient non nul ;
        # écrire les lignes valides en Parquet et renvoyer le chemin
        ...

    @task(outlets=[glycemies])
    def charger(chemin: str, data_interval_start=None):
        """Étape 4 : DELETE + INSERT du jour dans donnees/entrepot.duckdb, donc rejouable sans doublon."""
        import duckdb

        # À COMPLÉTER : table glycemies (valeur convertie en mg/dL comme en séance 1),
        # suppression des lignes du jour puis insertion depuis read_parquet(chemin)
        ...

    charger(valider(aplatir(extraire())))


fhir_glycemies_quotidien()
