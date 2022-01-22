#! /usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import getopt
import sys
from datetime import date

COMMON_DOCSTRING = """
Global options
    -a (--after) yyyy-mm-dd
        Query after this date.
    -b (--before) yyyy-mm-dd
        Query before this date.
    -h (--help)
        Display this uage message and exit
"""
USER_NAME="Bill"
GERRIT_ADDRESS="gerrit.xxxx.com"

def usage():
    print(COMMON_DOCSTRING) 

def get_gerrit_infos(before_time, after_time):

    COMMANDS=["ssh","-p","29418", USER_NAME + "@" + GERRIT_ADDRESS, "gerrit",
            "query",
            "--format=TEXT",
            "--current-patch-set",
            "\(status:merged OR status:open\)",
            "owner:self ",
            "before:" + before_time,
            "after:" + after_time]

    GREP_INSERTS_COMMANDS=['grep', '-i', 'sizeinsertions']
    GREP_DELETE_COMMANDS=['grep', '-i', 'sizeDeletions']
    AWK_COMMANDS=['awk','{print $2}']
    print(COMMANDS)
    gerrit_ans = subprocess.Popen(COMMANDS, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    grep_inserts_ans = subprocess.Popen(GREP_INSERTS_COMMANDS, stdin=gerrit_ans.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    awk_inserts_ans = subprocess.Popen(AWK_COMMANDS, stdin=grep_inserts_ans.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    inserts_out, err = awk_inserts_ans.communicate()

    sum_inserts=0
    for line in inserts_out.split('\n'):
        if line is not '':
            sum_inserts = sum_inserts + int(line)

    gerrit_ans = subprocess.Popen(COMMANDS, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    grep_delete_ans = subprocess.Popen(GREP_DELETE_COMMANDS, stdin=gerrit_ans.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    awk_delete_ans = subprocess.Popen(AWK_COMMANDS, stdin=grep_delete_ans.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    delete_out, err = awk_delete_ans.communicate()

    sum_delete=0
    for line in delete_out.split('\n'):
        if line is not '':
            sum_delete = sum_delete + int(line)

    print("total insertions is %d deleteions is %d" % (sum_inserts, sum_delete))


if __name__ == '__main__':  
    opts,args = getopt.getopt(sys.argv[1:],'-h-b:-a:',['help','before=','after='])
    after_time ="1900-01-01"
    date_format="%Y-%m-%d"
    before_time = date.today().strftime(date_format)
    for opt_name,opt_value in opts:
        if opt_name in ('-h','--help'):
            usage()
            exit()
        if opt_name in ('-b','--before'):
            before_time = opt_value
            print("[*] before time is ", before_time)
        if opt_name in ('-a','--after'):
            after_time = opt_value
            print("[*] after time is ", after_time)
    get_gerrit_infos(before_time, after_time)
