#!/bin/bash

wuser=$(ls /home | egrep 'zen|pi')
export FORMS_HOME="/home/$wuser/git/smarthome/"
serviceName="Web Flask"

test='curl --connect-timeout 10 --retry 2 --retry-delay 1 --write-out %{http_code} --silent --output /dev/null http://chibiko.noip.me/'

case $1 in
  start)
     cd "$FORMS_HOME"
    ./run.py 2>&1 >/dev/null &
   exit 0
  ;;
  stop)
    processes=$(ps aux |grep python |grep "run.py" | awk '{print $2}')
    if [[ -n "$processes" ]]; then

    for i in $processes
      do
        kill -9 $i
      done
    fi
    exit 0
  ;;
  status)
    processes=$(ps aux |grep python |grep "run.py")
    if [[ -n "$processes" ]]; then
      echo "Servise $serviceName is working"
    else
      echo "Service $serviceName is Stopped"
    fi

    exit 0
  ;;
  restart)
  if [[ "$test" -ne 200 ]]; then

  processes=$(ps aux |grep python |grep "run.py" | awk '{print $2}')
  if [[ -n "$processes" ]]; then

    for i in $processes
    do
      kill -9 $i
    done
  fi

  cd "$FORMS_HOME"
  ./run.py 2>&1 >/dev/null &
  exit 0

  fi
  ;;

  teststart)
    processes=$(ps aux |grep python |grep "run.py")
    sitestatus=`$test`
    if [[ -z "$processes" ]] || [[ $sitestatus != 302 ]]; then
      cd "$FORMS_HOME"
      ./run.py 2>&1 >/dev/null &
     exit 0

    fi


  ;;
  *)
    echo "usage: start|stop|restart|status"
    exit 0
  ;;
esac
