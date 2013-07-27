# User list: weixin userid <--> username
| Userid                       | Name         |
|:------------------------------|--------------|
| obF30jr0VD4HUjUq1kYusd5gSCBo | Denny        |
| obF30jvBV656EFFzbzFoqMGxPivM | sophia       |
| obF30jiGrBob1V_28lNS-6QpcEww | liki         |
| obF30jhxx0jdvJdkXZmnUxU9xqSA | ivan         |
| obF30jrvwuz1ub72PCI8VKJvavPY | LiuhuiDaisy  |
| obF30jrFUbQRnzDnT6IzjHuN-oGE | Stacy Ling47 |
| obF30jrdzu8p-X8q5pQLPYgaO2cU | phoebe       |
| obF30jkKnM1cmumAqeUmmoGGA3cs | you          |
| obF30jhY0fzM0AcjrLHLvHrluDrw | Rome Lee     |

# Common SQL
| Summary                          | SQL                                                                                                                                              |
|:----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------- |
| 列出最近50条，未被识别的消费记录 | select right(userid, 8), amount, branding, category, memo, left(notes, 8) from expenses where memo!='detected' order by expenseid desc limit 50; |
| 最近一周用户活跃度的排列榜       | select userid, count(1) from expenses where date > DATE_ADD(CURDATE(), INTERVAL -7 DAY) group by userid order by count(1) desc;                  |
| 最近输入的20条消息               | select amount, branding, category, memo, notes from expenses order by expenseid desc limit 20;                                                   |
