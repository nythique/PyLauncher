import discord
from discord.ext import commands
from discord import app_commands

class Notebook(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="notebook",
        description="Génère un notebook Jupyter (.ipynb) à partir de code Python fourni"
    )
    @app_commands.describe(
        titre="Titre du notebook (obligatoire)",
        code="Code Python à inclure dans le notebook (obligatoire)"
    )
    async def notebook(self, interaction: discord.Interaction, titre: str, code: str):
        import nbformat
        from nbformat.v4 import new_notebook, new_code_cell
        import io, time

        wait_embed = discord.Embed(
            description="<a:cargando:1377376325077172275> Génération du notebook en cours...",
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=wait_embed, ephemeral=True)

        start = time.perf_counter()
        nb = new_notebook()
        nb['cells'] = [new_code_cell(code)]
        nb['metadata']['title'] = titre

        # Correction ici : écriture dans StringIO puis conversion en BytesIO
        str_buffer = io.StringIO()
        nbformat.write(nb, str_buffer)
        data = str_buffer.getvalue().encode("utf-8")
        buffer = io.BytesIO(data)
        buffer.seek(0)
        elapsed = (time.perf_counter() - start) * 1000  # temps en ms

        file = discord.File(fp=buffer, filename=f"{titre.replace(' ', '_')}.ipynb")
        embed = discord.Embed(
            title="Notebook généré",
            description="Voici votre notebook Jupyter prêt à être téléchargé.",
            color=discord.Color.blurple()
        )
        embed.set_footer(
            text=f"PyLauncher • {elapsed:.1f} ms",
            icon_url=self.bot.user.display_avatar.url
        )
        await interaction.edit_original_response(embed=embed, attachments=[file])

async def setup(bot):
    await bot.add_cog(Notebook(bot))