#!/usr/bin/env bash

TEST_NAME="1.1.2. Escaneo de puertos con diversas técnicas"
TEST_VERSION="1.0"

NMAP_BIN=`which nmap`
DATE_FORMAT="+%d/%m/%y %H:%M:%S"


TASK_LIFETIME=600
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
	echo "\t${0} <file:targets>"
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
	local base_cmd="${NMAP_BIN} -iL ${target_ip} -n"

	exec_task_timeout "${base_cmd} -sT" $TASK_LIFETIME
	sleep $TASK_BREAKTIME
	exec_task_timeout "${base_cmd} -sS" $TASK_LIFETIME
	sleep $TASK_BREAKTIME
	exec_task_timeout "${base_cmd} -sA" $TASK_LIFETIME
	sleep $TASK_BREAKTIME
	exec_task_timeout "${base_cmd} -sF" $TASK_LIFETIME
	sleep $TASK_BREAKTIME
	exec_task_timeout "${base_cmd} -sX" $TASK_LIFETIME
	sleep $TASK_BREAKTIMR
	exec_task_timeout "${base_cmd} -sN" $TASK_LIFETIME
    sleep $TASK_BREAKTIMR
	exec_task_timeout "${base_cmd} -sU" $TASK_LIFETIME
}

function main () {
	banner

	if [ $# -lt 1 ]; then
		usage
		exit 1
	else
		file_targets=$1
	fi

	estimate_time

	run_test $file_targets
}

main $1
