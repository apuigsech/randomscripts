#!/bin/bash

#
# Since upgrading to El Capitan I'm suffering a lot of problems with power management of the wireless device.
# This stupid script running on background is monitoring connectivity and forcing wireless device to wake up on failure.
#

TESTHOST="8.8.8.8"

GOOD_IN_A_ROW=0
BAD_IN_A_ROW=0

while [ 1 ] ; do
	sleep 1s
	ping -q -o -t 1 ${TESTHOST} &> /dev/null
	case $? in
		0)
			BAD_IN_A_ROW=0
			let GOOD_IN_A_ROW=GOOD_IN_A_ROW+1
		;;
		2)
			GOOD_IN_A_ROW=0
			let BAD_IN_A_ROW=BAD_IN_A_ROW+1
		;;
	esac
	echo ${GOOD_IN_A_ROW} ${BAD_IN_A_ROW}
	if [ $BAD_IN_A_ROW -gt 0 ] ; then
		/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -s &
	fi
        if [ $BAD_IN_A_ROW -gt 3 ] ; then
                say "Internet is failing!"
        fi	
done
