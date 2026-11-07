#!/usr/bin/env bash
# Voies B et C : relit tout de suite le dossier dags/ et affiche les erreurs d'import.
# Usage, depuis le dossier td-airflow-sante :  bash scripts/rafraichir.sh
set -euo pipefail
cd "$(dirname "$0")/.."
export AIRFLOW_HOME="$PWD/.airflow"
export AIRFLOW__CORE__DAGS_FOLDER="$PWD/dags"
export AIRFLOW__CORE__LOAD_EXAMPLES=False
.venv/bin/airflow dags reserialize
.venv/bin/airflow dags list-import-errors
