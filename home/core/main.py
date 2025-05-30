from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH, CONTROLLER_PATH, TEMP_UPLOAD_PATH, STATUS, VERSION, STATUS
from gen.ces import create_notebook, run_code_in_notebook, delete_notebook
from datetime import datetime
from itertools import cycle
from discord.ext import commands, tasks
from discord import app_commands
from io import BytesIO
from colorama import Fore, Style
import discord, time, os,logging, re, asyncio

bot = None
MAX_DISCORD_MSG_LEN = 1800 # Limite de sécurité pour Discord.


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


def slowType(text, delay=0.1):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)

status = cycle(STATUS) 
@tasks.loop(seconds=3)
async def status_swap(bot):
    """Change le statut du bot Discord à intervalle régulier"""
    try:
        await bot.change_presence(activity=discord.CustomActivity(next(status)))
        logging.info(f"[INFO] Statut changé : {next(status)}")
    except Exception as e:
        print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du changement de statut" + Style.RESET_ALL)
        logging.error(f"[ERROR] Une erreur s'est produite lors du changement de statut : {e}")


def display_banner():
    version = VERSION
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    license_message = f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║   This software is developed by Nexium Portal on 01/05/2020.     ║
    ║   All rights reserved.                                           ║
    ║                                                                  ║
    ║   Version: {version}                                      ║
    ║   Bot started on: {current_date}                            ║
    ║                                                                  ║
    ║   Unauthorized copying, distribution, or modification of this    ║
    ║   software is strictly prohibited. Use is subject to the terms   ║
    ║   of the license agreement.                                      ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(Fore.YELLOW + license_message + Style.RESET_ALL)

def register_commands(bot_instance):
    global bot
    bot = bot_instance
    display_banner()
    logging.info("[INFO] Connexion aux API...")
    @bot.event
    async def on_ready():
        try:
            print(Fore.YELLOW + "[INFO] Démarrage des tâches périodiques..." + Style.RESET_ALL)
            logging.info("[INFO] Démarrage des tâches périodiques...")
            if not status_swap.is_running():
                status_swap.start(bot)
        except Exception as e:
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors du démarrage des tâches périodiques" + Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors du démarrage des tâches périodiques : {e}")
        
        try:
            logging.info("[INFO] Démarrage de la tache de synchronisation...")
            print(Fore.YELLOW + "[INFO] Démarrage de la tache de synchronisation..." + Style.RESET_ALL)
            client = bot.user
            synced = await bot.tree.sync()
            print(Fore.GREEN + f"[INFO] {len(synced)} commandes synchronisées avec succès !" + Style.RESET_ALL)
            logging.info(f"[INFO] {len(synced)} commandes synchronisées avec succès !")
            print(Fore.GREEN + f"[INFO] {len(bot.guilds)} serveurs connectés !" + Style.RESET_ALL)
            logging.info(f"[INFO] {len(bot.guilds)} serveurs connectés !")
            print(Fore.GREEN + f"[INFO] Le bot est connecté en tant que {client.name} (ID: {client.id}) !" + Style.RESET_ALL)
            logging.info(f"[INFO] Le bot est connecté en tant que {client.name} (ID: {client.id}) !")
            slowType(Fore.LIGHTGREEN_EX + f"[START] Le bot est prêt et en ligne !\n" + Style.RESET_ALL)
            logging.info(f"[START] Le bot est prêt et en ligne !")
        except Exception as e:
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de la synchronisation des commandes" + Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors de la synchronisation des commandes : {e}")
    
    @bot.event
    async def on_message(message):
        if message.author.bot:
            return
    
        match = re.search(r"```(py|python|bash|sh)\s*([\s\S]+?)```", message.content, re.IGNORECASE)
        if match:
            lang = match.group(1).lower()
            code = match.group(2).strip()
            if lang in ("py", "python"):
                lang = "python"
            elif lang in ("bash", "sh"):
                lang = "bash"
            else:
                await message.reply(f"Je n'execute pas du {lang}. Que du python, et du bash.")
                return
            lines = code.splitlines()
            if lines and lines[0].strip().lower() in ("thon", "ython", "on", "n"):
                lines = lines[1:]
            code = "\n".join(lines).strip()
    
            # ENVOI IMMEDIAT de l'embed "en cours d'exécution"
            wait_embed = discord.Embed(
                description="<a:cargando:1377376325077172275> Exécution du code en cours...",
                color=discord.Color.gold()
            )
            bot_msg = await message.reply(embed=wait_embed)
    
            # Exécution du code
            start_time = time.perf_counter()
            nb = await create_notebook()
            nb_id = nb.get("id")
            if not nb_id:
                error_msg = nb.get("error", "Erreur lors de la création du notebook.")
                await bot_msg.edit(embed=discord.Embed(description=error_msg, color=discord.Color.red()))
                return
            result = await run_code_in_notebook(nb_id, code, lang=lang)
            output = result.get("result", "Le code n'a pas de sortie.")
            elapsed = (time.perf_counter() - start_time)

            if len(output) > MAX_DISCORD_MSG_LEN:
                file_content = f"Résultat {lang} (exécuté en {elapsed:.2f} secondes)\n\n{output}"
                file = discord.File(BytesIO(file_content.encode("utf-8")), filename="resultat.txt")
                embed = discord.Embed(
                    color=discord.Color.gold()
                )
                embed.set_footer(
                    text=f"Code exécuté en {elapsed:.2f} secondes. Propulsé par Nexium Portal",
                    icon_url=bot.user.display_avatar.url
                )
                await bot_msg.edit(embed=embed, attachments=[file])
                return

            embed = discord.Embed(
                description=f"```{lang}\n{output}\n```",
                color=discord.Color.gold()
            )
            embed.set_footer(
                text=f"Code exécuté en {elapsed:.2f} secondes. Propulsé par Nexium Portal",
                icon_url=bot.user.display_avatar.url
            )
            await bot_msg.edit(embed=embed)
            await delete_notebook(nb_id)
            return
    
        await bot.process_commands(message)
    
    @bot.event
    async def on_message_edit(before, after):
        if after.author.bot:
            return
        
        match = re.search(r"```(py|python|bash|sh)\s*([\s\S]+?)```", after.content, re.IGNORECASE)
        if match:
            lang = match.group(1).lower()
            code = match.group(2).strip()
            if lang in ("py", "python"):
                lang = "python"
            elif lang in ("bash", "sh"):
                lang = "bash"
            else:
                await after.reply(f"Je n'exécute que du python ou du bash.")
                return
            lines = code.splitlines()
            if lines and lines[0].strip().lower() in ("thon", "ython", "on", "n"):
                lines = lines[1:]
            code = "\n".join(lines).strip()
    
            # Cherche le dernier message du bot qui répond à ce message
            async for msg in after.channel.history(limit=20, oldest_first=False):
                if msg.author == bot.user and msg.reference and msg.reference.message_id == after.id:
                    bot_msg = msg
                    break
            else:
                await after.reply("La session précedente est obselete. Veuillez en créer une nouvelle.")
                return
            
            wait_embed = discord.Embed(
                description="<a:cargando:1377376325077172275> Exécution du code en cours...",
                color=discord.Color.gold()
            )
            await bot_msg.edit(embed=wait_embed)
            # Exécution du code
            start_time = time.perf_counter()
            nb = await create_notebook()
            nb_id = nb.get("id")
            if not nb_id:
                error_msg = nb.get("error", "Erreur lors de la création du notebook.")
                await bot_msg.edit(embed=discord.Embed(description=error_msg, color=discord.Color.red()))
                return
            result = await run_code_in_notebook(nb_id, code, lang=lang)
            output = result.get("result", "Le code n'a pas de sortie.")
            elapsed = (time.perf_counter() - start_time)

            if len(output) > MAX_DISCORD_MSG_LEN:
                file_content = f"Résultat {lang} (exécuté en {elapsed:.2f} secondes)\n\n{output}"
                file = discord.File(BytesIO(file_content.encode("utf-8")), filename="resultat.txt")
                embed = discord.Embed(
                    color=discord.Color.gold()
                )
                embed.set_footer(
                    text=f"Code exécuté en {elapsed:.2f} secondes. Propulsé par Nexium Portal",
                    icon_url=bot.user.display_avatar.url
                )
                await bot_msg.edit(embed=embed, attachments=[file])
                return

            embed = discord.Embed(
                description=f"```{lang}\n{output}\n```",
                color=discord.Color.gold()
            )
            embed.set_footer(
                text=f"Code exécuté en {elapsed:.2f} secondes. Propulsé par Nexium Portal",
                icon_url=bot.user.display_avatar.url
            )
            await bot_msg.edit(embed=embed)
            await delete_notebook(nb_id)

    @bot.event
    async def on_command_error(ctx, error):
        """Gestion des erreurs de commande préfix"""
        if isinstance(error, commands.CommandNotFound):
            return  

        
    
   