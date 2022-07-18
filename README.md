# Dating and Matches
###### My analog of the website for Dating And Matches

`
DJANGO + CELERY + CHANNELS + DOCKER
`
 
###### Для работы нужно:

  В корне создать .env файл с такими параметрами:
  ```
    ALLOWED_HOSTS=
    DEBUG=
    SECRET_KEY=

    EMAIL_HOST=
    EMAIL_HOST_USER=
    EMAIL_HOST_PASSWORD=
    EMAIL_PORT=

    NAME=
    USER=
    PASSWORD=
    HOST=
    PORT=

    POSTGRES_PASSWORD=
    POSTGRES_USER=
    POSTGRES_DB=
  ```
  `docker-compose build`
  `docker-compose --env-file .env up`

###### Для создания суперюзера:

  `docker exec -it dm python ./manage.py createsuperuser`


###### ФОТОГРАФИИ:


<img width="1672" alt="Снимок экрана 2022-07-18 в 23 29 34" src="https://user-images.githubusercontent.com/15955132/179615822-d2f899e2-789b-4b39-9dbc-573dd9b894c5.png">
<img width="1672" alt="Снимок экрана 2022-07-18 в 23 30 40" src="https://user-images.githubusercontent.com/15955132/179615851-2d437117-81e3-4c30-9547-4c6ed2f35edb.png">
<img width="1672" alt="Снимок экрана 2022-07-18 в 23 39 02" src="https://user-images.githubusercontent.com/15955132/179615859-c94ed189-d3b2-4cf3-bb4f-cc70f5865609.png">
<img width="1672" alt="Снимок экрана 2022-07-18 в 23 44 09" src="https://user-images.githubusercontent.com/15955132/179615868-b81c850e-d410-4714-aebf-b4b07ebd1a7f.png">
<img width="1672" alt="Снимок экрана 2022-07-18 в 23 48 30" src="https://user-images.githubusercontent.com/15955132/179615873-cb95c60b-15cd-47e9-abcf-a483be2013c6.png">
<img width="1187" alt="Снимок экрана 2022-07-18 в 23 58 37" src="https://user-images.githubusercontent.com/15955132/179616240-652dd7c6-eb47-4e57-8221-d326a6453fa5.png">
