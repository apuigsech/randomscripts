#!/usr/bin/env bash 

TEST_NAME="1.3.2. Ataques comunes sobre web services"
TEST_VERSION="1.0"

CURL_BIN=`which curl`
DATE_FORMAT="+%d/%m/%y %H:%M:%S"

SAMPLES_DIR="attack_signatures"

TASK_LIFETIME=600
TASK_BREAKTIME=120


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
	$cmd &> /dev/null 
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
	local target_url=$1
	local base_cmd="${CURL_BIN} --insecure -H 'Content-Type: text/xml; charset=utf-8' -H 'SOAPAction:' -X POST "

	for filename in $(ls ${SAMPLES_DIR}); do
		write_log "TASK START ${filename}"
		 for sample in $(cat ${SAMPLES_DIR}/${filename}); do
		 	exec_task "${base_cmd} '${target_url} -d ${sample}'"
		 done
		 write_log "TASK END ${filename}"
		 sleep ${TASK_BREAKTIME}
	done
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
