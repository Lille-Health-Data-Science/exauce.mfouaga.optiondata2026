# TD Airflow · M2 Data Science en santé

Séance 2 de l'option Data (Université de Lille) : **samedi 7 novembre 2026, 8 h – 12 h**.
Ce dossier installe **Airflow 3.3.2** et son interface sur votre ordinateur.

> **À faire avant samedi, chez vous** (30 min environ, avec une bonne connexion : 2 Go à télécharger).
> Le Wi-Fi de la salle ne suffira pas pour l'installation de 30 personnes en même temps.

## Ce qu'il faut

- 8 Go de mémoire vive (4 Go libres pour Airflow) et 5 Go d'espace disque.
- Ce dossier :
  ```bash
  git clone https://github.com/Lille-Health-Data-Science/td-airflow-sante.git
  cd td-airflow-sante
  ```

Trois façons d'installer. Prenez la **A** si vous pouvez ; la **B** si Docker ne s'installe pas ou si votre
ordinateur a moins de 8 Go ; la **C** en dernier recours.

## A · Avec Docker (Windows, macOS, Linux) — recommandé

1. Installer **Docker Desktop** : <https://www.docker.com/products/docker-desktop/>
   - Windows : accepter l'activation de **WSL 2** proposée par l'installeur, puis redémarrer.
   - Ouvrir Docker Desktop, *Settings › Resources* : au moins **4 Go** de mémoire.
   - Linux : Docker Engine et le plugin compose suffisent ; lancer ensuite, dans ce dossier :
     `sed -i "s/^AIRFLOW_UID=.*/AIRFLOW_UID=$(id -u)/" .env`
2. Dans un terminal (PowerShell sous Windows), dans le dossier `td-airflow-sante` :
   ```bash
   docker compose up airflow-init    # première fois seulement : construit l'image et prépare la base (5 à 10 min)
   docker compose up -d              # démarre Airflow en arrière-plan
   ```
   La première commande doit se terminer par `airflow-init-1 exited with code 0`.
3. Ouvrir **<http://localhost:8080>** (1 à 2 minutes après le démarrage) ; identifiant **airflow**, mot de passe **airflow**.

Arrêter : `docker compose stop` · Relancer : `docker compose up -d` · Tout supprimer : `docker compose down --volumes --rmi local`

## B · Sans Docker (macOS, Linux, ou Windows avec WSL 2)

Il faut Python 3.10 à 3.14. Airflow ne fonctionne pas directement sous Windows : il faut WSL 2
(PowerShell en administrateur : `wsl --install`, redémarrer, puis ouvrir « Ubuntu » et y installer
`sudo apt install python3-venv git`).

```bash
bash scripts/installer_sans_docker.sh   # une fois (3 à 5 min)
bash scripts/lancer_sans_docker.sh      # à chaque fois ; laisser ce terminal ouvert
```

Ouvrir **<http://localhost:8080>** : pas de mot de passe. Arrêter : `Ctrl+C` dans le terminal.

## C · Dans le navigateur, avec GitHub Codespaces (dernier recours)

Sur la page GitHub du dépôt : *Code › Codespaces › Create codespace on main*. L'installation se lance seule
(5 min), puis l'interface s'ouvre dans un onglet. Compte GitHub étudiant conseillé (heures gratuites incluses).

## Vérifier que tout marche

1. Dans l'interface, la liste des DAG contient **verification_installation**.
2. Activer le DAG (interrupteur), puis **Trigger**.
3. Dans la vue **Grid**, les trois tâches passent au vert en moins d'une minute, et le fichier
   `donnees/verification.txt` apparaît dans votre dossier.

La dernière tâche teste aussi l'accès au serveur FHIR de la séance 1 ; si le réseau le bloque, elle reste verte
et l'écrit dans son journal.

**Samedi matin, lancez Airflow avant 8 h** (`docker compose up -d` ou `bash scripts/lancer_sans_docker.sh`).

## En cas de problème

| Message | Solution |
|---|---|
| `port is already allocated` ou `address already in use` (8080) | Un autre Airflow tourne déjà : `docker compose down`, ou fermer l'autre terminal ; sinon redémarrer l'ordinateur. |
| `Not enough memory available for Docker` | Docker Desktop › *Settings › Resources* : 4 Go ou plus. |
| `Permission denied` sur `logs/` (Linux) | Mettre votre identifiant dans `.env` (commande `sed` de l'étape A.1), puis `docker compose up airflow-init`. |
| Le DAG n'apparaît pas | Attendre 30 secondes ; une erreur d'import s'affiche en haut de la liste des DAG. |
| Plan B : erreur au clic sur **Trigger** | La base SQLite était occupée : réessayer quelques secondes plus tard. |
| Autre chose | Apporter une capture d'écran samedi, ou écrire à l'enseignant avant. |

## Contenu du dossier

| Élément | Rôle |
|---|---|
| `docker-compose.yaml` | Fichier officiel d'Airflow 3.3.2, 4 modifications repérées « M2 DSS » |
| `Dockerfile`, `requirements.txt` | Image Airflow + pandas, Pandera, DuckDB pour les TP |
| `dags/` | Les DAG lus par Airflow ; au départ, seulement `00_verification.py` |
| `exercices/` | Fichiers de la séance (exercice 1, TP) : **ne pas les copier dans `dags/` avant le cours** |
| `donnees/` | Fichiers produits par les DAG, partagés avec Airflow |
| `scripts/` | Installation sans Docker (plan B) |
| `.devcontainer/` | Configuration GitHub Codespaces (plan C) |
