# BOT Discord – Apprentissage gamifié de Python

_Auteurs : Mehdi Fehri, Emile Zeller, Hugo Schneider_

---

## 📚 Présentation du projet

Bienvenue sur notre projet !  
Nous avons conçu un bot Discord destiné à accompagner l'apprentissage du langage Python de manière ludique et motivante.  
Le bot agit comme un mentor virtuel : il propose des défis, génère des cours personnalisés et récompense les progrès des utilisateurs par des points d'expérience (XP) et des niveaux.

Notre ambition est de transformer l'étude du Python en une expérience dynamique, progressive et adaptée au rythme de chacun.

---

## ❓ Pourquoi ce projet ?

Apprendre un langage de programmation peut parfois sembler monotone ou difficile.  
Nous avons voulu introduire des mécaniques de gamification inspirées des jeux vidéo :  
- Progression par XP,
- Titres et niveaux motivants,
- Suivi personnalisé,
- Défis adaptés au niveau de chacun.

Le bot vise à maintenir l'intérêt des utilisateurs sur le long terme, tout en renforçant leurs compétences en Python à travers des interactions régulières et ciblées.

---

## 🚀 Fonctionnalités principales

Notre bot propose :

- **Défis automatiques** : des exercices pratiques adaptés au niveau de l'utilisateur, générés par l'IA.
- **Génération de mini-cours personnalisés** : explication claire d'un concept Python avec exemple et défi associé.
- **Suivi de la progression** : accumulation d'XP, montée en niveaux, historique des exercices réalisés.
- **Gamification** : titres motivants, classement entre utilisateurs, badges spéciaux pour récompenser l'assiduité.
- **Citations inspirantes** : pour maintenir la motivation des apprenants.
- **Relances en cas d'inactivité** : le bot rappelle les utilisateurs au bout de 72 heures sans activité.

Chaque interaction est conçue pour être engageante, adaptée et enrichissante.

---

## 🔧 Installation et configuration

### Prérequis
- Python 3.9 ou supérieur
- Un compte Discord et un serveur où installer le bot
- Un compte OpenAI (clé API nécessaire pour l'utilisation de GPT-3.5)

### Étapes d'installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/votre-utilisateur/votre-depot.git
   cd votre-depot
   ```

2. Installez les dépendances nécessaires :
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez le fichier `config.json` :
   ```json
   {
     "GPTKEY": "votre_clé_OpenAI",
     "GPT_MODEL": "gpt-3.5-turbo",
     "DISCORD_TOKEN": "votre_token_discord",
     "GUILD_ID": "id_de_votre_serveur"
   }
   ```

4. Lancez le bot :
   ```bash
   python bot.py
   ```

Le bot sera alors actif sur votre serveur Discord, prêt à interagir avec les utilisateurs !

---

## ⚙️ Comment fonctionne le bot ?

Dès qu'un utilisateur interagit avec le bot via les commandes `/prof`, `/cours`, `/défi`, etc., le bot :

- Analyse son profil (niveau, XP, historique).
- Génère une réponse personnalisée via OpenAI.
- Attribue de l'XP en fonction de la réussite.
- Met à jour les données utilisateurs stockées dans des fichiers JSON (`users.json`, `logs.json`, etc.).
- Propose de nouveaux contenus adaptés au niveau de l'utilisateur.

Chaque action est asynchrone pour garantir une réponse rapide, sans bloquer les autres utilisateurs.

---

## 🛠️ Architecture technique

- **bot.py** : cœur de l'application, gère les commandes Discord, l'attribution d'XP et la gestion des événements.
- **ai.py** : utilise OpenAI pour générer dynamiquement des cours, défis et réponses personnalisées.
- **utils.py** : fonctions de gestion de la persistance JSON, calculs d'XP, montées en niveau et historique des activités.

Toutes les données utilisateurs sont stockées localement dans des fichiers `.json`, assurant la mémoire longue durée et la personnalisation des parcours d'apprentissage.

---

## 📈 Progression et niveaux

Chaque action réalisée (suivre un cours, réussir un défi, répondre à un QCM) rapporte de l'XP.  
Lorsque l'utilisateur atteint un certain seuil d'XP, il passe au niveau supérieur et reçoit un nouveau titre motivant.

Exemple de palier :
```json
{ "niveau": 10, "xp": 250, "titre": "🔥 Initié des Boucles" }
```

L'évolution est conçue pour maintenir l'intérêt et encourager l'apprentissage régulier.

---

## 💪 Points forts

- **Mémoire individuelle complète** : XP, niveaux et historique sont conservés pour chaque utilisateur.
- **Adaptation intelligente** : la difficulté des défis est ajustée selon les performances récentes.
- **Architecture modulaire** : le code est propre, séparé par responsabilités (commandes, IA, gestion de données).
- **Approche ludique** : progression gratifiante, leaderboards et badges motivants.

---

## ⚠️ Limites connues

- Dépendance à l'API OpenAI (limites de quota, coût éventuel).
- Stockage en fichiers JSON (limité pour un nombre très élevé d'utilisateurs).
- Gestion d'erreurs partielle sur certaines commandes.
- Bot actuellement uniquement en français.
- Disponible uniquement via Discord (pas encore d'API Web publique).

---

## 🔭 Perspectives d'évolution

- Développement d'une interface Web complémentaire.
- Migration vers une base de données plus robuste (ex. SQLite, PostgreSQL).
- Enrichissement des cours et défis générés.
- Ajout d'un système de récompenses spéciales et de mini-jeux éducatifs.

---

## 🤝 Contribuer

Les contributions sont les bienvenues !  
N'hésitez pas à ouvrir une issue pour signaler un bug ou proposer une amélioration, ou à soumettre une pull request.

---

## 📬 Contact

Pour toute question ou suggestion, veuillez nous contacter via GitHub.

---
