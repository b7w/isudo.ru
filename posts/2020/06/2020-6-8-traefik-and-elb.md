# title: Traefik 2.0
# url: traefik-and-elb
# categories: [Programming]
# tags: [Яндекс.Облако, Traefik, Proxy, ELB, Docker, docker-compose]
# time: 2020-06-28 12:00:00.000000+03:00
# draft: true

![left](~traefik.png)
В очередной раз сетуя что в nginx нет встроенной поддержки let's encrypt, Я пошёл на просторы интернета поискать что-нить новенькое.
Из интересного Я нашёл nginx-le/nginx-le: Nginx with automatic let's encrypt (docker image).
Но это дополнительная обвязка из костылей, что не особо радует.
Опять наткнулся на traefik. Вспомнил что он обновился до версии 2, и решил потрогать его.
Все равно ничего больше то и нет. 


[clear][more]


### Придумаем себе проблему

Давайте предположим что нам необходимо сделать небольшое веб приложение. И конечно хочется что бы приложение было отказоустойчивым.
Допустим с базой данных мы решим вопрос выбрав Managed Database. А вот как быть с приложением? 
Нет, конечно мы возьмем Elastic Load Balancer, это будет точкой входа для пользователя в браузере. А дальше что?
У нас же конечно микросервисы. Их много, а балансировщик то один. Похоже надо еще прокси сервис, который сходит в разные приложения и соберет это под одним портом.

А еще конечно мы хотим что бы все было обмазано docker. И что бы можно было легко поднимать новые сервисы и масштабировать существующие. 

Можно конечно взять старый добрый nginx. Но тогда придется вташить отдельно let's encrypt, отдельно service discovery, а потом все это дружить.
И тут ненароком можно задуматься, а мож нафиг его и сразу поставить Kubernetes? На секунду, но задуматься.

И вот тут как раз и выходит на сцену Traefik. Он не только умеет let's encrypt, но и умеет напрямую ходить в docker engine и смотреть на контейнеры и их лейблы.
Это даёт возможность написать docker-compose файлик в котором будет не только описание запуска контейнера, но и настройки проксирования.


### А теперь браво решим проблему

Давайте попробуем все это развернуть и потестить. Заодно поиграемся с новым [Яндекс.Облаком](https://cloud.yandex.ru/). Terraform брать не будем ради таких забав, возьмем обычный [CLI](https://cloud.yandex.ru/docs/cli/quickstart).  

Создадим две виртулки с предустановленным docker, это что бы незапариваться с установкой самим. 

    :::sh
    > yc compute instance create-with-container \
        --name traefik-vm1 \
        --zone=ru-central1-a \
        --ssh-key ~/.ssh/id_rsa.pub \
        --public-ip --labels test=traefik \
        --cores 2 --memory 2G \
        --create-disk type=network-ssd,size=8 \
        --container-image containous/whoami
	> yc compute instance create-with-container \
        --name traefik-vm2 \
        --zone=ru-central1-b \
        --ssh-key ~/.ssh/id_rsa.pub \
        --public-ip --labels test=traefik \
        --cores 2 --memory 2G \
        --create-disk type=network-ssd,size=8 \
        --container-image containous/whoami


На каждой машине мы хотим развернуть traefik в виде прокси сервера и тестовое приложение на sub-url `/app`.
Для этого напишем простенький docker-compose.yml.

    :::yaml
    version: '3'
    services:
        traefik:
            image: traefik:v2.2
            command:
                # Подключаем отслеживание docker и убираем автоматическое побликование контейнеров
                - "--providers.docker=true"
                - "--providers.docker.watch=true"
                - "--providers.docker.exposedByDefault=false"
                # Вешаем сервер на 443 порт
                - "--entryPoints.web.address=:443"
                # Добавил простенький healthcheck самого traefik
                - "--ping=true"
                # Всякая всячина
                - "--api.insecure=true"
                - "--metrics.prometheus=true"
            restart: always
            ports:
                - 443:443
                - 8080:8080 # Порт админки traefik
            volumes:
                - /var/run/docker.sock:/var/run/docker.sock
            labels:
                # Регистрируем router с именем 'all' который будет перехватывать весь трафик 
                - traefik.http.routers.all.entrypoints=web
                - traefik.http.routers.all.rule=HostRegexp(`{any:.+}`)
    
        app:
            image: "containous/whoami"
            restart: always
            hostname: traefik-${VM}  # Пригодится для отладки
            labels:
              # Подключаем контейнер к traefik на sub-url '/app' с https 
              - traefik.enable=true
              - traefik.http.routers.app.tls=true
              - traefik.http.routers.app.rule=Path(`/app`)


Что бы запустить docker-compose, нам надо знать публичные IP аддреса виртуалок.
Для этого смотрим колонку 'EXTERNAL IP', в `yc compute instance list`
    
    :::sh
	> yc compute instance list
	+----------------------+-------------+---------------+---------+----------------+-------------+
    |          ID          |    NAME     |    ZONE ID    | STATUS  |  EXTERNAL IP   | INTERNAL IP |
    +----------------------+-------------+---------------+---------+----------------+-------------+
    | fhmg57b1c2sr5vo6sjuj | traefik-vm1 | ru-central1-a | RUNNING | 130.193.51.171 | 10.128.0.11 |
    | epda5ji37b6vf7jgivqv | traefik-vm2 | ru-central1-b | RUNNING | 84.201.164.166 | 10.129.0.19 |
    +----------------------+-------------+---------------+---------+----------------+-------------+

Каждый IP добавлюяем в known_hosts, иначе docker-compose будет падать.

    :::sh
	> ssh-keyscan 130.193.51.171 >> ~/.ssh/known_hosts
	> ssh-keyscan 84.201.164.166 >> ~/.ssh/known_hosts

Запускаем docker-compose для обоих виртуалок, дополнительно параметризуя вызов переменной окружения 'VM'.

    :::sh
	> VM=vm1 docker-compose -H 'ssh://yc-user@130.193.51.171' up -d
	> VM=vm2 docker-compose -H 'ssh://yc-user@84.201.164.166' up -d

Проверяем что у нас все удачно запустилось.

    :::sh
	> curl --silent --insecure https://130.193.51.171/app | grep Hostname
	Hostname: traefik-vm1
	> curl --silent --insecure https://84.201.164.166/app  | grep Hostname 
	Hostname: traefik-vm2


Теперь надо создать target-group с хостами на которые будет идти нагрузка.
Для этого нам понадобиться подсети и ip адреса машинок. Мы их получим с помощью магии jq и формата вывода json.

    :::sh
	> yc compute instance list --format json | jq '[.[] | {subnet: .network_interfaces[0].subnet_id, address: [.network_interfaces[].primary_v4_address.address]}]'
    [
      {
        "subnet": "e2lqhsko5mdlsdsmr4p0",
        "address": [
          "10.129.0.19"
        ]
      },
      {
        "subnet": "e9ba3jbnjvvqdhlu22j2",
        "address": [
          "10.128.0.11"
        ]
      }
    ]

Подсталяем subnet и address в команду ниже.

    :::sh
	> yc load-balancer target-group create \
        --region-id ru-central1 \
        --name traefik-tg \
        --target subnet-id=e2lqhsko5mdlsdsmr4p0,address=10.129.0.19 \
        --target subnet-id=e9ba3jbnjvvqdhlu22j2,address=10.128.0.11
    
    id: b7rhkak24g2ddrk3in55
    folder_id: b1g6ikhlpce8nn9mvl7r
    created_at: "2020-06-27T21:42:33Z"
    name: traefik-tg
    region_id: ru-central1
    targets:
    - subnet_id: e2lqhsko5mdlsdsmr4p0
      address: 10.129.0.19
    - subnet_id: e9ba3jbnjvvqdhlu22j2
      address: 10.128.0.11

Теперь нам надо создать балансировщик который будет слушать на https порту. target-group-id подставляем из предедушей команды.

    :::sh
	> yc load-balancer network-load-balancer create \
        --region-id ru-central1 \
        --name traefik-lb \
        --type external \
        --listener name=https,external-ip-version=ipv4,port=443 \
        --target-group target-group-id=b7rhkak24g2ddrk3in55,healthcheck-name=http,healthcheck-interval=2s,healthcheck-timeout=1s,healthcheck-unhealthythreshold=2,healthcheck-healthythreshold=2,healthcheck-http-port=8080,healthcheck-http-path=/ping

Получаем IP аддрес нашего балансировшика.

    :::sh
    > yc load-balancer network-load-balancer get traefik-lb --format json | jq '.listeners[0].address'
    "84.201.129.67"

Проверяем что у нас все удачно запустилось. 

    :::sh
	> curl --silent --insecure https://84.201.129.67/app | grep Hostname 
	Hostname: traefik-vm2
	> curl --silent --insecure https://84.201.129.67/app | grep Hostname 
	Hostname: traefik-vm1
	
Если подергать endpoint, то можно увидеть что в hostname значения меняются.
Что нотифицирует нам о том, что мы все правильно натроили.


### Scale it!

C виртуалками все просто. Стартуем ешë одну, запускаем docker-compose и добавляем в target-group.
Но мы же предполагаем что у нас жирные виртуалки, и 2-3 таких нам за глаза. 
Их надо утилизировать, запуская несколько инстансов одного приложения внутри каждой виртуалки.
И как не странно, но это очень просто сделать!

    :::sh
    > VM=vm1 docker-compose -H 'ssh://yc-user@130.193.51.171' up -d --scale app=3
    > VM=vm1 docker-compose -H 'ssh://yc-user@130.193.51.171' ps
    Connected (version 2.0, client OpenSSH_7.2p2)
    Authentication (publickey) successful!
           Name                      Command               State                          Ports
    -------------------------------------------------------------------------------------------------------------------
    traefik_app_1       /whoami                          Up      80/tcp
    traefik_app_2       /whoami                          Up      80/tcp
    traefik_app_3       /whoami                          Up      80/tcp
    traefik_traefik_1   /entrypoint.sh --providers ...   Up      0.0.0.0:443->443/tcp, 80/tcp, 0.0.0.0:8080->8080/tcp


Вся прелесть в том что traefik автоматически подхватывает новые инстансы и делает балансировку!
Можно убедиться в этом дернув API и увидев 3 'servers'.

    :::sh
    > curl -s 84.201.156.117:8080/api/http/services | jq '.[] | select(.type=="loadbalancer")'
    {
      "loadBalancer": {
        "servers": [
          {
            "url": "http://172.18.0.6:80"
          },
          {
            "url": "http://172.18.0.3:80"
          },
          {
            "url": "http://172.18.0.4:80"
          }
        ],
        "passHostHeader": true
      },
      "status": "enabled",
      "usedBy": [
        "app@docker"
      ],
      "serverStatus": {
        "http://172.18.0.3:80": "UP",
        "http://172.18.0.4:80": "UP",
        "http://172.18.0.6:80": "UP"
      },
      "name": "app-traefik@docker",
      "provider": "docker",
      "type": "loadbalancer"
    }


### Let's encrypt

Вспомним что вся движуха началась с let's encrypt. Так что давайте прикрутим нормальный сертификат к нашему приложению.
Воспользуемся DNS challenge, что бы не мучаться с прокидыванием дополнительных endpoint.
У меня домен хоститься на AWS, поэтому я вольспользуюсь Route53. Другие провайдеры можно посмотреть в [документации](https://docs.traefik.io/https/acme/#providers)
Поправим наш docker-compose.yml.

    :::yaml
    version: '3'
    services:
        traefik:
            image: traefik:v2.2
            command:
                - "--providers.docker=true"
                - "--providers.docker.watch=true"
                - "--providers.docker.exposedByDefault=false"
                - "--entryPoints.web.address=:443"
                # Добавляем resolver с именем aws и настраеваем email, provider и storage
                - "--certificatesresolvers.aws.acme.email=blog@isudo.ru"
                - "--certificatesresolvers.aws.acme.dnschallenge.provider=route53" 
                - "--certificatesresolvers.aws.acme.storage=/etc/traefik/acme.json" 
                - "--ping=true"
                - "--api.insecure=true"
                - "--metrics.prometheus=true"
            restart: always
            ports:
                - 443:443
                - 8080:8080
            environment:
                - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
                - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
            volumes:
                - /var/run/docker.sock:/var/run/docker.sock
                # Выносим хранение сертификатов на хост машину
                - /etc/traefik:/etc/traefik
            labels:
                - traefik.http.routers.all.entrypoints=web
                - traefik.http.routers.all.rule=HostRegexp(`{any:.+}`)

        app:
            image: "containous/whoami"
            restart: always
            hostname: traefik-${VM}  # Пригодится для отладки 
            labels:
              - traefik.enable=true
              # Добавляем совпадение по имени хоста и подключаем certresolver
              - traefik.http.routers.app.entrypoints=web
              - traefik.http.routers.app.tls=true
              - traefik.http.routers.app.tls.certresolver=aws
              - traefik.http.routers.app.rule=Host(`traefik.isudo.ru`) && Path(`/app`)


_Далее идет хитрость за кадром, которая тут не описана. 
А имеено привязака IP балансировшика '84.201.129.67' к домену 'traefik.isudo.ru'._


Когда домен готов к использовантю, можно обновить настройки контенеров на виртуалках.

    :::sh
    > export AWS_ACCESS_KEY_ID={{ your_aws_access_key_id }}
    > export AWS_SECRET_ACCESS_KEY={{ your_aws_secret_access_key }}
	> VM=vm1 docker-compose -H 'ssh://yc-user@130.193.51.171' up -d
	> VM=vm2 docker-compose -H 'ssh://yc-user@84.201.164.166' up -d
	
	
Ждем немного пока traefik дождется подтверждения challenge и подставит сертификат.
Проверить сертификат на каждой виртуалке можно через 'curl', добавив специальный флаг 'resolve'. 

    :::sh
    > curl --verbose --resolve 'traefik.isudo.ru:443:130.193.51.171' https://traefik.isudo.ru:443/app 2>&1 | grep 'Hostname\|CN='
    * Hostname traefik.isudo.ru was found in DNS cache
    *  subject: CN=traefik.isudo.ru
    *  issuer: C=US; O=Let's Encrypt; CN=Let's Encrypt Authority X3
    Hostname: traefik-vm1
    >
    > curl --verbose --resolve 'traefik.isudo.ru:443:84.201.164.166' https://traefik.isudo.ru:443/app 2>&1 | grep 'Hostname\|CN='
    * Hostname traefik.isudo.ru was found in DNS cache
    *  subject: CN=traefik.isudo.ru
    *  issuer: C=US; O=Let's Encrypt; CN=Let's Encrypt Authority X3
    Hostname: traefik-vm2

Ну и на последок можно дернуть запрос через балансировшик без флага `--insecure`, потому что у нас теперь не саподписанный сертификат.	
	
	:::sh
    > curl --silent https://traefik.isudo.ru/app | grep Hostname 
	Hostname: traefik-vm1
	
Работает!


### Почистим за собой

Облака дело не дешовое, поэтому надо удалить все добро которое мы насоздавали.

    :::sh
    > yc load-balancer network-load-balancer delete traefik-lb --async
    > yc load-balancer target-group delete traefik-tg --async
    > yc compute instance delete traefik-vm1 traefik-vm2 --async


### Подведем итоги

Плюсы.

Отказоустойчивости добились, можно масштабировать как контейнеры так и ноды.
Конфигурация приложений декларативная, на виртуалки лезть руками не надо.
Сделали прозрачную и автоматическую конфигурацию сертификатов.

Есть конечно и минусы.

Например трафик в такой схеме между виртуалками ходить не будет.
Надо еще докручивать health check, restart policy для контейнеров.

Тем не менее, в целом получилось недурно. Для небольшого приложения вполне годная структура для старта.
