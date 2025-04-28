import json
import asyncio
from openai import AsyncOpenAI
from utils import (
    get_recent_history,
    get_user_level_info,
    get_all_users,
    get_appropriate_challenge_level,  # Add this import
    get_recommended_course,  # Also add this import since you're using it
)

# ╭─────────────────────────────╮
# │ 1.  Configuration & client  │
# ╰─────────────────────────────╯
with open("config.json", "r") as f:
    cfg = json.load(f)

GPT_KEY   = cfg.get("GPTKEY")
GPT_MODEL = cfg.get("GPT_MODEL", "gpt-3.5-turbo")   # modifiable dans config.json

client = AsyncOpenAI(api_key=GPT_KEY)

# ╭─────────────────────────────╮
# │ 2.  Prompteur « Pipithon »  │
# ╰─────────────────────────────╯
PERSONALITY = """
Tu es Professeur Pipithon : un mentor chaleureux, drôle, exigeant, parlant avec la sagesse d'un ancien maghrébin-juif.

INSTRUCTIONS IMPORTANTES:
1. Tu ne dois JAMAIS accepter des questions hors-sujet. Tu es spécialiste UNIQUEMENT de Python et de programmation.
2. Si une question n'est pas liée à Python, au code ou à la programmation, réponds poliment qu'en tant que Professeur Pipithon, tu ne peux t'occuper que de sujets liés à Python et à la programmation.
3. Tous tes exemples, défis et exercices doivent être strictement liés à Python et au niveau du joueur.
4. Chaque réponse doit contenir un exemple de code Python pratique, des illustrations etc.

À CHAQUE réponse :
- Retourne STRICTEMENT un JSON respectant ce schéma :
{
  "greeting": "...",
  "answer": "...",
  "resource": "...",
  "exercise": {
    "title": "...",
    "statement": "...",
    "solution": "...",
    "xp": 10
  },
  "confirmation_request": "..."
}
- N'ajoute rien avant / après le JSON (pas de ``` ni de texte libre).
"""
COURSE_CREATOR_PERSONALITY = """  # <<< nouveau prompt
Tu es Professeur Pipithon.

Ta mission est d’écrire un MINI-COURS complet sur une notion demandée.
- 1. Explique la notion clairement et simplement.
- 2. Donne toujours un exemple concret codé en Python.
- 3. Si utile, fais une petite analogie imagée (facultatif).
- 4. Termine avec un défi simple pour l'élève.

⚡ Ton format de réponse doit être STRICTEMENT ce JSON :
{
  "title": "Titre du cours",
  "description": "Texte clair du mini-cours, avec l'exemple Python et explication",
  "level": 1
}
"""
# gabarit minimal pour remplir les trous
TEMPLATE = {
    "greeting": "",
    "answer": "",
    "resource": "",
    "exercise": {
        "title": "",
        "statement": "",
        "solution": "",
        "xp": 0
    },
    "confirmation_request": ""
}

def deep_merge(base, incoming):
    """merge récursif : garde base par défaut si clé manquante."""
    if isinstance(base, dict) and isinstance(incoming, dict):
        return {k: deep_merge(base[k], incoming.get(k)) for k in base}
    return incoming if incoming is not None else base


# ╭─────────────────────────────╮
# │ 3.  Fonction principale     │
# ╰─────────────────────────────╯
async def professeur_repond(user_id: str, question: str) -> dict | None:
    # ▸ profil
    user = get_all_users().get(str(user_id))
    if not user:
        return None

    level  = user.get("level", 1)
    title  = get_user_level_info(level)
    xp     = user.get("xp", 0)

    # ▸ historique condensé (7 jours)
    recent_exos    = get_recent_history(user_id, "exercises", days=7)
    recent_courses = get_recent_history(user_id, "courses",   days=7)
    recent_qcm     = get_recent_history(user_id, "qcm",       days=7)
    
    # ▸ recommandations adaptées
    recommended_level = get_appropriate_challenge_level(user_id)
    recommended_course = get_recommended_course(user_id)
    course_name = recommended_course["titre"] if recommended_course else "bases de Python"

    prompt = f"""{PERSONALITY}

Élève :
- Niveau : {level} ({title})
- XP : {xp}
- Derniers exercices : {recent_exos}
- Derniers cours     : {recent_courses}
- Derniers QCM       : {recent_qcm}
- Niveau recommandé pour le prochain défi : {recommended_level}
- Cours recommandé selon ses performances : {course_name}

IMPORTANT: Ta réponse doit être 100% en rapport avec Python. Si la question n'est pas liée à Python ou à la programmation, rappelle que tu n'es spécialisé que dans ce domaine.

Nouvelle question : "{question}"
"""

    # ▸ appel OpenAI (reste du code inchangé)

    # ▸ appel OpenAI
    try:
        rsp = await client.chat.completions.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            timeout=30,               # évite de rester bloqué
        )
        raw = (rsp.choices[0].message.content or "").strip()
        if not raw:
            print("⚠️ Réponse OpenAI vide.")
            return None

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as dec_err:
            print("⚠️ JSON mal formé :", dec_err, "\n---\n", raw[:200], "\n---")
            return None

        # ▸ complétion des clés manquantes
        return deep_merge(TEMPLATE, parsed)

    except Exception as e:
        # réseau, clé invalide, quota épuisé, etc.
        print(f"❌ Erreur OpenAI ({type(e).__name__}) : {e}")
        return None

async def creer_cours(question: str) -> dict | None:
    try:
        response = await client.chat.completions.create(
            model=GPT_MODEL,
            messages=[{"role": "user", "content": COURSE_CREATOR_PERSONALITY + f"\nSujet : {question}"}],
            temperature=0.5,
            timeout=30,
        )
        content = (response.choices[0].message.content or "").strip()

        if not content:
            print("⚠️ Réponse vide lors de la création de cours.")
            return None

        parsed = json.loads(content)
        return {
            "title": parsed.get("title", "Titre inconnu"),
            "description": parsed.get("description", "Pas de description disponible."),
            "level": parsed.get("level", 1)
        }
    except Exception as e:
        print(f"❌ Erreur OpenAI (cours) : {e}")
        return None


# ────────────────────────────────────────────────
# Petit test manuel (exécute : python ai.py)
# ────────────────────────────────────────────────
if __name__ == "__main__":
    async def _test():
        data = await professeur_repond("0", "Explique-moi les dictionnaires Python")
        print(json.dumps(data, indent=2, ensure_ascii=False))

    asyncio.run(_test())
