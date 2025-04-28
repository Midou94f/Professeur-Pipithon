# 🎯 Projet Python : Plateforme d'apprentissage gamifiée

## 📚 Introduction
Bienvenue sur notre projet de plateforme d'apprentissage gamifiée du Python !  
Notre objectif est de rendre l'apprentissage plus stimulant en combinant défis, motivation et suivi personnalisé.  
Le principe : apprendre en relevant des défis, accumulant de l'expérience (XP) et progressant à travers différents niveaux.

## ❓ Problématique
- Comment rendre l'apprentissage du Python plus motivant et progressif ?
- Comment suivre, enregistrer et encourager la progression individuelle des utilisateurs ?

## 💡 Solution proposée
Nous proposons un Bot éducatif interactif qui offre :
- Défis automatiques 🧩 adaptés au niveau de l'utilisateur,
- Citations motivantes 💬 pour soutenir l'apprentissage,
- Suivi personnalisé de l'expérience et progression en niveaux 🎮,
- Sauvegarde de la progression 📈,
- Gestion flexible des données via des fichiers JSON.

## 🛠️ Architecture générale
Le projet est structuré autour de trois modules Python principaux :
- `bot.py` : Logique principale du bot (réception des actions, attribution d'XP).
- `ai.py` : Génération dynamique de défis personnalisés.
- `utils.py` : Fonctions d'aide pour la gestion de l'XP, niveaux et fichiers JSON.

Les données sont stockées dans différents fichiers JSON :
- Citations, niveaux, utilisateurs, logs d'actions, messages standards, règles d'XP.

## 🧩 Fonctionnement de `bot.py`
- Réception des actions utilisateur.
- Génération dynamique de défis, appel de cours, QCM, citations.
- Attribution d'XP en fonction des actions réalisées.

```python
if action == "debut_defi":
    defi = generer_defi(user)
    attribuer_xp(user, "defi_reussi")
```
- Sauvegarde des actions dans les logs (`logs.json`).

## 🧠 Fonctionnement de `ai.py`
- Adaptation des défis en fonction du niveau de l'utilisateur pour une progression naturelle.

```python
def generer_defi(user):
    niveau = user["level"]
    if niveau < 10:
        return "Crée une fonction qui additionne deux nombres."
    else:
        return "Crée une fonction qui trie une liste."
```
- Approche personnalisée pour stimuler l'engagement.

## 🛠️ Fonctionnement de `utils.py`
- Gestion automatique de l'XP et des montées de niveau.
- Chargement et sauvegarde fiables des données utilisateur.

```python
def attribuer_xp(user, action):
    rules = charger_json("xp_rules.json")
    xp_gagne = rules[action]["base"] + user["level"] * rules[action]["bonus_par_niveau"]
    user["xp"] += xp_gagne
    verifier_niveau(user)
```

## 🗃️ Utilisation des fichiers JSON
- `citations.json` : Citations de motivation et d'humour.
- `users.json` : Sauvegarde permanente de la progression utilisateur.
- `levels.json` : Définition des titres de niveaux et paliers d'XP.
- `logs.json` : Historique détaillé des actions utilisateurs.
- `messages.json` : Messages standards liés aux QCM et défis.
- `xp_rules.json` : Règles de calcul de l'XP.

## 📈 Système XP et niveaux
- Attribution d'XP dynamique selon les actions utilisateur.
- Passage automatique aux niveaux supérieurs avec nouveaux titres.

```json
{ "niveau": 10, "xp": 250, "titre": "🔥 Initié des Boucles" }
```
- Motivation continue grâce à des récompenses visibles.

## 💪 Points forts du projet
- 📚 Mémoire utilisateur complète : XP, niveau et historique sont persistés.
- 🤖 Défis adaptatifs selon la progression de l'utilisateur.
- 🎮 Progression gamifiée engageante via XP et titres.
- 📁 Gestion flexible des données avec JSON.
- 🛠️ Architecture propre et facilement extensible.

## ⚠️ Limites actuelles
- `cours.json` vide : ajout de contenus pédagogiques à venir.
- Gestion d'erreurs à renforcer (ex. vérification des fichiers).
- Complexification progressive des défis en projet.
- Interface limitée à la console pour le moment.

## 🚀 Perspectives d'amélioration
- Intégration de vrais cours et quiz interactifs.
- Développement d'une interface Web (ex. Flask, Django).
- Personnalisation avancée des défis selon le profil utilisateur.
- Création de systèmes de badges et de mini-jeux éducatifs.
- Renforcement de la gestion d'erreurs pour plus de robustesse.

## 🧠 Conclusion
Notre plateforme propose un environnement d'apprentissage stimulant, progressif et personnalisable.  
Elle combine mémoire utilisateur, défis adaptatifs, progression gamifiée et architecture extensible pour accompagner durablement l'apprentissage du Python.

## 🤝 Contribuer
Toute contribution est la bienvenue !  
N'hésitez pas à ouvrir une issue ou à proposer une pull request pour enrichir ce projet.

---
