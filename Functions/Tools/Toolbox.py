async def transformRecords(fetch):
    dict_record = {}
    for row in fetch:
        dict_record[list(dict(row).values())[0]] = {}
        for item in list(dict(row).keys())[1:len(list(dict(row).keys()))]:
            dict_record[list(dict(row).values())[0]][item] = row[item]
    return dict_record

async def transformChannels(fetch):
    dict_record = {}
    for row in fetch:
        dict_record[row["name"]] = {}
        dict_record[row["name"]] = row["channel_id"]
    return dict_record