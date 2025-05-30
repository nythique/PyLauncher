import json, os, logging
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH, GLOBAL_CHANNEL_PATH
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

WHITELIST_PATH = GLOBAL_CHANNEL_PATH

def load_guild_channels():
    try:
        if not os.path.exists(WHITELIST_PATH):
            logging.warning(f"[WHITELIST] Fichier {WHITELIST_PATH} introuvable, initialisation par défaut.")
            return {"guild_channels": {}}
        with open(WHITELIST_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            logging.info(f"[WHITELIST] Chargement des salons whitelistés depuis {WHITELIST_PATH}.")
            return data
    except Exception as e:
        logging.error(f"[WHITELIST] Erreur lors du chargement : {e}")
        print(Fore.RED + f"[ERROR] Erreur lors du chargement de la whitelist : {e}" + Style.RESET_ALL)
        return {"guild_channels": {}}

def save_guild_channels(data):
    try:
        with open(WHITELIST_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        logging.info(f"[WHITELIST] Sauvegarde des salons whitelistés dans {WHITELIST_PATH}.")
    except Exception as e:
        logging.error(f"[WHITELIST] Erreur lors de la sauvegarde : {e}")
        print(Fore.RED + f"[ERROR] Erreur lors de la sauvegarde de la whitelist : {e}" + Style.RESET_ALL)

def get_whitelisted_channel(guild_id):
    data = load_guild_channels()
    return data.get("guild_channels", {}).get(str(guild_id))

def set_whitelisted_channel(guild_id, channel_id):
    data = load_guild_channels()
    data.setdefault("guild_channels", {})[str(guild_id)] = channel_id
    save_guild_channels(data)
    logging.info(f"[WHITELIST] Salon {channel_id} whitelisté pour le serveur {guild_id}.")

def remove_whitelisted_channel(guild_id):
    data = load_guild_channels()
    if str(guild_id) in data.get("guild_channels", {}):
        removed = data["guild_channels"].pop(str(guild_id))
        save_guild_channels(data)
        logging.info(f"[WHITELIST] Salon {removed} retiré pour le serveur {guild_id}.")
    else:
        logging.warning(f"[WHITELIST] Aucun salon whitelisté à retirer pour le serveur {guild_id}.")