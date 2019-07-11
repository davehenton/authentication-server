#!/bin/bash

#Author Peter Malaty

export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'

cd /opt/authentication-server
#cat ./cronscript.sh
pytest
#alembic upgrade head
alembic -c staging_alembic.ini upgrade head
#pserve staging.ini & 


