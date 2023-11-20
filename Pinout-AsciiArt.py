from kiutils.symbol import SymbolLib, Symbol, SymbolPin

def print_footprint(PN_dict):
    pin_nr = int(max([int(k) for k in PN_dict["pins"].keys()])) # get the nr of pins
    return_string = []
    left_pins_max_length = max([len(PN_dict["pins"][str(k+1)]) for k in range(pin_nr//2)])
    left_pin_nr_length = len(str(pin_nr//2))
    right_pin_nr_length = len(str(pin_nr))
    for k in range(pin_nr//2):
        return_string.append(PN_dict["pins"][str(k+1)].upper().rjust(left_pins_max_length)+' |['+(str(k+1)+']').rjust(left_pin_nr_length+1)+'   '+'['+(str(pin_nr-k)).rjust(right_pin_nr_length)+']| '+PN_dict["pins"][str(pin_nr-k)].upper())

    return_string.insert(0,(' '*(left_pins_max_length))+' +'+('-'*(7+right_pin_nr_length+left_pin_nr_length))+'+')
    return_string.append((' '*(left_pins_max_length))+" +"+('-'*(7+right_pin_nr_length+left_pin_nr_length))+"+")
    
    for k in return_string:
        print(k)

    return '\n'.join(return_string)

def get_PN_text(ret_dict,PN):
    footprint = (print_footprint(ret_dict[PN]))
    #temp = '#'+PN+'\n' + ('='*len(PN))+'\n\n'
    temp = "*Description*: "+ret_dict[PN]["description"]+'\n\n'
    temp += "*Datasheet*: "+ret_dict[PN]["datasheet"]+'\n\n'
    temp += "*Pinout*: "+'\n'+'\n\n```\n'+footprint+'\n```\n'
    return temp


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
            ret_dict[j.entryName]["pins"]={}
            ret_dict[j.entryName]["name"]=k.entryName
            ret_dict[j.entryName]["description"]=""
            ret_dict[j.entryName]["datasheet"]=""
            for l in k.properties:
                if(l.key == "Datasheet"):
                    ret_dict[j.entryName]["datasheet"]=l.value
                if(l.key == "ki_description"):
                    ret_dict[j.entryName]["description"]=l.value
            
        # Finding the pin number
        if(len(j.pins)>0):
            print([int(pnr.number) for pnr in j.pins])        
            pin_nr = max([int(pnr.number) for pnr in j.pins])
        #if(pin_nr % 2 != 0):
        #    pin_nr= pin_nr+1 # meaning the last pin is NC, it only holds with DIP or SOP packages

        for i in j.pins:
            ret_dict[j.entryName]["pins"][i.number]=i.name

        for i in range(1,pin_nr):
            if(str(i) not in ret_dict[j.entryName]["pins"].keys()):
                ret_dict[j.entryName]["pins"][str(i)]="NC"



# WRITE Files

for pn in ret_dict.keys():
    try:
        print(pn)
        temp = get_PN_text(ret_dict,pn)
        f = open('./PNs/'+pn+'.md','w')
        f.write(temp)
        f.close()
    except(KeyError):
        print("Error in the keys of "+pn)

print(ret_dict["74LS92"])
temp = get_PN_text(ret_dict,"74LS92")