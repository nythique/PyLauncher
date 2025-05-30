import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime

class SlashUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Affiche la latence du bot et de Discord")
    async def ping(self, interaction: discord.Interaction):
        ws_latency = round(self.bot.latency * 1000)
        color = discord.Color.green() if ws_latency < 100 else discord.Color.orange() if ws_latency < 250 else discord.Color.red()

        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"**WebSocket latency:** `{ws_latency} ms`",
            color=color,
            timestamp=datetime.now()
        )
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.display_avatar.url)
        embed.set_footer(
            text="PyLauncher • Nexium Portal | Powered by Discord.py",
            icon_url=self.bot.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(SlashUtils(bot))