import discord, requests, logging, time
from discord.ext import commands
from discord import app_commands
"""
Code pas encore terminé, mais voici la structure de base pour le module Pastebin.
"""
class Pastebin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pastebin", description="Publie sur Hastebin et retourne le lien")
    @app_commands.describe(
        contenu="Texte ou code à publier"
    )
    async def pastebin(self, interaction: discord.Interaction, contenu: str):
        await interaction.response.defer(thinking=True, ephemeral=True)
        start = time.perf_counter()
        try:
            response = requests.post("https://hastebin.com/documents", data=contenu.encode("utf-8"), timeout=10)
            elapsed = (time.perf_counter() - start) * 1000  # temps en ms
            if response.status_code == 200 and "key" in response.json():
                key = response.json()["key"]
                url = f"https://hastebin.com/{key}"
                embed = discord.Embed(
                    title="📝 Ton pastebin est prêt !",
                    description=f"[Clique ici pour voir ton pastebin]({url})",
                    color=discord.Color.blurple()
                )
                embed.set_footer(
                    text=f"PyLauncher • {elapsed:.1f} ms",
                    icon_url=self.bot.user.display_avatar.url
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                logging.info(f"[PASTEBIN] Pastebin créé par {interaction.user} ({interaction.user.id}) : {url} en {elapsed:.1f} ms")
            else:
                raise Exception("Erreur lors de la création du pastebin.")
        except Exception as e:
            elapsed = (time.perf_counter() - start) * 1000
            logging.error(f"[PASTEBIN] Erreur lors de la création du pastebin : {e}", exc_info=True)
            error_embed = discord.Embed(
                title="Erreur",
                description="❌ Impossible de créer le pastebin. Réessaie plus tard.",
                color=discord.Color.red()
            )
            error_embed.set_footer(
                text=f"PyLauncher • {elapsed:.1f} ms",
                icon_url=self.bot.user.display_avatar.url
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Pastebin(bot))