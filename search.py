# coding=utf-8
import requests
import codecs
import os.path
import os
from bs4 import BeautifulSoup
import sys, re, urllib

import traceback
import MailUtils
import time

url = 'http://www.ccgp-shanxi.gov.cn/view.php'

parameter = {
    u'ntype':u'fnotice',
    u'title':u'食品',
    u'type':u'全部',
    u'local':u'',
    u'number':u'',
    u'unit':u'',
    u'agency':u'',
    u'search':u'',
    u'page':u'1'
}
baseUrl = u'http://www.ccgp-shanxi.gov.cn'

#########################################
# 获得内容
########################################
def get_open_seats():
    resres = ""
    try:
        for key in [u"食品",u"食品药品监督管理局",u"慰问",u"米面油",u"粮油"]:
            parameter[u'title'] = key
            res = requests.get(url,params = parameter,timeout=10)
            while res.status_code!=200:
                print (u'retrying...重新获取网页页面')
                res = requests.get(url,params = parameter,timeout=50)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text,'html.parser')
            content = soup.find('table',id='node_list')

            try:
                contents = content.find_all('tr')[1::1]
            except Exception as e:
                        print (u'=======获取网页时候出现错误========',e)
                        continue
            for content in contents:
                title = content.find('a')['title']
                urlurl = baseUrl+"/"+content.find('a')['href']
                title_temp = title+"\r\n"

                sss = "【"+key+"】"
                sss = sss + title
                sss = sss + " " + content.find_all('td')[2].text
                sss = sss + " " + content.find_all('td')[3].text
                sss = sss + " " + content.find_all('td')[4].find("font").text
                sss = sss + " " + content.find_all('td')[5].text
                sss = sss + " " + urlurl
                
                resres = resres + sss +"\r\n"

    except Exception as e:
        print (u'=======获取网页时候出现错误========',e)
        msg = u'主程序出错，快去看看把。。。'
        MailUtils.sendmail(u"山西省政府采购网-获取网页时候出错",msg,MailUtils.getZZJ())
        return None
    else:
        return resres
    finally:
        pass

if __name__ == "__main__":
    try:
        print (u'正在查询网站。。。')
        nowRecos = get_open_seats()
        if nowRecos is None or nowRecos=="":
            print (u'没有新消息')
            print(u'we have no new message')
        else:
            print (nowRecos)
            # 格式化成2016-03-20 11:45:39形式
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            now = "招标公告-更新于 "+now
            #邮件主题和邮件内容
            if MailUtils.sendmail(now,nowRecos,MailUtils.getZZP()):
                print ("done!")
            else:
                print ("failed!")
    except Exception as e:
        print (u'主程序出错',e)
        msg = '主程序出错，快去看看把。。。'
        MailUtils.sendmail("山西省政府采购网-程序出错",msg,MailUtils.getZZJ())
        pass
    else:
        pass
