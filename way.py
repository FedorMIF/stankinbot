oldcaf = ["357a", "357b", "357c", "357f", "357g"]

per = ["224a", "226", "227", "228", "229", "230", "231", "232"]

oldau = ["510", "509", "508", "511", "506", "507", "505", "504", "503", "502", "501",
       "447", "448", "446", "445", "443", "444", "445", "441", "440", "439", "449", "450", "450a", "450b", "450c",
       "327", "322", "323", "324", "325", "326", "333", "332", "331", "320", "328","exit", "entry",
       "233", "225", "224", "223", "235", "234", "236", "237", "238", "239", "221", "220", "219", "218"]

newaud = ["0102", "0102a", "0103", "0105", "0106",
          "0201", "0202", "0203", "0204", "0206", "0207", "0208", "0209", "0210", "0211",
          "0303", "0304", "0305", "0306", "0307", "0308", "0309", "0310", "0311", "0312a",
          "0402", "0403", "0404", "0405", "0406", "0407", "0408", "0409", "0410", "0411",
          "0505", "0506", "0507", "0508", "0511", "0510", "0513", "0514", "0515", "0516", "0517",
          "0603", "0604", "0610", "0606", "0607", "0608", "0609", "0611", "0612", "0613", "0614",
          "0615", "0617", "0618", "0619", "0620", "0621", "0622", "0623", "0732",
          "0801", "0802", "0803", "0804", "0806", "0807", "0809", "0810", "0811", "0812",
          "0903", "0904", "0905", "0906", "0907", "0908", "0909", "0910", "0911", "0913", "0918",
          "0919", "0921", "0922", "0923", "0924", "kafe", "rektor", "exitnew", "entrynew"]

oldoldaud = ["201", "202", "203", "204", "205", "206", "207", "208", "209", "210", "211", "212",
             "213", "214", "215", "216", "217", "240a", "240b", "240c", "240d", "240e", "240f", "240g",
             "241", "242", "243", "244", "246", "247", "249", "249b", "249c", "250", "251", "254", "255", "256", "257",
             "301", "302", "303", "304", "305", "306", "306a", "307", "308", "309", "310",
             "311", "312", "313", "314", "314a", "339", "340", "341", "342", "343", "346", "349",
             "419", "417", "416", "415", "414", "413", "412", "411", "409", "408", "406", "405", "404", "403", "401"]

def pars_level(num):
    if num[0] == '0':
        return int(num[1])
    else:
        return int(num[0])

def pars_build(num):
    if num in oldcaf or num in per or num in oldau or num in newaud or num in oldoldaud:
        return True


def this_is_the_way(nums):
    level_st = pars_level(nums[0])
    level_end = pars_level(nums[1])
    way = []
    way.append(f'au{nums[0]}') #start
    if nums[0] in oldau or nums[0] in oldcaf:
        if nums [0] in oldcaf:
            if nums[1] in oldcaf:
                way.append(f'au{nums[1]}') #end
                return(way)
            else:
                way.append('oldcaftoold')
        
        if nums[1] in oldau:
            if level_st == level_end or (nums[0] in oldcaf and level_end == 2):
                way.append(f'au{nums[1]}') #end
                return(way)
            else:
                way.append(f'upstairs{level_st}old')
                way.append(f'downstairs{level_end}old')
                way.append(f'au{nums[1]}') #end
                return(way)
        
        elif nums[1] in oldoldaud:
            if level_st != 2: # если этаж не на этаже с переходом, то добавляем пункты со спуском/подьемом до 2ого жтажа
                way.append(f'upstairs{level_st}oldold')
                way.append('downstairs2old')

            way.append('oldtooldold')
            way.append('oldtooldoldhere') # переход из старого в совсем старый
            
            if level_end == 2:
                way.append(f'au{nums[1]}') # если конечный этаж на том же таже что и переход
                return(way)
            else:
                way.append(f'upstairs{level_st}oldold')
                way.append(f'downstairs{level_end}oldold')
                way.append(f'au{nums[1]}') #end
                return(way)
        
        elif nums[1] in per or nums[1] in newaud:
            if level_st != 2: # если этаж не на этаже с переходом, то добавляем пункты со спуском/подьемом до 1ого жтажа
                way.append(f'upstairs{level_st}old')
                way.append(f'upstairs1old')
               
            way.append('oldtopereh')
            way.append('oldtoperehhere')
            
            if nums[1] in per:
                way.append(f'au{nums[1]}')
                return(way)
            else:
                way.append('perehtonew')
                way.append('perehtonewhere')
                
                if level_end == 2:
                    way.append(f'au{nums[1]}')
                    return(way)
                else:
                    way.append('upstairs2new')
                    way.append(f'downstairs{level_end}new')
                    way.append(f'au{nums[1]}')
                    return(way)
    
    elif nums[0] in oldoldaud:
        if nums[1] in oldoldaud:
            if level_end == level_st:
                way.append(f'au{nums[1]}') #end
                return(way)
            else:
                way.append(f'upstairs{level_st}oldold')
                way.append(f'downstairs{level_end}oldold')
                way.append(f'au{nums[1]}') #end
                return(way)
        
        elif nums[1] in oldau or nums[1] in oldcaf:
            if level_st != 2: # если этаж не на этаже с переходом, то добавляем пункты со спуском/подьемом до 2ого жтажа
                way.append(f'upstairs{level_st}oldoldold')
                way.append('downstairs2oldold')

            way.append('oldoldtoold')
            way.append('oldoldtooldhere') # переход из совсем старого в старый

            if nums[1] in oldcaf:
                way.append(f'upstairs2old')
                way.append('oldtooldcafhere')
                way.append(f'au{nums[1]}') #end
                return(way)
            
            else:
                if level_end == 2:
                    way.append(f'au{nums[1]}') # если конечный этаж на том же таже что и переход
                    return(way)
                else:
                    way.append(f'upstairs{level_st}old')
                    way.append(f'downstairs{level_end}old')
                    way.append(f'au{nums[1]}') #end
                    return(way)

        elif nums[1] in per or nums[1] in newaud:
            if level_st != 2: # если этаж не на этаже с переходом, то добавляем пункты со спуском/подьемом до 2ого жтажа
                way.append(f'upstairs{level_st}oldold')
                way.append(f'downstairs2oldold')

            way.append('oldoldtoold')
            way.append('oldoldtooldhere') # переход из совсем старого в старый

            way.append('upstairs2old')
            way.append('upstairs1old')
               
            way.append('oldtopereh')
            way.append('oldtoperehhere')

            if nums[1] in per:
                way.append(f'au{nums[1]}')
                return(way)
            else:
                way.append('perehtonew')
                way.append('perehtonewhere')
                
                if level_end == 2:
                    way.append(f'au{nums[1]}')
                    return(way)
                else:
                    way.append('upstairs2new')
                    way.append(f'downstairs{level_end}new')
                    way.append(f'au{nums[1]}')
                    return(way)
    
    elif nums[0] in newaud or nums[0] in per:
        if nums[1] in newaud and nums[0] not in per:
            if level_end == level_st:
                way.append(f'au{nums[1]}') #end
                return(way)
            else:
                way.append(f'upstairs{level_st}new')
                way.append(f'downstairs{level_end}new')
                way.append(f'au{nums[1]}') #end
                return(way)
        elif nums[1] in oldau or nums[1] in oldcaf or nums[1] in oldoldaud or nums[1] in per:
            if level_st != 2:
                way.append(f'upstairs{level_st}new')
                way.append('downstairs2new')

            if nums[0] not in per:
                way.append('newtopereh')
                way.append('newtoperehhere')

            if nums[1] in per:
                way.append(f'au{nums[1]}')
                return(way)

            way.append('perehtoold')

            if level_end != 1:
                way.append('downstairs1old')
                way.append('downstairs2old')
            else:
                way.append(f'au{nums[1]}')
                return(way)

            if nums[1] in oldoldaud:
                way.append('oldtooldold')
                way.append('oldtooldoldhere') # переход из совсем старого в старый
            
            if level_end == 2:
                way.append(f'au{nums[1]}')
                return(way)
            
            if nums[1] in oldau:
                way.append(f'upstairs{level_st}old')
                way.append(f'downstairs{level_end}old')
                way.append(f'au{nums[1]}') #end
                return(way)
            elif nums[1] in oldoldaud:
                way.append(f'upstairs{level_st}oldold')
                way.append(f'downstairs{level_end}oldold')
                way.append(f'au{nums[1]}') #end
                return(way)
            elif nums[1] in oldcaf:
                way.append(f'upstairs2old')
                way.append('oldtooldcafhere')
                way.append(f'au{nums[1]}') #end
                return(way)

    way.append('au0102')
    return(way)
                