# coding=utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

#发件箱
fromaddr = "inscrypt2018@163.com"
smtpaddr = "smtp.163.com"
#目标邮箱 张中平"106941849@qq.com"
toaddrs = ["106941849@qq.com"]
#报错邮箱 "18835109707@163.com"
toaddrs2 = ["18835109707@163.com"]
#奇迹：给自己抄送一份就不会被认为是垃圾邮件了
ccaddrs = ["inscrypt2018@163.com"]
#subject = "测试邮件"
#授权码
password = "633211wo"
#password = "zhang1968311"

#########################
# subject: 主题，string
# msg：消息主体，string。 1. 如果接收者是163邮箱，则\r\n为换行符 2. 如果是QQ网页邮箱，则<br>是换行符 3.如果是QQ手机邮箱，则\r\n为换行符
# toaddrs: 目标邮箱，list of string
##########################
def sendmail(subject,msg,toaddrs):
    '''''
    @subject:邮件主题
    @msg:邮件内容
    @toaddrs:收信人的邮箱地址
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
        print ("发送成功")
        return True

###########################
# 获得张中平的邮箱
##########################
def getZZP():
    return ["106941849@qq.com"]
        
###########################
# 获得鹏英哥的邮箱
##########################
def getPYG():
    return ["1126779451@qq.com"]
    
###########################
# 获得张中俊的邮箱
##########################
def getZZJ():
    return ["18835109707@163.com","1014830422@qq.com"]
    
if __name__=="__main__":
    subject = "主题-测试邮件"
    msg = "这里是测试内容\r\n这里是第二行\r\n这里是第三行"
    toaddrs = ["18835109707@163.com"]
    sendmail(subject,msg,toaddrs)
    
