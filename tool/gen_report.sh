#!/bin/bash
##-------------------------------------------------------------------
## @copyright 2013 ShopEx Network Technology Co,.Ltd
## File : gen_report.sh
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-04-20>
## Updated: Time-stamp: <2013-05-19 11:52:46>
##-------------------------------------------------------------------
# export WECHAT_HOME="/home/wwwroot/wechat.woojuu.cc/";/home/wwwroot/wechat.woojuu.cc/tool/gen_report.sh 249950670@qq.com
email_list=${1:-"markfilebat@126.com,249950670@qq.com,liki.do@gmail.com"}
current_time=`date +%Y%m%d%H%M%S`
NON_DETECT_LIMIT=60
RECORD_LIMIT=20

function R_refresh() {
    Rscript $WECHAT_HOME/R/report.R $current_time
}

function sql_report() {
    exclude_user="userid not in ('unittest', 'obF30jr0VD4HUjUq1kYusd5gSCBo', 'obF30jiGrBob1V_28lNS-6QpcEww')"

    echo -e "\n======================= This week's frequent user list ================== "
    sql="mysql -uuser_2013 -pilovechina wj -e \"select userid, count(1) from expenses where date > DATE_ADD(CURDATE(), INTERVAL -7 DAY) group by userid having count(1)>4 order by count(1) desc;\" | cat -n"
    echo -e "$sql\n"
    eval $sql

    echo -e "\n======================= Lastet $NON_DETECT_LIMIT nondetected record ================== "
    sql="mysql -uuser_2013 -pilovechina wj -e \"select right(userid, 8), amount, branding, category, memo, left(notes, 8) from expenses where $exclude_user and memo!='detected' order by expenseid desc limit $NON_DETECT_LIMIT;\" | cat -n "
    echo -e "$sql\n"
    eval $sql
}

R_refresh
sql_output=$(sql_report)
html_fname="/tmp/woojuu_report_$current_time.html"

cat > $html_fname <<EOF
<html>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<body>
<img src="http://wechat.woojuu.cc/static/img/R/${current_time}report_user_compose.png" alt=""></img>
<br/>
<img src="http://wechat.woojuu.cc/static/img/R/${current_time}report_category_compose.png" alt=""></img>
<br/>
<img src="http://wechat.woojuu.cc/static/img/R/${current_time}report_daily_user_avg_count.png" alt=""></img>
<br/>
<img src="http://wechat.woojuu.cc/static/img/R/${current_time}report_daily_user_count.png" alt=""></img>
<br/>
<img src="http://wechat.woojuu.cc/static/img/R/${current_time}report_detect_comparsion.png" alt=""></img>
<br/>
<img src="http://wechat.woojuu.cc/static/img/R/${current_time}report_daily_time.png" alt=""></img>
<pre>
$sql_output
</pre>
</body>
</html>
EOF

echo $html_fname

mail -a 'Content-type: text/html; charset="utf-8"' -s "[`date +%Y-%m-%d_%H:%M`] Woojuu Daily Report" "$email_list"  < $html_fname

rm -rf $html_fname
## File : gen_report.sh ends