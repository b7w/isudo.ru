# title: ruTorrent - Gui для rTorrent, замена uTorrent
# url: rutorrent-gui-dlya-rtorrent-zamena-utorrent
# categories: [HowTo, Ubuntu]
# tags: [rTorrent, ruTorrent, Torrent]
# time: 2009-07-30 18:14:16

![left](~ru-torrent.png)
ruTorrent это великолепный web интерфейс к rTorrent. С виду он очень напоминает знаменитый и, к сожалению, не заменимый uTorrent. По функциональности он довольно наворочен. Но главный его конек это удобство и красота :) ! В нем реализована например тажа система меток, что и в uTorrent. Так же он локализован на многие языки, не исключая русский. И проблем с кирилецей нет. Конечно нельзя не упомянут о плагинах, которые здоровски расширяют функционал и легки в использовании.

[more]

### В поисках
Вышел я на это чудо случайно. Я все больше разочаровывался в rtGui - моей первой web оболочки для rTorrent. Он слишком прост. Я стал задумываться о более продвинутом решение wtorrent. Про него много где написано и я подумал проблем не будет. Но я сильно ошибался, при попытке инсталляции мне была выкинута длинная ошибка. В коей я понял, что мне нужно поставить pdo (Php Data Objects). Нашел это: sudo apt-get install libmysqlclient15-de, sudo pecl install pdo, sudo pecl install pdo_mysql. После выполнения коих мой апач рухнул напроч. Я было думал все, переустанавливать систему, но помог uninstall. Прям как отлегло. :-) В поисках решений я вот и наткунулся на ruTorrent


### ruToorent
Собственно [сайт проекта](http://code.google.com/p/rutorrent/). Сайт русифицирован, так что проблем должно не возникнуть. [Общее описание](http://code.google.com/p/rutorrent/wiki/Main), [Плагины](http://code.google.com/p/rutorrent/wiki/Plugins?wl=ru). Закачать можно при помощи svn. Что я вам и советую сделать, что бы потом можно было легко обновляться, он должен быть установлен: `sudo apt-get install subversion`, прочитать как забирать версии можно [тут](http://code.google.com/p/rutorrent/wiki/GetFromSVN).
Могут возникнуть нехорошие ошибки что ruToorent не может прочитать файлы, записать новые. Это из за прав на директории. Необходимы примерно следующие манипуляции

    sudo chown -R www-data:www-data /var/www/
    sudo chmod -R 777 /var/www/rutorrent/share


### Плагины
Стоит сразу же поставить пару основных плагинов. 
`_getdir` и `DataDir` - Эти плагины позволят вам при добавлении торрентов получать навигацию по диску виде выпадавшего списка и указывать имя папки закачки. Единственный минус каталоги рекурсивно не создаются, только последний. 
`EraseData` - добавляет в контекстное меню закачки пункт "Удалить вместе с данными". Но тут не без ложки дегтя - не удаляет папки, особенно если вы при создании указали свою. Я борюсь с этим путем ежедневного вызова скипта удаления пустых папок.

    :::python
    #!/usr/bin/python
    # -*- coding: utf-8 -*-
    import os
    def Walker(root):
            for name in os.listdir(root):
                    fullpath = os.path.join(root,name)
                    if os.path.isdir(fullpath):
                            Walker(fullpath)
                            if os.listdir(fullpath) == [] :
                                    try:
                                            os.rmdir(fullpath)
                                            print 'Remove:',fullpath
                                    except Exception, e:
                                            print e
    os.nice(10)
    Walker('/path/to/torrents/')

Потом надо добавить в `sudo nano /etc/crontab` что нить типо `00 9   * * *   root    python /path/to/script.py > /dev/null`

`TrackLabels` - добавляет набор автоматически формируемых по трекерам меток закачек на панель категорий. Про другие плагины можно почитать на сайте в разделе wiki. `RPC и HTTPRPC` - плагины которые избавляют от надобности прослойки mod_scgi/RPC2. То есть можно использовать любой веб сервер с поддержкой php, что здоровости упрощают настройку. Единственный минус они требовательные к ресурсам. Особенно второй, он снижает трафик за счет более компактного протокола и передачи только измененных данных. Я бы посоветовал поставить второй, скорость самой GUI может прилично возрасти


### Устанка rtorrent
Ну и напишу уж про установку самого клиента до кучи. Ставить из родных репозитариев безболезно, там древние версии так еще и без поддержки xml-rpc, который обязателен для gui.
Сборка из исходников [здесь](http://isudo.ru/2009/10/rtorrent-compilation/).

### PHP

    sudo apt-get install screen sqlite php5-common php5-cgi php5-sqlite php5-xmlrpc unzip php5-curl

### Web Servers
Теперь нам надо определиться с выбором веб сервера и запуска транспорта между rTorrnet и GUI. Существует три решения: Apache, Nginx, Lighttpd. 
Мне нравиться Nginx за простоту конфигов, он не поддерживает SCGI, но я без лишних проблем поставил HTTPRPC плагин. Lighttpd такой же легкий, но более многофункционален и может поднимать SCGI. Apache я не люблю совсем, но думаю он уже у многих стоит, так что я все равно приведу настройки и для него.


### Nginx
У меня есть хорошая статья по настройке Nginx + php. [кликаем](http://isudo.ru/2011/01/nginix-php-fpm-xcache-various-php-ini/). Единственное вряд ли вам понадобиться раздел "Настройка второго сервера php-cgi", его просто пропустите. Дальше просто установите HTTPRPC плагин и радуйтесь.


### Lighttpd
Тут к сожалению я не силен и никогда не смотрел в эту сторону серьезно. вот то что заработало у меня. `sudo apt-get install lighttpd`
`sudo nano /etc/lighttpd/lighttpd.conf` Надо раскоментировать строчку 

    server.modules              = (
        ...,
        "mod_scgi"
    )

И добавить в конце

    $HTTP["url"] =~ "^/" {
      dir-listing.activate = "disable"
    }
    scgi.server = (
            "/RPC2" =>
                    ( "127.0.0.1" =>
                            (
                                    "host" => "127.0.0.1",
                                    "port" => 5000,
                                    "check-local" => "disable"
                            )
                    )
            )

`sudo /etc/init.d/lighttpd restart`


### Apache

    sudo apt-get install apache2 libapache2-mod-php5 libapache2-mod-scgi
    sudo nano /etc/apache2/sites-available/default

и дописываем перед `</VirtualHost> `

    #LoadModule scgi_module /usr/lib/apache2/modules/mod_scgi.so
    SCGIMount /RPC2 127.0.0.1:5000

Скорее всего модуль scgi_module уже подключен так что эта строчка закоментирована.
Перезагружаем `/etc/init.d/apache2 restart`


### Запуск rTorrent
Есть официальный вариант

    sudo wget http://libtorrent.rakshasa.no/attachment/wiki/RTorrentCommonTasks/rtorrentInit.sh?format=raw \
    -O /etc/init.d/rtorrent

или мой вариант, он проще намного и не глючит у меня:

    sudo wget http://isudo.ru[~rtorrent.sh] \
    -O /etc/init.d/rtorrent

Использование: start, stop, restart, status (по работе screen), запуск screen `sudo nano /etc/init.d/rtorrent` Меняем в строке `user="user", "user"` на Ваше имя пользователя. Теперь собственно добавляем в автозапуск, и стартуем rtorrent:

    sudo chmod +x /etc/init.d/rtorrent
    sudo update-rc.d rtorrent defaults
    sudo /etc/init.d/rtorrent start

Проверяем что у нас запустилось: `screen -dr rtorrent` Выходим: `Ctrl+A` затем жмём `D`.

Есть еще одна маленькая пакость, а именно то что rtorrent имеет свойство падать без каких либо причин. И единственный способ поправить это запускать его периодически если он лежит. `sudo nano /etc/crontab` 

    00  *   * * *   root    bash /etc/init.d/rtorrent start > /dev/null


### Конфиг rTorrent
Можете скачать мой вариант и отредактировать под себя. А вообще есть хорошее описание всех параметров на русском [тут](http://ru.wikibooks.org/wiki/RTorrent)

    wget http://isudo.ru[~rtorrent.rc] -O .rtorrent.rc
    nano .rtorrent.rc

Настраиваем под свои нужды!!! Незабываем прописывать свои пути!!!

Быстрых вам закачек!
