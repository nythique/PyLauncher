import discord
from discord.ext import commands
from discord import app_commands
from home.plugin.rooter import get_admin_ids

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="stats", description="Affiche les statistiques globales du bot (admin uniquement)")
    async def stats(self, interaction: discord.Interaction):
        # Vérifie que l'utilisateur est admin global
        if interaction.user.id not in get_admin_ids():
            await interaction.response.send_message(
                "⛔ Seuls les administrateurs globaux peuvent utiliser cette commande.", ephemeral=True
            )
            return

        total_guilds = len(self.bot.guilds)
        total_users = sum(guild.member_count for guild in self.bot.guilds)
        total_channels = sum(len(guild.text_channels) for guild in self.bot.guilds)
        total_commands = len(self.bot.tree.get_commands())

        embed = discord.Embed(
            title="📊 Statistiques PyLauncher",
            color=discord.Color.blurple()
        )
        embed.add_field(name="Serveurs", value=str(total_guilds))
        embed.add_field(name="Utilisateurs", value=str(total_users))
        embed.add_field(name="Salons textuels", value=str(total_channels))
        embed.add_field(name="Commandes slash", value=str(total_commands))
        embed.set_footer(
            text="PyLauncher • Nexium Portal",
            icon_url=self.bot.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Stats(bot))