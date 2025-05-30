import discord
from discord.ext import commands
from discord import app_commands

class Visualize(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="visualize", description="Générer une image de l'arbre d'exécution")
    @app_commands.describe(message="Le code à visualiser")
    async def visualize(self, interaction: discord.Interaction, message: str):
        # À compléter avec ta logique de visualisation
        await interaction.response.send_message("Visualisation à venir...", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Visualize(bot))