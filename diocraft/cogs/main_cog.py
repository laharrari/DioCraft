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
    async def ping(self, ctx: commands.Command):
        await ctx.send("Pong")

    @commands.command()
    async def awl(self, ctx: commands.Command):
        if (await self.privilegeCheck(ctx)):
            player_name = ctx.message.content[5:]
            resp = self.mcr.command("/whitelist add {}".format(player_name))
            await ctx.send(resp)

    @commands.command()
    async def dwl(self, ctx: commands.Command):
        if (await self.privilegeCheck(ctx)):
            player_name = ctx.message.content[5:]
            resp = self.mcr.command("/whitelist remove {}".format(player_name))
            await ctx.send(resp)

    async def privilegeCheck(self, ctx: commands.Command):
        is_admin = False

        for role in ctx.message.author.roles:
            if (role.name == "Admins"):
                is_admin = True
        
        if (not is_admin):
            await ctx.send("{}, is not an Admin.".format(ctx.message.author.display_name))
        
        return is_admin