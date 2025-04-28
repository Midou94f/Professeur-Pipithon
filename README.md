# Professeur Pipithon - Bot Discord d'apprentissage Python 🐍

## Présentation

Professeur Pipithon est un bot Discord éducatif et interactif conçu pour rendre l'apprentissage du Python **motivant**, **progressif** et **personnalisé**.

- 📚 **Apprentissage par défis** : chaque utilisateur reçoit des défis adaptés à son niveau.
- 🎮 **Gamification** : XP, niveaux, titres et badges pour stimuler la progression.
- 🧠 **Intelligence adaptative** : difficulté des défis ajustée en fonction des réussites récentes.
- 🗂️ **Mémoire individuelle** : sauvegarde de l'XP, des cours suivis et des défis réussis.
- ✨ **Citations motivantes** : boost de moral avec des citations drôles et inspirantes.

## Fonctionnalités principales

- Commandes slash Discord (`/prof`, `/stats`, `/classement`, `/citation`, `/reset`)
- Génération automatique de cours, QCM et défis personnalisés via GPT.
- Suivi de l'expérience utilisateur dans des fichiers JSON (`users.json`, `levels.json`, `cours.json`, `citations.json`).
- Système de montée en niveau automatique avec titres motivants.
- Relance des utilisateurs inactifs et classement hebdomadaire.

## Architecture

| Composant  | Rôle | Détails |
|------------|------|---------|
| `bot.py`   | Interface Discord | Commandes, gestion XP, classement, tâches périodiques. |
| `ai.py`    | Génération IA | Création de cours/QCM personnalisés via OpenAI. |
| `utils.py` | Persistance JSON | Gestion des utilisateurs, XP, historique et sélection adaptative des défis. |
| `*.json`   | Base de données | Utilisateurs, niveaux, cours, citations, règles d'XP. |

Architecture pensée pour être **modulaire, robuste** et **évolutive**.

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-repo/professeur-pipithon.git
   cd professeur-pipithon

