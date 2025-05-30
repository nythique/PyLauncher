import discord
from discord.ext import commands
from discord import app_commands

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="config", description="ADMIN | Configurer le bot pour le serveur")
    @app_commands.describe(message="Paramètres à configurer")
    async def config(self, interaction: discord.Interaction, message: str):
        # À compléter avec ta logique de configuration
        await interaction.response.send_message("Configuration à venir...", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Config(bot))