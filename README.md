## Summary

**PyInger**: A simple Python script that pings a lists of hosts and sends out email notifications if something is down.


## Setup

1. Copy **pyinger.py** to your server
2. Create **pyinger_notification.log** in same location as pyinger.py (i.e. "touch pyinger_notification.log")
3. Create Cron entry to run pyinger.py periodically (see comment in script for Cron example)


## Initial Configuration

Make the following changes to get the script working:
* Update *loghandler* path to same location where you put the pyinger.py
* Update *hosts* to include any hosts that you want to ping (and receive notifications for when down)
* Update *smtp_host* to the address of your SMTP server
* Change *smtp_port* if your SMTP server uses a port besides 25
* If your SMTP server requires authentication, change *emailuser* and *emailpass* to have your email account information **AND** uncomment the line with *server.login(emailuser,emailpass)*
* Change *fromaddr* to whatever email address you want the reply address to be
* Update *tolist* with the email addresses you want to receive notifications at (when a host doesn't respond to ping)
* Update path in line beginning with *"if hstatusline in open..."* to same location as script

## Notes

The script will log the first instance when a host is down on any given date in *pyinger_notification.log* file.  I did this so only one notification per date is sent out when a host is down.  **(So you don't receive repeated notifications while you're bringing a host back up.)**

**You need to manually delete the line associated with the host in the pyinger_notification.log when you bring the host back up.  If you don't remove the line, no new notifications will be sent out for the host on the same date.**

## License

This project is licensed under the terms of the MIT license.
