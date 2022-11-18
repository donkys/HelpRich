import os
import json


json_data = ''

path = ''
  
def readJson(jsonfilename):
  with open(os.path.join(path,jsonfilename)+'.json' , 'r') as f:
    json_data = json.load(f)
    return json_data

def writeJson(jsonfilename,data):
  with open(os.path.join(path,jsonfilename)+'.json' , 'w') as outfile:
    json.dump(data, outfile)
