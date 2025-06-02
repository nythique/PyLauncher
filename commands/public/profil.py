import discord
from discord.ext import commands
from discord import app_commands
from home.plugin.firewall import load_rate_limits
import time
import logging

class Profil(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profil", description="Voir le profil du serveur et ses stats d'utilisation")
    async def profil(self, interaction: discord.Interaction):
        try:
            guild_id = str(interaction.guild.id)
            data = load_rate_limits()
            now = int(time.time())
            guild = data.get(guild_id)
            if not guild:
                logging.warning(f"[PROFIL] Aucune donnée trouvée pour le serveur {guild_id}")
                await interaction.response.send_message("Aucune donnée trouvée pour ce serveur.", ephemeral=True)
                return

            premium = guild.get("premium", False)
            count = guild.get("count", 0)
            reset_time = guild.get("reset_time", now + 86400)
            last_request = guild.get("last_request", 0)
            max_per_day = 130 if premium else 50
            min_interval = 1 if premium else 5
            reset_in = max(0, reset_time - now)
            h, m, s = reset_in // 3600, (reset_in % 3600) // 60, reset_in % 60

            # Barre d'utilisation (évite division par zéro)
            progress = int((count / max_per_day) * 10) if max_per_day else 0
            bar = "🟩" * progress + "⬜" * (10 - progress)

            color = discord.Color.gold() if premium else discord.Color.blue()
            icon = interaction.guild.icon.url if interaction.guild.icon else discord.Embed.Empty
            badge = "🌟" if premium else "🔹"

            description = (
                f"**Statut Premium :** {'🌟 Premium' if premium else 'Standard'}\n"
                f"**Requêtes aujourd'hui :** `{count} / {max_per_day}`\n"
                f"**Utilisation :** `{bar}`\n"
                f"**Intervalle minimal :** `{min_interval} seconde(s)`\n"
                f"**Prochain reset :** dans **{h}h {m}m {s}s**\n"
            )
            if last_request:
                description += f"**Dernière requête :** <t:{last_request}:R>\n"

            embed = discord.Embed(
                title=f"{badge} Profil du serveur : {interaction.guild.name}",
                color=color,
                description=description
            )
            if icon:
                embed.set_thumbnail(url=icon)
            embed.set_footer(text=f"ID du serveur : {guild_id}")

            await interaction.response.send_message(embed=embed, ephemeral=True)
            logging.info(f"[PROFIL] Statut envoyé pour le serveur {guild_id} ({interaction.guild.name})")
        except Exception as e:
            logging.error(f"[PROFIL] Erreur lors de l'affichage du profil pour {interaction.guild.id if interaction.guild else 'inconnu'} : {e}", exc_info=True)
            embed = discord.Embed(
                title="Erreur",
                description="❌ Une erreur est survenue lors de la récupération du profil du serveur."
                " Veuillez réessayer plus tard ou contacter le support si le problème persiste.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Profil(bot))