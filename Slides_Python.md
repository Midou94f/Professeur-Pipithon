# 🎯 Projet Python : Création d'un BOT Discord favorisant l'apprentissage de Python

Auteurs : FEHRI MEHDI, ZELLER EMILE, SCHNEIDER HUGO 

---
# 📚 Introduction
- Objectif : Créer un outil interactif et intelligent pour l'apprentissage de Python.
- Approche : Mélanger éducation et gamification pour stimuler la motivation.
- Principe : Apprendre en relevant des défis, accumulant de l'XP, progressant en niveaux et bénéficiant d'une expérience personnalisée.

---

# ❓ Problématique
- Comment rendre l'apprentissage du Python plus motivant et progressif ?
- Comment suivre, enregistrer et encourager la progression individuelle des utilisateurs ?

---

# 💡 Solution proposée
- Un Bot éducatif interactif qui propose :
  - Défis automatiques 🧩 (adaptés au niveau de l'utilisateur)
  - Suivi personnalisé d'XP et montée en niveau 🎮
  - Mémoire individuelle de la progression 📈
  - Citations motivantes pour garder la forme 💬
- Toutes les données sont gérées et stockées de manière flexible via des fichiers JSON.

---

# 🛠️ Architecture générale
- Trois modules Python principaux :
  - `bot.py` : orchestre toutes les interactions avec les utilisateurs en pilotant les actions et les récompenses
  - `ai.py` : génère des réponses personnalisées et des mini-cours adaptés au niveau de l'utilisateur via OpenAI
  - `utils.py` : gère l'attribution d'XP, la montée en niveaux, ainsi que la lecture et sauvegarde des données utilisateurs
- Fichiers JSON utilisés pour stocker :
  - Citations, niveaux, utilisateurs, historiques d'actions, messages standards, règles d'XP.

---

# 🧩 Fonctionnement de `bot.py`
- Fichier **central** qui orchestre toutes les interactions avec l'utilisateur.
- Selon l'action : génère un défi, propose un cours, lance un QCM ou affiche une citation.
- Gère en temps réel :
  - L'attribution de l'XP,
  - La montée en niveaux,
  - La sauvegarde des actions dans les logs (`logs.json`).

```python
if action == "debut_defi":
    defi = generer_defi(user)
    attribuer_xp(user, "defi_reussi")
```

---

# 🧠 Fonctionnement de `ai.py`
- Génère automatiquement des **défis et des mini-cours personnalisés** selon le niveau et l'historique de l'utilisateur.
- Utilise l'API **OpenAI GPT** pour produire du contenu structuré et pertinent.
- Permet une montée progressive de la difficulté pour adapter l'apprentissage.

```python
def generer_defi(user):
    niveau = user["level"]
    if niveau < 10:
        return "Crée une fonction qui additionne deux nombres."
    else:
        return "Crée une fonction qui trie une liste."
```
- Garantit des réponses toujours strictement orientées vers Python et sous format JSON exploitable.

---

# 🛠️ Fonctionnement de `utils.py`
- Gère tous les aspects techniques de la progression utilisateur :
  - Calcul et attribution dynamique de l'XP,
  - Vérification et mise à jour du niveau,
  - Chargement et sauvegarde fiables des fichiers JSON (`users.json`, `xp_rules.json`, `logs.json`).
- Permet de persister les progrès et d'assurer la mémoire longue durée du bot.

```python
def attribuer_xp(user, action):
    rules = charger_json("xp_rules.json")
    xp_gagne = rules[action]["base"] + user["level"] * rules[action]["bonus_par_niveau"]
    user["xp"] += xp_gagne
    verifier_niveau(user)
```

---

# 🗃️ Utilisation des fichiers JSON
- `users.json` : sauvegarde permanente de l'expérience, du niveau et de l'historique utilisateur.
- `levels.json` : structure des niveaux et paliers d'expérience.
- `logs.json` : enregistrement complet de toutes les actions effectuées par les utilisateurs.
- `messages.json` : messages standards (réponses aux QCM, cours, défis).
- `xp_rules.json` : règles précises de gain et perte d'XP.
- `citations.json` : citations motivantes et humoristiques envoyées de façon dynamique.

---

# 📈 Système XP et niveaux
- Chaque action (défi, QCM, cours) rapporte de l'XP calculé selon les règles dynamiques.
- Le franchissement d'un palier d'XP attribue automatiquement un nouveau niveau et un titre motivant.

```json
{ "niveau": 10, "xp": 250, "titre": "🔥 Initié des Boucles" }
```
- Objectif : maintenir l'engagement par une progression visible et gratifiante.

---

# 💪 Points forts du projet
- 📚 Mémoire individuelle complète : XP, niveaux, historique sauvegardés à chaque interaction.
- 🤖 Adaptation automatique des défis au niveau de l'utilisateur grâce à l'IA.
- 🎮 Progression ludique et gratifiante avec un système complet de niveaux et titres personnalisés.
- 📁 Utilisation efficace de fichiers JSON pour séparer données et logique de code.

---

# ⚠️ Limites identifiées
- Défis et cours encore génériques.
- Interface uniquement en ligne de commande (pas d'interface graphique pour l'instant).
- Gestion d'erreurs limitée.

---

# 🚀 Perspectives d'amélioration
- Implémentation complète de cours détaillés et interactifs.
- Amélioration de l'IA pour générer des défis véritablement personnalisés.
- Système de badges, trophées et récompenses spéciales.
- Création de mini-jeux éducatifs complémentaires.
- Meilleure gestion des erreurs et robustesse des sauvegardes.

---

# 🧠 Conclusion
- Notre projet propose une app d'apprentissage motivante, progressive et mémorielle.
- Il combine un suivi personnalisé, des défis adaptatifs, une progression gamifiée et une architecture souple.
- Il ouvre la voie à de nombreux développements futurs pour enrichir encore l'expérience utilisateur.

---

# ❓ Questions
Merci pour votre attention ! 🚀
N'hésitez pas si vous voulez tester notre plateforme et relever un premier défi !
