import discord
from discord.ext import commands
from discord import app_commands
from config.settings import SUPPORT_GUILD_ID
from home.plugin.rooter import (
    add_admin_id, remove_admin_id,
    ban_guild, unban_guild,
    ban_user, unban_user,
    get_admin_ids, get_banned_guilds, get_banned_users
)

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="config", description="ADMIN | Configure the bot (admins, bans...)")
    @app_commands.describe(
        action="Action to perform",
        identifier="User or server ID (required except for 'show')"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Add admin", value="add_admin"),
        app_commands.Choice(name="Remove admin", value="remove_admin"),
        app_commands.Choice(name="Ban guild", value="ban_guild"),
        app_commands.Choice(name="Unban guild", value="unban_guild"),
        app_commands.Choice(name="Ban user", value="ban_user"),
        app_commands.Choice(name="Unban user", value="unban_user"),
        app_commands.Choice(name="Show config", value="show"),
    ])
    async def config(self, interaction: discord.Interaction, action: app_commands.Choice[str], identifier: str = None):
        # Vérifie que l'utilisateur est membre et admin du serveur support
        support_guild = self.bot.get_guild(SUPPORT_GUILD_ID)
        member = support_guild.get_member(interaction.user.id) if support_guild else None
        if not member:
            await interaction.response.send_message(
                "⛔ You must be a member of the support server to use this command.", ephemeral=True
            )
            return
        if not member.guild_permissions.administrator:
            await interaction.response.send_message(
                "⛔ You must be an administrator on the support server to use this command.", ephemeral=True
            )
            return

        try:
            act = action.value
            if act == "show":
                admins = ', '.join(str(a) for a in get_admin_ids()) or "None"
                banned_guilds = ', '.join(str(g) for g in get_banned_guilds()) or "None"
                banned_users = ', '.join(str(u) for u in get_banned_users()) or "None"
                embed = discord.Embed(
                    title="Bot configuration",
                    color=discord.Color.blurple()
                )
                embed.add_field(name="Admins", value=admins, inline=False)
                embed.add_field(name="Banned guilds", value=banned_guilds, inline=False)
                embed.add_field(name="Banned users", value=banned_users, inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            # Pour toutes les autres actions, l'identifiant est requis et doit être numérique
            if not identifier or not identifier.isdigit():
                await interaction.response.send_message(
                    "Please provide a valid numeric ID for this action.", ephemeral=True
                )
                return

            id_int = int(identifier)
            if act == "add_admin":
                add_admin_id(id_int)
                msg = f"✅ Admin added: {id_int}"
            elif act == "remove_admin":
                remove_admin_id(id_int)
                msg = f"✅ Admin removed: {id_int}"
            elif act == "ban_guild":
                ban_guild(id_int)
                msg = f"🚫 Guild banned: {id_int}"
            elif act == "unban_guild":
                unban_guild(id_int)
                msg = f"✅ Guild unbanned: {id_int}"
            elif act == "ban_user":
                ban_user(id_int)
                msg = f"🚫 User banned: {id_int}"
            elif act == "unban_user":
                unban_user(id_int)
                msg = f"✅ User unbanned: {id_int}"
            else:
                msg = "Unknown action."
            await interaction.response.send_message(msg, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"Error during configuration: {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Config(bot))