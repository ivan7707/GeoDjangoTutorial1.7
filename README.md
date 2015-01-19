GeoDjangoTutorial1.7
====================

Python 3.4.2 
Django 1.7
Postgres 9.3.5

EDIT:  a pull request from tomscytale  made me realize that rather than update from 2.x to 3.x that I should have made the program compatible with both versions.  
If anyone using 2.x finds issues in using the program, please let me know, and I will update it to work on both versions of Python.


In learning Django and GeoDrango, I came across this tutorial.  

http://invisibleroads.com/tutorials/geodjango-googlemaps-build.html

It was built in Django 1.3.  I am using 1.7, so I decided to make it work and have it accessible to anyone else who is learning 
Django and GeoDjango.  

There is one issue I am still trying to resolve though, I had to add

@csrf_exempt to the save view in waypoints.views, otherwise I would get a 403 forbidden error.  

Please feel free to send any updates that you see fit.  

Here are the instructions that worked for me (I reinstalled it to make sure it worked) 

1)	Add virtual environment 

Virtualenv google1.7

2)	Move into virtual environment and activate it

Cd google1.7 

Activate

3)	Install Django 

Pip Install Django

4)	Add database 

I used pgAdminIII to install the database with postgis extension (or create a database from postgis_21_sample template that you install when installing pgAdminIII)

As per the tutorial, username and password are

geouser geodatabase

5)	Clone this into google1.7 folder

git clone https://github.com/ivan7707/GeoDjangoTutorial1.7.git

6)	Move into GeoDjangoTutorial1.7

cd GeoDjangoTutorial1.7

7) Run migrations

python manage.py migrate

8) Run the server

python manage.py runserver




Ivan
