![Streamlit](https://img.shields.io/badge/Streamlit-%23FE4B4B.svg?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)

# 🚗 Projet POC YourCarYourWay

Ce projet est une preuve de concept pour l'utilisation du chat en ligne.

> [!NOTE]
> Vous trouverez la documentation de la base de donnée dans [Wiki](https://github.com/Tom-DevWeb/OC-DA_Angular_Java-P13_YourCarYourWay/wiki).


## 🛠️ Installation

Pour installer le projet, exécuter les commandes suivantes :

```bash
# Cloner le projet

# Créer un environnement virtuel
python3 -m venv venv

# Activer l'environnement sur Linux ou MacOS
source venv/bin/activate

# OU activer l'environnement sous Windows
venv\Scripts\activate.bat   # cmd
venv\Scripts\Activate.ps1   # PowerShell

# Installer les librairies
pip install -r requirements.txt
```

## 🚀 Lancement

> [!IMPORTANT]
> Prérequis :
> Avoir Docker installé sur son environnement

```bash
# Lancement de Docker
docker compose up
```

```bash
# Lancer l'application
source venv/bin/activate
streamlit run main.py
```

## 🚮 Reset

```bash
# Éteindre conteneur docker et supprimer le volume
docker compose up -v
```
