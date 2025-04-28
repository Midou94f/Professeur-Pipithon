# Pipithon - Système Intelligent d'Apprentissage Python 🚀

Bienvenue dans **Pipithon**, un projet de gamification de l'apprentissage Python avec IA adaptative, XP, niveaux et défis !

---

## 🔍 Aperçu du projet

**Pipithon** propose à chaque joueur :
- des cours interactifs,
- des QCM de validation,
- des défis adaptés au niveau,
- un système de progression basé sur l'XP,
- une expérience personnalisée et motivante.

Chaque action enrichit l'expérience du joueur et lui permet de progresser dans les niveaux de maîtrise du Python !

---

## 🛠þ Fonctionnalités principales

- **Cours dynamiques** selon l'historique
- **Défis Python** répartis par niveau
- **QCM intelligents** pour vérifier la compréhension
- **IA adaptative** qui propose automatiquement le meilleur contenu
- **Système XP et niveaux** inspiré du gaming
- **Citadelle de citations** pour encourager 🌈
- **Historique et suivi** des activités
- **Exportation de statistiques**

---

## 📁 Structure du projet

```bash
pipithon/
├── ai.py              # Intelligence adaptative
├── bot.py             # Gestion des commandes
├── export.py          # Sauvegarde et export des données
├── utils.py           # Fonctions utilitaires
├── cours.json         # Contenu des cours
├── defis.json         # Liste des défis
├── citations.json     # Citations motivantes
├── messages.json      # Messages système et montée de niveau
├── levels.json        # XP et titres par niveau
├── users.json         # Données utilisateurs
├── logs.json          # Historique d'activités
├── xp_rules.json      # Règles d'attribution XP
└── README.md          # Ce fichier
```

---

## 🔧 Installation

### 1. Prérequis

- Python ≥ 3.8
- Bibliothèques : `discord`, `json`, `random`, `datetime`

```bash
pip install -r requirements.txt
```

### 2. Clés API (si besoin)

Si vous utilisez Discord, configurez votre `bot_token`.

---

## 🚷 Lancement du bot

```bash
python bot.py
```

- Utilisez les commandes `!start`, `!continuer`, `!stats`...
- L'IA se charge de tout vous proposer intelligemment !

---

## 💎 Système de Niveaux

| Niveau | XP nécessaire | Titre |
|:------:|:-------------:|:------|
| 1      | 0             | 🐣 Débutant de l'œuf |
| 5      | 100           | 🐍 Apprenti Python |
| 10     | 250           | 🔥 Initié des Boucles |
| 20     | 600           | 🧙‍♂️ Magicien du If |
| 30     | 1100          | 🤖 Maître des Fonctions |

*(Plus de 90 niveaux disponibles !)*

---

## 🎉 Exemple d'utilisation

```bash
!start
> Bienvenue jeune aventurier du Python !

!continuer
> Aujourd'hui, un défi t'attend : écrire une fonction qui affiche chaque lettre d'un mot...
```

---

## 🔄 Améliorations futures

- Mode tournoi multi-joueurs
- Badges et récompenses spéciaux
- Système de quêtes
- Progression visuelle sur un tableau de bord

---

## 👽‍♂️ Auteurs

Projet développé par Mehdi fehri, Zeller Emile, Schneider Hugo pour le cours **Techniques de Programmation II**.

---

> "Chaque jour où tu ouvres ton IDE est un jour où tu refuses d'abandonner."
> — Pipithon
