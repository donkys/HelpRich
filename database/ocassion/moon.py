def moon_phase(month, day, year):
    temp = 0
    ages = [18, 0, 11, 22, 3, 14, 25, 6, 17, 28, 9, 20, 1, 12, 23, 4, 15, 26, 7]
    offsets = [-1, 1, 0, 1, 2, 3, 4, 5, 7, 7, 9, 9]

    if day == 31:
        day = 1
    days_into_phase = ((ages[(year + 1) % 19] +
                        ((day + offsets[month-1]) % 30) +
                        (year < 1900)) % 30)
    index = int((days_into_phase + 2) * 16/59.0)
    #print(index)  # test
    if index > 7:
        index = 7

    # light should be 100% 15 days into phase
    light = int(2 * days_into_phase * 100/29)
    if light > 100:
        light = abs(light - 200);

    phrase = [  6,13,20,27,34,41,48,55,62,68,75,82,89,96,97,
               90,83,76,69,63,56,49,42,35,28,21,14, 7, 0, 0]

    for i in range(len(phrase)):
        if(phrase[i] != 0):
            if(light == phrase[i]):
                temp = i+1
                break
        else:
            if(index == 7):
                temp = 29
                break
            elif(index == 0):
                temp = 30
                break
        
    return temp


# put in a date you want ...
# 26jan2009 is the start of the Chinese New Year for 2009
# the moon is at its lowest intensity
'''
    if(temp <= 15):
        status = 'ขึ้น '+str(temp)+' ค่ำ'
    else:
        temp -= 15
        if(temp == 16):
            temp = 1
        status = 'แรม '+str(temp)+' ค่ำ'
'''
'''
month = 11
year = 2022  # use yyyy format
day = 12

temp = moon_phase(month, day, year)
print(f"วันที่ {temp} มีแสง {temp} เป็นวัน {temp}")'''
    #print("moon phase on %s is %s, light = %d%s" % (date, status, light, '%'))
