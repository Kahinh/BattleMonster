import lib

async def checkifguildslayerexist(global_slayerlist, guild_id, slayer):
    if guild_id not in global_slayerlist:
        global_slayerlist[guild_id] = {}
    if slayer.id not in global_slayerlist[guild_id]:
        global_slayerlist[guild_id][slayer.id] = lib.Classes.Slayers.Slayers(name=slayer.name)
    return global_slayerlist



async def send_messages(ctx, message, type="standard", delay=600, component={}):
    if type == "standard":
        await ctx.send(f"{message}", delete_after=delay)
    elif type == "embed":
        if component == {}:
            await ctx.send(embed=message, delete_after=delay)
        else:
            await ctx.send(embed=message, components=[component], delete_after=delay)