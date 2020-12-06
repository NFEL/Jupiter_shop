# Jupiter Shop

                                Backend of an online shop with geo tagging capabilities

# Features!

  - Acounting
  - Two layer categorizing (Categories (tech, food, etc...) - Sub Categories(mobile, laptops, lunch, brunch, etc...)
  - Simple view of tables in localhost browser
  - possible blueprints of static pages
  - PostgresSQL Support  ***(currently running on SQLite)***

# Planned to Impelement ...
  - Two layer search (string based, location based)
  - Products geo tagging
  - Products list
  - Map based search
  - Api connection to transfer sevices in each location (Iran -> [SnappBox](https://snapp-box.com/), [Alo Peyk](https://alopeyk.com/))
  - User session (aka. cookies)
 

# More on Impelements ...
 - REST api 
 - Ease of sahring location and reciving location
 - User data customization (Numpy - Tensorflow)
 - TLS certification
 - CDN activation
 - Celery compatibilites
 - An Docker img


  
### Frameworks
  - [Django](https://www.djangoproject.com/)
  - [GeoDjango](https://docs.djangoproject.com/en/3.1/ref/contrib/gis/)
  - [Folium](https://pypi.org/project/folium/)
  - [Geopy](https://geopy.readthedocs.io/)
  - [GDAL](https://gdal.org/)
  - [JQuery](https://jquery.com/)
  - [Pillow](https://pypi.org/project/Pillow/)
  - [Flutter](https://flutter.dev/)          
  - [PostGIS](https://postgis.net/)
   
### Database UML
PLease visit [draw.io](https://drive.google.com/file/d/14R0g7Brj5t1caZul5YIUCOl-7HmGmGiq/view?usp=sharing) for uml view of database ....

##### not so good Blueprints of UI
Please visit [Figma](https://www.figma.com/file/tgrmOtdWLUeY2xr4ENFqUF/Jupiter-Shop-Proto-type-....?node-id=123%3A80) for a view of UI ....

## Startup
As the time being this project does not have a host so far ...
Please run these commands if you have python 3+ installed ...

###### checking python version
    $ python --version 
    >>> Python 3.8.6
###### check if you have a working pip (python package manager) pip version 10+ is OK
    $ python -m pip --version
    >>> pip 20.1.1 from /usr/lib/python3/dist-packages/pip (python 3.8)
###### creating a virtual enviroment for your system  virtualenv version 10+ is OK
    $ python -m pip install virtualenv
    $ python -m virtualenv --version
    >>> virtualenv 20.1.0 from /home/$USER/.local/lib/python3.8/site-packages/virtualenv/__init__.py
    $ python -m virtualenv venv .
    $ source venv/bin/activate
    (venv) $ python -m pip install -r requirements.txt
    
##### Run Django webserver on localHost
    (venv) $ cd jupiter_shop/
    (venv) $ python manage.py runserver

#### Horray :) 
Now all you have to do is to open a browser and navigate :
  - http://localhost:8000/admin  to access database tables (username = admin ,password = admin)
  - http://localhost:8000/  to access a list view of table in html
  - Navigate to ./Webpages to see UI elements so o

### Screen Shots
- [Admin page](https://github.com/NFEL/Jupiter_shop/Screenshots/admin_page.png)
- [Product Listview](https://github.com/NFEL/Jupiter_shop/Screenshots/simple_list_view.png)

## Possible deadline is ***(یکم دی ماه 1399)***