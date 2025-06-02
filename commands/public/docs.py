import discord, logging
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from discord.ext import commands
from discord import app_commands
import pydoc
from config.settings import GROQ_TOKEN, MODEL, MAX_TOKENS, TOP_P, FREQUENCY, PRESENCE_PENALTY, TEMPERATURE
from groq import Groq

# Configuration des handlers de logs
info_handler = logging.FileHandler(SECURITY_LOG_PATH, encoding='utf-8')
info_handler.setLevel(logging.INFO)
info_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

error_handler = logging.FileHandler(ERROR_LOG_PATH, encoding='utf-8')
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter(
    '[%(levelname)s] %(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))

logging.getLogger().handlers = []
logging.getLogger().addHandler(info_handler)
logging.getLogger().addHandler(error_handler)
logging.getLogger().setLevel(logging.INFO)

class Docs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="docs", description="Consulte la documentation Python officielle (résumé en français)")
    @app_commands.describe(
        sujet="Fonction, module ou classe Python à consulter (ex: print, list, os, itertools...)"
    )
    async def docs(self, interaction: discord.Interaction, subject: str):
        sujet = subject.strip()
        base_url = "https://docs.python.org/3/library/"
        doc_url = f"{base_url}{sujet}.html"
        try:
            try:
                summary = pydoc.render_doc(sujet, "Help on %s")
                summary = summary.split('\n', 10)[-1]
                summary = summary[:400] + "..." if len(summary) > 400 else summary
            except Exception as e:
                logging.warning(f"[DOCS] Impossible de générer le résumé pour '{sujet}': {e}")
                summary = "Aucun résumé disponible, consulte la documentation officielle."

            # Traduction automatique en français via Groq
            try:
                client = Groq(api_key=GROQ_TOKEN)
                prompt = (
                    "Traduis en français ce résumé de documentation Python, sans ajouter de commentaire ni de salutation :\n"
                    f"{summary}"
                )
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {"role": "system", "content": "Tu es un assistant qui traduit en français de façon claire et concise."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=MAX_TOKENS,
                    top_p=TOP_P,
                    frequency_penalty=FREQUENCY,
                    presence_penalty=PRESENCE_PENALTY,
                    temperature=TEMPERATURE
                )
                summary_fr = response.choices[0].message.content.strip()
            except Exception as e:
                logging.error(f"[DOCS] Erreur lors de la traduction Groq pour '{sujet}': {e}", exc_info=True)
                summary_fr = "Résumé non traduit automatiquement. Consulte la documentation officielle pour plus de détails."

            embed = discord.Embed(
                title=f"Documentation Python : {sujet}",
                description=summary_fr,
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
            logging.info(f"[DOCS] Documentation envoyée pour '{sujet}' à {interaction.user}")
        except Exception as e:
            logging.error(f"[DOCS] Erreur inattendue pour '{sujet}': {e}", exc_info=True)
            error_embed = discord.Embed(
                title="Erreur lors de la consultation de la documentation",
                description="❌ Une erreur est survenue lors de la récupération de la documentation."
                " Veuillez réessayer plus tard, ou contacter le support si le problème persiste.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=error_embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Docs(bot))