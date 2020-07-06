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

    @commands.command(aliases=["wl"])
    async def whitelist(self, ctx: commands.Command):
        if (await self.privilegeCheck(ctx)):
            await ctx.send("You can whitelist")
            # await self.mcr.command("/whitelist add {}".format(player_name))

    async def privilegeCheck(self, ctx: commands.Command):
        is_admin = False

        for role in ctx.message.author.roles:
            if (role.name == "Admins"):
                is_admin = True
                await ctx.send("Is Admin")
        
        if (not is_admin):
            await ctx.send("Is not Admin")
        
        return is_admin