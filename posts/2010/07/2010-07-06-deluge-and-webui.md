# title: Deluge and WebUI
# url: deluge-and-webui
# categories: [HowTo, Ubuntu]
# tags: [Deluge, Torrent]
# time: 2010-07-06 15:51:08


![left](~deluge-logo.jpg)
Наиболее часто домашние серверы задумываються как торрен качалки. И конечно с хорошим веб интерфейсом. Я уже писал про связку rtorrent и rutorrent, но у многих так и не получаеться собрать исходники. Конечно можно поставить transmission, но он до ужаса простой. Но тут недавно выяснилось, как всегда случайно, что у нового Deluge появилась нормальная Web Gui. Да и сам торрент клиент являеться демоном, что и нужно для сервера.

[more]

Кстати говоря опотребляемых ресурсах. Говорят что rtorrent очень экономичен, но это не совсем правда. При установки Web Gui необходимо ставить тяжелый php и какой-нибудь веб сервер в придачу, что легко в сумме перегоняет Deluge. Хватит преамбулы, к установке.

    sudo apt-get install python-software-properties
    sudo add-apt-repository ppa:deluge-team/ppa
    sudo apt-get update
    sudo apt-get install deluged deluge-webui

Теперь надо создать пару конфигурационных файлов для запуска `sudo nano /etc/default/deluge-daemon` И добавляем в него следующее.

    # Configuration for /etc/init.d/deluge-daemon

    # The init.d script will only run if this variable non-empty.
    DELUGED_USER="deluge"

    # Should we run at startup?
    RUN_AT_STARTUP="YES"

    # Do not change this
    LANG="enUS"

Загружаем скрипт запуска

    sudo wget http://isudo.ru/files/deluge-daemon -O /etc/init.d/deluge-daemon
    sudo chmod 644 /etc/init.d/deluge-daemon
    sudo chmod +x /etc/init.d/deluge-daemon
    sudo update-rc.d deluge-daemon defaults
    sudo /etc/init.d/deluge-daemon start

Теперь только надо зайти на [http://localhost:9092](http://localhost:9092/) вбить стандартный пароль "deluge" и наслаждаться новым многофункциональным клиентом.

Правдо не обошлось без ложки дектя. На моем любимом Chrome дальше таблички ввода пароля дело не полшло, вобшем как и на Opera. Надеюсь это только на моих версиях. в FireFox все прошло на ура. Дальше еше веселее, даже стандартные плагины выкидывали ошибки в лог и не хотели запускаться. Похоже извечная проблема кодировок в питоне, я даже не стал разбираться.

Что мы имеем в сухом остатке. Отличный веб интерфейс. Действительно большой функционал и полная настройка без конфигов. Одни из наиболее важных моментов это установка пути закачки, ограничения для отдельных торрентов, а так же выбор файлов для закачки. А так же многое другое.

Deluge GUI по дефолту умеет много больше чем rutorrent, да и являеться цельной системой. А с плагинами можно еше расширить функционал. Но тем не менее я не рвусь поставить его себе на рабочию машинку ибо мне он показался сыроват. Но на заметку взять его точно стоит.
