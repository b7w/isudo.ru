# title: Приколы с KDE
# url: bugs-with-kde4
# categories: [Ubuntu]
# tags: [KDE]
# time: 2009-01-20 17:47:39

![left](~about-kde.png)
Вот решил посмотреть "красивый линукс", то есть Kde. Быстро смог найти, что существует дистрибутив Ubuntu c предустановленным Kde 4. Собственно что-то точное про эту рабочию среду можно найти на [Wikipedia](http://ru.wikipedia.org/wiki/KDE). Через минут сорок у  меня уже лежал новенький дистрибутив Kubuntu, и вперед ещё одна виртуальная машина. Установка идентична и не заняла много времени и проблем. Кстати Kde можно установить и на обычную Ubuntu, но это я узнал позже.

[more]

Kde 4 действительна красива. Немного не привычно сначала, но  поработав пол часика все кажется логичным и простым. Много настраиваемых спец эффектов, да и вообше много настроек, визуальную систему можно хорошо подогнать под себя. Я много читал что Kde тормознее чем Gnome, но я ничего не заметил. А на каком-то форуме даже увидел, что она ещё и меньше кушает памяти и процессов.

Самое интересное началось дальше. При попытке обновиться была выплюнута какая-то фатальная ошибка по середине процесса, но все удачно закончилось и не выкинуло из процесса. Странно не правда? ладно думаю работаешь и работаешь. Перезагружаемся, все путем картинки  свои выкидывает, пользователя просит. Но..но что это?! Емаё! Он загрузил Gnome! Вот это он дал.. Я вообще предполагал, что в этом дистрибутиве таковой отсутствует. Что то изменить и вернуть Kde не получилось.

Порывшись ещё немного в нете, случайно наткнулся на возможность установить Kde прямо повер Gnome на Ubuntu. Думаю дай попробую мож что лучше получиться. Но на всякий случай скопировал виртуалку.

### Установка Kde 4 на Ubuntu
Заходим в Система →  Администрирование → Sinaptic. Находим kubuntu-desktop отмечаем его галочкой и давим применить, дальше соглашаемся. Грузяться пакеты, в конце вылетает предложение выбрать стандартную рабочию систему gdm - Gmome или kde, выбираем. Дальше что бы зайти в Kde надо выйти из системы - сменить пользователя (log out). Дальше  нам предложат войти в систему, но прежде  нам надо зайти в настройки (в низу экрана)  → сессии и выбрать Kde. Вуаля регимся и наслаждаемся Kde. Ещё маленькая деталь, там будет английский язык. Надо установить русский и выбрать его как основной. Это не сложно, я думаю можно и самим разобраться.

Но приколы не закончились! При загрузке каких-то значков и попытке настроить эффекты, ОС встала в ступор и больше не подавала признаков жизни :-( Хорошо что я клонировал систему.

Признаться я был удивлен. Такая нестабильность меня поразила. В общем понятно почему сейчас все дистрибутивы используют Gmone - он надежнее. Но надеюсь разработчики что-нибудь придумаю не только красивое, но и стойкое. И тогда можно будет пересесть на Kde, ведь она действительно приятна и удобна.
