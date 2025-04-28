import json
import os
import random
from datetime import datetime, timedelta

# 📁 Chemin de base (ajustable selon structure)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Définir les chemins de fichiers constants
USERS_FILE = "users.json"
LEVELS_FILE = "levels.json"
AVATARS_FILE = "avatars.json"
COURS_FILE = "cours.json"
XP_RULES_FILE = "xp_rules.json"
CITATIONS_FILE = "citations.json"
MESSAGES_FILE = "messages.json"
DEFIS_FILE = "defis.json"
LOGS_FILE = "logs.json"


def load_json(filename):
    """
    Charge un fichier JSON et retourne son contenu sous forme de dictionnaire ou liste.
    """
    filepath = os.path.join(BASE_DIR, filename)
    if not os.path.exists(filepath):
        print(f"[⚠️] Fichier '{filename}' introuvable.")
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            print(f"[❌] Erreur de décodage JSON dans '{filename}': {e}")
            return None


def save_json(filename, data):
    """
    Sauvegarde des données (dict ou liste) dans un fichier JSON.
    """
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_all_users():
    users = load_json(USERS_FILE)
    return users if users else {}


def save_all_users(users):
    save_json(USERS_FILE, users)


def get_user(user_id):
    users = get_all_users()
    return users.get(str(user_id))


def create_user(user_id, user_name):
    users = get_all_users()
    uid = str(user_id)
    if uid not in users:
        users[uid] = {
            "id": uid,
            "name": user_name,
            "xp": 0,
            "level": 1,
            "history": {
            "exercises": [],
            "courses": [],
            "qcm": []
},
        "derniere_activite": datetime.utcnow().isoformat()
        }
        save_all_users(users)
        print(f"[✅] Utilisateur {user_name} créé avec succès.")
    return users[uid]


def update_user_xp(user_id, xp_gagne):
    users = get_all_users()
    uid   = str(user_id)
    user  = users.get(uid)
    if user:
        user["xp"] += xp_gagne
        # ───── correctif : compteur hebdomadaire ─────
        user["weekly_xp"] = user.get("weekly_xp", 0) + xp_gagne
        save_all_users(users)
    return user



def get_levels():
    return load_json(LEVELS_FILE) or []


def get_avatars():
    return load_json(AVATARS_FILE) or []


def get_current_level(xp):
    levels = get_levels()
    current_level = 1
    for level in sorted(levels, key=lambda l: l["niveau"]):
        if xp >= level["xp"]:
            current_level = level["niveau"]
        else:
            break
    return current_level


def check_level_up(user_id):
    users = get_all_users()
    user = users.get(str(user_id))
    if not user:
        return None

    old_level = user["level"]
    new_level = get_current_level(user["xp"])

    if new_level > old_level:
        user["level"] = new_level
        save_all_users(users)
        return get_level_up_message(new_level)
    return None


def get_level_up_message(niveau):
    levels = get_levels()
    avatars = get_avatars()

    level_info = next((l for l in levels if l["niveau"] == niveau), None)
    avatar = next(
        (a for a in avatars if a["niveau_min"] <= niveau <= a["niveau_max"]), None
    )

    if not level_info or not avatar:
        return None

    rang = level_info["titre"]
    emoji = avatar["emoji"]

    return f"🎉 Bravo ! Tu passes au niveau {niveau} : {emoji} **{rang}** ! Continue comme ça 💪"


def get_defis_for_level(defis, level):
    """Filtre les défis correspondant au niveau donné."""
    return [defi for defi in defis if defi["niveau"] == level]


def get_completed_defis(user_data):
    """Retourne la liste des ID de défis déjà complétés par l'utilisateur."""
    return user_data.get("defis_reussis", [])


def choisir_defi(defis, user_data):
    """Sélectionne un défi aléatoire non encore fait par l'utilisateur au bon niveau."""
    niveau = user_data.get("level", 1)
    defis_possibles = get_defis_for_level(defis, niveau)
    defis_faits = get_completed_defis(user_data)

    defis_non_faits = [d for d in defis_possibles if d["id"] not in defis_faits]

    if not defis_non_faits:
        return None  # Tous les défis ont été faits à ce niveau

    return random.choice(defis_non_faits)


def get_all_cours():
    return load_json(COURS_FILE) or {"cours": []}


def get_qcm_for_level(niveau):
    cours = get_all_cours()
    if not cours or "cours" not in cours:
        return []
    for chapitre in cours["cours"]:
        if chapitre["niveau"] == niveau:
            return chapitre.get("qcm", [])
    return []


def choisir_qcm(user_level):
    qcms = get_qcm_for_level(user_level)
    return random.choice(qcms) if qcms else None


def charger_xp_rules():
    return load_json(XP_RULES_FILE) or {}


def verifier_reponse_qcm(qcm, reponse_utilisateur):
    """
    Vérifie si la réponse utilisateur correspond à la bonne réponse du QCM.
    Retourne un booléen et le texte de la bonne réponse.
    """
    bonne_reponse = qcm.get("reponse", "")
    return (
        reponse_utilisateur.strip().lower() == bonne_reponse.strip().lower(),
        bonne_reponse,
    )


def traiter_qcm(user_id, qcm, reponse_utilisateur):
    """
    Vérifie la réponse et donne les XP si correcte. Retourne un message personnalisé.
    """
    juste, bonne_reponse = verifier_reponse_qcm(qcm, reponse_utilisateur)
    users = get_all_users()
    user = users.get(str(user_id))
    if not user:
        return "Utilisateur introuvable."

    if juste:
        xp_rules = charger_xp_rules()
        xp_gain = xp_rules.get("qcm_bonne_reponse", 10)
        user["xp"] += xp_gain
        message = f"✅ Bonne réponse ! Tu gagnes {xp_gain} XP."
        message_level = check_level_up(user_id)
        if message_level:
            message += "\n" + message_level
    else:
        message = f"❌ Mauvaise réponse. La bonne réponse était : **{bonne_reponse}**."

    save_all_users(users)
    return message


def get_cours_for_level(niveau):
    """
    Récupère l'objet cours (titre + sections) correspondant à un niveau donné.
    """
    cours_data = get_all_cours()
    if not cours_data or "cours" not in cours_data:
        return None

    for chapitre in cours_data["cours"]:
        if chapitre["niveau"] == niveau:
            return chapitre
    return None


def format_cours(cours):
    """
    Transforme le cours complet en une version lisible (titre, sections, exemples).
    Retourne une liste de strings (une par section).
    """
    if not cours:
        return ["Cours introuvable."]

    titre_global = f"📘 **{cours['titre']}**"
    sections_formatees = []

    for s in cours["sections"]:
        titre = f"\n📌 **{s['titre']}**"
        contenu = f"{s['contenu']}"
        exemple = (
            f"```python\n{s['code_exemple']}\n```" if s.get("code_exemple") else ""
        )
        sections_formatees.append(f"{titre}\n{contenu}\n{exemple}")

    return [titre_global] + sections_formatees


def get_all_citations():
    """
    Charge toutes les citations depuis le fichier JSON.
    """
    return load_json(CITATIONS_FILE) or []


def get_random_citation_by_category(categorie: str) -> str:
    """
    Retourne une citation aléatoire appartenant à la catégorie donnée.
    """
    citations = get_all_citations()
    if not citations:
        return "🤔 Aucune citation disponible pour le moment."

    filtres = [c for c in citations if c["categorie"] == categorie]  # ✅ nom ASCII
    if not filtres:
        return f"📚 Pas de citation trouvée pour la catégorie '{categorie}'."

    citation = random.choice(filtres)
    return f"💡 *{citation['texte']}*"


def deviner_categorie_selon_action(action):
    """
    Déduit la catégorie de citation selon l'action de l'utilisateur.
    """
    mapping = {
        "debut_defi": ["motivation", "curiosité"],
        "defi_reussi": ["réussite", "motivation", "humour"],
        "defi_echoue": ["échec", "confiance", "erreur"],
        "cours_demande": ["curiosité", "discipline"],
        "retour_apres_absence": ["motivation", "confiance"],
        "abandon": ["philosophie", "humilité"],
        "papotage": ["humour", "philosophie"],
        "defi_lent": ["patience", "discipline"],
    }

    catégories_possibles = mapping.get(action, ["motivation"])
    return random.choice(catégories_possibles)


def get_citation_selon_action(action):
    """
    Retourne une citation adaptée à l'action de l'utilisateur.
    """
    catégorie = deviner_categorie_selon_action(action)
    return get_random_citation_by_category(catégorie)


def get_all_messages():
    """
    Charge tous les messages prédéfinis depuis le fichier messages.json.
    """
    return load_json(MESSAGES_FILE) or {}


def get_message(event_name):
    """
    Retourne un message aléatoire correspondant à un événement donné.
    Exemple : 'accueil', 'defi_reussi', 'level_up', etc.
    """
    messages = get_all_messages()
    if not messages:
        return "🤖 Aucun message disponible."

    liste = messages.get(event_name, [])
    if not liste:
        return f"🤷‍♂️ Aucun message trouvé pour l'événement : {event_name}"

    return random.choice(liste)


def get_cours_by_level(level):
    """
    Récupère tous les chapitres associés au niveau spécifié.
    """
    cours = get_all_cours()
    if not cours:
        return []

    return [c for c in cours["cours"] if c["niveau"] == level]


def get_cours_by_chapitre(chapitre_nom):
    """
    Retourne un chapitre entier en fonction de son nom exact.
    """
    cours = get_all_cours()
    if not cours:
        return None

    for c in cours["cours"]:
        if c.get("chapitre", "").lower() == chapitre_nom.lower():
            return c
    return None


def get_qcm_for_chapitre(chapitre_nom):
    """
    Retourne la liste des QCM associés à un chapitre donné.
    """
    chapitre = get_cours_by_chapitre(chapitre_nom)
    return chapitre.get("qcm", []) if chapitre else []


def get_sections_for_chapitre(chapitre_nom):
    """
    Retourne la liste des sections pédagogiques d'un chapitre.
    """
    chapitre = get_cours_by_chapitre(chapitre_nom)
    return chapitre.get("sections", []) if chapitre else []


def get_citations_by_categorie(categorie):
    """
    Retourne toutes les citations appartenant à une catégorie donnée.
    """
    citations = get_all_citations()
    if not citations:
        return []

    return [c["texte"] for c in citations if c["categorie"] == categorie]


def get_random_citation(categorie):
    """
    Sélectionne une citation aléatoire parmi une catégorie donnée.
    """
    candidates = get_citations_by_categorie(categorie)
    if not candidates:
        return "🧞‍♂️ Pas de sagesse disponible pour cette situation..."
    return random.choice(candidates)


def get_xp_rules():
    return load_json(XP_RULES_FILE) or {}


def calculer_xp(action, niveau=1, rapide=False):
    """
    Calcule les XP associés à une action selon le niveau du joueur et les règles définies.
    """
    rules = get_xp_rules()
    total_xp = 0

    if action == "defi_reussi":
        base = rules.get("defi_reussi", {}).get("base", 0)
        bonus = rules.get("defi_reussi", {}).get("bonus_par_niveau", 0)
        total_xp = base + (bonus * niveau)
        if rapide:
            total_xp += rules.get("defi_termine_rapidement", {}).get("bonus", 0)

    elif action == "defi_echoue":
        base = rules.get("defi_echoue", {}).get("base", 0)
        bonus = rules.get("defi_echoue", {}).get("bonus_par_niveau", 0)
        total_xp = base + (bonus * niveau)

    elif action == "cours_suivi":
        total_xp = rules.get("cours_suivi", 0)

    elif action == "qcm_reussi":
        total_xp = rules.get("qcm_reussi", 0)

    elif action == "qcm_echoue":
        total_xp = rules.get("qcm_echoue", 0)

    elif action == "retour_apres_absence":
        total_xp = rules.get("retour_apres_absence", 0)

    elif action == "citation_lue":
        total_xp = rules.get("citation_lue", 0)

    elif action == "niveau_atteint":
        total_xp = rules.get("niveau_atteint", {}).get("bonus", 0)

    elif action == "defi_abandonne":
        total_xp = rules.get("defi_abandonne", {}).get("malus", 0)

    elif action == "inactivite_longue":
        total_xp = rules.get("inactivite_longue", {}).get("malus", 0)

    return total_xp


def attribuer_xp(user_id, action, niveau=1, rapide=False):
    """
    Applique directement les XP à un utilisateur pour une action donnée.
    """
    xp = calculer_xp(action, niveau=niveau, rapide=rapide)
    user = update_user_xp(user_id, xp)
    level_up_msg = check_level_up(user_id)

    feedback = f"✨ Tu as gagné {xp} XP pour l'action **{action}** !"
    if level_up_msg:
        feedback += f"\n{level_up_msg}"
    return feedback


def ensure_user_exists(user_id, user_name="Inconnu"):
    """
    Vérifie si un utilisateur existe, sinon le crée automatiquement.
    Permet d'éviter les bugs lors d'une action déclenchée trop tôt.
    """
    user = get_user(user_id)
    if not user:
        user = create_user(user_id, user_name)
    return user


def maj_derniere_activite(user_id):
    """
    Met à jour la dernière activité d'un utilisateur à l'instant présent.
    """
    users = get_all_users()
    uid = str(user_id)
    if uid in users:
        now = datetime.utcnow().isoformat()
        users[uid]["derniere_activite"] = now
        save_all_users(users)


def detecter_inactivite(user_id, seuil_jours=7):
    """
    Vérifie si l'utilisateur a été inactif depuis plus de `seuil_jours`.
    Retourne True si inactif, False sinon.
    """
    user = get_user(user_id)
    if not user or not user.get("derniere_activite"):
        return True  # Considéré comme inactif s'il n'a jamais été actif

    try:
        derniere_date = datetime.fromisoformat(user["derniere_activite"])
        maintenant = datetime.utcnow()
        return (maintenant - derniere_date) > timedelta(days=seuil_jours)
    except Exception as e:
        print(f"[❌] Erreur lecture date : {e}")
        return True


def log_action(user_id, action, details=None):
    """
    Enregistre une action utilisateur dans un fichier de log.
    """
    logs = load_json(LOGS_FILE) or []
    logs.append(
        {
            "user_id": str(user_id),
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )
    save_json(LOGS_FILE, logs)


def get_all_defis():
    """
    Charge tous les défis depuis le fichier DEFIS_FILE.
    """
    return load_json(DEFIS_FILE) or []

def append_to_history(user_id, category, title):
    users = get_all_users()
    if str(user_id) not in users:
        return

    user = users[str(user_id)]
    history = user.setdefault("history", {})
    category_list = history.setdefault(category, [])

    category_list.append({
        "title": title,
        "timestamp": datetime.utcnow().isoformat()
    })

    save_all_users(users)


def append_exercise(user_id, exercise_title):
    append_to_history(user_id, "exercises", exercise_title)


def append_course(user_id, course_title):
    append_to_history(user_id, "courses", course_title)


def append_qcm(user_id, qcm_title):
    append_to_history(user_id, "qcm", qcm_title)


def get_recent_history(user_id, category, days=7):
    users = get_all_users()
    if str(user_id) not in users:
        return []

    history = users[str(user_id)].get("history", {})
    category_list = history.get(category, [])
    cutoff = datetime.utcnow() - timedelta(days=days)

    return [entry["title"] for entry in category_list if datetime.fromisoformat(entry["timestamp"]) > cutoff]

import json

def get_user_level_info(level):
    with open("levels.json", "r") as f:
        levels = json.load(f)
    for lvl in levels:
        if lvl["niveau"] == level:
            return lvl["titre"]
    return "🐣 Inconnu"

def track_completed_challenge(user_id, challenge_title, success=True):
    """Enregistre qu'un défi a été complété avec succès ou non"""
    users = get_all_users()
    uid = str(user_id)
    user = users.get(uid)
    if not user:
        return
        
    # Initialiser la structure si elle n'existe pas
    if "completed_challenges" not in user:
        user["completed_challenges"] = []
        
    # Ajouter le défi avec son résultat et horodatage
    user["completed_challenges"].append({
        "title": challenge_title,
        "success": success,
        "timestamp": datetime.utcnow().isoformat(),
        "level_when_completed": user["level"]
    })
    
    save_all_users(users)

def get_appropriate_challenge_level(user_id):
    """Détermine le niveau approprié du défi en fonction des performances passées"""
    user = get_user(str(user_id))
    if not user:
        return 1
        
    base_level = user["level"]
    
    # Vérifier les performances récentes (derniers 5 défis)
    challenges = user.get("completed_challenges", [])[-5:]
    if not challenges:
        return base_level
        
    success_rate = sum(1 for c in challenges if c["success"]) / max(1, len(challenges))
    
    # Ajuster le niveau selon la performance
    if success_rate > 0.8:  # Plus de 80% de réussite
        return base_level + 1  # Proposer un défi du niveau supérieur
    elif success_rate < 0.3 and base_level > 1:  # Moins de 30% de réussite
        return max(1, base_level - 1)  # Revenir au niveau inférieur
        
    return base_level  # Rester au même niveau

def track_course_completion(user_id, course_title, completion_percentage):
    """Enregistre la progression dans un cours"""
    users = get_all_users()
    uid = str(user_id)
    user = users.get(uid)
    if not user:
        return
        
    courses = user.setdefault("courses_progress", {})
    
    # Mettre à jour seulement si meilleur score
    if course_title in courses:
        courses[course_title] = max(courses[course_title], completion_percentage)
    else:
        courses[course_title] = completion_percentage
        
    save_all_users(users)

def get_recommended_course(user_id):
    """Recommande un cours basé sur l'analyse des échecs dans les défis et QCM"""
    user = get_user(str(user_id))
    if not user:
        return None
    
    # Obtenir tous les cours disponibles pour son niveau
    cours_niveau = get_cours_for_level(user["level"])
    if not cours_niveau:
        return None
        
    # Si l'utilisateur est nouveau, recommander le cours de base
    if "completed_challenges" not in user or not user["completed_challenges"]:
        return cours_niveau
    
    # Analyser les défis échoués récemment
    failed_challenges = [
        c for c in user.get("completed_challenges", [])
        if not c.get("success", False) and 
        (datetime.utcnow() - datetime.fromisoformat(c["timestamp"])).days < 14
    ]
    
    # Si pas de défis échoués récents, recommander selon le niveau
    if not failed_challenges:
        return cours_niveau
        
    # Logique simplifiée pour recommander un cours
    # En réalité, vous pourriez analyser les titres des défis échoués
    # pour déterminer le thème où l'utilisateur a des difficultés
    return cours_niveau
