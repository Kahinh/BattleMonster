import lib
from zoneinfo import ZoneInfo

class Loop_time(lib.commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.generate_timed_tasks()

    async def timed_task(self):  # function that will loop, note: no decorator
        gamemode_name = self.bot.Gamemodes_spawn_time[lib.datetime.time(hour=lib.datetime.datetime.now().hour, minute=lib.datetime.datetime.now().minute, tzinfo=ZoneInfo('Europe/Paris'))]
        gamemodedata = self.bot.Gamemodes[gamemode_name]
        gamemode = await lib.Gamemode.get_Gamemode_Class(self.bot, gamemodedata)
        if gamemode.isReady() : await gamemode.handler_Spawn()

    def before_timed_task(self):
        async def wrapper():
            await self.bot.wait_until_ready()
        return wrapper

    def task_generator(self):
        task = lib.tasks.loop(time=list(self.bot.Gamemodes_spawn_time.keys()))(self.timed_task)
        task.before_loop(self.before_timed_task())
        task.start()  # pass the guild/channel ID here
        return task
    
    def generate_timed_tasks(self):
        self.task_generator()

async def setup(bot):
    await bot.add_cog(Loop_time(bot))
    lib.logging.warning("Loop_time : OK")