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

data = finddata('rawdata')
output = []
for value in data:
    output.append({'value' : value['name'],'synonyms':[value['name']]})
writeJson('objectlistdialogflow',output)