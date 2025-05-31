import discord
from discord.ext import commands
from discord import app_commands
from config.settings import GROQ_TOKEN, MODEL, FREQUENCY, TEMPERATURE, MAX_TOKENS, TOP_P, PRESENCE_PENALTY
from groq import Groq


class Explain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="explain", description="Donne une explication du code")
    @app_commands.describe(message="Le code à expliquer")
    async def explain(self, interaction: discord.Interaction, code: str, language: str = "fr"):
        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            client = Groq(api_key=GROQ_TOKEN)
            prompt = (
                f"Explique simplement ce que fait ce code Python, ligne par ligne, en {language} sans commentaire unile comme les salutation de ta part:\n"
                f"{code}\n\nExplication :"
            )
            response = client.chat.completions.create(
                model=MODEL,  
                messages=[
                    {"role": "system", "content": "Tu êtes un assistant qui explique le code Python de manière simple et claire. Sans commentaires inutiles."},
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
        except Exception as e:
            await interaction.followup.send(f"Erreur lors de l'explication : {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Explain(bot))