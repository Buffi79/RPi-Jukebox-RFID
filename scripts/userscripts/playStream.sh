#!/bin/bash


PATHDATA="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit 1
fi

url="$(curl -d $1 192.168.0.5:8022)"
echo $url
if [ -z "$url" ]
  then
    echo "No Url for RFID found"
    exit 1
fi

SMB_CREDENTIALS=`cat $PATHDATA/.env`
if [[ -z "$SMB_CREDENTIALS" ]]; then
    echo "SMB_CREDENTIALS for Sambashare not set -> fill in .env File -> un:pw"
    echo "SMB_CREDENTIALS for Sambashare not set -> fill in .env File -> un:pw" >> $PATHDATA/../../logs/debug.log
    exit 1 
fi

replace="smb://${SMB_CREDENTIALS}@"
url=$replace$url
echo $url

mpc stop
mpc clear

if [[ "$url" == *.mp3 ]];then
    mpc add $url
elif [[ "$url" == *.m3u ]];then
    mpc load $url
else
    echo "Stream? Try add-command"
    mpc add $url
fi

mpc play
exit 0
