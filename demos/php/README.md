PHP4DizPay Demo V1.0.0
=============================


REQUIREMENTS
------------
- PHP7.0.* or newer
- Mysql5.6 or newer
- ThinkPHP5.1.15 or newer 
- Composer version 1.6.4 or newer 
- make sure runtime path can write 

QUICK START
-----------
- cd your project 
- copy .env.example file to .env
- config .env file ,such as  database info, app_id, app_key and base_url
- composer install 
- import data.sql to mysql
- config your webserver(nginx or apache)
- open browser input your web url (such as http://127.0.0.1 or http://localhost)


WEB SERVER CONFIG EXAMPLE
-----------
- nginx config example 
```
server {
	listen       80;
	server_name  localhost ;
	root  /data/web/dizpay/public;
	location / {
		index  index.php;
        if (!-e $request_filename) {
            rewrite  ^(.*)$  /index.php?s=/$1  last;
        }
	}
	location ~ \.php$ {
		fastcgi_pass   127.0.0.1:9000;
		fastcgi_index  index.php;
		fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
		include        fastcgi_params;
	}
	access_log  logs/dizpay.access.log  main;
}
```

- apache config example 
```
<VirtualHost *:80>
    DocumentRoot "/data/web/dizpay/public"
    ServerName   localhost
</VirtualHost>
```

# Documentation
You can find the dizpay api documentation [on the website](https://www.dizpay.com/en/developer)