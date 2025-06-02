import discord, time, logging, io, pyflakes.api, pyflakes.reporter
from discord.ext import commands
from discord import app_commands
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH

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

class Analyze(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="analyze", description="Analyser le code Python pour détecter les erreurs")
    @app_commands.describe(code="Le code à analyser")
    async def analyze(self, interaction: discord.Interaction, code: str):
        wait_embed = discord.Embed(
            description="<a:cargando:1377376325077172275> Analyse du code en cours...",
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=wait_embed, ephemeral=True)
        try:
            start = time.perf_counter()
            output = io.StringIO()
            reporter = pyflakes.reporter.Reporter(output, output)
            pyflakes.api.check(code, "<input>", reporter=reporter)
            result = output.getvalue().strip()
            elapsed = (time.perf_counter() - start) * 1000  # ms

            if not result:
                result = "✅ Aucun problème détecté !"
                color = discord.Color.green()
            else:
                color = discord.Color.orange()

            embed = discord.Embed(
                title="🔎 Analyse du code Python",
                description=f"```{result}```",
                color=color
            )
            embed.set_footer(
                text=f"PyLauncher • Analyse statique en {elapsed:.1f} ms",
                icon_url=self.bot.user.display_avatar.url
            )
            await interaction.edit_original_response(embed=embed)
            logging.info(f"[ANALYZE] Analyse effectuée par {interaction.user} ({interaction.user.id}) en {elapsed:.1f} ms")
        except Exception as e:
            logging.error(f"[ANALYZE] Erreur lors de l'analyse du code par {interaction.user} ({interaction.user.id}): {e}", exc_info=True)
            embed = discord.Embed(
                title="Erreur lors de l'analyse",
                description=f"❌ Une erreur s'est produite lors de l'analyse du code :\n```{str(e)}```\n"
                            "Veuillez vérifier que le code est correct et réessayer.\n"
                            "Si le problème persiste, veuillez contacter le support.",
                color=discord.Color.red()
            )
            await interaction.edit_original_response(embed=embed)

async def setup(bot):
    await bot.add_cog(Analyze(bot))