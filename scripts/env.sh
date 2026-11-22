# Réglages Airflow des voies B et C. À charger dans un terminal avec :  source scripts/env.sh
# Ensuite, toutes les commandes « airflow ... » visent l'Airflow du TD.
_TD="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$_TD/.venv/bin:$PATH"
export AIRFLOW_HOME="$_TD/.airflow"
export AIRFLOW__CORE__DAGS_FOLDER="$_TD/dags"
export AIRFLOW__CORE__LOAD_EXAMPLES=False
export AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_ALL_ADMINS=True
export AIRFLOW__DAG_PROCESSOR__REFRESH_INTERVAL=30
unset _TD
