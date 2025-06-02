import json, time, os
from config.settings import GLOBAL_DATA_PATH, SECURITY_LOG_PATH, ERROR_LOG_PATH
import logging
from colorama import Fore, Style

RATE_LIMITS_FILE = GLOBAL_DATA_PATH

# Configuration des handlers de logs
info_handler = logging.FileHandler(SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

error_handler = logging.FileHandler(ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)

def load_rate_limits():
    try:
        if not os.path.exists(RATE_LIMITS_FILE):
            logging.warning(f"[RATE LIMIT] Fichier {RATE_LIMITS_FILE} introuvable, initialisation d'un nouveau dictionnaire.")
            return {}
        with open(RATE_LIMITS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            logging.info(f"[RATE LIMIT] Chargement des limites depuis {RATE_LIMITS_FILE}.")
            return data
    except Exception as e:
        logging.error(f"[RATE LIMIT] Erreur lors du chargement du fichier : {e}")
        print(Fore.RED + f"[ERROR] Erreur lors du chargement du fichier de rate limit : {e}" + Style.RESET_ALL)
        return {}

def save_rate_limits(data):
    try:
        with open(RATE_LIMITS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info(f"[RATE LIMIT] Sauvegarde des limites dans {RATE_LIMITS_FILE}.")
    except Exception as e:
        logging.error(f"[RATE LIMIT] Erreur lors de la sauvegarde du fichier : {e}")
        print(Fore.RED + f"[ERROR] Erreur lors de la sauvegarde du fichier de rate limit : {e}" + Style.RESET_ALL)

def check_guild_limits(guild_id):
    now = int(time.time())
    try:
        data = load_rate_limits()
        str_gid = str(guild_id)
        default = {
            "premium": False,
            "count": 0,
            "reset_time": now + 86400,
            "last_request": 0
        }
        guild = data.get(str_gid, default)
        # Reset du compteur si 24h passées
        if now >= guild["reset_time"]:
            logging.info(f"[RATE LIMIT] Réinitialisation du compteur pour le serveur {guild_id}.")
            guild["count"] = 0
            guild["reset_time"] = now + 86400
        # Limites selon premium
        max_per_day = 200 if guild["premium"] else 50
        min_interval = 1 if guild["premium"] else 5
        # Vérif intervalle
        if now - guild["last_request"] < min_interval:
            wait = min_interval - (now - guild["last_request"])
            logging.warning(f"[RATE LIMIT] Serveur {guild_id} : intervalle non respecté ({wait}s restants).")
            return False, f"⏳ Merci de patienter {wait}s entre chaque interaction."
        # Vérif quota
        if guild["count"] >= max_per_day:
            reset_in = guild["reset_time"] - now
            h, m, s = reset_in // 3600, (reset_in % 3600) // 60, reset_in % 60
            logging.warning(f"[RATE LIMIT] Serveur {guild_id} : quota quotidien atteint ({max_per_day}/jour).")
            return False, f"🚫 Limite quotidienne atteinte ({max_per_day}/jour). Réinitialisation dans {h}h {m}m {s}s."
        # Mise à jour
        guild["count"] += 1
        guild["last_request"] = now
        data[str_gid] = guild
        save_rate_limits(data)
        logging.info(f"[RATE LIMIT] Serveur {guild_id} : interaction acceptée (compteur = {guild['count']}/{max_per_day}).")
        return True, None
    except Exception as e:
        logging.error(f"[RATE LIMIT] Erreur lors de la vérification des limites pour le serveur {guild_id} : {e}")
        print(Fore.RED + f"[ERROR] Erreur lors de la vérification des limites : {e}" + Style.RESET_ALL)
        return False, "Erreur interne lors de la vérification du quota."

def set_guild_premium(guild_id, premium=True):
    try:
        data = load_rate_limits()
        str_gid = str(guild_id)
        guild = data.get(str_gid, {
            "premium": False,
            "count": 0,
            "reset_time": int(time.time()) + 86400,
            "last_request": 0
        })
        guild["premium"] = premium
        data[str_gid] = guild
        save_rate_limits(data)
        logging.info(f"[RATE LIMIT] Statut premium {'activé' if premium else 'désactivé'} pour le serveur {guild_id}.")
    except Exception as e:
        logging.error(f"[RATE LIMIT] Erreur lors du changement de statut premium pour le serveur {guild_id} : {e}")
        print(Fore.RED + f"[ERROR] Erreur lors du changement de statut premium : {e}" + Style.RESET_ALL)