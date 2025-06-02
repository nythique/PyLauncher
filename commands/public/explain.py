import discord, logging
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH, GROQ_TOKEN, MODEL, FREQUENCY, TEMPERATURE, MAX_TOKENS, TOP_P, PRESENCE_PENALTY
from discord.ext import commands
from discord import app_commands
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

class Explain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="explain", description="Donne une explication du code")
    @app_commands.describe(
        code="Le code à expliquer",
        language="Langue de l'explication"
    )
    @app_commands.choices(language=[
        app_commands.Choice(name="Français", value="fr"),
        app_commands.Choice(name="Anglais", value="en"),
        app_commands.Choice(name="Espagnol", value="es"),
        app_commands.Choice(name="Allemand", value="de"),
        app_commands.Choice(name="Italien", value="it"),
    ])
    async def explain(
        self,
        interaction: discord.Interaction,
        code: str,
        language: app_commands.Choice[str] = None
    ):
        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            lang = language.value if language else "fr"
            client = Groq(api_key=GROQ_TOKEN)
            prompt = (
                f"Explique ce que fait ce code Python, ligne par ligne, en {lang}. "
                "Ne commence pas par une salutation, ne conclus pas, ne donne aucun commentaire inutile ou phrase d'introduction ou de fin. "
                "Donne uniquement l'explication du code, de façon concise et claire.\n"
                f"{code}\n\nExplication :"
            )
            response = client.chat.completions.create(
                model=MODEL,  
                messages=[
                    {"role": "system", "content": "Tu es un assistant qui explique le code Python de manière simple, claire et concise, sans aucune salutation, introduction ou conclusion."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=MAX_TOKENS,
                top_p=TOP_P,
                frequency_penalty=FREQUENCY,
                presence_penalty=PRESENCE_PENALTY,
                stop=["\n\n"], 
                temperature=TEMPERATURE
            )
            explanation = response.choices[0].message.content.strip()
            embed = discord.Embed(
                title="Explication du code",
                description=explanation[:4000],
                color=discord.Color.blurple()
            )
            await interaction.followup.send(embed=embed, ephemeral=True)
            logging.info(f"[EXPLAIN] Explication envoyée à {interaction.user} ({interaction.user.id}) en {lang}")
        except Exception as e:
            logging.error(f"[EXPLAIN] Erreur lors de l'explication du code par {interaction.user} ({interaction.user.id}): {e}", exc_info=True)
            error_embed = discord.Embed(
                title="Erreur lors de l'explication",
                description=f"❌ Une erreur est survenue lors de l'explication : {e}\nVeuillez réessayer plus tard.",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=error_embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Explain(bot))