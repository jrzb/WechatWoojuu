python -c "import eventtrigger; eventtrigger.get_message('wechat_event', 'localhost')"

git push && git checkout master && git merge webserver && git pull && git push && git checkout webserver

mysql -hserver -uuser_2013 -pilovechina index_db -e "select * from index_db.userevent where event='unsubscribe' order by id desc limit 10;"

mysql -hserver -uuser_2013 -pilovechina index_db -e "select * from index_db.userprofile where index_key='username' limit 100;"

curl "http://173.255.227.47:8090/get_usertext?service_name=gh_2fba4c2ef423&username=obF30jq9JtHvWZMluihHIZHUOIjU"

insert into userprofile(username, service_name, index_key, index_value) values ("obF30jr0VD4HUjUq1kYusd5gSCBo", "gh_2fba4c2ef423", "username", "Denny")

select * from usertext where msgid!= '' and to_username='gh_05d5313dea46' order by createtime desc limit 100;
