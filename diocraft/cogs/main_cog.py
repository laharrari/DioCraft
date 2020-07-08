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
        allowed_roles = ["Minecraft"]
        if (await self.privilegeCheck(ctx, allowed_roles) and await self.channelCheck(ctx)):
            player_name = ctx.message.content[5:]
            resp = self.mcr.command("/whitelist add {}".format(player_name))
            await ctx.send(resp)

    @commands.command()
    async def dwl(self, ctx: commands.Command):
        allowed_roles = ["Admins"]
        if (await self.privilegeCheck(ctx, allowed_roles) and await self.channelCheck(ctx)):
            player_name = ctx.message.content[5:]
            resp = self.mcr.command("/whitelist remove {}".format(player_name))
            await ctx.send(resp)
    
    @commands.command()
    async def wl(self, ctx: commands.Command):
        if (await self.channelCheck(ctx)):
            await self.listWhitelist(ctx)

    @commands.command()
    async def online(self, ctx: commands.Command):
        if (await self.channelCheck(ctx)):
            await self.listPlayers(ctx)

    @commands.command()
    async def help(self, ctx: commands.Command):
        if (await self.channelCheck(ctx)):
            msg = "Thank you for using DioCraft! It is still currently under development :)\n\n"
            msg += "/online - Display list of all players that are online.\n"
            msg += "/wl - Display list of all players that are whitelisted.\n"
            msg += "/awl <name> - To add someone to the server whitelist.\n"
            msg += "/dwl <name> - To remove someone from the server whitelist.\n\n"
            msg += "If you have any questions or suggestions, please contact primal#7602! Thank you!"
            await ctx.send(msg)

    async def privilegeCheck(self, ctx: commands.Command, allowed_roles):
        is_admin = False

        for role in ctx.message.author.roles:
            if (role.name in allowed_roles):
                is_admin = True
        
        if (not is_admin):
            await ctx.send("{}, does not have permission.".format(ctx.message.author.display_name))
        
        return is_admin

    async def channelCheck(self, ctx: commands.Command):
        is_channel = False
        allowed_channels = [729859164209283104, 729513577186066473]
        # Change this to list to hold more channels.
        if (ctx.message.channel.id in allowed_channels):
            is_channel = True

        return is_channel

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