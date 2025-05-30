import discord
from discord.ext import commands
from discord import app_commands

class Challenge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="challenge", description="Générer un mini-problème Python")
    @app_commands.describe(message="Sujet ou thème du challenge")
    async def challenge(self, interaction: discord.Interaction, message: str):
        # À compléter avec ta logique de génération de challenge
        await interaction.response.send_message("Challenge à venir...", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Challenge(bot))