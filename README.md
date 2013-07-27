WechatWoojuu
=========

WechatWoojuu

### uwsgi deployment parameter

	uwsgi -x /home/wwwroot/wechat.io/uwsgi_config.xml -M -t 30 -A 1 -p 1 -d /var/log/uwsgi.log --vhost

	