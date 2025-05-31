import discord
from discord.ext import commands
from discord import app_commands
from home.plugin.firewall import set_guild_premium
from home.plugin.rooter import get_admin_ids

class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="unleash",
        description="Active ou désactive le premium pour un serveur (admin global uniquement)"
    )
    @app_commands.describe(
        guild_id="ID du serveur à modifier",
        status="Activer ou désactiver le premium (true/false)"
    )
    async def unleash(self, interaction: discord.Interaction, guild_id: str, status: str):
        # Vérifie que l'utilisateur est admin global
        if interaction.user.id not in get_admin_ids():
            embed = discord.Embed(
                title="Accès Premium",
                description=(
                    "⛔ Seuls les administrateurs globaux peuvent activer le premium directement.\n\n"
                    "Pour obtenir le premium sur votre serveur, merci de contacter le support Nexium Portal.\n"
                    "Le système de paiement automatique arrive bientôt !"
                ),
                color=discord.Color.orange()
            )
            embed.set_footer(
                text="Support Nexium Portal",
                icon_url=self.bot.user.display_avatar.url
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if status.lower() not in ["true", "false"]:
            embed = discord.Embed(
                description="Utilisation : `/premium <guild_id> <true|false>`",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            set_guild_premium(str(guild_id), premium=(status.lower() == "true"))
            msg = "Premium activé ✅" if status.lower() == "true" else "Premium désactivé ❌"
            embed = discord.Embed(
                description=f"{msg} pour le serveur avec l'ID **{guild_id}**.",
                color=discord.Color.green() if status.lower() == "true" else discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                description=f"❌ Erreur lors de la modification du premium : {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Premium(bot))