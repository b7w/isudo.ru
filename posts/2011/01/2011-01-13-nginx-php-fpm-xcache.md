# title: Nginx, php-fpm, xcache, various php.ini
# url: nginx-php-fpm-xcache-various-php-ini
# categories: [HowTo, Ubuntu]
# tags: [Nginx, php, XCache]
# time: 2011-01-13 13:24:16


![left](~never-ball.png)
Почему то статей про настройку Nginix и php-fpm на Ubuntu 10.10 мало. Все больше предпочитают собирать из исходников да загружать из левых репозиториев. А про настройку php с разными php.ini я вообще не видел. Хотя тема очень интересная. Поэтому я решил написать краткий manual по данной теме. Попутно описав некоторые параметры.

[more]

### Базовая настройка
Давайте поставим все необходимые пакеты. Их конечно прилично, но они не много места на диске занимаю и не помешают я думаю.

    sudo apt-get install nginx
    sudo apt-get install php5-fpm php5-mysql php5-curl php5-gd php5-imap php5-mcrypt php5-memcache php5-mhash php5-ps php5-pspell php5-snmp php5-sqlite php5-xmlrpc php5-xsl php5-json php5-xsl

Теперь нам надо сделать начальную настройку Web server и проверить как все работает.
Для начала отредактируем конфигурационный файл под что-то похожее. Причем лучше не удалять стандартный, а просто его полностью закомментировать. Там много полезного, кстати как и на этом [ресурсе](http://wiki.nginx.org/Configuration). Открываем конфиг `sudo nano /etc/nginx/sites-available/default`

    server {

        listen   80;

        server_name  localhost nextdomain;

        client_max_body_size 16m;
        keepalive_timeout  120;

        access_log  /var/log/nginx/localhost.access.log;
        error_log /var/log/nginx/localhost.error.log;

        location / {
            root   /var/www;
            index  index.html index.htm;
        }

        location ~ \.php$ {
            include /etc/nginx/fastcgi_params;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param  SCRIPT_FILENAME  /var/www$fastcgi_script_name;
        }
    }

Теперь что бы посмотреть работу php и его компонент запишем в какой нибудь файлик, допустим `sudo nano /var/www/test.php`, такой код.

    <?php
        phpinfo();
    ?>    

Перезапустим сервер, что бы применить наши изменения
    
    sudo /etc/init.d/nginx restart
    sudo /etc/init.d/php5-fpm restart

Заходим по `http://server_ip/test.php` и наблюдаем большие таблицы с кучей информации о php. Если все успешно, идем дальше.


### Настройка второго сервера php-cgi
Это действие не обязательно и можно перейти к установке xcache. Но если вам интересна, к примеру, идея запуска второго php-cgi сервера для тестовых действий, с включенным выводом ошибок и без кеширующего ускорителя, вам стоит почитать это.

Мы скопируем скрипт запуска и сделаем пару манипуляций над ним. А именно, мы заменим файл настройки php5-fpm.conf и добавим к строке запуска ключ `-c` что бы указать на другой php.ini.

    sudo cp /etc/init.d/php5-fpm /etc/init.d/php5-test
    sudo nano /etc/init.d/php5-test

редактируем

    :::ini
    php_fpm_BIN=/usr/bin/php5-fpm
    php_fpm_CONF=/etc/php5/fpm/php5-fpm-test.conf
    php_fpm_PID=/var/run/php5-fpm-test.pid
    php_CONF=/etc/php5/fpm/php-test.ini
    
    php_opts="--fpm-config $php_fpm_CONF -c $php_CONF"

Теперь собственно создадим конфигурационные файлы которые мы указали, и от редактируем их.

    sudo cp /etc/php5/fpm/php5-fpm.conf /etc/php5/fpm/php5-fpm-test.conf
    sudo cp /etc/php5/fpm/php.ini /etc/php5/fpm/php-test.ini

Это минимальный набор который надо заменить. Еще можно настроить количество процессов, но это уже разбирайтесь сами. `sudo nano /etc/php5/fpm/php5-fpm-test.conf`

    :::ini
    pid = /var/run/php5-fpm-test.pid
    error_log = /var/log/php5-fpm-test.log
    listen = 127.0.0.1:9001

Здесь я привел наиболее распространенные директивы, для общего сведения. `sudo nano /etc/php5/fpm/php-test.ini`

    :::ini
    display_errors = On
    post_max_size = 64M
    upload_max_filesize = 64M
    memory_limit = 32M
    
Запускаем наш тестовый php. 

    sudo /etc/init.d/php-test start
 
Можно создаться еще один блок `server` в Nginx и указать `fastcgi_pass   127.0.0.1:9001;`. Вот и все. 


### Настройка XCache
php сам по себе ни черта не умеет кешировать, поэтому очень тормазнутый. Так что давайте поставим акселератор php кода, для ускорени исполнения скриптов путём кэширования бинарного кода.

    sudo apt-get install php5-xcache
    sudo nano /etc/php5/conf.d/xcache.ini

Вот небольшой пример настройки

    :::ini
    ; zend_extension = /usr/lib/php5/20090626/xcache.so
    xcache.size = 64M	# хотя бы
    xcache.var_size = 32M
    xcache.count = 4		# количество ядер, в конфиге написанно как посмотреть
    xcache.cacher = On

Если вы заметили, то мы закомментировали строчку `zend_extension`. Это для того что бы включать ускоритель на отдельных php.ini. Если вы перезапустите php-fpm, то в `phpinfo()` увидите что раздела xcache, нету. Что бы включить его для отдельного php-cgi сервера надо скопировать `zend_extension = /usr/lib/php5/` в конец php.ini, перезапустить php. зайдите на _http://server_ip/test.php_ и убедитесь что xcache включен. 

На этом все. Коментарии и замечания по статье приветствуются.
