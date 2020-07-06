import discord
import socket
from mcrcon import MCRcon
from discord.ext import commands
from diocraft.diocraft import DioCraft

from diocraft.common_utils import server_ip
from diocraft.common_utils import server_port
from diocraft.common_utils import server_password

class MainCog(commands.Cog, name = "main"):
    def __init__(self, bot: DioCraft):
        super().__init__()
        
        self.mcr = MCRcon(server_ip, server_password, int(server_port))
        self.mcr.connect()

        self.bot = bot

    @commands.command()
    async def awl(self, ctx: commands.Command):
        if (await self.privilegeCheck(ctx, "Admins")):
            player_name = ctx.message.content[5:]
            resp = self.mcr.command("/whitelist add {}".format(player_name))
            await ctx.send(resp)

    @commands.command()
    async def dwl(self, ctx: commands.Command):
        if (await self.privilegeCheck(ctx, "Admins")):
            player_name = ctx.message.content[5:]
            resp = self.mcr.command("/whitelist remove {}".format(player_name))
            await ctx.send(resp)
    
    @commands.command()
    async def wl(self, ctx: commands.Command):
        await self.listWhitelist(ctx)

    @commands.command()
    async def online(self, ctx: commands.Command):
        await self.listPlayers(ctx)

    @commands.command()
    async def help(self, ctx: commands.Command):
        msg = "Thank you for using DioCraft! It is still currently under development :)\n\n"
        msg += "/wl - Display list of all players that are whitelisted.\n"
        msg += "/awl <name> - To add someone to the server whitelist.\n"
        msg += "/dwl <name> - To remove someone from the server whitelist.\n\n"
        msg += "If you have any questions or suggestions, please contact primal#7602! Thank you!"
        await ctx.send(msg)

    async def privilegeCheck(self, ctx: commands.Command, roleName):
        is_admin = False

        for role in ctx.message.author.roles:
            if (role.name == roleName):
                is_admin = True
        
        if (not is_admin):
            await ctx.send("{}, is not an Admin.".format(ctx.message.author.display_name))
        
        return is_admin

    async def listWhitelist(self, ctx: commands.Command):
        resp = self.mcr.command("/whitelist list").split(" ")
        result = "The following {} players are whitelisted:\n".format(resp[2])
        resp = resp[5:]
        lastName = resp[len(resp) - 1]
        resp = resp[:-1]

        for name in resp:
            result += name[:-1] + "\n"

        result += lastName

        await ctx.send(result)

    async def listPlayers(self, ctx: commands.Command):
        resp = self.mcr.command("/list").split(" ")
        result = "There {} players online:\n".format(resp[2])
        resp = resp[10:]
        lastName = resp[len(resp) - 1]
        resp = resp[:-1]

        for name in resp:
            result += name[:-1] + "\n"

        result += lastName

        await ctx.send(result)