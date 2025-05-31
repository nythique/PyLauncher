from home.core.client import create_bot
from home.core.main import register_commands
from colorama import Fore, Style
from config.settings import ERROR_LOG_PATH, SECURITY_LOG_PATH
import logging


"""Handler pour les logs info et warning"""
info_handler = logging.FileHandler(SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

"""Handler pour les logs error"""
error_handler = logging.FileHandler(ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

"""On réinitialise la config root et on ajoute les handlers"""
logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)

try:
    logging.info("[INFO] Initialisation du bot...")
    print(Fore.GREEN + "[INFO] Initialisation du bot..." + Style.RESET_ALL)
    bot = create_bot()
    try:
        logging.info("[INFO] Chargement des cogs...")
        print(Fore.GREEN + "[INFO] Chargement des cogs..." + Style.RESET_ALL)
        import asyncio
        async def load_cogs():
            try:
                await bot.load_extension("commands.admin.errors")
                await bot.load_extension("commands.admin.setpremium")
                await bot.load_extension("commands.admin.empty")
                await bot.load_extension("commands.admin.config")
                await bot.load_extension("commands.public.help")
                await bot.load_extension("commands.public.ping")
                await bot.load_extension("commands.public.explain")
                await bot.load_extension("commands.public.analyze")
                await bot.load_extension("commands.public.challenge")
                await bot.load_extension("commands.public.visualize")
                await bot.load_extension("commands.public.set")
                await bot.load_extension("commands.public.profil")
            except Exception as e:
                logging.error(f"[ERROR] Erreur lors du chargement d'une cog : {e}")
                print(Fore.RED + f"[ERROR] Erreur lors du chargement d'une cog : {e}" + Style.RESET_ALL)
        asyncio.run(load_cogs())
    except Exception as e:
        print(Fore.RED + f"[ERROR] Erreur lors du chargement des cogs" + Style.RESET_ALL)
        logging.error(f"[ERROR] Erreur lors du chargement des cogs : {e}")
    register_commands(bot)
except Exception as e:
    logging.error(f"[ERROR] Erreur lors de l'initialisation du bot : {e}")
    print(Fore.RED + f"[ERROR] Erreur lors de l'initialisation du bot : {e}" + Style.RESET_ALL)
    