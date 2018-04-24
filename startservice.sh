#!/bin/bash

wuser=$(ls /home | egrep 'zen|pi')
export FORMS_HOME="/home/$wuser/git/smarthome/"

test=$(curl --connect-timeout 25 --retry 3 --retry-delay 20 --write-out %{http_code} --silent --output /dev/null http://127.0.0.1/)

if [[ "$test" -ne 200 ]]; then

  processes=$(ps aux |grep python |grep "run.py")
  if [[ -n "$processes" ]]; then

    for i in $processes
    do
      kill -9 $i
    done
  fi

  cd "$FORMS_HOME"
  ./run.py

fi