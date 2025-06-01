import discord
from discord.ext import commands
from discord import app_commands
import pyflakes.api
import pyflakes.reporter
import io
import time

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
        wait_message = await interaction.response.send_message(embed=wait_embed, ephemeral=True)
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
        except Exception as e:
            embed = discord.Embed(
                title="Erreur lors de l'analyse",
                description=f"❌ Une erreur s'est produite lors de l'analyse du code :\n```{str(e)}```"
                "Veuillez vérifier que le code est correct et réessayer."
                " Si le problème persiste, veuillez contacter le support.",
                color=discord.Color.red()
            )
            await interaction.edit_original_response(embed=embed)

async def setup(bot):
    await bot.add_cog(Analyze(bot))