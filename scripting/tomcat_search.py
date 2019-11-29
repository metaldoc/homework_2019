#!/usr/bin/python
import datetime
import os
import subprocess
import time
import signal

timenow = datetime.datetime.now()
logfile = open('test.log', mode='r')
trigger = 'test message'
tomcat_home = '/opt/tomcat7/'


def tomcat_restart():
    os.chdir(tomcat_home + "bin/")
    subprocess.call('sh catalina.sh stop', shell=True)
    time.sleep(20)
    try:
        grepres = subprocess.check_output("ps -ef | grep tomcat | grep -v 'grep\|python' | awk '{print $2}'", shell=True)
        if len(grepres) > 0:
            os.kill(int(grepres.strip()), signal.SIGKILL)
    except subprocess.CalledProcessError as e:
        pass
    subprocess.call('sh catalina.sh start', shell=True)


def main():
    for line in logfile:
        if trigger in line:
            timestamp_str = line.split('[')[1].split(']')[0][:-6]
            timestamp = datetime.datetime.strptime(timestamp_str, '%d/%b/%Y:%H:%M:%S')
            delta = timenow - timestamp
            delta_minutes = delta.seconds // 60
            if delta_minutes < 45:
                continue
            else:
                tomcat_restart()


if __name__ == '__main__':
    main()
logfile.close()
