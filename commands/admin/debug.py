import discord
from discord.ext import commands
from discord import app_commands
from config.settings import ERROR_LOG_PATH
from home.plugin.rooter import get_admin_ids
import os, logging
from colorama import Fore, Style

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="debug", description="Affiche les dernières lignes du fichier de logs d'erreur (admin global uniquement)")
    @app_commands.describe(lines="Nombre de lignes à afficher (défaut : 10)")
    async def debug(self, interaction: discord.Interaction, lines: int = 10):
        # Vérifie que l'utilisateur est admin global
        if interaction.user.id not in get_admin_ids():
            await interaction.response.send_message(
                "⛔ Seuls les administrateurs globaux peuvent utiliser cette commande.", ephemeral=True
            )
            print(Fore.BLUE + f"[SECURITY] Utilisateur non autorisé a tenté d'accéder aux erreurs : {interaction.user.name}" + Style.RESET_ALL)
            logging.warning(f"[SECURITY] Utilisateur non autorisé a tenté d'accéder aux erreurs : {interaction.user.name}")
            return

        log_path = ERROR_LOG_PATH
        if not os.path.exists(log_path):
            await interaction.response.send_message("Le fichier de logs d'erreur n'existe pas.", ephemeral=True)
            return
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                lines_content = f.readlines()[-lines:]
            if not lines_content:
                await interaction.response.send_message("Aucune erreur trouvée dans les logs.", ephemeral=True)
                return
            msg = "".join(lines_content)[-1900:]
            embed = discord.Embed(
                title="Dernières erreurs du bot",
                description=f"```{msg}```",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            print(Fore.GREEN + f"[INFO] Logs d'erreur envoyés" + Style.RESET_ALL)
            logging.info(f"[INFO] Logs d'erreur envoyés à {interaction.user.name}")
        except Exception as e:
            await interaction.response.send_message("Erreur lors de la lecture des logs.", ephemeral=True)
            print(Fore.RED + f"[ERROR] Erreur lors de la lecture des logs" + Style.RESET_ALL)
            logging.error(f"[ERROR] Erreur lors de la lecture des logs : {e}")

async def setup(bot):
    await bot.add_cog(Admin(bot))