# title: PostgreSQL, мысли в слух
# url: postgresql-thoughts-about
# wordpress_id: 139
# categories: [Ubuntu]
# tags: [PostgreSQL]
# time: 2009-07-04 12:55:28


![left](~postgresql-logo.png)
Наткнулся я на СУБД под названием PostgreSQL. И стало что-то жутко интересно. Углубился в гугль и к несчастью толкового нашел мало. И это не от того, что данная СУБД плоха и не доходит до уровня собрата MySql. В общем она не очень популярна хоть и является мошным инструментом. Я не буду разводить "войны" MySql vs PostgreSQL, я лишь напишу сугубо свое мнение, которое сложилось у меня во время чтения статей и использования обоих программ.

[more]

Первый и думаю самый интересный вопрос будет: кто быстрее? Но тут зарыт топор, ибо статей сравнения производительности раз, два и обчелся. Я нашел этому только одно объяснения - пока никто не придумал средства тестирования. У каждого свой подход, свое железо, свои конфигурационные файлы, а на выходе полный бардак. Из того что я видел, я заключил: первое - Post много лучше на многоядерных системах (от 16 просессоров), второе - он лучше с реально огромными базами данных, третье - он быстрее на сложных вопросах. Хороший этому пример компании Skyp. Да да, у них стоит PostgreSQl и база на 350 мил. пользователей и обещания, что все будет работать до 1 миллиарда . Также они создали некоторые полезные штуки для базы, которые активно используются. Из выше сказанного я заключил, что эта СУБД хороша в приличных предприятиях со сложной структурой.

Наверное захочется задать следующих вопрос - а этих пунктов уже не достаточно, что бы не перейти на Post? Ну покрайне мере у меня таки промелькнула эта мысль. И я поставил себе. Первое что раздражает - очень мало информации.
Что бы разрешить пользователю конектится с другого ip надо прописывать в файл. И тут начинается магия. То что должно работать не работает, любые манипуляции безуспешны. А потом бац и заработала, с настройками которые ты уже пробовал. При попутке создать базу, он нагло ругался что кто-то уже копается в таблицы, бред какой-то. Так же работа на php с ним мене приятна чем с тем же MySQl. Возвращаемые ошибки совсем не информативны. В общем у меня сложилось мнение совсем не дружелюбной платформы. Может именно  по этому все веб программирование пишется под Mysql.

Все таки немного о производительности. Особо в конфигах я не лазил. Ибо там их напорядок больше чем в mysql, при том что я в последнем использовал часть готового. Еше можно упомянуть что встретился с проблемой SHMMAX (задает максимальный размер сегмента совместно используемой памяти) и SHMALL (максимальное выделение страниц совместно используемой памяти в системе). Расчитывается так: 128МБ * 1024 *1024 = 134217728. прописывается в `/proc/sys/kernel/shmmax` и `/proc/sys/kernel/shmall` разово или для для каждой загруски системы в `/etc/sysctl.conf`

	kernel.shmmax=134217728
	kernel.shmall=134217728

Я использовал базу данных GeoLiteCity. Она свободно распространяется, имеет примерно 4,1млн записей в одной таблице и 250 во второй всего мегабайт на 125. Я написал запрос объединения и выборки русских регионов. И стоит отметил что Post слегка по бысрее. Но следующее что я заметил, при повторных запросах Post опять уходит в расчеты, когда MySql откидывает все из кэша. Может я где-то промахнулся с настройкой, но в нете больше информации не нашел по этому вопросу. Кстати это ешё один плюс в сторону Mysql, ведь обычно веб используют одни и те же запросы и если их кешировать, то можно резко повысить скорость.

Кстати говоря:

 * MySQL - это ПРОДУКТ с открытым исходным кодом. За этими словами стоит сильная компания SUN которая в последнее время водиться с Oracle. Это явный плюс
 * PostgreSQL - это ПРОЕКТ с открытым исходным кодом. Принять участие может любой желающий.  Это же и минус. Так как нет того, кто бы ее продвигал.

На этом я заканчиваю мою сумбурную записку, ибо добавить особо нечего. Опять повторюсь обе СУБД очень хорошие. Просто мне кажется у них разные области применения.

Ресурсы для ознакомления:

 * Неплохое детальное сравнение Mysql и PostgreSQL [link](http://madjack.ru/developer/2009/08/mysql-vs-postgresql.html)

_Так же буду безгранично рад, если кто то дополнит данную информацию и просветит народ._
