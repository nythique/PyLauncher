import discord
from discord.ext import commands
from discord import app_commands
from home.plugin.firewall import load_rate_limits
import time

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profil", description="Voir le profil du serveur et ses stats d'utilisation")
    async def status(self, interaction: discord.Interaction):
        guild_id = str(interaction.guild.id)
        data = load_rate_limits()
        now = int(time.time())
        guild = data.get(guild_id)
        if not guild:
            await interaction.response.send_message("Aucune donnée trouvée pour ce serveur.", ephemeral=True)
            return

        premium = guild.get("premium", False)
        count = guild.get("count", 0)
        reset_time = guild.get("reset_time", now + 86400)
        last_request = guild.get("last_request", 0)
        max_per_day = 130 if premium else 50
        min_interval = 1 if premium else 5
        reset_in = reset_time - now
        h, m, s = reset_in // 3600, (reset_in % 3600) // 60, reset_in % 60

        # Style avancé
        color = discord.Color.gold() if premium else discord.Color.blue()
        icon = interaction.guild.icon.url if interaction.guild.icon else discord.Embed.Empty
        badge = "🌟" if premium else "🔹"
        bar = "🟩" * int((count / max_per_day) * 10) + "⬜" * (10 - int((count / max_per_day) * 10))

        embed = discord.Embed(
            title=f"{badge} Profil du serveur : {interaction.guild.name}",
            color=color,
            description=(
                f"**Statut Premium :** {'🌟 Premium' if premium else 'Standard'}\n"
                f"**Requêtes aujourd'hui :** `{count} / {max_per_day}`\n"
                f"**Utilisation :** `{bar}`\n"
                f"**Intervalle minimal :** `{min_interval} seconde(s)`\n"
                f"**Prochain reset :** dans **{h}h {m}m {s}s**\n"
                f"**Dernière requête :** <t:{last_request}:R>" if last_request else ""
            )
        )
        if icon:
            embed.set_thumbnail(url=icon)
        embed.set_footer(text=f"ID du serveur : {guild_id}")

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Status(bot))