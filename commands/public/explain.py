import discord
from discord.ext import commands
from discord import app_commands

class Explain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="explain", description="Donne une explication du code")
    @app_commands.describe(message="Le code à expliquer")
    async def explain(self, interaction: discord.Interaction, message: str):
        # À compléter avec ta logique d'explication
        await interaction.response.send_message("Explication du code à venir...", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Explain(bot))