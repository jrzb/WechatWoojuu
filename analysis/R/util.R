# -*- coding: utf-8 -*-
#!/usr/bin/R
##-------------------------------------------------------------------
## @copyright 2013
## File : util.R
## Author : filebat <markfilebat@126.com>
## Description :
## --
## Created : <2013-04-04>
## Updated: Time-stamp: <2013-05-22 17:26:24>
##-------------------------------------------------------------------
library(DBI)
library(RMySQL)

################### Configuration #################
dbhost="127.0.0.1"
dbuser="user_2013"
dbpwd="ilovechina"
dbname="wj"
###################################################

## querymysql("select date, amount, notes from expenses where userid='liki' and memo='meal' order by date limit 100;")
querymysql = function(sql, host=dbhost, user=dbuser, password=dbpwd, db=dbname) {
  m <- dbDriver("MySQL")
  conn <- dbConnect(m, host=dbhost, user=dbuser, password=dbpwd, db=dbname)
  dbSendQuery(conn, "SET NAMES utf8")
  res = dbSendQuery(conn, sql)
  dd <- fetch(res, n=-1)
  dbClearResult(res)
  dbDisconnect(conn)
  return(dd)
}

pause = function() {
  print ("Pause, press any key to continue:")
  readline()
}
###################################################

###########################################################################
fun1 = function(picprefix) {
  sql="select left(date, 10) as date, count(distinct userid) as count from expenses where date > DATE_ADD(CURDATE(), INTERVAL -7 DAY) group by left(date, 10) order by left(date, 10) asc;"
  filename = paste(Sys.getenv(x = "WECHAT_HOME"), "/app/static/img/R/", picprefix, "report_daily_user_count.png", sep="", collapse="")
  png(filename = filename, width = 320, height = 360, units = "px", pointsize = 12, bg = "white")

  dd = querymysql(sql)
  dd$date<-as.Date(dd$date, "%Y-%m-%d")
  plot(count~date, dd, xaxt="n", type="p", col="blue",
       xlab="Date (YY-MM-DD)", ylab="Count", yaxs="i")
  lines(dd$date, dd$count)
  
  title("Daily access users",
        sub = "Identify user vitality",
        cex.main = 2, font.main= 3.5, col.main= "blue",
        cex.sub = 0.9, font.sub = 3.5, col.sub = "blue")

  axis(1, dd$date, format(dd$date, "%Y-%m-%d"))
  dev.off()
}
###########################################################################

fun2 = function(picprefix) {
  filename = paste(Sys.getenv(x = "WECHAT_HOME"), "/app/static/img/R/", picprefix, "report_detect_comparsion.png", sep="", collapse="")
  png(filename = filename, width = 320, height = 360, units = "px", pointsize = 12, bg = "white")

  sql="select left(date, 10) as date, count(1) as count from expenses where date > DATE_ADD(CURDATE(), INTERVAL -7 DAY) group by left(date, 10);"
  dd = querymysql(sql)
  dd$date<-as.Date(dd$date, "%Y-%m-%d")
  plot(count~date, dd, xaxt="n", type="p", col="blue",
       xlab="Date (YY-MM-DD)", ylab="Count", yaxs="i")
  lines(dd$date, dd$count)

  sql2="select left(date, 10) as date, count(1) as count from expenses where memo!='detected' and date > DATE_ADD(CURDATE(), INTERVAL -7 DAY) group by left(date, 10);"
  dd2 = querymysql(sql2)
  dd2$date<-as.Date(dd2$date, "%Y-%m-%d")

  par(col="brown")
  points(dd2$date, dd2$count)
  lines(dd2$date, dd2$count)
  par(col="black")
  
  title("Daily new records",
        sub = "Identify records quantity/quality",
        cex.main = 2, font.main= 3.5, col.main= "blue",
        cex.sub = 0.9, font.sub = 3.5, col.sub = "blue")

  axis(1, dd$date, format(dd$date, "%Y-%m-%d"))
  dev.off()
}
###########################################################################

###########################################################################
fun3 = function(picprefix) {
  sql="select left(date, 10) as day, substring(date, 11, 3) as hhmm from expenses where date > DATE_ADD(CURDATE(), INTERVAL -7 DAY) order by date asc;"
  filename = paste(Sys.getenv(x = "WECHAT_HOME"), "/app/static/img/R/", picprefix, "report_daily_time.png", sep="", collapse="")
  png(filename = filename, width = 320, height = 360, units = "px", pointsize = 12, bg = "white")

  dd = querymysql(sql)
  dd$day<-as.Date(dd$day, "%Y-%m-%d")
  ##dd$hhmm<-as.Date(dd$hhmm, "%HH:%MM")
  plot(hhmm~day, dd, xaxt="n", type="p", col="blue",
       xlab="Date (YY-MM-DD)", ylab="Hour", yaxs="i")
  
  title("Daily input time",
        sub = "Identify busy hours",
        cex.main = 2, font.main= 3.5, col.main= "blue",
        cex.sub = 0.9, font.sub = 3.5, col.sub = "blue")

  axis(1, dd$day, format(dd$day, "%Y-%m-%d"))
  axis(2, c(0, 1, 3, 6, 9, 12, 15, 19, 24))
  dev.off()
}
###########################################################################

###########################################################################
fun4 = function(picprefix) {
  filename = paste(Sys.getenv(x = "WECHAT_HOME"), "/app/static/img/R/", picprefix, "report_user_compose.png", sep="", collapse="")
  png(filename = filename, width = 320, height = 360, units = "px", pointsize = 12, bg = "white")
  sql="select count(distinct userid) as count, concat('Total users:', count(distinct userid)) as label from expenses;"
  
  dd = querymysql(sql)

  sql="select userid, count(1) from expenses where  date > DATE_ADD(CURDATE(), INTERVAL -7 DAY) group by userid having count(1)>=5;"
  dd2 = querymysql(sql)

  sql="select userid, count(1) from expenses where  date > DATE_ADD(CURDATE(), INTERVAL -7 DAY) group by userid having count(1)<=2;"
  dd3 = querymysql(sql)

  dd[2,1] <- length(dd2$userid)
  dd[2,2] <- paste("Active:", dd[2,1], sprintf("\n%2.f", dd[2,1]*100 / dd[1,1]), "%")

  dd[3,1] <- length(dd3$userid)
  dd[3,2] <- paste("Normal:", dd[3,1], sprintf("\n%2.f", dd[3,1]*100 / dd[1,1]), "%")

  dd[1,1] <- dd[1,1] - dd[2,1] - dd[3,1]
  dd[1,2] <- paste("Other:", dd[1,1], sprintf("\n%2.f",  dd[1,1]*100 / (dd[1,1] + dd[2,1] + dd[3,1])), "%")

  pie(dd$count, labels=dd$label, main="Users Composition")
  dev.off()
}
###########################################################################

###########################################################################
fun5 = function(picprefix) {
  filename = paste(Sys.getenv(x = "WECHAT_HOME"), "/app/static/img/R/", picprefix, "report_category_compose.png", sep="", collapse="")
  png(filename = filename, width = 320, height = 360, units = "px", pointsize = 12, bg = "white")

  #sql="select count(1) as count, concat(concat(category, ":"), count(1)) as label from expenses group by category order by count(1) desc;"
  sql="select count(1) as count, concat(category, count(1)) as label from expenses group by category order by count(1) desc limit 6;"
  dd = querymysql(sql)
  pie(dd$count, labels=dd$label, main="Record Composition", family='MingLiU')
  dev.off()
}
###########################################################################
fun6 = function(picprefix) {
  filename = paste(Sys.getenv(x = "WECHAT_HOME"), "/app/static/img/R/", picprefix, "report_daily_user_avg_count.png", sep="", collapse="")
  png(filename = filename, width = 320, height = 360, units = "px", pointsize = 12, bg = "white")

  sql="select left(date, 10) as date, count(1) as count from expenses where date > DATE_ADD(CURDATE(), INTERVAL -7 DAY) group by left(date, 10);"
  dd = querymysql(sql)
  dd$date<-as.Date(dd$date, "%Y-%m-%d")

  sql="select left(date, 10) as date, count(distinct userid) as count from expenses where date > DATE_ADD(CURDATE(), INTERVAL -7 DAY) group by left(date, 10) order by left(date, 10) asc;"
  dd2 = querymysql(sql)
  dd2$date<-as.Date(dd2$date, "%Y-%m-%d")

  dd$count = dd$count / dd2$count
  plot(count~date, dd, xaxt="n", type="p", col="blue",
       xlab="Date (YY-MM-DD)", ylab="Count", yaxs="i")
  lines(dd$date, dd$count)
  
  title("Daily users' avg count",
        sub = "Avg input",
        cex.main = 2, font.main= 3.5, col.main= "blue",
        cex.sub = 0.9, font.sub = 3.5, col.sub = "blue")

  axis(1, dd$date, format(dd$date, "%Y-%m-%d"))
  dev.off()
}
###########################################################################

###########################################################################
## File : util.R ends
