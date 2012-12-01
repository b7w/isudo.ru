# title: Fabric автоматизация проектов
# url: fabric-projects-automation
# categories: [HowTo, Scripts, Ubuntu]
# tags: [Commands, Fabric, HowTo, Python, Shell]
# time: 2011-11-23 12:06:17


![left](~fabric.png)
В очередной раз вызывая длинный набор команд запуска тестов, понял что хватит этих портянок. Первое что пришло в голову просто написать shell скрипт. Быстро, но не особо расширяемо. Хотелось что-нибудь на python. И действительно, оказалось такое есть. Называеться Fabric.

Одно из самых интересных штук которые fabric умеет делать, это ходить по разным хостам через ssh и выполнять команды, а также копировать файлы.
При этом мы сохраняем всю мощь и гибкость языка python. 

[more]

Давайте установим последнею версию. 

    sudo pip install fabric

Поведение fabric очень похоже на make. В каталоге надо создать файл `fabfile.py`. И вызвать его `fab task:args task2:args`. Если же надо запустить файл в другой директории, например по cron, надо передать путь в параметре `-f`
А теперь давайте сделаем простенький скрипт для запуска тестов django проекта.

    :::python
    from fabric.api import env
    from fabric.context_managers import lcd, hide, cd
    from fabric.operations import local, abort, put, sudo
    
    __all__ = ['test']
    env.hosts = [u"user@anotherhost:22"]
    env.passwords = { u"user@anotherhost:22" : u"pass" } 
    
    def test( app=u"limited", setting=u"settings" ):
        """
        Run django test. Args - app=limited, setting=2
        """
        local( u"clear" )
        local( u"echo '' > app.log" )
        local( u"manage.py test {app} --settings={set}; return 0".format(app=app, set=setting))
        local( u"cat app.log" )

Давайте посмотрим что тут произошло. Мы объявили задание `test` с двумя аргументами. Их можно будет передать так:
    
    fab test:limited,2
    fab test:app=limited,setting=setting2

В массиве `__all__ ` мы перечислим какие функции можно использовать как задания. Кстати первая строка комментариев функции идет как документация к заданию. Список всех заданий можно посмотреть так `fab -l`. `env.hosts` хранит массив все хостов на которые надо зайти и отработать задание. Пароли можно хранить в `env.passwords` в виде словаря хост: пароль.

Функция [local](http://readthedocs.org/docs/fabric/en/latest/api/core/operations.html#fabric.operations.local) это исполнение команд только на локальной машине. Для удаленных команд используйте [run](http://readthedocs.org/docs/fabric/en/latest/api/core/operations.html#fabric.operations.run) и [sudo](http://readthedocs.org/docs/fabric/en/latest/api/core/operations.html#fabric.operations.sudo). Сначала мы очищаем экран, очищаем лог файл, запускаем тест, выводим лог. Особо дотошные заметят, что в запуске теста есть еще команда `return 0`, это такой маленький хак. При обнаружении ошибки в тестах, посылается код ошибки отличный от нуля и fabric делает аборт и не выводит вывод команды.

Теперь давайте напишем что-нибудь поинтересней. Например собрать документацию с sphinx и отправить ее на рабочий сервер.

    :::python
    def docs( ):
        """
        Build documentation
        If not found '1 warning' in stdout, abort
        """
        with lcd( u"docs" ):
            with hide( u"stdout" ):
                local( u"make clean" )
            r = local( u"make html", capture=True )
            if r.find( u"1 warning" ) == -1:
                abort( u"Not found '1 warning'" )
    
    def deploy_docs( app=u"limitedfm" ):
        """
        Deploy documentation to server
        """
        docs( )
        with hide( u"running", u"stdout" ):
            put( u"docs/build/html", u"/var/www/{app}".format( app=app ), use_sudo=True )

Вся прелесть в том что мы можем вызывать другие задания в блоке кода. В этом примере мы написали `docs` что бы собрать документацию, а вторым заданием `deploy_docs` загрузить полученные странички на сервер. Как можно наблюдать очень удобно управлять выводом команд. Это функции [hide](http://docs.fabfile.org/en/1.3.2/api/core/context_managers.html#fabric.context_managers.hide), [show](http://docs.fabfile.org/en/1.3.2/api/core/context_managers.html#fabric.context_managers.show), [settings](http://docs.fabfile.org/en/1.3.2/api/core/context_managers.html#fabric.context_managers.settings). Параметром `capture` мы сказали подавить вывод команды. Так же мы сделали небольшую проверку. Если в выводе была строка '1 warning' значит все прошло успешно, если же число будет больше мы остановим процесс. В `deploy_docs` мы просто залили директорию на удалены сервер. Кстати можно использовать [rsync_project](http://docs.fabfile.org/en/1.3.2/api/contrib/project.html#fabric.contrib.project.rsync_project) для минимизации объема передаваемых данных и увеличения скорости. 

Еще можно упомянуть что есть [декораторы](http://readthedocs.org/docs/fabric/en/latest/api/core/decorators.html#module-fabric.decorators) для ограничения выполнения заданий только на отдельных хостах и простенькая [интеграция с dajngo](http://readthedocs.org/docs/fabric/en/latest/api/contrib/django.html#module-fabric.contrib.django). Мне кажется для старта этого хватит, а все остальное можно посмотреть в [документации](http://readthedocs.org/docs/fabric/en/latest/).
