# title: Делаем FTP и Web FileShare
# url: create-ftp-web-filshare
# categories: [HowTo, Scripts, Ubuntu]
# tags: [FileShare, FTP, HomeServer, HowTo]
# time: 2010-12-30 15:10:15


![left](~file-share.png)
Не знаю как вас, но меня уже давно задолбал глючный падающий FTP протокол. Периодически слышу от друзей: не работает, не загружает, а как им пользоваться? В общем я серьезно задумался над запуском какого нибудь простенького Web файл менеджера. К сожалению такой подход не давал простой загрузки папок и файлов. И отказаться полностью от FTP не получилось. Так что моей задачей стала объедение пользователей двух систем. Чем мы и займемся :-)

[more]

FTP у меня стоит Pure-FTPd. Man [здесь](http://forum.ubuntu.ru/index.php?topic=16733.msg115844#msg115844). Мне просто он больше всего нравится.Встроенная поддержка многих СУБД. Контроль над uid gid пользователя, ограничения его по IP и а главное он сам умет создать директорию пользователя, если такой нет. Там еще есть ограничения по скорости и еще что-то. Но я этим не пользуюсь. Хотя при желании можно использовать и другие FTP сервера, лишь бы в них можно было выбирать информацию из MySql своими запросами.

С Web File Share все намного сложнее. Их очень много, и я даже нашел пару красивых движков на Ajax, например [AjaxPlorer](http://www.ajaxplorer.info/wordpress/). Но вскоре отказался в пользу [File Thingie](http://www.solitude.dk/filethingie/). Потому что они все жутко тормозные и глючные, и еще хранят гигами какой-то непонятный cache. Да и с мобильных на них заходить бесполезно. Ну и в конце концов простой php file manager проще под себя переписывать.

Давай те посмотрим, а что же нам надо реализовать. Для прав записи в FTP нам нужен соответствующий пользователь в системе, а точнее его ID. Для Web Share нам просто нужны флаги на право изменять, создавать, закачивать. плюс к обоим еще и на просмотр. Не плохо правда? Совершенно разные поля, и если посчитать то шесть штук. Многовато конечно, зато при таком раскладе можно будет по отдельности вкл/выкл протоколы.

Поговорим о модели. В силу того что в File Thingie есть пользователи и группы, я решил не отходить от этой структуры. Если с группой все просто, там будет храниться только путь к домашней папке. То с пользователями посложнее. Тут я еще добавил статус пользователя и список IP. А так как у нас получилось прилично прав, то мы их тоже вынесем в отдельную таблицу. Так мы сможем в дальнейшем добавлять какие-то свои флаги без особых проблем и потери наглядности. Давайте уже напишем сами таблицы.

    :::sql
    CREATE TABLE `Users` (
    	`id` INT(10) NOT NULL AUTO_INCREMENT,
    	`Pid` INT(10) NOT NULL COMMENT 'Permission ID',
    	`Gid` INT(10) NOT NULL COMMENT 'Goup ID',
    	`Status` ENUM('0','1') NOT NULL DEFAULT '0',
    	`User` VARCHAR(16) NOT NULL,
    	`Password` VARCHAR(16) NOT NULL,
    	`IPAccess` VARCHAR(512) NOT NULL DEFAULT '*' COMMENT 'Split IP by \';\'',
    	`Comment` TEXT NULL,
    	PRIMARY KEY (`id`),
    	UNIQUE INDEX `User` (`User`)
    )
    COLLATE='utf8_general_ci'
    ENGINE=MyISAM
    ROW_FORMAT=DEFAULT

    CREATE TABLE `Groups` (
    	`id` INT(10) NOT NULL AUTO_INCREMENT,
    	`Name` VARCHAR(16) NOT NULL DEFAULT '',
    	`Dir` VARCHAR(64) NOT NULL,
    	PRIMARY KEY (`id`),
    	UNIQUE INDEX `id` (`id`)
    )
    COLLATE='utf8_general_ci'
    ENGINE=MyISAM
    ROW_FORMAT=DEFAULT
    
    CREATE TABLE `Permissions` (
    	`id` INT(10) NOT NULL AUTO_INCREMENT,
    	`Name` VARCHAR(32) NOT NULL DEFAULT '',
    	`FTP_Read` ENUM('0','1') NOT NULL DEFAULT '1' COMMENT 'All privileges for FTP',
    	`FTP_Write` ENUM('0','1') NOT NULL DEFAULT '0' COMMENT 'All privileges for FTP',
    	`Share_Read` ENUM('0','1') NOT NULL DEFAULT '1' COMMENT 'To view data via Share',
    	`Share_Action` ENUM('0','1') NOT NULL DEFAULT '0' COMMENT 'Set to FALSE if you want to disable file actions (rename, move, delete, edit, duplicate)',
    	`Share_Create` ENUM('0','1') NOT NULL DEFAULT '1' COMMENT 'Set to FALSE if you want to disable file/folder/url creation',
    	`Share_Upload` ENUM('0','1') NOT NULL DEFAULT '1' COMMENT 'Set to FALSE if you want to disable file uploads',
    	PRIMARY KEY (`id`),
    	UNIQUE INDEX `id` (`id`)
    )
    COLLATE='utf8_general_ci'
    ENGINE=MyISAM
    ROW_FORMAT=DEFAULT

Ну и вставим пользователя

    :::sql
    INSERT INTO `Permissions` (`Name`, `FTP_Read`, `FTP_Write`, `Share_Read`, `Share_Action`, `Share_Create`, `Share_Upload`) VALUES ('All Permission', '1', '1', '1', '1', '1', '1');
    
    INSERT INTO `Groups` (`Name`, `Dir`) VALUES ('Sample Share', 'share/Sample_Share');
    
    INSERT INTO `Users` (`Pid`, `Gid`, `Status`, `User`, `Password`, `IPAccess`, `Comment`) VALUES (1, 1, '1', 'B7W', '123', '*', 'Первый юзвер!');

Я думаю тут более менее все понятно. Кроме пару моментов. Начнем с `IPAccess`. Сюда можно писать IP адреса с которых возможен вход или '*' для любого. Выбирать эти адреса мы будем с помощью `LIKE "%UserIP%"`, поэтому нам плевать чем мы будем разделять их между собой.
Поле `Dir`, скажете что здесь может быть?! Очень даже может. Самая подлянка зарыта как раз тут. У нас FTP хочет абсолютный путь к папке, а File Thingie подавай относительный от его места установки. Я решил эту проблему монтированием данных к папке с File Thingie. И в базе пишем относительный путь, для FTP просто прибавим недостающий кусок. И `FTP_Write`. А штука здесь в том, что нам то надо системный ID пользователя, а у нас `0/1`. Я извернулся и сделал выборку так:

    :::sql
    SELECT IF( Permissions.FTP_Write=1,"2001","33") as UiD...

Если 1, то вернеться 33, в противном случае 2001. 33 - это www-data, чьи и все данные, что бы можно было изменять через файлы из php. 2001 - пользователь FTP, просто что бы просматривать файлы. Немножко заморочено, но мне так больше нравиться.

Собственно давайте напишем sql запросы для FTP, все что было раньше в конфигурационном файле связанное с ними надо закоментить.

    :::sql
    MYSQLGetPW	SELECT Password FROM Users LEFT JOIN Permissions ON Users.Pid = Permissions.id WHERE User="\L" AND Status="1" AND FTP_Read="1" AND (IPAccess = "*" OR IPAccess LIKE "%\R%");
    
    MYSQLGetUID	SELECT IF( Permissions.FTP_Write=1,"2001","33") as UiD FROM Users LEFT JOIN Permissions ON Users.Pid = Permissions.id WHERE User="\L" AND status="1" AND FTP_Read="1" AND (ipaccess = "*" OR ipaccess LIKE "%\R%");
    
    MYSQLGetGID	SELECT IF( Permissions.FTP_Write=1,"2001","33") as UiD FROM Users LEFT JOIN Permissions ON Users.Pid = Permissions.id WHERE User="\L" AND status="1" AND FTP_Read="1" AND (ipaccess = "*" OR ipaccess LIKE "%\R%");
    
    MYSQLGetDir	SELECT CONCAT("/Path/to/Share/",Dir) as Dir FROM Users LEFT JOIN Groups ON Users.Gid = Groups.id LEFT JOIN Permissions ON Users.Pid = Permissions.id WHERE User="\L" AND Status="1" AND FTP_Read="1" AND (IPAccess = "*" OR IPAccess LIKE "%\R%")

Вот, не забудьте поменять путь `/Path/to/Share/` на ваш в последней стр. FTP настроен. Можно зайти и проверить. Переходим к Web GUI. Прям напишем сразу код.

    :::xml+php5
    # Rewrite Users data
    $ft['groups'] = array();
    $ft['users'] = array();
    
    # Create dir in new groups if not exist.
    $ft["settings"]["CreateDIR"] = TRUE;
    
    $ft["settings"]["DBHost"] = "localhost";
    $ft["settings"]["DBUser"] = "";
    $ft["settings"]["DBPass"] = "";
    $ft["settings"]["DBName"] = "";
    
    $ft["settings"]["Sql"] = "SELECT `User`,`Password`,`Groups`.`Name`,`Dir`,`Share_Action`,`Share_Create`,`Share_Upload`
    		FROM `Users`
    		LEFT JOIN Groups ON Users.Gid = Groups.id
    		LEFT JOIN Permissions ON Users.Pid = Permissions.id
    		WHERE `Users`.`Status` = '1' AND `Permissions`.`Share_Read` = '1';";
    
    mysql_connect($ft["settings"]["DBHost"],$ft["settings"]["DBUser"],$ft["settings"]["DBPass"]) OR DIE("Can not connect!");
    mysql_select_db($ft["settings"]["DBName"]) or die("Can not select DB"); 
    
    $sql_res = mysql_query($ft["settings"]["Sql"]) or die("Can not execute query");
    
    while ($row=mysql_fetch_array($sql_res)) {
    
    	$ft['users'][ $row['User'] ] = array(
    		'password' => $row['Password'],
    		'group' => $row['Name']
    	);
    
    	$FA = False;	if($row['Share_Action']) $FA = True;
    	$CR = False;	if($row['Share_Create']) $CR = True;
    	$UP = False;	if($row['Share_Upload']) $UP = True;
    
    	if ( (file_exists($row['Dir']) == false) && $ft["settings"]["CreateDIR"] ) mkdir($row['Dir'], 0700,true);
    
    	$ft['groups'][$row['Name']] = array(
    		'DIR' => $row['Dir'],
    		'FILEACTIONS' => $FA,
    		'CREATE' => $CR,
    		'UPLOAD' => $UP
    	);
    }

Вот и весь скрипт. Не забудте прописать Базу Данных. После надо в основной файл добавить `include('name.php');` после всех настроек. Еще на всякий в FILEBLACKLIST добавить этоже имя файла.

Можно конечно закончить, если бы не одна "хня". А именно, когда мы удаляем пользователя, в то время как он листает каталоги, Он по волшебству ни черта не отрубается, а получает глобальные права. Клева - да? Я написал автору, так что ждем обновлений. А пока мы сделаем хак. По отключаем все глобальные права и поставим неправильный путь. Так что максимум что увидит отключеный пользователь - это "Не могу отобразить каталог".

    :::xml+php5
    # turn off admin
    $ft["settings"]["DIR"] = "LoL";
    $ft["settings"]["UPLOAD"] = FALSE;
    $ft["settings"]["CREATE"] = FALSE;
    $ft["settings"]["FILEACTIONS"] = FALSE;

Вот теперь полный порядок. Думаю на этом можно и закончить статью.
