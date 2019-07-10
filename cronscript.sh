#!/bin/bash

#Author Peter Malaty

export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'

while(true); do
if [ -d /opt/authentication-server/.pytest_cache ]; then
sleep 10s
break
fi
sleep 5s
done

cd /opt/authentication-server
while(true); do
netstat -anpt | grep 8000 | grep python
if [ $? != 0 ]; then
pserve staging.ini 
fi

sleep 5s
done
