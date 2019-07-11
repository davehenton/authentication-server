#!/bin/bash

#Author Peter Malaty

export PATH='/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
BRANCH="$1"

cd /opt/authentication-server
#cat ./cronscript.sh

pytest
#alembic upgrade head
alembic -c staging_alembic.ini upgrade head
#pserve staging.ini & 

echo "Initializing Code Coverage"

curl -L https://codeclimate.com/downloads/test-reporter/test-reporter-latest-linux-amd64 > ./cc-test-reporter
chmod +x ./cc-test-reporter
pip3.7 install coverage

coverage run -m pytest

echo "Coverage Code Quality by Peter"
coverage report -m


echo "Initializing Code Quality Checks and report submission by CodeClimate"
coverage xml

echo "Pete engine ENV Generation"
export GIT_COMMIT=$(git log | grep -m1 -oE '[^ ]+$')
#export CODECLIMATE_REPO_TOKEN='30423619d0d8265bce3b093504c08d9618be22da7c4264a821087c3ad5e0fc8a'
export CC_TEST_REPORTER_ID='30423619d0d8265bce3b093504c08d9618be22da7c4264a821087c3ad5e0fc8a'
export GIT_COMMITTED_AT="$(date +%s)"
export GIT_BRANCH="$BRANCH"
./cc-test-reporter before-build 

./cc-test-reporter after-build -d -t coverage.py

if [ $? == 0 ]; then
echo "Everything Completed Successfully ... Cheers ... Peter"
else
echo "Whoops, something went wrong, send to Peter please"
fi

