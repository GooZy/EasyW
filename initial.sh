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

mkdir instance
echo '' > instance/easyw.db

# make sure virtualenv is installed
package=virtualenv
if python -c "import $package" >/dev/null 2>&1
then
    echo "$package FOUND"
else
    echo "$package NOT FOUND. Please use 'pip install virtualenv' to install."
    exit 1
fi

# install virtualenv and python packages
virtualenv env --python=python2.7
source env/bin/activate
pip install -r requirements.txt

# init db
cd easyw
export FLASK_APP=bootstrap.py
flask initdb

echo "Initial successfully."
