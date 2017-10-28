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
```shell
git clone https://github.com/izderadicka/mybookshelf2
```
Optionally you can use `--depth 1` argument if not interested in code history.
Then change directory to deploy directory:
```
cd mybookshelf2/deploy
```
Initially run `./init.sh` and then edit `.env` eventually  `config.js`, `crossbar.config.json` , `docker-compose.yml` as needed (all contains decent values that works for me, but you might need slightly different setup):
- MBS2_ENVIRONMENT is either stage or development 
- CODE_VOLUME is either .. (to use locally available code, for development) or code - to use docker volume (for stage and production, volume must be created and code cloned into it)
- POSTGRES_PASSWORD - is database password - that one you'd like to change for sure
- MBS2_WAMP_SECURE - remove for development environment

For stage environment only create code volume and build client:
```shell
docker-compose build crossbar
./create_code_volume.sh
./build_client.sh
```
For stage environment you should also use SSL, put your server private key and certificate into ssl directory as `server.key.pem` and `server.cert.pem` (basically in format suitable for nginx server, certificate should contain also intermediate CA ceritificates. If you want to create your own certificates check [this nice article](https://jamielinux.com/docs/openssl-certificate-authority/index.html) how to build your own CA.

Create database tables and data directories (retry if fails due to server connection error):
```shell
docker-compose run --rm app python3 manage.py create_tables -a -c
```
And finally you can start everything (use `-d` to run in background):
```shell
docker-compose up
```

In case of development environment you'll need to serve client with browserSync (and CORS must be enabled on API server):
```shell
./watch_client.sh
```

You also might want to change default password for admin user:
```shell
docker-compose run --rm app python3 manage.py change_password -p your_secret_password admin
```shell

Eventually add other regular users as:
```shell
docker-compose run --rm app python3 manage.py create_user user_name user_email
```

Then you can try application in browser - for staging https://localhost:8088 (or whatever host and port you've chosen for deployment), development http://locahost:6006 (simple client) and http://localhost:9000 - SPA Javascript client.

For direct deployment (on OS, VM) study Docker Scripts - basically you'll need to install similar dependencies on that machine.

For development alternatively  you can use python virtualenv and run db and other services locally (that's how I'm developing).

To run tests you should also initialize test database( run as postgres superuser):
```
psql ebooks_test < ../sql/create_test_db.sql
psql ebooks_test < init_db.sql
```
 
 For production (and possibly too for stage environment) do not forget to replace SECRET_KEY, SECRET_KEY2 and DELEGATED_TOKEN
 in settings.py with your own secrets!
 This command can generate good random string:
 ```
 head -c 64 /dev/urandom | base64 -w 0 | tr -d =; echo
 ```