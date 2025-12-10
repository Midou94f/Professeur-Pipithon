# 🤖 Professeur Pipithon  
### Un professeur Python intelligent, interactif, avec intégration IA & Bot Discord  
*(Toutes les clés API et tokens ont été volontairement supprimés du dépôt pour des raisons de sécurité.)*

---

## 1. Présentation générale du projet

**Professeur Pipithon** est un assistant pédagogique conçu pour apprendre Python de manière simple, progressive et interactive.  
Le projet combine trois composantes :

1. **Un moteur pédagogique local** (explications, quiz, corrections)  
2. **Une intégration IA (API OpenAI ou équivalent)** pour enrichir les réponses  
3. **Un bot Discord** permettant d’utiliser le professeur dans un serveur Discord

L’objectif : rendre l’apprentissage du code **accessible**, **dynamique** et **conversationnel**.

Toutes les clés d’accès API (OpenAI) et les tokens Discord ont été **retirés volontairement** avant mise en ligne afin de sécuriser l’environnement.

---

## 2. Intégration de l’IA (OpenAI)

Le projet incorpore une couche d’intelligence artificielle permettant :

- la génération d’explications personnalisées  
- l’analyse d’erreurs de code  
- la création dynamique de quiz  
- l’adaptation du niveau selon l’utilisateur  

### Exemple simplifié d’appel IA (clés supprimées)

```python
from openai import OpenAI

client = OpenAI(api_key="VOTRE_CLE_API_ICI")

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Tu es un professeur Python bienveillant."},
        {"role": "user", "content": "Peux-tu m'expliquer ce qu'est une variable ?"}
    ]
)
print(response.choices[0].message["content"])
Dans le dépôt, toutes les clés d’API ont été remplacées par des variables vides ou par des placeholders.

3. Bot Discord intégré
Le projet inclut la possibilité de faire fonctionner Professeur Pipithon directement dans un serveur Discord.

Fonctionnalités du bot :

répondre aux questions Python en temps réel

proposer des quiz dans un salon Discord

analyser les réponses de l’utilisateur

reformuler / corriger / expliquer via l’IA intégrée

supporter Markdown dans les messages

Exemple simplifié (token supprimé)
python
Copier le code
import discord

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("!python"):
        question = message.content.replace("!python", "")
        reponse = professeur.repond(question)
        await message.channel.send(reponse)

client.run("DISCORD_TOKEN_ICI")  # Token supprimé dans le dépôt
Le token Discord a été volontairement supprimé du code public.

4. Structure du dépôt

5. Fonctionnement du professeur

Le script principal enseigne la programmation Python via :

explications claires

exemples concrets

quiz automatiques

corrections détaillées

logique pédagogique adaptative

Le professeur peut être utilisé :

✔ en local (terminal)
✔ dans un salon Discord
✔ avec ou sans IA (mode dégradé)

6. Sécurité & confidentialité
Afin de rendre le projet public, toutes les informations sensibles ont été supprimées :

❌ clé API OpenAI

❌ token Discord

❌ variables d’environnement privées

Le README explique leur usage, mais aucune donnée confidentielle n’est stockée dans le dépôt.

7. Installation & exécution locale
bash
Copier le code
git clone https://github.com/Midou94f/Professeur-Pipithon
cd Professeur-Pipithon
python professeur_pipithon.py
Pour activer l’IA, ajouter une variable d’environnement :

bash
Copier le code
export OPENAI_API_KEY="votre_clé"

8. Exécuter le bot Discord
Créer un bot via https://discord.com/developers

Insérer votre token dans bot_discord.py

Installer les dépendances :

bash
Copier le code
pip install discord.py openai python-dotenv
Lancer le bot :

bash
Copier le code
python bot_discord.py

9. Roadmap (améliorations prévues)

 Version Web (Streamlit / FastAPI)

 Gestion des profils élèves

 Suivi de progression

 Mode “mini-projet” (TP guidés)

 Système de badges pédagogiques

 Mémoire longue sur Discord

10. Licence
Licence MIT.

11. Auteur
Projet développé par Mehdi Fehri, Emile Zeller et Hugo Scheinder dans le cadre de leur master en statistiques et data science, pour rendre l’apprentissage Python plus intuitif, moderne et accessible.
