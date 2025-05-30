import discord
from discord.ext import commands
from home.plugin.firewall import set_guild_premium
from home.plugin.rooter import get_admin_ids

class Premium(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="setpremium")
    async def setpremium(self, ctx, guild_id: str, status: str):
        """Active ou désactive le premium pour un serveur (admin global uniquement)."""
        await ctx.message.delete()
        if ctx.author.id not in get_admin_ids():
            embed = discord.Embed(
                description="⛔ Seuls les administrateurs globaux peuvent utiliser cette commande.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed, delete_after=8)
            return

        if status.lower() not in ["true", "false"]:
            embed = discord.Embed(
                description="Utilisation : `!setpremium <guild_id> <true|false>`",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed, delete_after=8)
            return

        try:
            set_guild_premium(str(guild_id), premium=(status.lower() == "true"))
            msg = "Premium activé ✅" if status.lower() == "true" else "Premium désactivé ❌"
            embed = discord.Embed(
                description=f"{msg} pour le serveur avec l'ID **{guild_id}**.",
                color=discord.Color.green() if status.lower() == "true" else discord.Color.red()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                description=f"❌ Erreur lors de la modification du premium : {e}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Premium(bot))