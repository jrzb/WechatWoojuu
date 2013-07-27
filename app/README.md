curl "http://127.0.0.1:5000/summary?userid=dennyledger&categories=&fromdate=2013-02-29%2012:08:03&enddate=2013-04-29%2012:08:03"

curl  -d "userid=dennyledger&notes=37 超大杯星巴克焦糖玛奇朵" "http://0.0.0.0:5000/add_expense" 2>/dev/null

git push && git checkout master && git merge webserver && git pull && git push && git checkout webserver

git stash && git pull && git stash apply && uwsgi -x uwsgi_config.xml

python -c "import app; import data; data.refresh_not_detected_expense()"

select expenseid, amount, branding, left(memo, 20), left(notes, 24) from expenses where memo!='detected' order by expenseid desc limit 200;

curl -d "msg=你好呀" "http://0.0.0.0:5000/aiml_chat" 2>/dev/null
curl  -d "userid=obF30jr0VD4HUjUq1kYusd5gSCBo&notes=你好吗" "http://0.0.0.0:5000/add_expense" 2>/dev/null
