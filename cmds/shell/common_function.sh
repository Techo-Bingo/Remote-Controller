#!/bin/bash
g_task_dir=$(pwd)


function init()
{
	report_info "11" "server init ok"
}

function _report()
{
	echo "$1|$2|$3" >${g_task_dir}/__progress__.txt
	chmod 777 ${g_task_dir}/__progress__.txt
}

function report_info()
{
	_report "$1" "RUNNING" "$2"
}

function report_err()
{
	_report "$1" "FAILED" "$2"
	exit 1
}

function compress()
{
	cd ${g_task_dir}
	local dst_file=$1
	# 7za 速度太慢了
	# which 7za &>/dev/null && { echo "${dst_file}.7z"; 7za a ${dst_file}.7z * &>/dev/null && { chmod 777 ${dst_file}.7z; return 0; } || return 1; }
	which tar &>/dev/null && { echo "${dst_file}.tar.gz"; tar zcvf ${dst_file}.tar.gz * &>/dev/null && { chmod 777 ${dst_file}.tar.gz; return 0; } || return 1; }
	which zip &>/dev/null && { echo "${dst_file}.zip"; zip ${dst_file}.zip * &>/dev/null && { chmod 777 ${dst_file}.zip; return 0; } || return 1; }
	return 1
}


