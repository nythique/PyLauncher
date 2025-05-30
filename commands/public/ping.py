import discord
from discord.ext import commands
from discord import app_commands

class SlashUtils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ping", description="Affiche la latence du bot et de Discord")
    async def ping(self, interaction: discord.Interaction):
        bot_latency = round(self.bot.latency * 1000)
        color = discord.Color.green() if bot_latency < 150 else discord.Color.orange()
        embed = discord.Embed(
            title=f"🏓 Pong ! {bot_latency} ms",
            color=color
        )
        embed.set_footer(text="Lunaris IA • Nexium Portal")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(SlashUtils(bot))