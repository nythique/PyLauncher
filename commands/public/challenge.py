import discord
from discord.ext import commands
from discord import app_commands

class Challenge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="challenge", description="Générer un mini-problème Python")
    @app_commands.describe(
        niveau="Niveau de difficulté du challenge",
        message="Sujet ou thème du challenge (optionnel)"
    )
    @app_commands.choices(niveau=[
        app_commands.Choice(name="Nuls", value="nuls"),
        app_commands.Choice(name="Débutant", value="debutant"),
        app_commands.Choice(name="Intermédiaire", value="intermediaire"),
        app_commands.Choice(name="Avancé", value="avance"),
        app_commands.Choice(name="Pro", value="pro"),
    ])
    async def challenge(self, interaction: discord.Interaction, niveau: app_commands.Choice[str], message: str = None):
        # Ici tu peux ajouter la logique de génération de challenge selon le niveau et le thème
        await interaction.response.send_message(
            f"Challenge à venir...\nNiveau choisi : **{niveau.name}**\nThème : {message or 'aucun'}",
            ephemeral=True
        )

async def setup(bot):
    await bot.add_cog(Challenge(bot))