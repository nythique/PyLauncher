from bot.bot import bot
from colorama import Fore, Style
from config.settings import DISCORD_TOKEN, ERROR_LOG_PATH, SECURITY_LOG_PATH
import logging
import sys
import traceback

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

def log_uncaught_exceptions(exctype, value, tb):
    logging.critical("Une exception non interceptée a été levée :", exc_info=(exctype, value, tb))
    print(Fore.RED + "[CRITICAL] Exception non interceptée ! Voir le fichier de logs pour plus de détails." + Style.RESET_ALL)

sys.excepthook = log_uncaught_exceptions

if __name__ == "__main__":
    try:
        logging.info("[INFO] Démarrage du bot...")
        print(Fore.GREEN + "[INFO] Démarrage du bot..." + Style.RESET_ALL)
        bot.run(DISCORD_TOKEN)
    except KeyboardInterrupt:
        logging.warning("[WARNING] Arrêt du bot par l'utilisateur (KeyboardInterrupt).")
        print(Fore.YELLOW + "[WARNING] Arrêt du bot par l'utilisateur." + Style.RESET_ALL)
    except Exception as e:
        logging.error(f"[ERROR] Erreur lors du démarrage du bot : {e}", exc_info=True)
        print(Fore.RED + f"[ERROR] Erreur lors du démarrage du bot : {e}" + Style.RESET_ALL)