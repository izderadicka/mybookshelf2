How to deploy
-------------

Solution consists of 5 components:
- Database - must be PostgresSQL >= 9.5
- Javascript client (must be built)
- Web and API - server -  Flask - requires Python 3.5
- Crossbar.io - WAMP router - recommended to run on Python 3.5 (for best asyncio support)
- backend server - requires Python 3.5

Currently Docker and Docker-Compose scripts are available for deployment (in deploy dir)

Run `./init.sh` and then edit `.env` and `environment.js` as needed.

This is how to deploy in development mode (app server is running as Flask development server):
```
cd deploy
docker-compose run --rm app python3 manage.py create_tables -a -c
docker-compose up
```
Then you can try simple web ui on http://localhost:6006.   Also you can setup development environment for SPA client -  install node and all dependencies (see Dockerfile-build-client) and then you can run gulp watch from /client directory - then http:localhost:9000 will start advanced client (CORS must be enabled on API server).

For direct deployment (on OS, VM) study Docker Scripts - basically you'll need to install similar dependencies on that machine.
 