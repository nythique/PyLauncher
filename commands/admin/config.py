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

    @app_commands.command(name="config", description="DEVS | Gérer les règles du bot")
    @app_commands.describe(
        action="Action à effectuer",
        identifier="Identifiant du serveur ou de l'utilisateur (si nécessaire)"
    )
    @app_commands.choices(action=[
        app_commands.Choice(name="Ajouter un admin", value="add_admin"),
        app_commands.Choice(name="Enléver un admin", value="remove_admin"),
        app_commands.Choice(name="Ban un serveur", value="ban_guild"),
        app_commands.Choice(name="Deban un serveur", value="unban_guild"),
        app_commands.Choice(name="Ban un utilisateur", value="ban_user"),
        app_commands.Choice(name="Deban un utilisateur", value="unban_user"),
        app_commands.Choice(name="Voir la config", value="show"),
    ])
    async def config(self, interaction: discord.Interaction, action: app_commands.Choice[str], identifier: str = None):
        support_guild = self.bot.get_guild(SUPPORT_GUILD_ID)
        member = support_guild.get_member(interaction.user.id) if support_guild else None
        if not member:
            await interaction.response.send_message(
                "⛔ Vous n'avez pas accès à cette commande. Assurez-vous d'être sur le serveur de support.", ephemeral=True
            )
            return
        if not member.guild_permissions.administrator:
            await interaction.response.send_message(
                "⛔ Vous n'avez pas les permissions nécessaires pour utiliser cette commande.", ephemeral=True
            )
            return

        try:
            act = action.value
            if act == "show":
                admins = ', '.join(str(a) for a in get_admin_ids()) or "None"
                banned_guilds = ', '.join(str(g) for g in get_banned_guilds()) or "None"
                banned_users = ', '.join(str(u) for u in get_banned_users()) or "None"
                embed = discord.Embed(
                    title="Configuration du bot",
                    description="Voici les informations de configuration actuelles du bot.",
                    color=discord.Color.blurple()
                )
                embed.add_field(name="Administrateurs", value=admins, inline=False)
                embed.add_field(name="Serveurs ban", value=banned_guilds, inline=False)
                embed.add_field(name="Utilisateurs ban", value=banned_users, inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return

            if not identifier or not identifier.isdigit():
                await interaction.response.send_message(
                    "⛔ Veuillez fournir un identifiant valide (numérique) pour cette action.", ephemeral=True
                )
                return

            id_int = int(identifier)
            if act == "add_admin":
                add_admin_id(id_int)
                msg = f"✅ Admin ajouté: {id_int}"
            elif act == "remove_admin":
                remove_admin_id(id_int)
                msg = f"✅ Admin rétiré: {id_int}"
            elif act == "ban_guild":
                ban_guild(id_int)
                msg = f"🚫 Serveur ban: {id_int}"
            elif act == "unban_guild":
                unban_guild(id_int)
                msg = f"✅ Serveur deban: {id_int}"
            elif act == "ban_user":
                ban_user(id_int)
                msg = f"🚫 Utilisateur ban: {id_int}"
            elif act == "unban_user":
                unban_user(id_int)
                msg = f"✅ Utilisateur deban: {id_int}"
            else:
                msg = "⛔ Action non reconnue."
            await interaction.response.send_message(msg, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"⛔ Une erreur est survenue : {str(e)}", ephemeral=True)
            print(f"[ERROR] Erreur dans la commande config: {str(e)}")
            logging.error(f"[ERROR] Erreur dans la commande config: {str(e)}")

async def setup(bot):
    await bot.add_cog(Config(bot))