from flask import Flask, request
from linebot.models import *
from linebot import *
from database.stat import scraping
import os
import json
import requests
import datetime
#addition
from database.ocassion import moon

app = Flask(__name__)

line_bot_api = LineBotApi('GcGu9h7UBo4AH+/x91TH+S0uAoCGS2IMkqDo5QOVTL901iilBeqiqN2fkIZel+DC8TLTXkDE5k2IiCMsFpFxegUKuRmeOWoSziI0q47qdutC39i227e3mEvbhYbdwoHJywr/pBJLC/zBojlKRicgTQdB04t89/1O/w1cDnyilFU=')#Channel Access Token
handler = WebhookHandler('2b67c2ba8adc6569151cb7bd23c7848f')#Channel Secret


@app.route("/callback", methods=['POST'])
def callback():

    body =  request.get_data(as_text=True)

    req = request.get_json(silent=True, force=True)

    intent = req["queryResult"]["intent"]["displayName"]
    text = req['originalDetectIntentRequest']['payload']['data']['message']['text']
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id = req['originalDetectIntentRequest']['payload']['data']['source']['userId']
    disname = line_bot_api.get_profile(id).display_name
    session = '0'
    lottonum = '0'
    object = '0'
    date = 0
    dreamtype ='0'
    typeofstat = '0'
    
    if intent == 'ผลหวยงวดที่ต้องการinput':
        session = req["queryResult"]["outputContexts"][0]["parameters"]["date-time"]
    if intent == 'ตรวจหวย':
        session = req["queryResult"]["outputContexts"][0]["parameters"]["date-time"]
        lottonum = req["queryResult"]["outputContexts"][0]["parameters"]["number"]
    if intent == 'แสดงผลเลขเด็ดไสย' :
        object = req["queryResult"]["outputContexts"][0]["parameters"]["object"]
        date = int(req["queryResult"]["outputContexts"][0]["parameters"]["number"])
        dreamtype = req["queryResult"]["outputContexts"][0]["parameters"]["typeofdream"]
    if intent == 'แสดงผลเลขเด็ดสถิติ' :
        typeofstat = req["queryResult"]["outputContexts"][0]["parameters"]["typeofstat"]

    print(lottonum)

    print('id = ' + id)
    print('name = ' + disname)
    print('text = ' + text)
    print('intent = ' + intent)
    print('reply_token = ' + reply_token)
    print('session = '+session)
    print('object = ' + object)
    print('date = ' + str(date))
    print('dreamtype = '+dreamtype)
    print('typeofstat = '+typeofstat)

    reply(intent,text,reply_token,id,disname,session,lottonum,object,date,dreamtype,typeofstat)

    return 'OK'

@app.route('/', methods=['GET'])
def main():
    return '<h1>HELLO KUB</h>'

def reply(intent,text,reply_token,id,disname,session,lottonum,object,date,dreamtype,typeofstat):
    
    headers = {
            "X-RapidAPI-Key": "ef84c01068mshb5691d5b16962bap144153jsn57b0ab53dd0e",
	        "X-RapidAPI-Host": "thai-lottery-result.p.rapidapi.com"
        }

    if intent == 'ทดสอบ':
        text_message = TextSendMessage(text='โค้ดสามารถรันได้ปกติ\U00002B50')
        line_bot_api.reply_message(reply_token,text_message)

    if intent == 'ตรวจหวย':
        #text_message = TextSendMessage(text='เทสๆ ฮัลโหลๆ')
        #lotto = "737867%2C737866%2C349012%2C737788%2C344503%2C985003%2C123456"

        a = [int(lottonum) for lottonum in lottonum]

        counter = 0
        for item in a:
            counter+=1

        lotto = ""

        for i in range(counter):

            temp = a[i]
            if i == (counter-1):
                lotto += str(temp)
            else:
                lotto += str(temp) +"%2C"

        lottoyear = session[0]+session[1]+session[2]+session[3]
        lottomonth = session[5]+session[6]
        lottoday = session[8]+session[9]
        
        date = lottoyear+lottomonth+lottoday

        url = "https://thai-lottery-result.p.rapidapi.com/check"
        payload = "date="+date+"&lottery_number="+lotto
        headers = {
            "content-type": "application/x-www-form-urlencoded",
            "X-RapidAPI-Key": "ef84c01068mshb5691d5b16962bap144153jsn57b0ab53dd0e",
	        "X-RapidAPI-Host": "thai-lottery-result.p.rapidapi.com"
            }

        response = requests.request("POST", url, data=payload, headers=headers)
        json_data = json.loads(response.text)
        getcache(response.text)

        ans = ""
        prizename = ""
        prize = ""
        for i in range(counter):
            userlotto = json_data["payload"]["results"][i]["number"]
            iswin = json_data["payload"]["results"][i]["isWin"]

            if iswin:
                prizename = json_data["payload"]["results"][i]["result"][0]["name"]
                prize = json_data["payload"]["results"][i]["result"][0]["prizeMoney"]
                prizename = "\nถูก"+prizename+" \U00002705"
                prize = "มูลค่า "+str(format(prize, ',d'))+" บาท"
            else:
                prize = 'เสียใจด้วยคุณไม่ถูกรางวัล \U0000274C'
            temp = "\U000027A1หมายเลย {} {}\n{}\n".format(userlotto.zfill(6),prizename,prize)  
            ans += temp
            
            prizename = ''

        text_message = TextSendMessage(text='ผลสลากกินแบ่งรัฐบาลของคุณ\n{}'.format(ans[:len(ans) - 1]))
        line_bot_api.reply_message(reply_token,text_message)

    if intent == 'ผลสลากกินแบ่งงวดล่าสุด':
        #text_message = TextSendMessage(text='ทดสอบ Intent สำเร็จ')

        url = "https://thai-lottery-result.p.rapidapi.com/"
        querystring = {"page":"1"}
        responselast = requests.request("GET", url, headers=headers, params=querystring)

        json_datalast = json.loads(responselast.text)
        day = json_datalast['payload']['results'][0]['date']['day']
        month = json_datalast['payload']['results'][0]['date']['month']
        year = json_datalast['payload']['results'][0]['date']['year']
        date = "{}{}{}".format(year,str(month).zfill(2),str(day).zfill(2))

        print(date)

        url = "https://thai-lottery-result.p.rapidapi.com/results/"
        url += date

        response = requests.request("GET", url, headers=headers)
        json_data = json.loads(response.text)
        getcache(response.text)
        
        day = json_data['payload']['date']['day']
        month = json_data['payload']['date']['month']
        year = json_data['payload']['date']['year']

        firstprizenum = ''
        secondprizenum = ''
        thirdprizenum = ''
        lasttwodigitnum = ''
        lastthreedigitnum = ''
        firstthreedigitnum = ''

        firstprize_data = json_data['payload']['results']['FirstPrize']
        firstprizeprice = firstprize_data['info']['prizeMoney']
        firstprizeamount = firstprize_data['info']['amount']
        for i in range(firstprizeamount):
            firstprizenum += '\U00002796 หมายเลข: '+str(firstprize_data['numbers'][i]).zfill(6)+'\n'
        firstprize = '\U00002B50 รางวัลที่ 1 \U00002B50\nมูลค่า {} จำนวน {} รางวัล\n{}'.format(str(format(firstprizeprice, ',d')),firstprizeamount,firstprizenum)

        secondprize_data = json_data['payload']['results']['SecondPrize']
        secondprizeprice = secondprize_data['info']['prizeMoney']
        secondprizeamount = secondprize_data['info']['amount']
        for i in range(secondprizeamount):
            secondprizenum += '\U00002796 หมายเลข: '+str(secondprize_data['numbers'][i]).zfill(6)+'\n'
        secondprize = '\U00002B50 รางวัลที่ 2 \U00002B50\nมูลค่า {} จำนวน {} รางวัล\n{}'.format(str(format(secondprizeprice, ',d')),secondprizeamount,secondprizenum)

        thirdprize_data = json_data['payload']['results']['ThirdPrize']
        thirdprizeprice = thirdprize_data['info']['prizeMoney']
        thirdprizeamount = thirdprize_data['info']['amount']
        for i in range(thirdprizeamount):
            thirdprizenum += '\U00002796 หมายเลข: '+str(thirdprize_data['numbers'][i]).zfill(6)+'\n'
        thirdprize = '\U00002B50 รางวัลที่ 3 \U00002B50\nมูลค่า {} จำนวน {} รางวัล\n{}'.format(str(format(thirdprizeprice, ',d')),thirdprizeamount,thirdprizenum)

        firstthreedigit_data = json_data['payload']['results']['FirstThreeDigitsPrize']
        firstthreedigitprice = firstthreedigit_data['info']['prizeMoney']
        firstthreedigitamount = firstthreedigit_data['info']['amount']
        for i in range(firstthreedigitamount):
            firstthreedigitnum += '\U00002796 หมายเลข: '+str(firstthreedigit_data['numbers'][i]).zfill(3)+'\n'
        firstthreedigitprize = '\U00002B50 รางวัลเลข 3 ตัวหน้า \U00002B50\nมูลค่า {} จำนวน {} รางวัล\n{}'.format(str(format(firstthreedigitprice, ',d')),firstthreedigitamount,firstthreedigitnum)

        lastthreedigit_data = json_data['payload']['results']['LastThreeDigitsPrize']
        lastthreedigitprice = lastthreedigit_data['info']['prizeMoney']
        lastthreedigitamount = lastthreedigit_data['info']['amount']
        for i in range(lastthreedigitamount):
            lastthreedigitnum += '\U00002796 หมายเลข: '+str(lastthreedigit_data['numbers'][i]).zfill(3)+'\n'
        lastthreedigitprize = '\U00002B50 รางวัลเลข 3 ตัวท้าย \U00002B50\nมูลค่า {} จำนวน {} รางวัล\n{}'.format(str(format(lastthreedigitprice, ',d')),lastthreedigitamount,lastthreedigitnum)

        lasttwodigit_data = json_data['payload']['results']['LastTwoDigitsPrize']
        lasttwodigitprice = lasttwodigit_data['info']['prizeMoney']
        lasttwodigitamount = lasttwodigit_data['info']['amount']
        for i in range(lasttwodigitamount):
            lasttwodigitnum += '\U00002796 หมายเลข: '+str(lasttwodigit_data['numbers'][i]).zfill(2)+'\n'
        lasttwodigitprize = '\U00002B50 รางวัลเลข 2 ตัวท้าย \U00002B50\nมูลค่า {} จำนวน {} รางวัล\n{}'.format(str(format(lasttwodigitprice, ',d')),lasttwodigitamount,lasttwodigitnum)

        result = f'สลากกินแบ่งรัฐบาลงวดที่ {day}/{month}/{year} \n{firstprize}{firstthreedigitprize}{lastthreedigitprize}{lasttwodigitprize}{secondprize}{thirdprize}'
        text_message = TextSendMessage(text=result)
        line_bot_api.reply_message(reply_token,text_message)

    if intent == 'ผลหวยงวดที่ต้องการinput':
    #text_message = TextSendMessage(text='ทดสอบ Intent สำเร็จ')

        url = "https://thai-lottery-result.p.rapidapi.com/results/"

        custyear = session[0]+session[1]+session[2]+session[3]
        custmonth = session[5]+session[6]
        custday = session[8]+session[9]
        
        custdate = custyear+custmonth+custday

        #custdate = '20220816'
        
        url += custdate

        response = requests.request("GET", url, headers=headers)

        json_data = json.loads(response.text)
        getcache(response.text)
            
        day = json_data['payload']['date']['day']
        month = json_data['payload']['date']['month']
        year = json_data['payload']['date']['year']

        firstprizenum = ''
        secondprizenum = ''
        thirdprizenum = ''
        lasttwodigitnum = ''
        lastthreedigitnum = ''
        firstthreedigitnum = ''

        firstprize_data = json_data['payload']['results']['FirstPrize']
        firstprizeprice = firstprize_data['info']['prizeMoney']
        firstprizeamount = firstprize_data['info']['amount']
        for i in range(firstprizeamount):
            firstprizenum += '\U00002796 หมายเลข: '+str(firstprize_data['numbers'][i]).zfill(6)+'\n'
        firstprize = '\U00002B50 รางวัลที่ 1 \U00002B50\nมูลค่า {} จำนวน {} รางวัล\n{}'.format(str(format(firstprizeprice, ',d')),firstprizeamount,firstprizenum)

        secondprize_data = json_data['payload']['results']['SecondPrize']
        secondprizeprice = secondprize_data['info']['prizeMoney']
        secondprizeamount = secondprize_data['info']['amount']
        for i in range(secondprizeamount):
            secondprizenum += '\U00002796 หมายเลข: '+str(secondprize_data['numbers'][i]).zfill(6)+'\n'
        secondprize = '\U00002B50 รางวัลที่ 2 \U00002B50\nมูลค่า {} จำนวน {} รางวัล\n{}'.format(str(format(secondprizeprice, ',d')),secondprizeamount,secondprizenum)

        thirdprize_data = json_data['payload']['results']['ThirdPrize']
        thirdprizeprice = thirdprize_data['info']['prizeMoney']
        thirdprizeamount = thirdprize_data['info']['amount']
        for i in range(thirdprizeamount):
            thirdprizenum += '\U00002796 หมายเลข: '+str(thirdprize_data['numbers'][i]).zfill(6)+'\n'
        thirdprize = '\U00002B50 รางวัลที่ 3 \U00002B50\nมูลค่า {} จำนวน {} รางวัล\n{}'.format(str(format(thirdprizeprice, ',d')),thirdprizeamount,thirdprizenum)

        firstthreedigit_data = json_data['payload']['results']['FirstThreeDigitsPrize']
        firstthreedigitprice = firstthreedigit_data['info']['prizeMoney']
        firstthreedigitamount = firstthreedigit_data['info']['amount']
        for i in range(firstthreedigitamount):
            firstthreedigitnum += '\U00002796 หมายเลข: '+str(firstthreedigit_data['numbers'][i]).zfill(3)+'\n'
        firstthreedigitprize = '\U00002B50 รางวัลเลข 3 ตัวหน้า \U00002B50\nมูลค่า {} จำนวน {} รางวัล\n{}'.format(str(format(firstthreedigitprice, ',d')),firstthreedigitamount,firstthreedigitnum)

        lastthreedigit_data = json_data['payload']['results']['LastThreeDigitsPrize']
        lastthreedigitprice = lastthreedigit_data['info']['prizeMoney']
        lastthreedigitamount = lastthreedigit_data['info']['amount']
        for i in range(lastthreedigitamount):
            lastthreedigitnum += '\U00002796 หมายเลข: '+str(lastthreedigit_data['numbers'][i]).zfill(3)+'\n'
        lastthreedigitprize = '\U00002B50 รางวัลเลข 3 ตัวท้าย \U00002B50\nมูลค่า {} จำนวน {} รางวัล\n{}'.format(str(format(lastthreedigitprice, ',d')),lastthreedigitamount,lastthreedigitnum)

        lasttwodigit_data = json_data['payload']['results']['LastTwoDigitsPrize']
        lasttwodigitprice = lasttwodigit_data['info']['prizeMoney']
        lasttwodigitamount = lasttwodigit_data['info']['amount']
        for i in range(lasttwodigitamount):
            lasttwodigitnum += '\U00002796 หมายเลข: '+str(lasttwodigit_data['numbers'][i]).zfill(2)+'\n'
        lasttwodigitprize = '\U00002B50 รางวัลเลข 2 ตัวท้าย \U00002B50\nมูลค่า {} จำนวน {} รางวัล\n{}'.format(str(format(lasttwodigitprice, ',d')),lasttwodigitamount,lasttwodigitnum)

        result = f'สลากกินแบ่งรัฐบาลงวดที่ {day}/{month}/{year} \n{firstprize}{firstthreedigitprize}{lastthreedigitprize}{lasttwodigitprize}{secondprize}{thirdprize}'
        text_message = TextSendMessage(text=result)
        line_bot_api.reply_message(reply_token,text_message)
        
    if intent == 'แสดงผลเลขเด็ดสถิติ':
        data = scraping.getData(str(typeofstat))
        result = 'จากการเก็บข้อมูลตั้งแต่ปี 2533 \n\U00002B50ได้ข้อมูลเลขดังนี้\U00002B50\n'

        for i in range(len(data)):
            if i == (len(data) - 1):
                result = result + 'หมายเลข '+str(data[i]['number'])+'   เคยออกมา '+str(data[i]['sum'])+'ครั้ง'
            else:
                result = result + 'หมายเลข '+str(data[i]['number'])+'   เคยออกมา '+str(data[i]['sum'])+'ครั้ง\n'

        print(result)
        text_message = TextSendMessage(text=result)
        line_bot_api.reply_message(reply_token,text_message)

    if intent == 'แสดงผลเลขเด็ดไสย':
    #part Date
        temp = str(datetime.datetime.now())
        year = int(temp[0:4])
        month = int(temp[5:7])
        day = int(date)

        phrase = moon.moon_phase(month, day, year)

        ocassion_path = 'database/ocassion'
        ocassion_data = finddata('ocassion_data', ocassion_path)
        
        ocassion = ocassion_data[(phrase-1)]['description']
        #แสดงผล
        print(ocassion_data)
        print(ocassion)

    #part Object and Dream
        firstLetter = object[0]
        #Check สระ
        vowels = ['แ','เ','ไ','โ','ใ']
        for letter in vowels:
            if(firstLetter == letter):
                firstLetter = object[1]  
        #get data
        dreampath = 'database/rulebased'
        object_data = finddata(firstLetter, dreampath)

        #แสดงผล
        print(type(object_data))
        print(object_data)

        pos = 0
        for i in range(len(object_data)):
            if(object_data[i]['name'] == object):
                pos = i

        twodigit = ''
        threedigit = ''
        for x in object_data[pos][dreamtype]:
            if(x < 100):
                twodigit += ' '+str(x).zfill(2)
            else:
                threedigit += ' '+str(x).zfill(3)

        result = '\U0001F634 ผลลัพธ์การทำนายฝันของคุณ\n'+ocassion+'\n\U00002B50 เลขนำโชคของคุณ\nเลข 2 ตัวท้าย\n   '+twodigit+'\nเลข 3 ตัวท้าย\n   '+threedigit
        #result = 'dreamtype = '+dreamtype+'\ndate = '+str(date)+'object = '+object+'\nfirstLetter = '+firstLetter+' ocassion = '+ocassion
        text_message = TextSendMessage(text=result)
        line_bot_api.reply_message(reply_token,text_message)
        

    if intent == 'แสดงวันที่สลากกินแบ่งรัฐบาลประกาศผลล่าสุด':
        #text_message = TextSendMessage(text='ทดสอบ Intent สำเร็จ')

        url = "https://thai-lottery-result.p.rapidapi.com/latest"
        response = requests.request("GET", url, headers=headers)

        json_data = json.loads(response.text)
        getcache(response.text)

        day = json_data['payload'][0]['date']['day']
        month = json_data['payload'][0]['date']['month']
        year = json_data['payload'][0]['date']['year']

        text_message = TextSendMessage(text='สลากกินแบ่งรัฐบางวดล่าสุดคือวันที่\n \U00002B50 {}/{}/{}  \U00002B50'.format(day,str(month).zfill(2),year))
        line_bot_api.reply_message(reply_token,text_message)

    if intent == 'วันที่สลากกินแบ่งรัฐบาลประกาศผล24งวดล่าสุด':
        #text_message = TextSendMessage(text='ทดสอบ Intent สำเร็จ')

        url = "https://thai-lottery-result.p.rapidapi.com/"
        querystring = {"page":"1"}
        response = requests.request("GET", url, headers=headers, params=querystring)

        json_data = json.loads(response.text)
        getcache(response.text)

        date = ""
        for i in range(24):
            day = json_data['payload']['results'][i]['date']['day']
            month = json_data['payload']['results'][i]['date']['month']
            year = json_data['payload']['results'][i]['date']['year']
            temp = "วันที่ {:0>2d} เดือน {:0>2d} ปี {:0>4d}\n".format(day,month,year)
            date += temp

        text_message = TextSendMessage(text='สลากกินแบ่งรัฐบาล 24 งวดล่าสุด\n{}'.format(date))
        line_bot_api.reply_message(reply_token,text_message)

def getcache(jsonfile:str):
    print(jsonfile)
    #Serializing json
    json_object = json.dumps(jsonfile, indent=4)
    
    file_name = "cache-"

    a = str(datetime.datetime.now())
    for i in range (19):
        if i == 10 or i == 13 or i == 16:
            file_name += '-'
        else:    
            file_name += a[i]

    file_name += ".txt"

    path = "cache"
    # Writing to sample.json
    with open(os.path.join(path, file_name), 'w',encoding="utf8") as outfile:
        outfile.write(json_object)

def finddata(file_name:str, path:str):
    file_name += '.json'
    # getdata
    with open(os.path.join(path, file_name), 'r',encoding="utf8") as outfile:
        return json.load(outfile)

if __name__ == "__main__":
    app.run()