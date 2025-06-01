import discord
from discord.ext import commands
from discord import app_commands
from config.settings import GROQ_TOKEN, MODEL, FREQUENCY, TEMPERATURE, MAX_TOKENS, TOP_P, PRESENCE_PENALTY
from groq import Groq
import time

class Transpiling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="transpile", description="Convertit du code en Python")
    @app_commands.describe(
        language="Langage source du code à convertir",
        code="Le code à convertir en Python"
    )
    @app_commands.choices(language=[
        app_commands.Choice(name="JavaScript", value="JavaScript"),
        app_commands.Choice(name="Java", value="Java"),
        app_commands.Choice(name="C", value="C"),
        app_commands.Choice(name="C++", value="C++"),
        app_commands.Choice(name="PHP", value="PHP"),
        app_commands.Choice(name="Ruby", value="Ruby"),
        app_commands.Choice(name="Go", value="Go"),
        app_commands.Choice(name="Rust", value="Rust"),
        app_commands.Choice(name="TypeScript", value="TypeScript"),
        app_commands.Choice(name="Autre", value="Autre"),
    ])
    async def transpile(
        self,
        interaction: discord.Interaction,
        language: app_commands.Choice[str],
        code: str
    ):
        wait_embed = discord.Embed(
            description="<a:cargando:1377376325077172275> Transpilation du code en cours...",
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=wait_embed, ephemeral=True)
        try:
            start = time.perf_counter()
            client = Groq(api_key=GROQ_TOKEN)
            prompt = (
                f"Convertis ce code {language.value} en code Python équivalent. "
                "Ne donne que le code Python, sans explication, sans commentaire, sans introduction ni conclusion.\n"
                f"Code à convertir :\n{code}\n\nCode Python :"
            )
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "Tu es un assistant qui convertit du code d'autres langages vers Python. Tu ne donnes que le code Python, sans explication ni commentaire."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=MAX_TOKENS,
                top_p=TOP_P,
                frequency_penalty=FREQUENCY,
                presence_penalty=PRESENCE_PENALTY,
                stop=["\n\n"],
                temperature=TEMPERATURE
            )
            elapsed = (time.perf_counter() - start) * 1000  # temps en ms
            python_code = response.choices[0].message.content.strip()
            embed = discord.Embed(
                title=f"Transpilation {language.value} → Python",
                description=f"```python\n{python_code[:3800]}```",
                color=discord.Color.blurple()
            )
            embed.set_footer(
                text=f"PyLauncher • Transpilation en {elapsed:.1f} ms. Propulsé par Nexium Portal",
                icon_url=self.bot.user.display_avatar.url
            )
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Erreur lors de la transpilation",
                description=f"❌ Signalement d'erreur : {str(e)}\n\n"
                "Veuillez vérifier que le code est correct et réessayer."
                "Si le problème persiste, veuillez contacter le support.",
                color=discord.Color.red()
            )
            embed.set_footer(
                text="PyLauncher",
                icon_url=self.bot.user.display_avatar.url
            )
            await interaction.edit_original_response(embed=embed)

async def setup(bot):
    await bot.add_cog(Transpiling(bot))