import discord
from discord.ext import commands
from discord import app_commands
import pydoc

class Docs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="docs", description="Consulte la documentation Python officielle")
    @app_commands.describe(
        sujet="Fonction, module ou classe Python à consulter (ex: print, list, os, itertools...)"
    )
    async def docs(self, interaction: discord.Interaction, sujet: str):
        sujet = sujet.strip()
        base_url = "https://docs.python.org/3/library/"
        doc_url = f"{base_url}{sujet}.html"
        # Essaye de récupérer un résumé avec pydoc
        try:
            summary = pydoc.render_doc(sujet, "Help on %s")
            summary = summary.split('\n', 10)[-1]  # Prend les premières lignes utiles
            summary = summary[:400] + "..." if len(summary) > 400 else summary
        except Exception:
            summary = "Aucun résumé disponible, consulte la documentation officielle."

        embed = discord.Embed(
            title=f"Documentation Python : {sujet}",
            description=summary,
            color=discord.Color.blurple(),
            url=doc_url
        )
        embed.add_field(
            name="Lien vers la documentation officielle",
            value=f"[Voir la doc]({doc_url})",
            inline=False
        )
        embed.set_footer(
            text="PyLauncher • Documentation Python",
            icon_url=self.bot.user.display_avatar.url
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Docs(bot))