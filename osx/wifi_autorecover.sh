#!/bin/bash

#
# Since upgrading to El Capitan I'm suffering a lot of problems with power management of the wireless device.
# This stupid script running on background is monitoring connectivity and forcing wireless device to wake up on failure.
#

# BEGIN of config
INTERFACE="en0"
TESTHOST="8.8.8.8"
SLEEP_TIME=1s
BAD_IN_A_ROW_RECOVER_SOFT=1
BAD_IN_A_ROW_RECOVER_HARD=5
BAD_IN_A_ROW_ALERT=10

RECOVER_SOFT=recover-scan
RECOVER_HARD=recover-reboot
ALERT=alert
# END of config


# Recover by scanning for wifi networks - works on the vast majority of use cases.
function recover-scan {
	echo "RECOVER SCAN!"
	/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport ${INTERFACE} -s &> /dev/null
	sleep 1s
}

# Recover by rebooting the wifi interface
function recover-reboot {
	echo "RECOVER REBOOT!"
	sudo ifconfig ${INTERFACE} down && sleep 1s && sudo ifconfig ${INTERFACE} up
	sleep 5s
}

# Alerting that something is going really wrong
function alert {
	echo "ALERT!"
	say "Internet is failing!"
}

function main {
	GOOD_IN_A_ROW=0
	BAD_IN_A_ROW=0	
	while [ 1 ] ; do
		sleep ${SLEEP_TIME}

		TIME_AVG=$(ping -q -o -t 1 -c 1 -v ${TESTHOST} | awk '/round-trip/{print $4}' | cut -d '/' -f 2 ; PING_EXIT=${PIPESTATUS[0]}) 
		PING_EXIT=${PIPESTATUS[0]}
	
		if [[ -z "${TIME_AVG}" ]] ; then
			PING_EXIT=3
		fi

		case ${PING_EXIT} in
			0)
				BAD_IN_A_ROW=0
				let GOOD_IN_A_ROW=GOOD_IN_A_ROW+1
			;;
			2)
				GOOD_IN_A_ROW=0
				let BAD_IN_A_ROW=BAD_IN_A_ROW+1
			;;
			3)
				GOOD_IN_A_ROW=0
				let BAD_IN_A_ROW=BAD_IN_A_ROW+2
			;;
		esac

		echo ${GOOD_IN_A_ROW} ${BAD_IN_A_ROW} ${TIME_AVG} ${PING_EXIT} 

		if [ ${BAD_IN_A_ROW} -ge ${BAD_IN_A_ROW_RECOVER_SOFT} ] ; then
			$RECOVER_SOFT
		fi

		if [ ${BAD_IN_A_ROW} -ge ${BAD_IN_A_ROW_RECOVER_HARD} ] ; then
			$RECOVER_HARD
		fi

        if [ ${BAD_IN_A_ROW} -gt ${BAD_IN_A_ROW_ALERT} ] ; then
        	$ALERT
        fi	
	done
}

main