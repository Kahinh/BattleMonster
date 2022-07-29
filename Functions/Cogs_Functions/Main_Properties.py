def get_Channels(self, var_TestProd, PostgreSQL_Channels):
    Channels = {}
    for channel in PostgreSQL_Channels[var_TestProd]:
        Channels[channel] = self.bot.get_channel(int(PostgreSQL_Channels[var_TestProd][channel]))
    return Channels
