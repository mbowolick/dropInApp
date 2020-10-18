#!/usr/bin/env bash
if grep -q REPLACE_HERE_MERCHANT_ACCOUNT "params.ini" ; then
  printf "\n |-----------------------------------------------------------------------------| \n "
  printf "|  params.ini file is not updated. Please do this before running the app.     | \n "
  printf "|-----------------------------------------------------------------------------| \n "
  printf "\n"
  exit 
fi
export FLASK_APP=dropInApp
export FLASK_ENV=development
flask run
