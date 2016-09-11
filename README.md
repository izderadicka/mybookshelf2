MyBookshelf2
============

Web platform for managing ebooks. 

Features:
--------

- multi user
- latest technologies 
  - Aurelia Javascript framework for SPA front-end client. 
  - Flask for restful API server
  - PostgreSQL for data
  - Crossbar.io for online communication
  - Asyncio based backend for long running tasks (conversions etc.)
- Each book can have many files - even of same type
- Full text search
- Cover images
- Ebook files conversion
- Easy upload (extracts metadata from file
- Alternative very simple web front end, which works well on ebook devices (black&white, no Javascript)
- Command line client
- and more

**Now Alpha Version - use at your own risk**

How to deploy
-------------

Solution consists of 5 components:
- Database - must be PostgresSQL >= 9.5
- Javascript client (must be build)
- Web and API - server -  Flask - requires Python 3.5
- Crossbar.io - WAMP router - recommneded to run on Python 3.5 (for best asyncio support)
- backend server - requires Python 3.5

Currently Docker and Docker-Compose scripts are available for deployment (in deploy dir):

```
cd deploy
docker-compose run --rm app python3 manage.py create_tables -a -c
docker-compose up
```

For direct deployment study Docker Scripts.
 