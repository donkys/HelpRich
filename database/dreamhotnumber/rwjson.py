import os
import json
json_data = ''
path = 'datareal'
  
def readJson(jsonfilename):
  with open(jsonfilename+'.json' , 'r') as f:
    json_data = json.load(f)
    return json_data

def writeJson(jsonfilename,data):
  with open(jsonfilename+'.json' , 'w') as outfile:
    json.dump(data, outfile)
