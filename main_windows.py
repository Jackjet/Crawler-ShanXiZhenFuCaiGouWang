# coding=utf-8
import requests
import codecs
import os.path
import os
from bs4 import BeautifulSoup
from twilio.rest import Client
import sys, re, urllib  
import smtplib  
import traceback  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart  

url = 'http://www.ccgp-shanxi.gov.cn/view.php'

parameter = {
    "app":"",
    "type":"",
    "nav":100,
    "page":1
}
baseUrl = 'http://www.ccgp-shanxi.gov.cn'
basedir = u'F:\\PythonDev\\codes\\SCALWER\\SXZFCGW\\'
#############################################
#得到上一次访问的新闻
#
#
##############################################
def getLastReco():
    f = codecs.open(basedir+u'lastReco.txt','r+','utf-8')
    recos = f.readlines()
    f.close()
    return recos

#########################################
# 获得内容
#
#
########################################
def get_open_seats():
    lastRecos = getLastReco()
    f = codecs.open(basedir+u'lastReco.txt','w','utf-8')
    #是否向文件中写入了新的内容
    flag=False
    resres = ""
    page = 1
    try:
        while(page<=6):
            parameter['page'] = page
            res = requests.get(url,params = parameter,timeout=10)
            while res.status_code!=200:
                print ('retrying...重新获取网页页面')
                #print('indexing..........')
                res = requests.get(url,params = parameter,timeout=50)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text,'html.parser')
            content = soup.find('table',id='node_list')
            try:
                contents = content.find('tbody').find_all('tr')
            except Exception as e:
                        print ('=======获取网页时候出现错误========',e)
                        #print('searching...................')
                        continue
            for content in contents:
                title = content.find_all('td')[0].find('a')['title']
                title_temp = title+"\r\n"
                #如果是新的招标公告
                if(title_temp not in lastRecos):
                    f.write(title+"\r\n")
                    flag=True
                #如果是旧的招标公告，说明下面的公告都是旧的，没有必要再往下了
                #其实可以改成break，但是为了鲁棒性，这里
                else:
                    pass
                
                #print title,type(title),title.find(u'农业')
                #if ((title.find(u'农业')!=-1 or title.find(u'食品')!=-1 or title.find(u'畜牧')!=-1 or title.find(u'质量')!=-1 or title.find(u'农产品')!=-1)and (not(title_temp in lastRecos))):
                
                
                sss = ""
                sss = sss + title
                sss = sss + " " + content.find_all('td')[1].text
                sss = sss + " " + content.find_all('td')[2].text
                sss = sss + " " + content.find_all('td')[3].text
                sss = sss + " " + baseUrl+"/"+content.find_all('td')[0].find('a')['href']
                resres = resres + sss +"\r\n"
            page = page + 1
        if not flag:
            f.writelines(lastRecos)
    except Exception as e:
        print ('=======获取网页时候出现错误========',e)
        #sendMessage("+8618835109707",'获取网页时候出错，快去看看把。。。')
        return None
    else:
        return resres
    finally:
        f.close()

#发件箱
fromaddr = "inscrypt2018@163.com"
#fromaddr = "zjzhang_2@stu.xidian.edu.cn"
smtpaddr = "smtp.163.com"  
#,"106941849@qq.com"
toaddrs = ["106941849@qq.com"]
#奇迹：给自己抄送一份就不会被认为是垃圾邮件了
ccaddrs = ["inscrypt2018@163.com"]
#subject = "测试邮件"
#授权码
password = "633211wo"
#password = "zhang1968311"

#
# subject:主题
# msg：消息主体
# 
#
def sendmail(subject,msg,toaddrs,fromaddr,smtpaddr,password):  
    ''''' 
    @subject:邮件主题 
    @msg:邮件内容 
    @toaddrs:收信人的邮箱地址 
    @fromaddr:发信人的邮箱地址 
    @smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com 
    @password:发信人的邮箱密码 
    '''  
    mail_msg = MIMEMultipart()  
    mail_msg['Subject'] = subject  
    mail_msg['From'] =fromaddr  
    mail_msg['To'] = ','.join(toaddrs)
    mail_msg['Cc'] = ', '.join(ccaddrs)
    mail_msg.attach(MIMEText(msg, 'plain', 'utf-8'))  
    try:  
        s = smtplib.SMTP()  
        s.connect(smtpaddr)  #连接smtp服务器  
        s.login(fromaddr,password)  #登录邮箱  
        s.sendmail(fromaddr, toaddrs+ccaddrs, mail_msg.as_string()) #发送邮件  
        s.quit()
    except Exception as e:  
        print ("Error: unable to send email")
        print (traceback.format_exc())
        return False
    else:
        return True
        
import time
if __name__ == "__main__":
    try:
        print (u'正在查询网站。。。')

        nowRecos = get_open_seats()
        print (nowRecos)
        if nowRecos is None or nowRecos=="":
            print (u'没有新消息')
            print(u'we have no new message')
        else:
            print (nowRecos)
            # 格式化成2016-03-20 11:45:39形式
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
            now = "招标公告-更新于 "+now
            if sendmail(now,nowRecos.replace("\r\n","</br>"),toaddrs,fromaddr,smtpaddr,password):  #邮件主题和邮件内容  
            #这是最好写点中文，如果随便写，可能会被网易当做垃圾邮件退信  
                print ("done!")
            else:
                print ("failed!") 
        #name = raw_input()
    except Exception as e:
        print (u'主程序出错',e)
        msg = '主程序出错，快去看看把。。。'
        sendmail("山西省政府采购网-程序出错",msg,toaddrs,fromaddr,smtpaddr,password)
        #sendMessage("+8618835109707",'主程序出错，快去看看把。。。')
        pass
    else:
        pass
