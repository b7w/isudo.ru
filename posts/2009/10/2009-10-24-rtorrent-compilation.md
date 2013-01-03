# title: Собираем rTorrent из исходников
# url: rtorrent-compilation
# categories: [HowTo, Ubuntu]
# tags: [rTorrent, SVN, Torrent]
# time: 2009-10-24 12:02:14


![left](~transmission-logo.png)
При установке rTorrent из репозитария мы получаем очень старую версию. И все бы ничего, но библиотека xmlrpc-c, тоже очень древняя и как в следствие мы получаем урезанное Gui управление. Например в моем любимом ruTorrent невозможно даже управлять скоростью закачки. Так же с rTorrent бывают проблемы на некоторых трекерах, хотя может все дело в конфиге  , так что последняя сборка нам не помешает!

[more]

[Появилась более свежая и полная статья!](http://isudo.ru/2011/09/rtorrent-compilation-2/)

Ничего военного в компиляции нету, но все же лучше потренироваться где нить на виртуальной машине :)

План прост как никогда, мы ставим xmlrpc-c. Потом libtorrent. Ну и на закуску нашего клиента с поддержкой xmlrpc . Исходники будем забирать по SVN. Это удобно и так будет легко следить за последними билдами.

Нам потребуется следуюшее, тут много чего но может не все. При сборке должно будет высветиться нужные еше пакеты.

	sudo apt-get install checkinstall subversion build-essential make autoconf autotools-dev automake libtool libcurl4-openssl-dev libsigc++-2.0-dev pkg-config libncurses5-dev

Теперь нам надо удалить старые установленные пакеты, если они есть.

	sudo apt-get remove rtorrent libtorrent11 libxmlrpc-c3 libxmlrpc-c3-dev libxmlrpc-core-c3 libxmlrpc-core-c3-dev

Небольшое отступление. Наверное все слышали про make install, но этот способ далек от идеала. Система не знает о программе, бинарники валяются где им хочется и главное их потом сложно удалить. Для этого придумали такую штуку как checkinstall. Она собирает нормальный deb пакет, привычный для системы. Я буду пользоваться этим способом. Но так же можно и старым.

В последних версиях svn твориться какая-то фигня, а ruTorrent 3.0 поддерживае rTorrent до 1148 билда (это '-r1148'  ключ к svn). Так что я приведу еше рабочие строчки для сборки из заархивированных пакетов с сайта. Проверено на Ubuntu Server 10.04 beta1.

	:::bash
	svn co https://xmlrpc-c.svn.sourceforge.net/svnroot/xmlrpc-c/advanced xmlrpc-c
	cd xmlrpc-c
	./configure --prefix=/usr
	make
	sudo checkinstall -D

	cd ..
	# svn co svn://rakshasa.no/libtorrent/trunk
	# cd trunk
	# cd libtorrent
	wget http://libtorrent.rakshasa.no/downloads/libtorrent-0.12.6.tar.gz
	tar zxfv libtorrent-0.12.6.tar.gz
	cd libtorrent-0.12.6
	./autogen.sh
	./configure --prefix=/usr
	make
	sudo checkinstall -D

	# cd ../rtorrent
	cd ..
	wget http://libtorrent.rakshasa.no/downloads/rtorrent-0.8.6.tar.gz
	tar zxfv rtorrent-0.8.6.tar.gz
	cd rtorrent-0.8.6
	./autogen.sh
	./configure --with-xmlrpc-c --prefix=/usr
	make
	sudo checkinstall -D

Вот в общем и все, теперь настраивать сам клиент [кликаем](http://isudo.ru/2009/07/rutorrent-gui-for-rtorrent/)

Статья написана по мотивам [темы на форуме](http://forum.ubuntu.ru/index.php?topic=70377.0) и [Этой статьи](http://www.permlug.org/node/3941/), спасибо ее Автору за сборку xmlrpc
