import json
import os
import random

from openai import AsyncOpenAI  # ✅ client asynchrone officiel
client = AsyncOpenAI(
    api_key="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"
)
from utils import (
    get_all_citations,
    get_all_cours,
    get_levels,
    get_user,
    get_xp_rules,
)

# ──────────────────────────────────────────────────────────────────────────────
# 2.  Contexte personnalisé
# ──────────────────────────────────────────────────────────────────────────────
def get_context_for_user(user_id: str) -> str:
    user = get_user(user_id)
    if not user:
        return "Utilisateur inconnu."

    niveaux = get_levels()
    xp_rules = get_xp_rules()
    cours = get_all_cours()
    citations = get_all_citations()

    niveaux_summary = ", ".join(
        f"Niveau {lvl['niveau']} : {lvl['titre']}" for lvl in niveaux
    )
    return f"""
🧠 CONTEXTE :
Nom : {user.get('name', 'Apprenti')}
Niveau : {user.get('level', 1)}
XP : {user.get('xp', 0)}

📘 Règles XP :
{json.dumps(xp_rules, indent=2, ensure_ascii=False)}

🏆 Rangs :
{niveaux_summary}

📚 Cours disponibles :
{[c['chapitre'] for c in cours['cours']]}

💬 Citations disponibles :
{len(citations)} catégories

L'élève interagit avec Professeur Pipithon, une IA bienveillante, drôle et exigeante.
Il attend des réponses pédagogiques, personnalisées, encourageantes et parfois spirituelles.
""".strip()


# ──────────────────────────────────────────────────────────────────────────────
# 3.  Réponse IA 100 % asynchrone (ne bloque plus Discord)
# ──────────────────────────────────────────────────────────────────────────────
async def professeur_repond(user_id: str, message_utilisateur: str) -> str:
    prompt = f"""{get_context_for_user(user_id)}

👨‍🏫 Message de l'élève :
"{message_utilisateur}"

🧠 Réponse du Professeur Pipithon :
"""
    try:
        resp = await client.chat.completions.create(
            model="gpt-4o-mini",  # ou "gpt-4o" si dispo
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Tu es Professeur Pipithon, une IA maghrébine et juive, "
                        "drôle, sage, parfois moqueuse affectueusement, mais "
                        "toujours là pour aider."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
            max_tokens=350,
        )
        return resp.choices[0].message.content
    except Exception as exc:  # noqa: BLE001
        return f"[❌] Erreur IA : {exc}"
