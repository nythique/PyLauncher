import discord, logging, time
from config.settings import SECURITY_LOG_PATH, ERROR_LOG_PATH
from discord.ext import commands
from discord import app_commands
from config.settings import GROQ_TOKEN, MODEL, FREQUENCY, TEMPERATURE, MAX_TOKENS, TOP_P, PRESENCE_PENALTY
from groq import Groq

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

class Challenge(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="challenge", description="Générer un mini-problème Python")
    @app_commands.describe(
        niveau="Niveau de difficulté du challenge",
        subject="Sujet ou thème du challenge (optionnel)"
    )
    @app_commands.choices(niveau=[
        app_commands.Choice(name="Nuls", value="nuls"),
        app_commands.Choice(name="Débutant", value="debutant"),
        app_commands.Choice(name="Intermédiaire", value="intermediaire"),
        app_commands.Choice(name="Avancé", value="avance"),
        app_commands.Choice(name="Pro", value="pro"),
    ])
    async def challenge(self, interaction: discord.Interaction, niveau: app_commands.Choice[str], subject: str = None):
        wait_embed = discord.Embed(
            description="<a:cargando:1377376325077172275> Génération du challenge en cours...",
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=wait_embed, ephemeral=True)
        try:
            start = time.perf_counter()
            client = Groq(api_key=GROQ_TOKEN)
            prompt = (
                f"Génère un mini-problème Python adapté à un niveau '{niveau.name}'. "
                f"{'Le thème est : ' + subject if subject else ''} "
                "Le challenge doit être court, clair, et adapté au niveau. "
                "Ne donne que l'énoncé du problème, sans solution, sans salutation, sans explication."
            )
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "Tu es un assistant qui crée des mini-challenges Python adaptés au niveau demandé. Tu ne donnes que l'énoncé du problème, sans solution ni explication."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=MAX_TOKENS,
                top_p=TOP_P,
                frequency_penalty=FREQUENCY,
                presence_penalty=PRESENCE_PENALTY,
                stop=["\n\n"],
                temperature=TEMPERATURE
            )
            elapsed = (time.perf_counter() - start) * 1000  # ms
            challenge_text = response.choices[0].message.content.strip()
            embed = discord.Embed(
                title=f"Challenge Python ({niveau.name})",
                description=challenge_text[:3800],
                color=discord.Color.blurple()
            )
            embed.set_footer(
                text=f"PyLauncher • Challenge généré en {elapsed:.1f} ms",
                icon_url=self.bot.user.display_avatar.url
            )
            await interaction.edit_original_response(embed=embed)
            logging.info(f"[CHALLENGE] Challenge '{niveau.name}' généré par {interaction.user} ({interaction.user.id}) en {elapsed:.1f} ms")
        except Exception as e:
            logging.error(f"[CHALLENGE] Erreur lors de la génération du challenge ({interaction.user}): {e}", exc_info=True)
            embed = discord.Embed(
                title="Erreur lors de la génération",
                description=f"❌ Une erreur s'est produite :\n```{str(e)}```\nVeuillez vérifier que le niveau est correct et réessayer.\nSi le problème persiste, veuillez contacter le support.",
                color=discord.Color.red()
            )
            embed.set_footer(
                text="PyLauncher",
                icon_url=self.bot.user.display_avatar.url
            )
            await interaction.edit_original_response(embed=embed)

async def setup(bot):
    await bot.add_cog(Challenge(bot))