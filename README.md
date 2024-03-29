<h1 align="center"> Dating and Matches API and MONOLITH</h1>
<h3 align="center">My analog of the website for Dating And Matches</h3>

## Technology <img src="https://user-images.githubusercontent.com/15955132/214321830-f3ccbde2-954e-4751-bdd3-c75ac96a8a0d.png" width="20" height="20">  
  

![icons8-python-48](https://user-images.githubusercontent.com/15955132/214317185-5e615db0-3bfd-4b32-8622-7bb0ea674c05.png)&nbsp;
<img src="https://storage.caktusgroup.com/media/blog-images/drf-logo2.png" width="50" height="50">&nbsp;
![icons8-django-48](https://user-images.githubusercontent.com/15955132/214319364-ae374fbf-3081-4381-bd4a-c3f39540d1d9.png)&nbsp;
<img src="https://user-images.githubusercontent.com/15955132/214613677-bc246cf5-0cb6-4d2e-88f6-712cb1110b88.png" width="50" height="50">&nbsp;
![icons8-docker-48](https://user-images.githubusercontent.com/15955132/214317222-a7e07749-425f-42f3-b0a6-4478d7ab68ec.png)&nbsp;
<img src="https://user-images.githubusercontent.com/15955132/214614949-23ef31f6-f27c-4919-8ace-1c88c3c9124b.png" width="100" height="50">&nbsp;
<img src="https://user-images.githubusercontent.com/15955132/214614298-70541229-f161-4094-be0f-7842221d0597.png" width="100" height="50">&nbsp;
<img src="https://user-images.githubusercontent.com/15955132/214620755-e48b8d16-c800-43d5-adfb-ad68758ad396.png" width="100" height="50">  
```Python    DRF   Django  Celery   Docker     Channel   Redis     JS      ```  


## About the project

A dating web-application which allows people to choose dating partners with specific preferences based on their photos. The main aspect is a rating system based on the grades under the photos. 

My GitHub project now has two versions. The first version is a monolithic version without an API and with simple matching logic, while the second version works purely on an API basis. Both versions have documentation and tests.


```Monolithic Version:```
Description: The monolithic version is a fully functional application developed without using an API. It includes all the functionality for working with users, profiles, photos, and chats. The matching logic is implemented within the monolithic application.
Documentation: The monolithic version has documentation that describes the API endpoints, database structure, data models, views, and the basic principles of the application's operation.
Tests: The monolithic version includes tests that verify the functionality and correctness of various components of the application, including models, views, and functional capabilities.

```API-Based Version:```
Description: The API-based version is developed using an API for interaction with client applications. It provides a set of endpoints through which clients can exchange data with the server. All matching logic and user interaction functionality are based on API requests.
Documentation: The API-based version also has documentation that describes all available API endpoints, required parameters, data formats, and possible responses from the server.
Tests: The API-based version includes tests that verify the proper functioning of API endpoints, data validation, error handling, and other aspects related to the API.
Both versions of the project are self-contained and have their own documentation and tests to ensure reliability, functionality, and ease of development and usage.

Chat works via web sockets.


## Launch

⋅*Create file `.env`  
⋅*Fill it:  
```ts
SECRET_KEY_MONOLITH=YOURK_SECRET_KEY
DEBUG=True_of_False
DB_NAME_MONOLITH=YOUR_DB_NAME
DB_USER_MONOLITH=YOUR_DB_USER
DB_PASS_MONOLITH=YOUR_DB_PASS

SECRET_KEY_API=YOURK_SECRET_KEY
DEBUG_API=True_of_False
DB_NAME_API=YOUR_DB_NAME
DB_USER_API=YOUR_DB_USER
DB_PASS_API=YOUR_DB_PASS

EMAIL_HOST=YOUR_EMAIL_HOST
EMAIL_HOST_USER=YOUR_EMAIL_HOST_USER
EMAIL_HOST_PASSWORD=YOUR_EMAIL_HOST_PASSWORD
EMAIL_PORT=YOUR_EMAIL_PORT
```   

⋅*Run the `docker-compose build`   
⋅*Start project `docker-compose --env-file .env up`   
⋅*Create superuser `docker-compose run --rm django sh -c "python manage.py createsuperuser"`  

## Photographies
<img width="1000" alt="screen_1" src="https://user-images.githubusercontent.com/15955132/214617241-ad3c87f2-8856-4fe6-bf01-836c06e5fbd0.png">
<img width="1000" alt="screen_2" src="https://user-images.githubusercontent.com/15955132/214617285-228ea344-f7f6-488b-ac1d-20119c297f02.png">
<img width="1000" alt="screen_3" src="https://user-images.githubusercontent.com/15955132/214617316-6a5f86f2-dbab-4b05-800e-699e451be7ab.png">
<img width="1000" alt="screen_4" src="https://user-images.githubusercontent.com/15955132/214617492-6ad880d5-a187-4a32-8c22-926b314824e1.png">
<img width="1000" alt="screen_5" src="https://user-images.githubusercontent.com/15955132/214617462-696d0a24-9a83-46e8-a68d-a428555b60b6.png">
<img width="1000" alt="screen_6" src="https://user-images.githubusercontent.com/15955132/214617531-989fe986-e0e3-46e3-aec3-635c328f4f6c.png">





