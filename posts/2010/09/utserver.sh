#!/bin/bash
#

User="user"

Name="utserver"

#-------


if [ `whoami` != root ]; then
        echo "-> You are not Root!"
        echo
        exit 1
fi


Status() {
        if [ "`su -c "screen -ls | grep $Name" $User `" != "" ]; then
         echo "-> Screen work"
        else
         echo "-> Screen dosn't work"
        fi
}


Start() {
        if [ "`su -c "screen -ls | grep $Name" $User `" != "" ]; then
         echo "-> Screen already work"
        else
          echo "-> Trying to start"
          su -c "screen -dm -S $Name nice -n 8 $Name" $User
          sleep 1
          Status
        fi
}

Stop() {
        if [ "`su -c "screen -ls | grep $Name" $User `" = "" ]; then
         echo "-> Screen already stop"
        else
         echo "-> Stoping screen"
         su -c "screen -r $Name -X quit" $User
	 killall $Name
         sleep 1
         Status
        fi
}
Screen() {
    su -c "screen -x $Name" $User
}

case "$1" in
        start) Start ;;
        stop) Stop ;;
        status) Status ;;
        restart)
         Stop
         Start
        ;;
        screen) Screen ;;
        *)
          echo "-> Help -> Usage: [ start|stop|restart|status|screen ]"

        ;;
esac

exit 0
