import sqlite3
import bs4
import requests
import json
import os
import time

data = requests.get(
    'https://www.myhora.com/หวย/สถิติหวย-ย้อนหลัง-30-ปี.aspx?mode=year-range&value=30')

#Scraping web
def setScraping():
    soup = bs4.BeautifulSoup(data.text)
    return soup

#Connect Database
conn = sqlite3.connect('database/stat/hora.db')

# fp = []
# dp0 = []
# dp1 = []
# dp2 = []
# tp0 = []
# tp1 = []
# tp2 = []
# tp3 = []

# sessions = []

def convertMonth(month):
    if month == "มกราคม":
        return "01"
        # return "January"
    elif month == "กุมภาพันธ์":
        return "02"
        # return "February"
    elif month == "มีนาคม":
        return "03"
        # return "March"
    elif month == "เมษายน":
        return "04"
        # return "April"
    elif month == "พฤษภาคม":
        return "05"
        # return "May"
    elif month == "มิถุนายน":
        return "06"
        # return "June"
    elif month == "กรกฎาคม":
        return "07"
        # return "July"
    elif month == "สิงหาคม":
        return "08"
        # return "August"
    elif month == "กันยายน":
        return "09"
        # return "September"
    elif month == "ตุลาคม":
        return "10"
        # return "October"
    elif month == "พฤศจิกายน":
        return "11"
        # return "November"
    elif month == "ธันวาคม":
        return "12"
        # return "December"

def writeTime():
  with open('database/stat/updateDB.json' , 'w') as outfile:
    data = {"time" : time.time()}
    json.dump(data, outfile)

def readTime():
  with open('database/stat/updateDB.json' , 'r') as f:
    json_data = json.load(f)
    return json_data["time"]

def allPrize(prize):
    a = {i: prize.count(i) for i in prize}
    list_allSortedPrizes = sorted(a.items(), key=lambda i: i[1], reverse=True)
    print(list_allSortedPrizes)

    return list_allSortedPrizes

def setData():
    soup = setScraping()
    for c in soup.find_all('div', {'class': 'rowx div-link'}):

        # mapping data ------------------------------------
        date = [c.find('div', {'class': 'colx'}).text.strip(),
                c.find_all('div', {'class': 'colx sx-hide'})[0].text.strip(),
                c.find_all('div', {'class': 'colx sx-hide'})[1].text.strip()]
        
        firstPrize = c.find('div', {'class': 'colx row-hld'}).text
        underPrize = c.find_all('div', {'class': 'colx row-hld sx-hide'})[0:3]
        threePrize = c.find_all(
            'div', {'class': 'colx row-hld sx-hide'})[3].text.strip().split(" ")

        # print test -------------------------------------
        # print(date, end = " ")
        # print(c.find('div',{'class' : 'colx' }).text,end = " ")
        # print(c.find_all('div',{'class' : 'colx sx-hide' })[0].text,end = " ")
        # print(c.find_all('div',{'class' : 'colx sx-hide' })[1].text,end = "\n")

        #clean string -------------------------------------
        firstPrize = firstPrize.strip()
        underPrize[0] = underPrize[0].text.strip()
        underPrize[1] = underPrize[1].text.strip()
        underPrize[2] = underPrize[2].text.strip()

        #add to DATABASE
        params = (date[0], convertMonth(date[1]), date[2], firstPrize, underPrize[0], underPrize[2], underPrize[1], 
            threePrize[0], threePrize[1], threePrize[2], threePrize[3])  
        conn.execute("INSERT INTO PRIZETHIRTY VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", params)

        #add to Session -------------------------------------
        # session = {'date': date, 'firstPrize': firstPrize,
        #         'underPrize': underPrize, 'threePrize': threePrize}
        # sessions.append(session)

        #add to each Column -------------------------------------
        # fp.append(firstPrize)
        # dp0.append(underPrize[0])
        # dp1.append(underPrize[1])
        # dp2.append(underPrize[2])
        # tp0.append(threePrize[0])
        # tp1.append(threePrize[1])
        # tp2.append(threePrize[2])
        # tp3.append(threePrize[3])

    # commit Database -------------------------------------
    conn.commit()
    writeTime()
    print("เพิ่มระเบียงข้อมูลสำเร็จ")


def sqlQuery2Session(sec, month, year, top, column):
    if (sec == 1):
        sqlQuery = ' SELECT ' + column + ', COUNT(' + column + ') AS SUM from "PRIZETHIRTY" \
            WHERE (DAY = "29" OR DAY = "1" OR DAY = "31" OR DAY = "30" OR DAY = "2") \
                AND (MONTH = '+ str(month) +') AND (CAST("YEAR" AS INTEGER) >= '+ str(year) +') \
            GROUP BY "' + column + '" \
            HAVING COUNT("' + column + '") > 1 \
            order by COUNT("' + column + '") DESC \
            LIMIT '+ str(top) +';'
        return sqlQuery
    elif (sec == 2):
        sqlQuery = ' SELECT ' + column + ', COUNT(' + column + ') AS SUM from "PRIZETHIRTY" \
            WHERE (DAY = "13" OR DAY = "14" OR DAY = "15" OR DAY = "16" OR DAY = "17") \
                AND (MONTH = '+ str(month) +') AND (CAST("YEAR" AS INTEGER) >= '+ str(year) +') \
            GROUP BY "' + column + '" \
            HAVING COUNT("' + column + '") > 1 \
            order by COUNT("' + column + '") DESC \
            LIMIT '+ str(top) +';'
        return sqlQuery
    return ''

def sqlQueryMonth(month, year, top, column):
    sqlQuery = ' SELECT ' + column + ', COUNT(' + column + ') AS SUM from "PRIZETHIRTY" \
        WHERE (DAY = "13" OR DAY = "14" OR DAY = "15" OR DAY = "16" OR DAY = "17") \
            AND (MONTH = '+ str(month) +') AND (CAST("YEAR" AS INTEGER) >= '+ str(year) +') \
        GROUP BY "' + column + '" \
        HAVING COUNT("' + column + '") > 1 \
        order by COUNT("' + column + '") DESC \
        LIMIT '+ str(top) +';'
    return sqlQuery

def sqlQueryAll(top, column):
    sqlQuery = ' SELECT ' + column + ', COUNT(' + column + ') AS SUM from "PRIZETHIRTY" \
        GROUP BY "' + column + '" \
        HAVING COUNT("' + column + '") > 1 \
        order by COUNT("' + column + '") DESC \
        LIMIT '+ str(top) +';'
    return sqlQuery

def addDatabase():
    t = time.time()
    if(t - readTime() > (3600.0 * 24)):
        print("update Time")
        conn.execute("DELETE FROM PRIZETHIRTY")
        conn.commit()
        setData()

def getData(column:str):
    addDatabase()
    #sql = sqlQuery2Session(1, 10, 2540, 10, "TWOUP")
    #sql = sqlQueryMonth(10, 2540, 10, "TWOUP")
    
    sql = sqlQueryAll(5, column)
    
    cursor = conn.execute(sql)
    str = []

    for row in cursor:
        str.append({"number" : row[0], "sum" : row[1]})
    #conn.close()
    return str

#print(getData('TWOUP'))

#Close connection database.







