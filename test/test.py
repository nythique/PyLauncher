import discord
from discord.ext import commands, tasks

class TestCog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def cog_load(self):
        print("COG_LOAD APPELÉ")
        self.test_loop.start()

    @tasks.loop(seconds=5)
    async def test_loop(self):
        print("BOUCLE TEST APPELÉE")

    @test_loop.before_loop
    async def before_test_loop(self):
        print("Attente que le bot soit prêt...")
        await self.bot.wait_until_ready()
        print("Bot prêt, boucle test va démarrer.")

async def setup(bot):
    await bot.add_cog(TestCog(bot))