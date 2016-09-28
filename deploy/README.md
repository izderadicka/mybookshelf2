How to deploy
=============

Solution consists of 5 components:
- Database - must be PostgresSQL >= 9.5
- Javascript client (must be built)
- Web and API server -  Flask - requires Python 3.5
- Crossbar.io - WAMP router - recommended to run on Python 3.5 (for best asyncio support)
- backend server - requires Python 3.5

Currently Docker and Docker-Compose scripts are available in this dir to help deployment.
There are two deployment models:
- development - deployed locally, where you can edit code and play with it (server runs as Flask development server and client is served with BrowserSync)
- staging - with deployment to production environment web server is running in uwsgi server behing nginx server. Static resources and client are server with nginx server.

To start deployment clone git repo:
```
git clone https://github.com/izderadicka/mybookshelf2
```
Optionally you can use `--depth 1` argument if not interested in code history.
Then change directory to deploy directory:
```
cd mybookshelf2/deploy
```
Initially run `./init.sh` and then edit `.env` and `config.js` as needed:
MBS2_ENVIRONMENT is either stage or development 
CODE_VOLUME is either .. (to use locally available code, for development) or code - to use docker volume (for stage and production, must be created)

For stage environment only create code volume and build client:
```
docker-compose build crossbar
./create_code_volume.sh
./build_client.sh
```
Create database tables and data directories:
```
docker-compose run --rm app python3 manage.py create_tables -a -c
```
And finally you can start everything (use `-d` to run in background):
```
docker-compose up
```

In case of development environment you'll need to serve client with browserSync (and CORS must be enabled on API server):
```
./watch_client.sh
```

You also might want to change default password for admin user:
```
docker-compose run --rm app python3 manage.py change_password -p your_secret_password admin
```

Then you can try application in browser - for staging http://localhost:8088 (or whatever host and port you've chosen for deployment), development http://locahost:6006 (simple client) and http://localhost:9000 - SPA Javascript client.

For direct deployment (on OS, VM) study Docker Scripts - basically you'll need to install similar dependencies on that machine.

For development alternativelly you can use python virtualenv and run db and other services locally.
 