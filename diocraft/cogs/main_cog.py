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

    @commands.command()
    async def help(self, ctx: commands.Command):
        msg = "Thank you for using DioCraft! It is still currently under development :)\n\n"
        msg += "/awl <name> - To add someone to the server whitelist.\n"
        msg += "/dwl <name> - To remove someone from the server whitelist.\n\n"
        msg += "If you have any questions or suggestions, please contact primal#7602! Thank you!"
        await ctx.send(msg)

    async def privilegeCheck(self, ctx: commands.Command):
        is_admin = False

        for role in ctx.message.author.roles:
            if (role.name == "Admins"):
                is_admin = True
        
        if (not is_admin):
            await ctx.send("{}, is not an Admin.".format(ctx.message.author.display_name))
        
        return is_admin