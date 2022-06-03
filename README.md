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


<img width="1678" alt="Снимок экрана 2022-05-22 в 14 39 48" src="https://user-images.githubusercontent.com/15955132/169696618-04e39728-5147-4251-8ee5-4f420cde069a.png">
<img width="1678" alt="Снимок экрана 2022-05-22 в 14 40 13" src="https://user-images.githubusercontent.com/15955132/169696646-bb63a015-177b-4f99-a3d5-5e7934251f01.png">
<img width="1678" alt="Снимок экрана 2022-05-22 в 14 40 23" src="https://user-images.githubusercontent.com/15955132/169696649-90f9d4e3-89d2-4e11-85a2-6d7cc747a4e2.png">
<img width="1678" alt="Снимок экрана 2022-05-22 в 14 39 58" src="https://user-images.githubusercontent.com/15955132/169696652-fbf0c2a3-a1a4-4b49-82b0-69fe7145f8cc.png">
<img width="1678" alt="Снимок экрана 2022-05-22 в 15 21 40" src="https://user-images.githubusercontent.com/15955132/169696658-1602d87b-200b-45a9-babd-6deca0f17b20.png">
<img width="1678" alt="Снимок экрана 2022-05-22 в 15 15 04" src="https://user-images.githubusercontent.com/15955132/169696663-1b883602-eb6f-4859-acfb-65fb90ad3bbe.png">
<img width="1678" alt="Снимок экрана 2022-05-22 в 15 15 29" src="https://user-images.githubusercontent.com/15955132/169696667-9ebad44f-2067-4931-84d6-b618e978c9fa.png">
