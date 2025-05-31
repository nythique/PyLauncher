import discord
from discord.ext import commands
from discord import app_commands
from config.settings import GROQ_TOKEN
import groq, os


class Explain(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="explain", description="Donne une explication du code")
    @app_commands.describe(message="Le code à expliquer")
    async def explain(self, interaction: discord.Interaction, message: str):
        await interaction.response.defer(thinking=True, ephemeral=True)
        try:
            client = groq.Groq(api_key=GROQ_TOKEN)
            prompt = (
                "Explique simplement ce que fait ce code Python, ligne par ligne, en français :\n"
                f"{message}\n\nExplication :"
            )
            response = client.chat.completions.create(
                model="llama3-8b-8192",  # Ou un autre modèle Groq disponible
                messages=[
                    {"role": "system", "content": "Tu es un assistant Python qui explique le code simplement en français."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=512,
                temperature=0.2,
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