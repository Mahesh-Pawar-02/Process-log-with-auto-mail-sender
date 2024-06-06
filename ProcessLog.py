# Automation script which accept time interval from user and create log file in that Marvellous directory which contains 
# information of all running processes. After creating the log file send that log file through mail.

import os
import time
import urllib.error
import psutil
import urllib.request
import smtplib
import schedule
from sys import *
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def is_connected():
    try:
        urllib.request.urlopen('https://www.google.co.in/',timeout = 1)
        return True
    except urllib.error as err:
        return False
    
def MailSender(filename, time):
    try:
        fromaddr = "------------------------"
        toaddr = "--------------------------"

        msg = MIMEMultipart()

        msg['From'] = fromaddr
        msg['To'] = toaddr

        body = """
    Hello..!
    Greeting from Mahesh Pawar.
    Please find the attached document which contains Log of Running Process.
    Log File is created at : %s

    This is auto generated mail.

    Thanks and Regards,

    Mahesh Pawar
    RID : PM0100047
    +91 **********
    """ %(time)

        Subject = """
        Process Log generated at : %s
        """%(time)

        msg['Subject'] = Subject
        msg.attach(MIMEText(body,'plain'))
        attachment = open(filename,"rb")
        p = MIMEBase('application','octet-stream')
        p.set_payload((attachment).read())
        encoders.encode_base64(p)
        p.add_header('Content-Disposition', "attachment; filename = %s" %filename)
        msg.attach(p)
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login(fromaddr,"qvbp xnrv pbcb pxaf")
        text = msg.as_string()
        s.sendmail(fromaddr,toaddr,text)
        s.quit()

        print("Log file successfully sent through mail...")

    except Exception as E:
        print("Unable to send mail",E)

def ProcessLog(log_dir = "Process_Logs"):
    listprocese = []

    if not os.path.exists(log_dir):
        try:
            os.mkdir(log_dir)
        except:
            pass
    
    timestamp = time.ctime()
    timestamp = timestamp.replace(" ","")
    timestamp = timestamp.replace(":","_")
    timestamp = timestamp.replace("/","_")

    separator = "_"*80
    log_path = os.path.join(log_dir, "Log%s.log" %(timestamp))
    f = open(log_path, "w")
    f.write(separator + "\n")
    f.write("Process Logger : "+time.ctime() + "\n")
    f.write(separator + "\n")
    f.write("\n")

    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
            vms = proc.memory_info().vms/(1024*1024)
            pinfo['vms'] = vms
            listprocese.append(pinfo)
        
        except(psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    for element in listprocese:
        f.write("%s\n"%element)

    print("Log File is successfully generated at location %s",(log_path))

    connected = is_connected()
 
    if connected:
        StartTime = time.time()
        MailSender(log_path,time.ctime())
        endTime = time.time()

        print("Took %s seconds to send email"%(endTime-StartTime))
    else:
        print("There is a no internet connection")

def main():
    print("--------------Created by Mahesh Pawar---------------")
    
    print("Application name is : "+argv[0])

    if(len(argv) != 2):
        print("ERROR : Invalid number of arguments")
        exit()
    
    if(argv[1] == "-h") or (argv[1] == "-H"):
        print("This script is used log record of running process")
        exit()

    if(argv[1] == "-u") or (argv[1] == "-U"):
        print("Uage : Application_Name Time_In_Minites ")
        exit()

    try:
        schedule.every(int(argv[1])).minutes.do(ProcessLog)
        while True:
            schedule.run_pending()
            time.sleep(1)

    except ValueError:
        print("ERROR : Invalid datatype of input")

    except Exception as e:
        print("ERROR : Invalid Input", e)

if __name__ == "__main__":
    main()