from diocraft.common_utils import discord_token
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand

class DioCraft(commands.Bot):
    def __init__(self, **options):
        super().__init__("/", help_command = None, **options)

        self.discord_token = discord_token

        from diocraft.cogs.main_cog import MainCog
        self.add_cog(MainCog(self))

    def run(self, *args, **kwargs):
        super().run(self.discord_token, *args, **kwargs)

    async def on_ready(self):
        print("Bot is ready!")