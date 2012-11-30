# title: Работа с процессами
# url: work-with-pids
# categories: [Ubuntu]
# tags: [Commands, Pids]
# time: 2009-10-03 17:25:23


![left](~hand.png)
При написание скиптов я часто встречался с проблемами проверки работы программы, или на оборот ее завершения. Приходилось как-то выкручиваться, изврашаться. Код становился некрасивым, да ешё за частую и бажным. В общем чувствовалась нехватка опыта и знаний окуржения.

Постепенно бродя по просторам интернета, я все же поднабрался дельных команд. С коими и хочу поделиться.

[more]

Первая стандартная утилита это ps

	ps -A | grep [Programm]

Но нужного нам Pid'а выводится еше много лишней информации. Это решается с помошью сложного AWK. И тогда будет нужный нам Pid.

	ps -A | grep [Programm] | awk '{print($1)}'

Второй способ и более наглядный это pgrep

	pgrep [Programm]

Ну вот вроде с поиском процессов разобрались. Теперь надо разобраться, а что собственно с ними делать.
Начнем с завершения процессов.

	kill `ps -A | grep [Programm]`
	kill `pgrep [Programm]`
	killall [Programm]
	pkill [Programm]

Если две первые думаю понятно что делают, то для последних двух стоит упомянуть. Например Killall требует точного названия процесса. А pKill является эквивалентом первых двух.

Переходим к установке приоритетов
Есть два способа. Первый - Стартовать программу с измененным приоритетом. Это хорошо для своих скрипов, скажем синхронизации.

	nice -n [Priority] [Programm]

Где [Priority] это число от -20 - высший приоритет, до 19 - низший приоритет. Только не стоит увлекаться с наивысшим, есть вероятность подвешивания системы.
Но этот метод не всегда приемлем. И приоритет надо менять уже на запущенных программах

	renice [Priority] `pgrep [Programm]`

Еше есть сетевая программка netstat, ей неплохо отслеживать порты.

	netstat -anp | grep [Programm]

Ну вот и вся наука :-)

Для более глубоких знаний изучаем маны.