import discord, logging
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from discord.ext import commands
from discord import app_commands
from home.plugin.rooter import get_admin_ids

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

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stats", description="DEVS | Statistiques globales")
    async def stats(self, interaction: discord.Interaction):
        try:
            if interaction.user.id not in get_admin_ids():
                logging.warning(f"[STATS] Accès refusé à {interaction.user} ({interaction.user.id})")
                await interaction.response.send_message(
                    "⛔ Vous n'avez pas l'autorisation d'utiliser cette commande.", ephemeral=True
                )
                return

            total_guilds = len(self.bot.guilds)
            total_users = sum(guild.member_count or 0 for guild in self.bot.guilds)
            total_channels = sum(len(guild.text_channels) for guild in self.bot.guilds)
            total_commands = len(self.bot.tree.get_commands())

            embed = discord.Embed(
                title="📊 Statistiques PyLauncher",
                color=discord.Color.blurple()
            )
            embed.add_field(name="Serveurs", value=str(total_guilds))
            embed.add_field(name="Utilisateurs", value=str(total_users))
            embed.add_field(name="Salons textuels", value=str(total_channels))
            embed.add_field(name="Commandes slash", value=str(total_commands))
            embed.set_footer(
                text="PyLauncher • Nexium Portal",
                icon_url=self.bot.user.display_avatar.url
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logging.info(f"[STATS] Statistiques envoyées à {interaction.user} ({interaction.user.id})")
        except Exception as e:
            logging.error(f"[STATS] Erreur lors de l'affichage des stats par {interaction.user} ({interaction.user.id}): {e}", exc_info=True)
            error_embed = discord.Embed(
                title="Erreur lors de l'affichage des statistiques",
                description="❌ Une erreur est survenue lors de la récupération des statistiques.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Stats(bot))