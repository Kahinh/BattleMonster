import lib
import typing

class Sync(lib.discord.ext.commands.Cog):
    def __init__(self, bot: lib.commands.Bot) -> None:
        self.bot = bot
        super().__init__()

    @lib.commands.command()
    @lib.commands.guild_only()
    @lib.commands.has_role("Admin")
    async def sync(
    self, ctx: lib.commands.Context, guilds: lib.commands.Greedy[lib.discord.Object], spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except lib.discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @lib.commands.command()
    @lib.commands.guild_only()
    async def ping(self, ctx):
        await ctx.send("Hello")

# Works like:
# !sync -> global sync
# !sync ~ -> sync current guild
# !sync * -> copies all global app commands to current guild and syncs
# !sync ^ -> clears all commands from the current guild target and syncs (removes guild commands)
# !sync id_1 id_2 -> syncs guilds with id 1 and 2

async def setup(bot):
    await bot.add_cog(Sync(bot))
    lib.logging.warning("Sync : OK")