# title: MySql and Files BackUp
# url: mysql-and-files-backup
# categories: [Programming, Ubuntu]
# tags: [BackUp, MySql, Python, rdiff-backup]
# time: 2011-01-06 21:18:21


![left](~meliae-trashcan.png)
Я уже давно собирался сделать человеческий скрипт резервного копирования MySql, что бы каждый раз не лазить и не править. Вот я на праздниках и решил написать. Заодно еще решил туда впаять и [rdiff-backup](http://www.nongnu.org/rdiff-backup/), что бы и файлы можно было резервировать, к стати путем incremental backups.

[more]

Скрипт написан на Python и хорошо закоментирован. Так что он легко поддается изменению. Самого кода не так много, меньше 300 строк. Плюс конфигурационный файл. Давайте я перечислю возможности.

  * Скрипт может сохранят отдельные базы в отдельные дни. По средством `mysqldump`
  * Сохранение всех баз
  * Удаление старых дампов
  * Добавление ключей к mysqldump
  * Возможность задания шаблона файла, например '/2011-01/2011-01-06/2011-01-06-Name'. 
  * Вывод ошибок в лог
  * Вывод уведомлений в лог
  * Отправка ошибок на email
  * Backup через rdiff-backup по дням недели
  * Указание доп. ключей
  * Указание папок для --exclude
  * Удаление старых копий
  * Вызов отдельных заданий через аргументы
  * Вызов всех заданий через аргумент

Скачать можно либо через mercurial `hg clone http://hg.isudo.ru/Projects/pyBackup/` либо [архивом](http://hg.isudo.ru/Projects/pyBackup/archive/tip.tar.gz) или даже [посмотреть](http://hg.isudo.ru/Projects/pyBackup/)  

Если вас привлек скрипт то необходимо произвести следующие операции для его установки.
Для скрипта нам понабиться установить драйвер MySQL для python и сам rdiff-backup. Конечно сам MySQL должен быть уже установлен :-)

    :::sh
    sudo apt-get install rdiff-backup
    sudo apt-get install python-mysqldb

Надо добавить в cron для ежедневного запуска `sudo nano /etc/crontab`. Вот примерно такую строчку для пуска в 5:00

    00 05   * * *   root    python /path/to/BackUp.py all

Еще надо позаботиться что бы хватало прав для записи в лог файл. Надеюсь скрипт поможет вам дорогой читатель.
