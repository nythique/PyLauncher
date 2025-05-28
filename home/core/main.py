from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH, CONTROLLER_PATH, TEMP_UPLOAD_PATH, STATUS, VERSION, STATUS
from gen.ces import create_notebook, run_code_in_notebook, pause_notebook, delete_notebook
from datetime import datetime
from itertools import cycle
from discord.ext import commands, tasks
from discord import app_commands
from io import BytesIO
from colorama import Fore, Style
import discord, time, os,logging, re

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
                    description="Le résultat est trop long pour être affiché ici. Voici le fichier complet :",
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
                    description="Le résultat est trop long pour être affiché ici. Voici le fichier complet :",
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
    
    @bot.tree.command(name="empty", description="DEV|Vider les fichiers de logs.")
    async def empty(interaction: discord.Interaction):
        admin_user = []
        if not interaction.user.id not in admin_user:
            await interaction.response.send_message("Attention ! Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
            print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté de vider les logs : {interaction.user.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté de vider les logs : {interaction.user.name}")
            return
        files_to_clear = {
            "Log File (Sécurité)": SECURITY_LOG_PATH,
            "Log File (Erreur)": ERROR_LOG_PATH,
        }
        errors = []
        for file_name, file_path in files_to_clear.items():
            try:
                print(Fore.YELLOW + f"[INFO] Vidage de {file_name}. Demandé par {interaction.user.name}" + Style.RESET_ALL)
                logging.info(f"[INFO] Vidage de {file_name}. Demandé par {interaction.user.name}")
                if not os.path.exists(file_path):
                    errors.append(f"{file_name} n'existe pas.")
                    continue
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write("")
                print(Fore.GREEN + f"[INFO] {file_name} a été vidé." + Style.RESET_ALL)
                logging.info(f"[INFO] {file_name} a été vidé. Demandé par {interaction.user.name}")
            except Exception as e:
                errors.append(f"Erreur lors du vidage de {file_name} : {e}")
                logging.error(f"[ERROR] Erreur lors du vidage de {file_name} : {e}")
                print(Fore.RED + f"[ERROR] Erreur lors du vidage de {file_name}" + Style.RESET_ALL)
        if errors:
            error_message = "\n".join(errors)
            await interaction.response.send_message(f"Des erreurs se sont produites :\n{error_message}", ephemeral=True)
            logging.error(f"[ERROR] Des erreurs se sont produites :{error_message}")
            print(Fore.RED + f"[ERROR] Des erreurs se sont produites" + Style.RESET_ALL)
        else:
            try:
                await interaction.response.send_message("Tous les fichiers de logs ont été vidés avec succès.", ephemeral=True)
                print(Fore.GREEN + f"[INFO] Tous les fichiers de logs ont été vidés avec succès." + Style.RESET_ALL)
            except Exception as e:
                logging.error(f"[ERROR] Une erreur s'est produite lors de l'envoi de l'imformation à {interaction.user.name} : {e}")
                print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'envoi de l'imformation à {interaction.user.name}" + Style.RESET_ALL)      

    @bot.tree.command(name="help", description="Afficher l'aide du bot.")
    async def help(interaction: discord.Interaction):
        try:
            bot_user = bot.user
            embed = discord.Embed(
                title="Aide de Lunaris",
                description="Voici les principales commandes et fonctionnalités du bot :",
                color=discord.Color.blue()
            )
            embed.set_thumbnail(url=bot_user.display_avatar.url)
            embed.add_field(name="/help", value="Affiche ce message d'aide.", inline=False)
            embed.add_field(
                name="/empty",
                value="Vide les fichiers de logs du bot (Nexium team seulement).",
                inline=False
            )
            embed.add_field(
                name="Interaction",
                value="Mentionne le bot ou utilise son nom pour discuter avec lui.",
                inline=False
            )
            embed.set_footer(text="Développé par Nexium Portal • Lunaris IA")
            invite_url = f"https://discord.com/oauth2/authorize?client_id={bot_user.id}&scope=bot"
            embed.add_field(
                name="Lien d'invitation",
                value=f"[Clique ici pour inviter le bot]({invite_url})",
                inline=False
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(Fore.GREEN + f"[INFO] Message d'aide envoyé à {interaction.user.name}" + Style.RESET_ALL)
            logging.info(f"[INFO] Message d'aide envoyé à {interaction.user.name}")
        except Exception as e:
            await interaction.response.send_message(f"Une erreur s'est produite lors de l'envoi de l'aide : {e}", ephemeral=True)
            print(Fore.RED + f"[ERROR] Une erreur s'est produite lors de l'envoi de l'aide : {e}" + Style.RESET_ALL)
            logging.error(f"[ERROR] Une erreur s'est produite lors de l'envoi de l'aide : {e}")

    @bot.tree.command(name="latence", description="Affiche la latence du bot et de Discord.")
    async def latence(interaction: discord.Interaction):
        """Affiche la latence du bot et de Discord dans un embed."""
        bot_latency = round(bot.latency * 1000)
        if bot_latency < 150:
            embed = discord.Embed(
                title=f"🏓 Pong ! {bot_latency} ms",
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title=f"🏓 Pong ! {bot_latency} ms",
                color=discord.Color.orange()
            )
        embed.set_footer(text="Lunaris IA • Nexium Portal")
        await interaction.response.send_message(embed=embed, ephemeral=True)
        print(Fore.GREEN + f"[INFO] Ping demandé par {interaction.user.name}" + Style.RESET_ALL)
        logging.info(f"[INFO] Ping demandé par {interaction.user.name}")
    
        # Ajoute ceci dans ton main.py ou un fichier de commandes
    
    @bot.tree.command(name="report", description="Envoyer un rapport ou signaler un problème à l'équipe")
    @app_commands.describe(message="Décris ton problème ou ta suggestion")
    async def report(interaction: discord.Interaction, message: str):
        """Permet à un utilisateur d'envoyer un rapport à l'admin ou dans un salon dédié."""
        await interaction.response.send_message(
            "Merci pour ton rapport ! L'équipe a bien reçu ta demande.", ephemeral=True
        )
    
        REPORT_CHANNEL_ID = 1360403767274508355 
    
        report_embed = discord.Embed(
            title="",
            description=f"```{message}```",
            color=discord.Color.orange()
        )
        report_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        report_embed.set_footer(
            text=f"Identifiant de {interaction.user.display_name}: {interaction.user.id})"
        )
        report_embed.timestamp = datetime.now()
    
        # Envoie dans le salon de rapports
        channel = bot.get_channel(REPORT_CHANNEL_ID)
        if channel:
            await channel.send(embed=report_embed)
        else:
            # Si le salon n'existe pas, envoie en DM à l'admin (remplace l'ID)
            ADMIN_ID = 123456789012345678  # <-- À remplacer par ton ID Discord
            admin = await bot.fetch_user(ADMIN_ID)
            await admin.send(embed=report_embed)


    @bot.command(name="errors")
    async def errors(ctx, lines: int = 10):
        """Affiche les dernières lignes du fichier de logs d'erreur."""
        await ctx.message.delete() #"""Supprime le message de la commande"""
        await ctx.defer() #"""Défère la réponse pour éviter le timeout"""
        """Vérifie si l'utilisateur a les permissions nécessaires"""
        admin_user = []
        if not ctx.author.id not in admin_user:
            print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté d'accéder aux erreurs : {ctx.author.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté d'accéder aux erreurs : {ctx.author.name}")
            return
        log_path = ERROR_LOG_PATH
        if not os.path.exists(log_path):
            await ctx.send("Le fichier de logs d'erreur n'existe pas.")
            return
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines_content = f.readlines()[-lines:]
            if not lines_content:
                await ctx.send("Aucune erreur trouvée dans les logs.")
                return
            msg = "```" + "".join(lines_content)[-1900:] + "```"
            await ctx.send(msg)
            print(Fore.GREEN + f"[INFO] Logs d'erreur envoyés" + Style.RESET_ALL)
            logging.info(f"[INFO] Logs d'erreur envoyés à {ctx.author.name}")
        except Exception as e:
            await ctx.send(f"Erreur lors de la lecture des logs.")
            print(Fore.RED + f"[ERROR] Erreur lors de la lecture des logs" + Style.RESET_ALL)
            logging.error(f"[ERROR] Erreur lors de la lecture des logs : {e}")