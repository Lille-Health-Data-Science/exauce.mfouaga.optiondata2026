#!/usr/bin/env bash
# Plan B : lance Airflow (interface, scheduler, etc.) dans un seul processus.
# Interface : http://localhost:8080 (pas de mot de passe). Arrêt : Ctrl+C.
set -euo pipefail
cd "$(dirname "$0")/.."
export PATH="$PWD/.venv/bin:$PATH"        # standalone relance la commande airflow
export AIRFLOW_HOME="$PWD/.airflow"
export AIRFLOW__CORE__DAGS_FOLDER="$PWD/dags"
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_ALL_ADMINS=True
exec airflow standalone
