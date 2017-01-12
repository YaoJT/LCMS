# -*- coding: cp936 -*-
import numpy as np
import pandas as pd
import requests
import lxml.etree as etree
import time

out_file = open('arable_NCP_new.csv','w+')
out_file.write('{0},{1},{2},{3},{4},{5},{6}\n'.format('record_num','name','href','resource','publish_time','database','record_time'))

cookies = {"IsAutoLogin":False,"UserName":"CAU","ShowName":"%e4%b8%ad%e5%9b%bd%e5%86%9c%e4%b8%9a%e5%a4%a7%e5%ad%a6","UserType":"bk","r":"UTq0ym"}
url = 'http://epub.cnki.net/kns/brief/brief.aspx?curpage=1&RecordsPerPage=50&QueryID=8&ID=&turnpage=1&tpagemode=L&dbPrefix=SCDB&Fields=&DisplayMode=listmode&PageName=ASP.brief_result_aspx#J_ORDER'
start_page = 1
page_num = 38
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection':'keep-alive',
    'Cookie':'kc_cnki_net_uid=7b015f31-9729-8b1b-5cff-1ce40e78bba0; __unam=48ae63-1574a5bb02c-6489e978-2; Ecp_ClientId=4160620165709170038; ASP.NET_SessionId=4dnm1lencizuzjr2l4y0w1i1; RsPerPage=50; ASPSESSIONIDASDTQRAQ=KDIDCPBCPICGBCMLCFOJKOPB; ASPSESSIONIDQCARRBSR=IHKNCPBCFFBCHECDGLIFGKHO; LID=WEEvREcwSlJHSldRa1Fhb09jMjQwK0pZbDBTZVhSeWRHcGhsK2pNaVoraz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4ggI8Fm4gTkoUKaID8j8gFw!!; c_m_LinID=LinID=WEEvREcwSlJHSldRa1Fhb09jMjQwK0pZbDBTZVhSeWRHcGhsK2pNaVoraz0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4ggI8Fm4gTkoUKaID8j8gFw!!&ot=01/10/2017 21:07:32; c_m_expire=2017-01-10 21:07:32; Ecp_LoginStuts={"IsAutoLogin":false,"UserName":"CAU","ShowName":"%e4%b8%ad%e5%9b%bd%e5%86%9c%e4%b8%9a%e5%a4%a7%e5%ad%a6","UserType":"bk","r":"UTq0ym"}',
    'Host':'epub.cnki.net',
    'Upgrade-Insecure-Requests':1,
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'    
    }
session = requests.session()
record_num = 1
for page in range(start_page,page_num+1):
    url_page = url.replace('curpage='+str(start_page),'curpage='+str(page))
    print url_page
    while True:
        response = session.get(url_page,headers = headers)
        aa = etree.HTML(response.text)
        aa = aa.xpath('//table[@class="GridTableContent"]//tr')
        if len(aa)>1:
            for num in range(1,len(aa)):
                print 'page:{0} num:{1}'.format(page,num)
                try:
                    resource = aa[num][3][0].text.replace('\r','').replace('\n','').replace(' ','')
                except:
                    resource = aa[num][3].text.replace('\r','').replace('\n','').replace(' ','')
                text_list = [str(record_num),
                             aa[num][1][0][0].text.replace("document.write(ReplaceChar1(ReplaceChar(ReplaceJiankuohao(",
                                                           '').replace("</font>",'').replace('))))','').replace("<font class=Mark>",'').replace(',',''),
                             aa[num][1][0].values()[1],resource,
                             aa[num][4].text.replace('\r','').replace('\n','').replace(' ','').replace(',',''),
                             aa[num][5].text.replace('\r','').replace('\n','').replace(' ','').replace(',',''),
                             time.ctime()]
                text = ''
                for t in text_list:
                    text += t+','
                text += '\n'
                out_file.write(text.encode('utf-8'))
                print text
                record_num += 1
##            time.sleep(5)
            break        
        else:
            ff = raw_input('press anykey to continue: ')
            print 'continue'
            
    
out_file.close()
            
            
        

    
