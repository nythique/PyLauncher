import discord
from discord.ext import commands
from discord import app_commands

class History(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="history", description="Affiche l'historique personnel")
    async def history(self, interaction: discord.Interaction, message: str):
        # À compléter avec ta logique d'historique
        await interaction.response.send_message("Historique à venir...", ephemeral=True)

async def setup(bot):
    await bot.add_cog(History(bot))