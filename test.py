import lib

Slayers_list = {
    121 : lib.Classes.Slayers.Slayers(name = "Kahinh"),
    122 : lib.Classes.Slayers.Slayers(name = "Kahinh"),
    123 : lib.Classes.Slayers.Slayers(name = "Kahinh"),
    124 : lib.Classes.Slayers.Slayers(name = "Kahinh"),
    125 : lib.Classes.Slayers.Slayers(name = "Kahinh"),
    126 : lib.Classes.Slayers.Slayers(name = "Kahinh"),
    127 : lib.Classes.Slayers.Slayers(name = "Kahinh"),
}

#lib.PostgreSQL_Tools.updateSlayers(Slayers_list, "Slayers")
lib.PostgreSQL_Tools.updateTables(Slayers_list)