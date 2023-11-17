from kiutils.symbol import SymbolLib, Symbol, SymbolPin

def print_footprint(PN_dict):
    pin_nr = int(max([int(k) for k in PN_dict.keys()])) # get the nr of pins
    return_string = []
    left_pins_max_length = max([len(PN_dict[str(k+1)]) for k in range(pin_nr//2)])
    right_pin_nr_length = len(str(pin_nr))
    for k in range(pin_nr//2):
        return_string.append(PN_dict[str(k+1)].upper().ljust(left_pins_max_length)+'|['+str(k+1)+']\t'+('['+str(pin_nr-k)).rjust(right_pin_nr_length+1)+']|'+PN_dict[str(pin_nr-k)].upper())

    return_string.insert(0,(' '*(left_pins_max_length))+'+'+('-'*(6+right_pin_nr_length))+'+')
    return_string.append((' '*(left_pins_max_length))+"+"+('-'*(6+right_pin_nr_length))+"+")
    for k in return_string:
        print(k)

    return '\n'.join(return_string)



file_position = "./test/74xx.kicad_sym"

symbolLib = SymbolLib().from_file(file_position)

ret_dict = {}

for k in symbolLib.symbols:
    print(k.entryName)
    print("***********")
    for j in k.units:
        print(j.entryName)
        if(j.entryName not in ret_dict.keys()):
            ret_dict[j.entryName]={}
        for i in j.pins:
            print(i.name)
            print(i.number)
            ret_dict[j.entryName][i.number]=i.name




print(ret_dict['74HC595'])

temp = (print_footprint(ret_dict['74LS298']))
f = open('text.txt','w')
f.write(temp)
f.close()