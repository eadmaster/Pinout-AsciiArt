from kiutils.symbol import SymbolLib, Symbol


file_position = "./test/74xx.kicad_mod"

symbolLib = SymbolLib().from_file(file_position)

for k in symbolLib:
    print(k.entryName)

