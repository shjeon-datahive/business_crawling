import pymysql
import random
import time
from pymysql.cursors import Cursor
import requests
from bs4 import BeautifulSoup
import pandas

already_title = []
def write_log(title, start_day, end_day, homepage):
  
  try:
    conn = pymysql.connect(host = '13.125.248.43',port=3306, user = 'datahive',password="Mobile1!", db = 'tomo', charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "insert into tomo.business values (%s, %s, %s,%s,%s)"
    curs.execute(sql, (0,title, start_day, end_day, homepage))
    conn.commit()
    conn.close()
  except pymysql.err.InternalError as e:
    print(e.args)

def update_title():
  
  try:
    conn = pymysql.connect(host = '13.125.248.43',port=3306, user = 'datahive',password="Mobile1!", db = 'tomo', charset='utf8')
    curs = conn.cursor(pymysql.cursors.DictCursor)
    sql = "select title from tomo.business"
    curs.execute(sql)
    res = curs.fetchall()
    
    for i in range(len(res)):
      already_title.append(res[i]["title"])
    
    conn.close()
  except pymysql.err.InternalError as e:
    print(e.args)
	  

update_title()
url = "https://www.bizinfo.go.kr/see/seea/selectSEEA100.do"

response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    num = (soup.select_one(".txtAgL > a")['onclick'][32:37])
    num = int(num)
    for i in range(0,1000):
      try:
        url2 = "https://www.bizinfo.go.kr/see/seea/selectSEEA140Detail.do?pblancId=PBLN_0000000000{}".format(num-i)
        
        response2 = requests.get(url2)
        if response2.status_code == 200:
          html2 = response2.text
          soup2 = BeautifulSoup(html2, 'html.parser')
          title = soup2.select_one("#pNm").getText()
          day = soup2.select(".infoTable > tbody > tr > td")[1].get_text(strip=True).replace('\t', '').replace(' ', '')
          homepage = soup2.find('a', {"title":"기본브라우저로 이동됩니다"})['href']
          start_day = day[0:10]
          end_day = day[-10:]
          if title not in already_title:
            write_log(title, start_day, end_day, homepage)
            print("전송")
            
          else:
            pass
          time.sleep(1)
      except:
        print("예외")
        # time.sleep(1)






