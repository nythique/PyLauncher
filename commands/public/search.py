import discord
from discord.ext import commands
from discord import app_commands
from config.settings import GROQ_TOKEN, MODEL, FREQUENCY, TEMPERATURE, MAX_TOKENS, TOP_P, PRESENCE_PENALTY
from groq import Groq
import time

class Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="search",
        description="Obtiens une réponse à une question Python"
    )
    @app_commands.describe(
        query="Question ou sujet Python à rechercher"
    )
    async def search(self, interaction: discord.Interaction, query: str):
        wait_embed = discord.Embed(
            description="<a:cargando:1377376325077172275> Génération du notebook en cours...",
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=wait_embed, ephemeral=True)
        try:
            start = time.perf_counter()
            client = Groq(api_key=GROQ_TOKEN)
            prompt = (
                f"Réponds de façon claire, précise et en français à la question suivante sur Python. "
                "Ne donne que la réponse, sans salutation, sans introduction, sans conclusion, sans commentaire inutile.\n"
                f"Question : {query}\n\nRéponse :"
            )
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "Tu es un assistant Python qui répond de façon claire, concise et précise, uniquement en français, sans salutation ni commentaire inutile."},
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
            answer = response.choices[0].message.content.strip()
            embed = discord.Embed(
                title=f"Réponse à : {query}",
                description=answer[:3800],
                color=discord.Color.blurple()
            )
            embed.set_footer(
                text=f"PyLauncher • {elapsed:.1f} ms",
                icon_url=self.bot.user.display_avatar.url
            )
            await interaction.edit_original_response(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="Erreur lors de la recherche",
                description=f"❌ Une erreur est survenue : {e}",
                color=discord.Color.red()
            )
            embed.set_footer(
                text="PyLauncher",
                icon_url=self.bot.user.display_avatar.url
            )
            await interaction.edit_original_response(embed=embed)

async def setup(bot):
    await bot.add_cog(Search(bot))