#!/usr/bin/env bash
# check path
var=`pwd`
if [[ "$var" =~ "EasyW"$ ]]
then
    echo "Check path succeeded."
else
    echo "Please go to the project directory."
    exit 1
fi

source env/bin/activate
cd easyw
export FLASK_APP=bootstrap.py
flask run -h 0.0.0.0 -p 9715
