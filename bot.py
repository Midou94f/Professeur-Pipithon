# bot.py — Professeur Pipithon v2
from __future__ import annotations
import asyncio                    # ← ajoute
from datetime import datetime, timedelta
import random
import json

import discord
from discord.ext import commands, tasks
from discord import app_commands, Interaction, ui, ButtonStyle
from discord.ui import Select, View

from ai import professeur_repond, generer_cours_complet, creer_cours
from utils import (
    ensure_user_exists, append_exercise, update_user_xp, check_level_up,
    get_all_users, get_user_level_info, get_random_citation_by_category,
    get_avatars, get_levels, maj_derniere_activite, track_completed_challenge,
    save_all_users,   # ⇦ déjà ici, inutile de le réimporter plus bas
)


# ───────────────────────────────────────────────
# Helper visuel : barre de progression XP
# ───────────────────────────────────────────────
def progress_bar(xp: int, next_xp: int, size: int = 12) -> str:
    pct = min(xp / next_xp, 1)
    fill = int(pct * size)
    return "█" * fill + "░" * (size - fill)

def xp_to_next(level: int) -> int:
    """Renvoie l'XP requis pour atteindre le niveau suivant (simple paliers  +50)."""
    palette = {1: 25, 2: 50}           # premiers niveaux plus courts
    return palette.get(level, 50 + 25 * ((level - 3) // 5))

# ───────────────────────────────────────────────
# Initialisation du bot
# ───────────────────────────────────────────────
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Stocke les ID de message de level-up déjà envoyés pour éviter le spam
_levelup_cache: set[int] = set()



# ───────────────────────────────────────────────
# Événements de base
# ───────────────────────────────────────────────



@bot.event
async def on_member_join(member: discord.Member):
    ensure_user_exists(member.id, member.name)
    embed = discord.Embed(
        title="🐍 Bienvenue dans le monde de Python!",
        description=f"Salut **{member.display_name}** ! Je suis **Professeur Pipithon**, ton mentor personnel.",
        color=0x00B894
    )
    embed.add_field(
        name="Comment je peux t'aider?",
        value="• `/prof` - Pose-moi n'importe quelle question sur Python\n"
              "• `/stats` - Consulte ton niveau actuel et tes XP\n"
              "• `/classement` - Vois qui progresse le plus cette semaine\n"
              "• `/citation` - Un peu de sagesse pour te motiver",
        inline=False
    )
    embed.add_field(
        name="Comment progresser?",
        value="À chaque question et défi complété, tu gagnes de l'XP et tu montes en niveau! Plus tu apprends, plus les défis seront adaptés à tes compétences.",
        inline=False
    )
    embed.set_footer(text="Que l'aventure commence! Tape /prof pour ta première question.")
    
    try:
        await member.send(embed=embed)
    except:
        # Si DM désactivés, envoyer dans le channel de bienvenue
        if member.guild.system_channel:
            await member.guild.system_channel.send(f"{member.mention}", embed=embed)
    ensure_user_exists(member.id, member.name)
    await member.send(
        f"Bienvenue {member.display_name} ! Je suis **Professeur Pipithon** 🐍\n"
        "Tape `/aide` sur le serveur pour découvrir les commandes.\n"
        "Que l'aventure commence !"
    )

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"❌ Erreur : `{error}`")

@bot.event
async def on_ready():
    try:
        synced = await bot.tree.sync()
        print(f"✅ Slash-commands synchronisées ({len(synced)})")
    except Exception as e:
        print("Sync error :", e)
    print(f"Professeur Pipithon est prêt – connecté en tant que {bot.user}")
    leaderboard_task.start()
    inactivity_ping.start()  # <-- ajoute cette ligne

    # Message de bienvenue global dans tous les serveurs
    for guild in bot.guilds:
        if guild.system_channel:  # Canal d'annonces système du serveur
            embed = discord.Embed(
                title="🐍 Professeur Pipithon est en ligne!",
                description="Bonjour à tous! Je suis votre assistant Python personnel.",
                color=0x00B894
            )
            embed.add_field(
                name="Commandes disponibles:",
                value="• `/prof` - Pose-moi une question sur Python\n"
                      "• `/stats` - Consulte ton niveau et tes XP\n"
                      "• `/classement` - Vois qui progresse le plus\n"
                      "• `/citation` - Un peu de motivation",
                inline=False
            )
            embed.set_footer(text="Je suis là pour vous aider à progresser en Python!")
            
            try:
                await guild.system_channel.send(embed=embed)
            except:
                pass  # En cas d'erreur de permission
                

# ───────────────────────────────────────────────
# Slash-commandes
# ───────────────────────────────────────────────
@bot.tree.command(name="aide", description="Affiche la liste des commandes")
async def slash_aide(inter: Interaction):
    maj_derniere_activite(inter.user.id)
    await inter.response.send_message(
        "**Commandes disponibles :**\n"
        "• `/prof` – pose une question (cours + défi IA)\n"
        "• `/stats` – vois ton niveau et tes XP\n"
        "• `/classement` – top 10 hebdo\n"
        "• `/citation` – petite sagesse motivante",
        ephemeral=True,
    )

@bot.tree.command(
    name="prof",
    description="Pose une question à Professeur Pipithon",
)
@app_commands.describe(question="Ta question, ton bloc de code ou ton sujet")
async def slash_prof(inter: Interaction, question: str):
    # 1 ─ accusé de réception
    await inter.response.defer()

    # 2 ─ profil
    user = ensure_user_exists(inter.user.id, inter.user.display_name)
    maj_derniere_activite(inter.user.id)

    # 3 ─ appel IA
    data = await professeur_repond(user["id"], question)
    if not data:
        await inter.followup.send("❌ Erreur interne : impossible d'obtenir la réponse.")
        return

    # ───────────────────────────────────────────
    # 4 ─ déballage sécurisé de la réponse IA
    # ───────────────────────────────────────────
    greeting  = data.get("greeting", "Salut aventurier !")
    answer    = data.get("answer",  "Je n'ai pas pu rédiger l'explication.")
    resource  = data.get("resource", "")
    exercise  = data.get("exercise", {}) or {}

    ex_title     = exercise.get("title", "Exercice surprise")
    ex_statement = exercise.get("statement", "Mets en pratique la notion vue.")
    ex_solution  = exercise.get("solution", "Solution bientôt disponible.")
    ex_xp        = exercise.get("xp", 5)
    confirm      = data.get("confirmation_request", "Dis-moi si c'est clair !")

    # 5 ─ mémorisation + XP
    append_exercise(user["id"], ex_title)
    track_completed_challenge(user["id"], ex_title, success=None)  # On n'a pas encore le résultat
    update_user_xp(user["id"], ex_xp)
    lvlup_msg = check_level_up(user["id"])


    # 6 ─ badge (serveur uniquement)
    if inter.guild:
        member = inter.guild.get_member(inter.user.id)
        if member:
            await give_badge(member, user["xp"])

    # 7 ─ embed principal
    next_xp = xp_to_next(user["level"])
    bar     = progress_bar(user["xp"], next_xp)
    footer  = f"[{bar}] {user['xp']}/{next_xp} XP – Nv {user['level']}"

    embed = discord.Embed(description=greeting, color=0x00B894)
    embed.add_field(name="📖 Explication", value=answer, inline=False)
    if resource:
        embed.add_field(name="🔗 Ressource", value=resource, inline=False)
    embed.add_field(
        name="🧩 Défi",
        value=f"**{ex_title}**\n{ex_statement}",
        inline=False,
    )
    embed.add_field(name="Solution", value=f"||{ex_solution}||", inline=False)
    embed.add_field(name="❓", value=confirm, inline=False)
    embed.set_footer(text=footer)

    await inter.followup.send(embed=embed, view=ConfirmView(challenge_title=ex_title, user_id=user["id"]))


    # 8 ─ message de level-up (anti-spam)
    if lvlup_msg and inter.channel and inter.channel.id not in _levelup_cache:
        _levelup_cache.add(inter.channel.id)
        up = discord.Embed(
            title="🚀 Ascension accomplie !",
            description=f"**{inter.user.mention} atteint le {lvlup_msg} !**\n"
                        "Un pas de plus vers la maîtrise du code 🧠💻",
            color=0xF1C40F,
        )
        up.set_image(
            url=random.choice(
                [
                    "https://media.giphy.com/media/3o6ZsWJq0VwJ8Lzxio/giphy.gif",
                    "https://media.giphy.com/media/3o7abldj0b3rxrZUxW/giphy.gif",
                    "https://media.giphy.com/media/5GoVLqeAOo6PK/giphy.gif",
                    "https://media.giphy.com/media/l0MYC0LajbaPoEADu/giphy.gif",
                    "https://media.giphy.com/media/l0MYNVDd7Q1bs3Mso/giphy.gif",
                ]
            )
        )
        await inter.channel.send(embed=up)



@bot.tree.command(name="stats", description="Voir ton niveau et tes XP")
async def slash_stats(inter: Interaction):
    user = ensure_user_exists(inter.user.id, inter.user.display_name)
    maj_derniere_activite(inter.user.id)

    lvl = user["level"]
    xp = user["xp"]
    titre = get_user_level_info(lvl)
    emoji = next(
        (a["emoji"] for a in get_avatars() if a["niveau_min"] <= lvl <= a["niveau_max"]),
        "🐣",
    )
    next_xp = xp_to_next(lvl)
    bar = progress_bar(xp, next_xp)

    await inter.response.send_message(
        f"**{inter.user.display_name}** – {emoji} {titre}\n"
        f"Niveau {lvl} · {xp}/{next_xp} XP\n`{bar}`",
        ephemeral=True,
    )

@bot.tree.command(name="citation", description="Un mot motivant du Professeur")
async def slash_citation(inter: Interaction):
    ensure_user_exists(inter.user.id, inter.user.display_name)
    maj_derniere_activite(inter.user.id)
    await inter.response.send_message(
        get_random_citation_by_category("motivation"), ephemeral=True
    )

# ───────────────────────────────────────────────
# Leaderboard hebdomadaire
# ───────────────────────────────────────────────
@bot.tree.command(name="classement", description="Top 10 des XP gagnés cette semaine")
async def slash_classement(inter: Interaction):
    leaderboard = build_leaderboard()
    embed = discord.Embed(
        title="🏆 Classement hebdomadaire", description=leaderboard, color=0xF1C40F
    )
    await inter.response.send_message(embed=embed)

def build_leaderboard() -> str:
    cutoff = datetime.utcnow() - timedelta(days=7)
    users = get_all_users().values()
    sorted_users = sorted(
        users,
        key=lambda u: u.get("weekly_xp", 0),
        reverse=True,
    )[:10]
    lines = []
    for i, u in enumerate(sorted_users, 1):
        lines.append(f"**#{i}** {u['name']} – {u.get('weekly_xp', 0)} XP")
    return "\n".join(lines) if lines else "Pas encore de participants."

@tasks.loop(hours=24)
async def leaderboard_task():
    """Calcule l’XP gagné sur 7 jours glissants et reset les caches level-up toutes les 24 h."""
    users = get_all_users()
    for u in users.values():
        # Weekly XP = différence entre xp actuel et xp de la semaine passée stocké en metadata
        start_xp = u.setdefault("xp_snapshot", u["xp"])
        u["weekly_xp"] = max(u["xp"] - start_xp, 0)
    # Reset snapshot tous les lundi 00:00 UTC
    if datetime.utcnow().weekday() == 0:
        for u in users.values():
            u["xp_snapshot"] = u["xp"]
    _levelup_cache.clear()

from utils import save_all_users
users = get_all_users()
save_all_users(users)


# ───────────────────────────────────────────────
# Lancement et pimpage du bot
# ───────────────────────────────────────────────
@bot.tree.command(name="oui", description="Confirme que tu as compris")
async def slash_oui(inter: Interaction):
    user = ensure_user_exists(inter.user.id, inter.user.display_name)
    update_user_xp(user["id"], 5)  # +5 XP pour réussite

    if inter.guild:
        member = inter.guild.get_member(inter.user.id)
        if member:
            await give_badge(member, user["xp"])  # Donne badge si niveau atteint

    await inter.response.send_message(
        "✨ Parfait ! +5 XP pour ta détermination.", ephemeral=True
    )

@bot.tree.command(name="non", description="Indique que tu es bloqué")
async def slash_non(inter: Interaction):
    user = ensure_user_exists(inter.user.id, inter.user.display_name)
    update_user_xp(user["id"], 2)  # +2 XP pour persévérance

    if inter.guild:
        member = inter.guild.get_member(inter.user.id)
        if member:
            await give_badge(member, user["xp"])

    await inter.response.send_message(
        "🔄 Pas de souci, reformule ta question et +2 XP pour ta persévérance !",
        ephemeral=True
    )


# ─ Rappel d'inactivité ─
@tasks.loop(hours=12)
async def inactivity_ping():
    now = datetime.utcnow()
    users = get_all_users()
    for uid, u in users.items():
        raw = u.get("derniere_activite")                # peut être None ou malformé
    try:
        last = datetime.fromisoformat(raw) if isinstance(raw, str) else now
    except ValueError:                              # chaîne invalide
        last = now

    if now - last > timedelta(hours=72):

            user_obj = await bot.fetch_user(int(uid))
            try:
                await user_obj.send(
                    "👋 Hé ! Ça fait trois jours sans pratiquer : une nouvelle question ?"
                )
            except discord.Forbidden:
                pass
            u["derniere_activite"] = now.isoformat()



# ─ Analyse rapide de code collé ─
@bot.tree.command(name="coach", description="Analyse ton code et donne des conseils")
@app_commands.describe(code="Colle ton code Python ici")
async def slash_coach(inter: Interaction, code: str):
    await inter.response.defer(ephemeral=True)
    critique = f"Ton code commence par {code.splitlines()[0][:30]}…\n"
    if "print(" not in code:
        critique += "• Pas de print : comment testes-tu ?\n"
    if "while True" in code and "break" not in code:
        critique += "• Boucle infinie repérée : pense à un break 😉\n"
    await inter.followup.send(critique)


# ─ Attribution de rôles badges ─
BADGE_ROLES = {
    100: "🥉 Débrouillard",
    500: "🥈 Persévérant",
    1000: "🥇 Inarrêtable",
}

async def give_badge(member: discord.Member, xp: int):
    guild = member.guild
    for thresh, role_name in BADGE_ROLES.items():
        if xp >= thresh:
            role = discord.utils.get(guild.roles, name=role_name)
            if role and role not in member.roles:
                await member.add_roles(role, reason="Nouveau badge XP")
                try:
                    await member.send(f"🏅 Tu gagnes le badge **{role_name}** !")
                except discord.Forbidden:
                    pass

# Appelle cette fonction dans update_user_xp
# après avoir mis à jour l'XP :
#   member = guild.get_member(user_id)
#   await give_badge(member, new_xp)



import pydoc
@bot.tree.command(name="explain", description="Doc rapide d'un mot Python")
@app_commands.describe(term="mot-clé ou fonction")
async def slash_explain(inter: Interaction, term: str):
    await inter.response.defer(ephemeral=True)
    try:
        info = pydoc.render_doc(term, "Help on %s")
        await inter.followup.send(f"```{info[:1500]}```")
    except:
        await inter.followup.send("Rien trouvé.")


from discord import ui, Interaction, ButtonStyle

class ConfirmView(ui.View):
    def __init__(self, challenge_title: str, user_id: int):
        super().__init__(timeout=120)
        self.challenge_title = challenge_title
        self.user_id = user_id

    @ui.button(label="✅ J'ai compris", style=ButtonStyle.success)
    async def understood(self, interaction: Interaction, button: ui.Button):
        # Noter que l'utilisateur a réussi le défi
        track_completed_challenge(self.user_id, self.challenge_title, success=True)
        update_user_xp(self.user_id, 10)  # Bonus XP pour réussite

        await interaction.response.send_message(
            "✨ Super ! Défi réussi (+10 XP). "
            "Quand tu veux une nouvelle question, tape simplement `/prof`.",
            ephemeral=True
        )

    @ui.button(label="❌ Je suis bloqué", style=ButtonStyle.danger)
    async def stuck(self, interaction: Interaction, button: ui.Button):
        # Noter que l'utilisateur a échoué le défi
        track_completed_challenge(self.user_id, self.challenge_title, success=False)
        update_user_xp(self.user_id, 2)  # Petit XP pour l'effort

        await interaction.response.send_message(
            "🔄 Pas grave, l'erreur fait partie de l'apprentissage (+2 XP). "
            "Repose une question avec `/prof` pour plus d'explications.",
            ephemeral=True
        )


    @ui.button(label="🌀 Un autre exemple", style=ButtonStyle.primary)
    async def more(self, interaction: Interaction, _button: ui.Button):
        await interaction.response.send_message(
            "Pas de souci ! Reformule ta demande avec `/prof …` et j'illustre autrement.",
            ephemeral=True,
        )

@bot.tree.command(name="creercours", description="Crée un mini-cours avec l'aide de l'IA.")
@app_commands.describe(sujet="Le sujet du mini-cours que tu veux créer")
async def slash_creercours(inter: Interaction, sujet: str):
    await inter.response.defer()

    cours = await creer_cours(sujet)
    if not cours:
        await inter.followup.send("❌ Impossible de créer le cours.")
        return

    # Enregistrement dans cours.json
    try:
        with open("cours.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    data[cours["title"]] = {
        "description": cours["description"],
        "niveau": cours["level"]
    }

    with open("cours.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # Affichage sur Discord
    embed = discord.Embed(
        title=f"📚 Nouveau cours : {cours['title']}",
        description=cours['description'],
        color=0x3498DB,
    )
    await inter.followup.send(embed=embed)

# fin de bot.py
import json
with open("config.json") as f:
    config = json.load(f)

@bot.tree.command(name="reset", description="Remet ton profil à zéro (XP, niveau, historique)")
async def slash_reset(inter: Interaction):
    users = get_all_users()
    uid = str(inter.user.id)
    if uid in users:
        users[uid].update({
            "xp": 0,
            "level": 1,
            "weekly_xp": 0,
            "history": {"exercises": [], "courses": [], "qcm": []},
        })
        save_all_users(users)
        await inter.response.send_message("🔄 Ton profil a été réinitialisé.", ephemeral=True)
    else:
        await inter.response.send_message("Profil introuvable.", ephemeral=True)

# ───────────────────────────────────────────────
# Slash-commande /cours  → propose la liste
# ───────────────────────────────────────────────

import re, json
from discord.ui import Select, View

@bot.tree.command(name="cours", description="Choisis un chapitre à étudier")
async def slash_cours(inter: Interaction):
    user = ensure_user_exists(inter.user.id, inter.user.display_name)
    lvl  = user["level"]

    # Liste « dynamique » – ici simple mapping pour l’exemple
    chapitres_par_niv = {
        1: ["Variables & types", "Opérateurs arithmétiques"],
        2: ["Conditions if/else", "Boucles for"],
        3: ["Fonctions simples", "Listes & tuples"],
        # …
    }
    propositions = chapitres_par_niv.get(lvl, ["Sujet libre : demandes-en un !"])

    # Sélecteur Discord
    select = Select(
        placeholder="Choisis un chapitre…",
        options=[discord.SelectOption(label=c) for c in propositions],
        min_values=1, max_values=1,
    )

    async def on_select(interaction: Interaction):
        chapitre = select.values[0]
        await interaction.response.defer()                    # pensons aux 3 s
        cours = await generer_cours_complet(chapitre, lvl)
        if not cours:
            await interaction.followup.send("Erreur IA.", ephemeral=True)
            return

        # 🔸 1. Sauvegarde dans cours.json
        try:
            with open("cours.json", "r", encoding="utf-8") as f:
                data = json.load(f) or {}
        except FileNotFoundError:
            data = {}
        data.setdefault("cours", {})[chapitre] = cours        # on écrase pas, on met à jour
        with open("cours.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        # 🔸 2. Ajout à l’historique utilisateur
        user["history"]["courses"].append(chapitre)
        save_all_users(get_all_users())

        # 🔸 3. Envoi du cours
        embed = discord.Embed(
            title=f"📘 {cours['title']}",
            description=cours["description"],
            color=0x3498DB,
        )
        embed.add_field(
            name=f"🧩 Défi : {cours['challenge']['title']}",
            value=cours['challenge']['statement'],
            inline=False,
        )
        embed.add_field(
            name="Solution (clique pour révéler)",
            value=f"||{cours['challenge']['solution']}||",
            inline=False,
        )
        await interaction.followup.send(embed=embed)

        # 🔸 4. Démarrer le QCM tout de suite
        await lancer_qcm(interaction.channel, inter.user, cours["qcm"])

    select.callback = on_select
    view = View()
    view.add_item(select)

    await inter.response.send_message(
        "Voici les chapitres que je te recommande :",
        view=view,
        ephemeral=True
    )

# ───────────────────────────────────────────────
# Petite helper QCM (très simple)
# ───────────────────────────────────────────────
async def lancer_qcm(channel, user, qcm_list):
    for i, q in enumerate(qcm_list, 1):
        opts = "\n".join(f"{chr(0x1F1E6 + j)}. {o}"
                         for j, o in enumerate(q["options"]))
        await channel.send(f"**Q{i}. {q['question']}**\n{opts}")

        def check(msg):
            return (msg.author == user
                    and msg.channel == channel
                    and re.match(r"[a-dA-D]$", msg.content.strip()))

        try:
            msg = await bot.wait_for("message", timeout=60, check=check)
            bonne = q["answer"].lower() == msg.content.lower()
            await channel.send("✅ Correct !" if bonne else f"❌ Mauvaise réponse. ({q['answer']})")
            if bonne:
                update_user_xp(user.id, 3)   # mini XP par bonne réponse
        except asyncio.TimeoutError:
            await channel.send("⏱️ Temps écoulé pour cette question.")

    await channel.send("📚 QCM terminé ! Tape `/prof` pour continuer.")

bot.run(config["TOKEN"])


