#!/bin/bash

if [ $# -ne "1" ]; then
    echo "usage: $0 #mode"
    echo "mode: op , test"
    exit
fi
TODAY=`date +%Y%m%d`
NOWSECS=`date +%s`
TODAY2=`date +%Y-%m-%d`
TIMESTAMP=`date --date="$TODAY2 00:00:00" +%s`
MODE=$1
if [ $MODE == "test" ]; then
    DB_HOST="172.18.8.8"
    DB_PORT=3306
    DB_USER=test
    DB_PWD=test
    DB_NAME=news
else
	exit
fi
#exit
expect -c "
spawn mysql -h$DB_HOST -P$DB_PORT -u$DB_USER -p
expect \"*assword*\"
send \"$DB_PWD\r\"
expect \"mysql>\"
send \"use $DB_NAME; create table notice_$TODAY charset=utf8 select * from notice where create_time < $TIMESTAMP ; \r\"
expect \"mysql>\"
send \"delete from notice where create_time < UNIX_TIMESTAMP(STR_TO_DATE('$TODAY 00:00:00', '%Y%m%d %H:%i:%S')); \r\"
expect \"mysql>\"
exit
"
