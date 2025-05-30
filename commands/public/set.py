import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from home.plugin.pipeline import set_whitelisted_channel
from config.settings import REPORT_CHANNEL_ID

class Set(commands.GroupCog, name="set"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="channel", description="Définir le salon autorisé pour ce serveur")
    @app_commands.describe(channel="Salon à whitelister")
    async def channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        # Vérifie que l'utilisateur est admin sur ce serveur
        member = interaction.guild.get_member(interaction.user.id)
        if not member or not member.guild_permissions.administrator:
            await interaction.response.send_message(
                "⛔ Vous devez être administrateur du serveur pour utiliser cette commande.", ephemeral=True
            )
            return

        set_whitelisted_channel(interaction.guild.id, channel.id)
        await interaction.response.send_message(
            f"✅ Salon whitelisté pour ce serveur : {channel.mention}", ephemeral=True
        )

    @app_commands.command(name="report", description="Envoyer un rapport ou signaler un problème à l'équipe")
    @app_commands.describe(message="Décris ton problème ou ta suggestion")
    async def report(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(
            "Merci pour ton rapport ! L'équipe a bien reçu ta demande.", ephemeral=True
        )
        report_embed = discord.Embed(
            title="Nouveau rapport",
            description=f"```{message}```",
            color=discord.Color.orange()
        )
        report_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        report_embed.set_footer(
            text=f"Identifiant de {interaction.user.display_name}: {interaction.user.id}"
        )
        report_embed.timestamp = datetime.now()

        channel = self.bot.get_channel(REPORT_CHANNEL_ID)
        if channel:
            await channel.send(embed=report_embed)
        else:
            ADMIN_ID = 1233020939898327092 
            admin = await self.bot.fetch_user(ADMIN_ID)
            await admin.send(embed=report_embed)

async def setup(bot):
    await bot.add_cog(Set(bot))