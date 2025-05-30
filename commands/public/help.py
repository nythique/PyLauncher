import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Afficher l'aide du bot")
    async def help(self, interaction: discord.Interaction):
        bot_user = self.bot.user
        embed = discord.Embed(
            title="Aide de Lunaris",
            description="Voici les principales commandes et fonctionnalités du bot :",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=bot_user.display_avatar.url)
        embed.add_field(name="/help", value="Affiche ce message d'aide.", inline=False)
        embed.add_field(
            name="/ping",
            value="Affiche la latence du bot et de Discord.",
            inline=False
        )
        embed.set_footer(text="Développé par Nexium Portal • Lunaris IA")
        invite_url = f"https://discord.com/oauth2/authorize?client_id={bot_user.id}&scope=bot"
        embed.add_field(
            name="Lien d'invitation",
            value=f"[Clique ici pour inviter le bot]({invite_url})",
            inline=False
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Help(bot))