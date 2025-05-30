import discord
from discord.ext import commands
from config.settings import ERROR_LOG_PATH
import os, logging
from colorama import Fore, Style

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="errors")
    async def errors(self, ctx, lines: int = 10):
        """Affiche les dernières lignes du fichier de logs d'erreur."""
        await ctx.message.delete()
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

async def setup(bot):
    await bot.add_cog(Admin(bot))