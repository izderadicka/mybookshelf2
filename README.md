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
- Alternative very simple web front end, which works well on ebook devices (black&white, no Javascript)
- Command line client
- and more

**Now Alpha Version - use at your own risk**

Can be easily deployed using Docker - look at README.md in deploy directory. 