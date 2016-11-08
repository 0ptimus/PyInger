#!/usr/bin/env python

##############################################################################
# PyInger: A simple Python script to ping hosts and send email
# notifications to people if something is down.
# 
# Author: Chris Dea
# Email: optimus@gmail.com
#
# License: MIT License
#
# Example Cron entry to run script every 30 minutes:
# */30 * * * * /home/user/pythonscripts/pyinger/pyinger.py >/dev/null 2>&1
#
##############################################################################

import smtplib
import email
from email.MIMEText import MIMEText
import logging
import datetime

log = logging.getLogger('pyinger')
### Update path below to the directory where you put pyinger.py ###
loghandler = logging.FileHandler('/home/user/pythonscripts/pyinger/pyinger.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
loghandler.setFormatter(formatter)
log.addHandler(loghandler) 
log.setLevel(logging.INFO)
### Add hosts that you want to ping here ###
hosts = ['host1.domain.com', 'host2.domain.com']

def ping(host):
    """
    Returns True if host responds to a ping request
    """
    import os, platform

    # Ping parameters as function of OS
    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"

    # Ping
    return os.system("ping " + ping_str + " " + host) == 0


def sendemail():
    smtp_host = 'smtp.yourdomain.com'
    smtp_port = 25
    emailuser = 'someuser'
    emailpass = 'somepassword'
    server = smtplib.SMTP()
    server.connect(smtp_host,smtp_port)
    server.ehlo()
    server.starttls()
### Uncommment line below if your SMTP server requires authentication ###
#    server.login(emailuser,emailpass)
### Change this to whatever you want your your from address to be
    fromaddr = 'pyinger@yourdomain.com'
### Add recipients to receive notifications when hosts do not respond to ping ###
    tolist = ['someone@randomdomain.com', 'someoneelse@randomdomain.com']
    sub = host + ' is down!'

    msg = email.MIMEMultipart.MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = email.Utils.COMMASPACE.join(tolist)
    msg['Subject'] = sub
    messagebody = 'The following host did not respond to ping and appears to be down:\n%s' % host
    msg.attach(MIMEText('The following host did not respond to ping and appears to be down:\n' + host, 'plain'))
    msg.attach(MIMEText(messagebody, 'plain'))
    server.sendmail(emailuser,tolist,msg.as_string())


def notificationsent(host):
    today = datetime.date.today()
    global formattedtoday
    formattedtoday = today.strftime('%m/%d/%y')
    global hstatusline
    hstatusline = host + ' - notification sent - ' + formattedtoday
    if hstatusline in open('/home/user/pythonscripts/pyinger/pyinger_notification.log').read():
        print "Notification about %s host being down was already sent today (%s)." % (host, formattedtoday)
        return True
    else:
        print "Notification about %s host being down has NOT been sent today (%s)." % (host, formattedtoday)
        print "Sending notification..."
        return False


for host in hosts:
    if ping(host) == True:
        print "OK - %s host responded to ping!" % host
    else:
        print "DOWN - %s host not responding to ping! Houston, we have problem!" % host
        log.warning('==> %s host is down!', host)
        if notificationsent(host) == False:
            ### Update path below to the directory where you put pyinger.py ###
            file = open('/home/user/pythonscripts/pyinger/pyinger_notification.log', 'a')
            file.write(hstatusline)
            file.write("\n")
            file.close()
            sendemail()
            log.info('==> sent NEW notification that %s host is down', host)
        else:
            log.info('==> already sent notification that %s host is down', host)
