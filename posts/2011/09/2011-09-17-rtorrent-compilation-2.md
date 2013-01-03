title: Собираем rTorrent из исходников 2
url: rtorrent-compilation-2
categories: [HowTo, Ubuntu]
tags: [rTorrent, Torrent]
time: 2011-09-17 21:27:03


![left](~transmission-logo.png)
В версиях Ubuntu до 10.10 включительно при установке rTorrent из оригинальных репозиториев, мы получаем весьма старую версию библиотек и саму программу, собранную без поддержки некоторых важных функций. Для корректной работы WebGUI, таких как ruTorrent, wTorrent и пр. необходимо обновить эти библиотеки и пересобрать rTorrent с поддержкой функций этой библиотеки.

[more]

Статья ориентирована на пользователей Ubuntu до версии 10.10 включительно.

Ничего особенно сложного в этом нет. План прост – собрать свежую версию библиотеки xmlrpc-c. Не ниже 1.11.0, на момент написания статьи – 1.16.38. А так же пересобрать libtorrent/rtorrent с поддержкой этой самой xmlrpc-c. Соберем deb-пакеты с помощью checkinstall. Это позволит нам в дальнейшем легко удалить их с помощью apt или aptitude. 

Если в системе уже установлены старые версии – удаляем их:

    sudo apt-get --purge remove libxmlrpc-core-c3 libxmlrpc-core-c3-dev libxmlrpc-c3 libxmlrpc-c3-dev libtorrent11 libtorrent11-dev rtorrent

Теперь устанавливаем необходимые для сборки пакеты:

    sudo apt-get install build-essential checkinstall libcurl4-openssl-dev libncurses5-dev libncursesw5-dev libsigc++-2.0-dev libtool

Зависимости потянут за собой еще несколько связанных пакетов. Замечу что категорически рекомендуется помимо `libncurses5-dev` ставить библиотеку `libncursesw5-dev`, чтобы в rtorrent могли корректно отображаться пути, содержащие русские буквы.

Если планируется собирать из svn, то нужно доустановить еще несколько пакетов:

    sudo apt-get install subversion autoconf automake 

В системах контроля версий, в нашем случае svn, можно всегда забрать последние свежие версии – но новое не означает лучшее. Я предпочитаю собирать программы из tarball’ов. Это упакованные tar’ом исходные тексты стабильных версий.

Подготовка закончена, можно начинать. Создаем отдельную папку, где мы будем производить все манипуляции:

    mkdir ~/src
    cd ~/src

Стабильные версии xmlrpc-c всегда доступны на Sourceforge [здесь](http://sourceforge.net/projects/xmlrpc-c/). Скачиваем архив с исходниками: [xmlrpc-c-1.16.38.tgz](http://sourceforge.net/projects/xmlrpc-c/files/Xmlrpc-c%20Super%20Stable/1.16.38/) и переносим в рабочую папку. Можно приступать, выполняем в консоли:

    :::sh
    tar xvzf xmlrpc-c-1.16.38.tgz
    cd xmlrpc-c-1.16.38
    ./configure --prefix=/usr
    make
    checkinstall

Думаю стоит немного пояснить команды. Первой мы распаковываем архив с исходниками в рабочую папку. Третья – команда конфигурирования, проверяет наличие необходимых для сборки файлов и создает Make-файлы (правила для компиляции). Опция `--prefix=/usr` указывает куда следует устанавливать скомпилированные файлы. По умолчанию они установятся в каталоги '/usr/local/bin' и '/usr/local/lib', что позволяет иметь одновременно и программу, установленную из репозиториев, и собственноручно собранную. В данном случае скомпилированные бинарники и библиотеки установятся в '/usr/bin' и '/usr/lib' соответственно. Четвертая - команда компиляции и пятая - запускает процесс сборки deb-пакета. 

При создании пакета вас попросят добавить описание пакета - тут уж все на ваш вкус. Единственное может появиться ошибка несоответствия версии стандарта deb и версии из исходных текстов. Просто скопируйте версию вида x.x.x из названия tarball’а. В остальном ничего править не обязательно, поэтому смело нажимайте Enter.

Если вы используете svn необходимо вызвать `./autogen.sh` перед `./configure` при сборке libtorrent и rtorrent.

Теперь приступим к сборке libtorrent:

    :::sh
    cd ~/src
    wget http://libtorrent.rakshasa.no/downloads/libtorrent-0.12.9.tar.gz
    tar xvzf libtorrent-0.12.9.tar.gz
    cd libtorrent-0.12.9
    ./configure --prefix=/usr --with-posix-fallocate
    make
    checkinstall

Опция `--with-posix-fallocate` позволяет избежать фрагментации скачиваемых торрентов путем выделения места на диске сразу под весь объем файла(ов). Что бы включить эту функцию в самой программе добавьте строчку `system.file_allocate.set = yes` в конфигурационный файл.

Собираем rtorrent:

    :::sh
    cd ~/src
    wget http://libtorrent.rakshasa.no/downloads/rtorrent-0.8.9.tar.gz
    tar xvzf rtorrent-0.8.9.tar.gz
    cd rtorrent-0.8.9
    ./configure --prefix=/usr --with-xmlrpc-c
    make
    checkinstall

Все готово, теперь настраивать сам клиент [кликаем](http://isudo.ru/2009/07/rutorrent-gui-for-rtorrent/)

Статья предоставлена `DelphiN91`, [тема на ruTracker.org](http://rutracker.org/forum/viewtopic.php?p=47583579#47583579).

По любым проблемам и вопросам милости просим в комментарии.
