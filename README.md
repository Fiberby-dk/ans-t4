SWAPI API adventure
===========

Introduction
-----------
The SWAPI API is one of the founding pillars on Internet. For your easy 
access to information about the Starwars franchise. Ever wanted
to know who directed the episode or characters that appears in 
different Episodes?  
SWAPI is your trusted friend and makes sure all the information 
is up to date, wherever in the world you are. 

# Starwars?
Starwars is a scifi/fantasy franchise. The first episode 
"Episode IV: A new hope" premiered in 1977, which resulted 
in a gigant success.

# Why API?
A web api enables developers to create amazing and flexible 
applications across a myriad of platforms. This project presents 
the data as a traditional web page, but it could just as easy be
worked out as a application on your phone. 

# But why? 
This implementation of the SWAPI api aim to provide an easy access
to all the interesting facts about the Starwars universe. 


Note for futher development
-----------
The implementation of the API has just begun! This particular solution is 
made in Flask which is a micro web framework in Python. Implementation
for 'Planets, species, vehicales and starship' are yet to be done. 

As a starting point, head over to app.py where you see the routing 
of the application. Currently people and films are implemented. 
To create your own implementation you can easily derive from the
base class BaseEntity (in swapi.py), which does most of the work 
fetching the data. These are the files of interest. 


* app.py 
  Here you will define the routing and preparation for the html
  output. 
  
* swapi.py
  Is responsible to fetch the data. 
  
* templates/
  The HTML templates, flask is using jinja to compose HTML and 
  the data from your flask application. 

Many of the entities in the API has relations to other entities, which 
may result in a many sub queries. Using caching with memcached or redis
will speed up the application this process instead of fetching the same
data over and over again.


Datamodel for SWAPI
-----------
Note: I prefer to map out data models visually with tools such as DIA. 
Where it's easier to find out relationships between different entities. 
Anyway I'll try to describe the different relationships from the API in the API. 
Many of the entites are quite the same.

# The Film entity
Let's start with the **Film** entity it has relations to what characters appears in the 
movie. As well as planets, starships, vehicales and species. These relationships would be
a "sibling/many to many" relationship. Which means there is a "pivot" database table between the 
main entities.

# Improvements of the SWAPI (https://swapi.dev/api/)
As an API it's quite rudimentary made. As a developer you would probably want to 
get more information about the related data. At least a name (such as for the person entity). 
It would save a lot more resources to deliver a title, id and an url for instance
when getting the data for the films. As it is now, it requires the implementation to 
do a lot of caching in order to deliver a responsive solution. 
For instance Django has two nifty features called _select_related_ and _prefetch_related_ 
which can join in relevant tables in the database and speed up things considerably.
In the background this tries to join in relevant database tables, which results in 
a lot less stress for the database when working with RDB.

