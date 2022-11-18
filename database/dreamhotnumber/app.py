from rwjson import *
import json

query=[ 'ก','ข','ค','ฆ','ง','จ','ฉ','ช','ซ','ญ','ด','ต','ถ','ท','ธ','น',
        'บ','ป','ผ','ฝ','พ','ภ','ม','ย','ร','ล','ว','ศ','ส','ห','อ','ฮ']

data = readJson('data')

for letterquery in query:
    output = []
    for name in data:
        firstLetter = name['name'][0]
        vowels = ['แ','เ','ไ','โ','ใ']
        for letter in vowels:
            if(firstLetter == letter):
                firstLetter = name['name'][1]

        if(firstLetter == letterquery):
            output.append(name)
            writeJson(firstLetter,output)
