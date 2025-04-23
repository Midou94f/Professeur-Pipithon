from datetime import datetime

import discord
from ai import professeur_repond
from discord.ext import commands
from utils import (
    attribuer_xp,
    choisir_defi,
    choisir_qcm,
    ensure_user_exists,
    format_cours,
    get_all_defis,
    get_all_users,
    get_avatars,
    get_cours_for_level,
    get_levels,
    get_random_citation_by_category,
    get_user,
    load_json,
    log_action,
    maj_derniere_activite,
    save_all_users,
    save_json,
    traiter_qcm,
)

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
bot.qcm_en_cours = {}
bot.defi_en_cours = {}  # Pour suivre les défis en cours


@bot.event
async def on_ready():
    print(f"✅ Professeur Pipithon est prêt ! Connecté en tant que {bot.user}")


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"❌ Une erreur est survenue : `{error}`")


@bot.command(name="aide")
async def aide(ctx):
    maj_derniere_activite(ctx.author.id)
    await ctx.send(
        """
🛠️ **Commandes disponibles** :

📘 `!cours` – Reçois un cours adapté à ton niveau.
🎯 `!defi` – Lance un défi codé à ton niveau.
🧠 `!qcm` – Teste tes connaissances par un QCM.
🎓 `!prof <message>` – Pose une question à l'IA Professeur Pipithon.
📜 `!citation` – Reçois une citation de sagesse adaptée.
📈 `!stats` – Consulte ton niveau, XP et progression.
⏳ `!temps` – Affiche ta dernière activité et détecte une inactivité.
❓ `!help` – Récapitulatif des commandes.
"""
    )


@bot.command(name="prof")
async def prof(ctx, *, question):
    user = ensure_user_exists(ctx.author.id, ctx.author.name)
    maj_derniere_activite(ctx.author.id)
    await ctx.send("💬 Réflexion du Professeur Pipithon en cours...")
    reponse = await professeur_repond(ctx.author.id, question)
    await ctx.send(reponse)


@bot.command(name="citation")
async def citation(ctx):
    ensure_user_exists(ctx.author.id, ctx.author.name)
    maj_derniere_activite(ctx.author.id)
    citation = get_random_citation_by_category("motivation")
    await ctx.send(citation)


@bot.command(name="stats")
async def stats(ctx):
    user = ensure_user_exists(ctx.author.id, ctx.author.name)
    maj_derniere_activite(ctx.author.id)
    level = user.get("level", 1)
    xp = user.get("xp", 0)
    defis_reussis = len(user.get("defis_reussis", []))
    defis_rates = len(user.get("defis_rates", []))
    titre = next(
        (lvl["titre"] for lvl in get_levels() if lvl["niveau"] == level), "Inconnu"
    )
    emoji = next(
        (
            a["emoji"]
            for a in get_avatars()
            if a["niveau_min"] <= level <= a["niveau_max"]
        ),
        "🐣",
    )

    await ctx.send(
        f"""
📊 **Statistiques de {ctx.author.name}** :
Niveau : {level} – {emoji} {titre}
XP total : {xp}
Défis réussis : {defis_reussis}
Défis ratés : {defis_rates}
"""
    )


@bot.command(name="temps")
async def temps(ctx):
    user = get_user(ctx.author.id)
    if not user or not user.get("derniere_activite"):
        await ctx.send("Aucune activité détectée.")
        return

    maj_derniere_activite(ctx.author.id)
    last_dt = datetime.fromisoformat(user["derniere_activite"])
    diff = datetime.utcnow() - last_dt
    jours, reste = diff.days, diff.seconds
    heures, minutes = reste // 3600, (reste % 3600) // 60

    await ctx.send(f"⏱️ Dernière activité il y a {jours}j {heures}h {minutes}min.")


@bot.command(name="cours")
async def cours(ctx):
    user = ensure_user_exists(ctx.author.id, ctx.author.name)
    maj_derniere_activite(ctx.author.id)
    log_action(user["id"], "cours_demande")
    cours = get_cours_for_level(user["level"])
    if not cours:
        await ctx.send("📚 Aucun cours disponible pour ton niveau.")
        return

    xp_msg = attribuer_xp(user["id"], "cours_suivi", niveau=user["level"])
    sections = format_cours(cours)
    await ctx.send(f"{xp_msg}\n" + "\n\n".join(sections))


@bot.command(name="defi")
async def defi(ctx):
    user = ensure_user_exists(ctx.author.id, ctx.author.name)
    maj_derniere_activite(ctx.author.id)
    log_action(user["id"], "debut_defi")
    defis = get_all_defis()
    defi = choisir_defi(defis, user)

    if not defi:
        await ctx.send("🚫 Tu as déjà complété tous les défis de ton niveau !")
        return

    # Sauvegarder le défi en cours
    bot.defi_en_cours[ctx.author.id] = defi

    # Mettre à jour le dernier défi de l'utilisateur
    users = get_all_users()
    users[str(ctx.author.id)]["dernier_defi"] = defi["id"]
    save_all_users(users)

    await ctx.send(
    f"🧩 **Défi** :\n{defi['intitule']}\n✍️ Réponds avec `!repond <ta_reponse>`"
)



@bot.command(name="repond")
async def repond(ctx, *, reponse):
    user = ensure_user_exists(ctx.author.id, ctx.author.name)
    maj_derniere_activite(ctx.author.id)

    if ctx.author.id not in bot.defi_en_cours:
        await ctx.send("🤔 Aucun défi en attente de réponse.")
        return

    defi = bot.defi_en_cours.pop(ctx.author.id)

    # Vérifier la réponse (implémentation simple, à adapter selon tes besoins)
    if reponse.strip().lower() == defi.get("solution", "").strip().lower():
        # Défi réussi
        users = get_all_users()
        user_id = str(ctx.author.id)
        if user_id in users:
            if "defis_reussis" not in users[user_id]:
                users[user_id]["defis_reussis"] = []
            users[user_id]["defis_reussis"].append(defi["id"])
            save_all_users(users)

        xp_msg = attribuer_xp(user_id, "defi_reussi", niveau=user.get("level", 1))
        await ctx.send(f"✅ Bravo ! Tu as réussi le défi !\n{xp_msg}")
    else:
        # Défi échoué
        users = get_all_users()
        user_id = str(ctx.author.id)
        if user_id in users:
            if "defis_rates" not in users[user_id]:
                users[user_id]["defis_rates"] = []
            users[user_id]["defis_rates"].append(defi["id"])
            save_all_users(users)

        xp_msg = attribuer_xp(user_id, "defi_echoue", niveau=user.get("level", 1))
        await ctx.send(
            f"❌ Dommage, ta réponse n'est pas correcte. La solution était : `{defi.get('solution', 'Solution non disponible')}`\n{xp_msg}"
        )


@bot.command(name="qcm")
async def qcm(ctx):
    user = ensure_user_exists(ctx.author.id, ctx.author.name)
    maj_derniere_activite(ctx.author.id)
    log_action(user["id"], "qcm_lance")
    qcm = choisir_qcm(user["level"])

    if not qcm:
        await ctx.send("😓 Aucun QCM disponible pour ton niveau.")
        return

    bot.qcm_en_cours[ctx.author.id] = qcm
    question = f"❓ **{qcm['question']}**\n\nOptions : {', '.join(qcm['options'])}\nRéponds avec `!rep <ta_réponse>`"
    await ctx.send(question)


@bot.command(name="rep")
async def rep(ctx, *, reponse):
    user = ensure_user_exists(ctx.author.id, ctx.author.name)
    maj_derniere_activite(user["id"])

    if ctx.author.id not in bot.qcm_en_cours:
        await ctx.send("🤔 Aucun QCM en attente de réponse.")
        return

    qcm = bot.qcm_en_cours.pop(ctx.author.id)
    resultat = traiter_qcm(user["id"], qcm, reponse)
    log_action(
        user["id"], "qcm_repondu", {"question": qcm["question"], "reponse": reponse}
    )
    await ctx.send(resultat)


bot.run("MTM2MzkyNTk5MTAyNTgwNzQ3MQ.GTf9Xe.sFr0K2Dw0LOe0mk6lI_CG1QOj5LSjRDGiigVVs")
