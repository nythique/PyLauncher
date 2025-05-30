import discord
from discord.ext import commands
from discord import app_commands

class Analyze(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="analyze", description="Renvoie les erreurs / warnings")
    @app_commands.describe(message="Le code à analyser")
    async def analyze(self, interaction: discord.Interaction, message: str):
        # À compléter avec ta logique d'analyse
        await interaction.response.send_message("Analyse du code à venir...", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Analyze(bot))