# title: Пишем Админку на shell
# url: write-admin-on-shell
# categories: [Programming, HowTo, Ubuntu]
# tags: [AdminGui, Shell]
# time: 2009-06-25 20:10:50


![left](~shell.jpg)
Думаю после некоторого времени работы с командной строкой надоедает бить одни и теже команды, и даже не помогает что они запоминаются. Да что уж говорить, порой просто забываешь где что лежит. Особенно стало надоедать выставлять разные права доступа на файлы веб сервера. Я уже давно подумывал написать что-то для управления всей этой радостью. И вот последней каплей стало то, что надо было выполнять над севером некоторые действия людям совершенно не разбираюшимся в Linux.

[more]

Я выбрал путь одно файла. Хоть у меня и были уже некоторые скриты резервирования конфигов, баз данных. Но мне захотелось что бы все было в одном файле и легко копировалось. Особенно очень удобно держать этот скрипт у себя на веб сервере и с помошью команды wget заливать на новую виртуальную машину. Если все же необходимо подключить какой-то скрипт, то можно реализовать так:

	. /path/to/script или source /path/to/script

Или если надо запустить уже существующий:

	bash /path/to/script

Разместить скрипт луше всего или у себя в домашней директории или прямо в файловой системе. Название придумать покороче, что бы вбивать его не надоедало.

Что бы скрипт хоть немного напоминал подобие меню мы будем использовать команду clear и нашу функцию myecho. Первая очишает экран. Последняя будет выводить просьбу что-нить нажать, что бы продолжить работу. Это необходимо для т, что бы мы увидели ошибки, пока экран не очистился. Вот сама функция, она же будет началом скрипта.

	:::bash
	#!/bin/bash
	myecho() {
		echo
		echo Нажмите Enter для продолжения
		read
	}

Дальше само меню у нас будет состоять из обычного цыкла while и case. Для человека хоть немного знакомого с програмирование говорить нечего. В обратном случае гугль вам в помошь, хотя на примере думаю понятно будет.

	:::bash
	#!/bin/bash
	n=1
	while [ "$n" -ne 0 ];
	do
		clear
		echo -= Admin panel =-
		echo 1 — chmod 777 for www
		echo 2 — Web server Status
		echo Введите номер меню
		echo или 0 для выхода.

		case $n in
			0)
			echo Bye! Made by BW on iSudo.ru
			;;

			1)
			sudo chmod 777 -R /var/www/
			myecho
			;;

			2)
			sudo /etc/init.d/apache2 status
			sudo /etc/init.d/mysql status
			myecho
			;;

			*)
			echo —==Не верная команда==—
			;;
		esac
	done
	exit 0 # конец выполнения програмы

Еше можно реализовать структуру IF. У меня она выполняет функцию открыть лог файл или вывести последение 10 строк. Все запихнуто в цикл, что бы выводилось пока ответ не будет правильный y/n.

	:::bash
	#!/bin/bash
	flag=0
	while [ $flag = 0 ];
	do
		echo Отркрыть файл? Или вывести 10 последних стр? {y/n}
		read n2
		if [ $n2 = "y" ]
		then
			sudo nano /var/log/apache2/error.log
			flag=1
		fi

		if [ $n2 = "n" ]
		then
			sudo tail /var/log/apache2/error.log
			flag=1
		fi
	done

Вот вообшем и весь скрипт. Это я конечно образно. У меня уже почти 600 строк в своем. Но принцип один и тот же. В каждом елементе case еше case.

Вобшем пишем свои админки, ибо хороший Админ - ленивы Админ :-)
