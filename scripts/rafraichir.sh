#!/usr/bin/env bash
# Voies B et C : relit tout de suite le dossier dags/ et affiche les erreurs d'import.
# Usage, depuis le dossier td-airflow-sante :  bash scripts/rafraichir.sh
set -euo pipefail
cd "$(dirname "$0")/.."
source scripts/env.sh
airflow dags reserialize >/dev/null 2>&1 && echo "Dossier dags/ relu : rechargez la page d'Airflow."
echo "Erreurs d'import (« No data found » = aucune) :"
airflow dags list-import-errors 2>/dev/null
