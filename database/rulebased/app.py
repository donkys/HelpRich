import json
from random import randint

def finddata(file_name:str):
    file_name += '.json'
    # getdata
    with open(file_name, 'r') as outfile:
        return json.load(outfile)

def writeJson(jsonfilename,data):
  with open(jsonfilename+'.json' , 'w') as outfile:
    json.dump(data, outfile)


query=[ 'ก','ข','ค','ฆ','ง','จ','ฉ','ช','ซ','ญ','ด','ต','ถ','ท','ธ','น',
        'บ','ป','ผ','ฝ','พ','ภ','ม','ย','ร','ล','ว','ศ','ส','ห','อ','ฮ']

for letter in query:
    a = 0
    #get data
    data = finddata(letter)
    #check number
    for i in data:
        notbad = []
        bad = []
        possible = i['good']
        arr = []
        for ad in possible:
            temp = str(ad)
            for j in temp:
                arr.append(int(j))

        number = ''
        for random in range(2):
            number = ''
            for random in range(2):
                number += str(arr[randint(0,(len(arr)-1))])

            notbad.append(int(number))
        for random in range(2):
            number = ''
            for random in range(3):
                number += str(arr[randint(0,(len(arr)-1))])

            notbad.append(int(number))
        #print(f'notbad is {notbad}')

        number = ''
        for random in range(2):
            number = ''
            for random in range(2):
                number += str(arr[randint(0,(len(arr)-1))])

            bad.append(int(number))
        for random in range(2):
            number = ''
            for random in range(3):
                number += str(arr[randint(0,(len(arr)-1))])

            bad.append(int(number))
        #print(f'bad is {bad}')

        i['notbad'] = notbad
        i['bad'] = bad
        print(i)
        
    writeJson(letter, data)
