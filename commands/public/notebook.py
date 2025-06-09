import discord
import logging
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from discord.ext import commands
from discord import app_commands


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

class Notebook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="notebook",
        description="Génère un notebook Jupyter  à partir d'un code"
    )
    @app_commands.describe(
        titre="Titre du notebook",
        code="Code Python à inclure dans le notebook"
    )
    async def notebook(self, interaction: discord.Interaction, titre: str, code: str):
        import nbformat
        from nbformat.v4 import new_notebook, new_code_cell
        import io, time

        try:
            wait_embed = discord.Embed(
                description="<a:cargando:1377376325077172275> Génération du notebook en cours...",
                color=discord.Color.blurple()
            )
            await interaction.response.send_message(embed=wait_embed, ephemeral=True)

            start = time.perf_counter()
            nb = new_notebook()
            nb['cells'] = [new_code_cell(code)]
            nb['metadata']['title'] = titre

            # Écriture dans StringIO puis conversion en BytesIO
            str_buffer = io.StringIO()
            nbformat.write(nb, str_buffer)
            data = str_buffer.getvalue().encode("utf-8")
            buffer = io.BytesIO(data)
            buffer.seek(0)
            elapsed = (time.perf_counter() - start) * 1000  # temps en ms

            file = discord.File(fp=buffer, filename=f"{titre.replace(' ', '_')}.ipynb")
            embed = discord.Embed(
                title="Notebook généré",
                description="Voici votre notebook Jupyter prêt à être téléchargé.",
                color=discord.Color.blurple()
            )
            embed.set_footer(
                text=f"PyLauncher • {elapsed:.1f} ms",
                icon_url=self.bot.user.display_avatar.url
            )
            await interaction.edit_original_response(embed=embed, attachments=[file])
            logging.info(f"[NOTEBOOK] Notebook généré pour {interaction.user} ({titre}) en {elapsed:.1f} ms")
        except Exception as e:
            logging.error(f"[NOTEBOOK] Erreur lors de la génération du notebook : {e}", exc_info=True)
            error_embed = discord.Embed(
                title="Erreur lors de la génération du notebook",
                description=f"❌ Une erreur est survenue : {e}",
                color=discord.Color.red()
            )
            await interaction.edit_original_response(embed=error_embed)

async def setup(bot):
    await bot.add_cog(Notebook(bot))