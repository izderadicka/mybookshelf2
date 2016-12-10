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
- Easy upload (extracts metadata from the file)
- Can organize books in shelves
- Books rating
- Alternative very simple web front end, which works well on ebook devices (black&white, no Javascript)
- Command line client
- and more

For more information see [project homepage](http://zderadicka.eu/projects/python/mybookshelf2-ebooks-management-and-sharing/)

Project is now almost in beta stage (I'm using it for my ebooks collection for some time), 
I think it's reasonably stable for people to try it.

Can be easily deployed using Docker - look at README.md in deploy directory. 

Missing parts
-------------

Mass conversion - All ebooks of an author, series, bookshelf. It was available in previous version, I found it quite useful.
So this will be probably next priority.

Online user mamagement - registration, password change/reset, rights assigment - as it is not priority for myself 
it's not yet implemented.  Users can be now managed by command line utility ```manage.py```.

User preferences/profile -  prefered formats for conversion, conversion parameters, external info sources, 
etc.  
There is possibility to store per user preferences as JSON, but the implementation of preferences is
yet to be done.

Documentation - unfortunatelly it usually my weak part.

