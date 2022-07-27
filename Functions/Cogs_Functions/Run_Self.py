def get_Channels(self, var_TestProd, PostgreSQL_Channels_list):
    Channels_list = {}
    for channel in PostgreSQL_Channels_list[var_TestProd]:
        Channels_list[channel] = self.bot.get_channel(int(PostgreSQL_Channels_list[var_TestProd][channel]))
    return Channels_list
