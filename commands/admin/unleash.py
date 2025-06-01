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
        description="DEVS : Gérer les limitations d'un serveur"
    )
    @app_commands.describe(
        serverID="Id du serveur",
        max="Limiter ou non ? (true/false)"
    )
    async def unleash(self, interaction: discord.Interaction, serverID: str, max: str):
        if interaction.user.id not in get_admin_ids():
            embed = discord.Embed(
                title="Accès Refusé",
                description=(
                    "⛔ Vous n'avez pas le droit d'utiliser cette commande.\n"
                    "Pour debloquer les limitations du serveur, contactez le support."
                ),
                color=discord.Color.red()
            )
            embed.set_footer(
                text="Support Nexium Portal",
                icon_url=self.bot.user.display_avatar.url
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if status.lower() not in ["true", "false"]:
            embed = discord.Embed(
                description="Utilisation : `/unleash <serverId> <true|false>`",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            set_guild_premium(str(guild_id), premium=(status.lower() == "true"))
            msg = "Limites supprimées ✅" if status.lower() == "true" else "Limites imposées ❌"
            embed = discord.Embed(
                description=f"{msg} pour le serveur avec l'ID **{serverId}**.",
                color=discord.Color.green() if status.lower() == "true" else discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                description=f"Erreur s'est produite : {e}",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Premium(bot))