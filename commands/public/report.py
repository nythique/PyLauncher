import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="report", description="Envoyer un rapport ou signaler un problème à l'équipe")
    @app_commands.describe(message="Décris ton problème ou ta suggestion")
    async def report(self, interaction: discord.Interaction, message: str):
        await interaction.response.send_message(
            "Merci pour ton rapport ! L'équipe a bien reçu ta demande.", ephemeral=True
        )

        REPORT_CHANNEL_ID = 1360403767274508355  # À adapter
        report_embed = discord.Embed(
            title="",
            description=f"```{message}```",
            color=discord.Color.orange()
        )
        report_embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.avatar.url)
        report_embed.set_footer(
            text=f"Identifiant de {interaction.user.display_name}: {interaction.user.id})"
        )
        report_embed.timestamp = datetime.now()

        channel = self.bot.get_channel(REPORT_CHANNEL_ID)
        if channel:
            await channel.send(embed=report_embed)
        else:
            ADMIN_ID = 123456789012345678  # <-- À remplacer par ton ID Discord
            admin = await self.bot.fetch_user(ADMIN_ID)
            await admin.send(embed=report_embed)

async def setup(bot):
    await bot.add_cog(Report(bot))