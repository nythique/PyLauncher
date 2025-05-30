import discord
from discord.ext import commands
from discord import app_commands
import pyflakes.api
import pyflakes.reporter
import io

class Analyze(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="analyze", description="Renvoie les erreurs / warnings Python")
    @app_commands.describe(message="Le code à analyser")
    async def analyze(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(thinking=True, ephemeral=True)
        output = io.StringIO()
        reporter = pyflakes.reporter.Reporter(output, output)
        pyflakes.api.check(message, "<input>", reporter=reporter)
        result = output.getvalue().strip()
        if not result:
            result = "✅ Aucun problème détecté !"
            color = discord.Color.green()
        else:
            color = discord.Color.orange()
        embed = discord.Embed(
            title="Analyse du code",
            description=f"```{result}```",
            color=color
        )
        await interaction.followup.send(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Analyze(bot))