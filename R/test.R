#!/usr/bin/R
##-------------------------------------------------------------------
## @copyright 2013
## File : test.R
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-04-04>
## Updated: Time-stamp: <2013-05-12 09:13:10>
##-------------------------------------------------------------------
source("./util.R")

###########################################################################
sql="select left(date, 10) as date, count(distinct userid) as count from expenses where date > DATE_ADD(CURDATE(), INTERVAL -7 DAY) group by left(date, 10) order by left(date, 10) asc;"
filename="./report_daily_user_count.png"

png(file=filename, bg="white")
dd = querymysql(sql)
dd$date<-as.Date(dd$date, "%Y-%m-%d")
plot(count~date, dd, xaxt="n", type="p", col="blue",
     xlab="Date (YY-MM-DD)", ylab="count", main="Daily users count", yaxs="i")
axis(1, dd$date, format(dd$date, "%Y-%m-%d"))
#axis(2, as.integer(summary(dd$count)))
abline(dd$count, dd$date)
dev.off()
###########################################################################
## File : test.R ends
