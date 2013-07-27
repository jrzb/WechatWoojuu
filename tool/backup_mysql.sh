#!/bin/bash
##-------------------------------------------------------------------
## @copyright 2013
## File : backup_mysql.sh
## Author : filebat <markfilebat@126.com>
## Description : 
## --
## Created : <2013-02-01>
## Updated: Time-stamp: <2013-04-29 00:12:24>
##-------------------------------------------------------------------
#sample: sudo ./backup_mysql.sh  "db1" "username1" "password1" "/root/mysql_backup"

function backup_mysql() {
    db_name=${1?}
    db_username=${2?}
    db_pwd=${3?}
    backup_dir=${4?}

    if [ ! -d $backup_dir ]; then
        mkdir -p $backup_dir
    fi;

    my_print " Backup mysql"
    mysqldump --user=$db_username --password=$db_pwd $db_name | gzip > "$backup_dir"/$db_name-`date +%Y%m%d%H%M`.sql.gz
    my_print " Remove old backup files 60 days ago"
    find $backup_dir -name "*.gz" -mtime +60 -exec /bin/rm {} \;
}

function my_print()
{
    local msg=${1?}
    echo -ne `date +['%Y-%m-%d %H:%M:%S']`"$msg\n"
}

db_name=${1?"mysql db name"}
db_username=${2?"mysql db username"}
db_pwd=${3?"mysql db password"}
backup_dir=${4?"directory to store the backup set"}

backup_mysql "$1" "$2" "$3" "$4"

## File : backup_mysql.sh ends
