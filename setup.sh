#!/usr/bin/env bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
printf "\n |-----------------------------------------------------------------------------| \n "
printf "|  Don't forget to run \". venv/bin/activate\" and update params.ini.           | \n "
printf "|-----------------------------------------------------------------------------| \n "
printf "\n"
if ! test -f "params.ini"; then
    cp exampleParams.ini params.ini
fi

