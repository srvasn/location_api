#locaton_api

This is a REST API built using Django with a Postgres database.
It can create Vendor records (regular) and Region records (with a GeoPolygon component).

**Running the API**

1. Clone the repository.

2. Create and activate a python virtualenvironment 

    _Follow this link_
    (https://realpython.com/blog/python/python-virtual-environments-a-primer/)
    
3. Install dependencies using the following command

    `pip install -r requirements.txt`
    
4. Create tables using
    
    `python manage.py migrate`
    
5. Create a superuser

    `python manage.py createsuperuser`
    
5. Run the server using
    
    `python manage.py runserver`
    
6. User `curl` or an http client like Postman to test.

    _(Sample payloads provided in sample_json.pdf)_

**Usage**

The following endpoints are available.

1. `/vendors/`
 
    GET : List all registered vendors
    POST : Create a new vendor

2. `/vendors/< pk >/`

    GET : List vendor with < pk >  
    
    PUT : Update vendor with < pk >

3. `/regions/`

    GET : List all regions present
    
    POST : Create a new region

4. `/regions/< pk >/`
    
    GET : List region with < pk >
    
    PUT : Update region with < pk >

5. `/regions/contains/?lat=_value_&lng=_value_`

    GET : Return regions containing the point denoted by lat and lng values
    
    
**Add ons**

Includes a Heroku `Procfile` for easy deployment.
 
**Notes**

You NEED a working installation of PostgreSQL and the PostGEOS add on to
make sure GeoLocation queries are supported. More information about setting
up a PostgreSQL GeoDjango project can be found here.

_https://www.imagescape.com/blog/2011/09/21/geo-django-quickstart/_

**Contact**

Fire an email to srvasn@gmail.com in case you have any queries.