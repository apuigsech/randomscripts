#!/usr/bin/env bash 

TEST_NAME="2.1.1. Ofuscación de payloads web"
TEST_VERSION="1.0"

NIKTO_BIN=`which nikto`
DATE_FORMAT="+%d/%m/%y %H:%M:%S"

SAMPLES_DIR="attack_signatures"

TASK_LIFETIME=300
TASK_BREAKTIME=60

#
# RUN: sudo nikto -update
#

function banner () {
	echo "################################################################################"
	echo "# ${TEST_NAME} (${TEST_VERSION})"
	echo "################################################################################"
}

function usage () {
	echo "Usage:"
	echo "  ${0} <target_url>"
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

function url_parse() {
	# extract the protocol
	proto="`echo $1 | grep '://' | sed -e's,^\(.*://\).*,\1,g'`"
	# remove the protocol
	url=`echo $1 | sed -e s,$proto,,g`

	# extract the user and password (if any)
	userpass="`echo $url | grep @ | cut -d@ -f1`"
	pass=`echo $userpass | grep : | cut -d: -f2`
	if [ -n "$pass" ]; then
		user=`echo $userpass | grep : | cut -d: -f1`
	else
		user=$userpass
	fi

	# extract the host -- updated
	hostport=`echo $url | sed -e s,$userpass@,,g | cut -d/ -f1`
	port=`echo $hostport | grep : | cut -d: -f2`
	if [ -n "$port" ]; then
		host=`echo $hostport | grep : | cut -d: -f1`
	else
		host=$hostport
		port=80
	fi

	# extract the path (if any)
	path="`echo $url | grep / | cut -d/ -f2-`"
}

function run_test () {
	local target_url=$1
	url_parse $target_url
	local base_cmd="${NIKTO_BIN} -host ${host} -port ${port}"

	exec_task_timeout "${base_cmd} -evasion 1" ${TASK_LIFETIME}
	sleep ${TASK_BREAKTIME}
	exec_task_timeout "${base_cmd} -evasion 2" ${TASK_LIFETIME}
	sleep ${TASK_BREAKTIME}
	exec_task_timeout "${base_cmd} -evasion 3" ${TASK_LIFETIME}
	sleep ${TASK_BREAKTIME}
	exec_task_timeout "${base_cmd} -evasion 4" ${TASK_LIFETIME}
	sleep ${TASK_BREAKTIME}
	exec_task_timeout "${base_cmd} -evasion 5" ${TASK_LIFETIME}
	sleep ${TASK_BREAKTIME}
	exec_task_timeout "${base_cmd} -evasion 6" ${TASK_LIFETIME}
	sleep ${TASK_BREAKTIME}
	exec_task_timeout "${base_cmd} -evasion 7" ${TASK_LIFETIME}
	sleep ${TASK_BREAKTIME}
	exec_task_timeout "${base_cmd} -evasion 8" ${TASK_LIFETIME}
}

function main () {
	banner
	if [ $# -lt 1 ]; then
		usage
		exit 1
	else
		target_url=$1
	fi

	run_test $target_url
}

main $1
