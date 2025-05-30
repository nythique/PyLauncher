import json, os, logging
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH, CONTROLLER_PATH
from colorama import Fore, Style

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

CONFIG_PATH = CONTROLLER_PATH

def load_admin_config():
    try:
        if not os.path.exists(CONFIG_PATH):
            logging.warning(f"[ROOTER] Fichier de config {CONFIG_PATH} introuvable, initialisation par défaut.")
            return {"ADMIN_IDS": [], "banned_guilds": [], "banned_users": []}
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            logging.info(f"[ROOTER] Chargement de la config admin depuis {CONFIG_PATH}.")
            return data
    except Exception as e:
        logging.error(f"[ROOTER] Erreur lors du chargement de la config admin : {e}")
        print(Fore.RED + f"[ERROR] Erreur lors du chargement de la config admin : {e}" + Style.RESET_ALL)
        return {"ADMIN_IDS": [], "banned_guilds": [], "banned_users": []}

def save_admin_config(data):
    try:
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info(f"[ROOTER] Sauvegarde de la config admin dans {CONFIG_PATH}.")
    except Exception as e:
        logging.error(f"[ROOTER] Erreur lors de la sauvegarde de la config admin : {e}")
        print(Fore.RED + f"[ERROR] Erreur lors de la sauvegarde de la config admin : {e}" + Style.RESET_ALL)

def get_admin_ids():
    return load_admin_config().get("ADMIN_IDS", [])

def get_banned_guilds():
    return load_admin_config().get("banned_guilds", [])

def get_banned_users():
    return load_admin_config().get("banned_users", [])

def add_admin_id(admin_id):
    data = load_admin_config()
    if admin_id not in data["ADMIN_IDS"]:
        data["ADMIN_IDS"].append(admin_id)
        save_admin_config(data)
        logging.info(f"[ROOTER] Ajout de l'admin {admin_id}.")
    else:
        logging.warning(f"[ROOTER] L'admin {admin_id} est déjà présent.")

def remove_admin_id(admin_id):
    data = load_admin_config()
    if admin_id in data["ADMIN_IDS"]:
        data["ADMIN_IDS"].remove(admin_id)
        save_admin_config(data)
        logging.info(f"[ROOTER] Suppression de l'admin {admin_id}.")
    else:
        logging.warning(f"[ROOTER] L'admin {admin_id} n'était pas présent.")

def ban_guild(guild_id):
    data = load_admin_config()
    if guild_id not in data["banned_guilds"]:
        data["banned_guilds"].append(guild_id)
        save_admin_config(data)
        logging.info(f"[ROOTER] Serveur banni : {guild_id}.")
    else:
        logging.warning(f"[ROOTER] Le serveur {guild_id} est déjà banni.")

def unban_guild(guild_id):
    data = load_admin_config()
    if guild_id in data["banned_guilds"]:
        data["banned_guilds"].remove(guild_id)
        save_admin_config(data)
        logging.info(f"[ROOTER] Serveur débanni : {guild_id}.")
    else:
        logging.warning(f"[ROOTER] Le serveur {guild_id} n'était pas banni.")

def ban_user(user_id):
    data = load_admin_config()
    if user_id not in data["banned_users"]:
        data["banned_users"].append(user_id)
        save_admin_config(data)
        logging.info(f"[ROOTER] Utilisateur banni : {user_id}.")
    else:
        logging.warning(f"[ROOTER] L'utilisateur {user_id} est déjà banni.")

def unban_user(user_id):
    data = load_admin_config()
    if user_id in data["banned_users"]:
        data["banned_users"].remove(user_id)
        save_admin_config(data)
        logging.info(f"[ROOTER] Utilisateur débanni : {user_id}.")
    else:
        logging.warning(f"[ROOTER] L'utilisateur {user_id} n'était pas banni.")