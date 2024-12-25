How to deploy
=============

Solution consists of 4 components:
- Database - must be PostgresSQL >= 9.5
- Javascript client (must be built with Gulp)
- Web and API server -  Flask - requires Python 3.5+
- backend server - requires Python 3.5+

Currently Docker and Docker-Compose scripts are available in this dir to help deployment.
There are two deployment models:
- development - deployed locally, where you can edit code and play with it (server runs as Flask development server and client is served with BrowserSync)
- staging - with deployment to production environment web server is running in uwsgi server behind nginx proxy. Static resources and client are server with nginx server. nginx also provides SSL termination.

Basic deployment instructions
=============================

To start deployment clone git repo:
```shell
git clone https://github.com/izderadicka/mybookshelf2
```
Optionally you can use `--depth 1` argument if not interested in code history.
Then change directory to deploy directory:
```
cd mybookshelf2/deploy
```
Run `./init.sh [development|stage]` and script will guide you though deployment. Script will ask you for two passwords - one for database and other for MyBookshelf2 admin user.

For stage environment you will need SSL key, put your server private key and certificate into ssl directory as `server.key.pem` and `server.cert.pem` (basically in format suitable for nginx server, certificate should contain also intermediate CA certificates. If you want to create your own certificates check [this nice article](https://jamielinux.com/docs/openssl-certificate-authority/index.html) how to build your own CA.

For development environment you can then see full client at http://localhost:9000 and lite client as http://localhost:6006.

For stage environment full client is at https://localhost:4443/client/ and lite client is at https://localhost:4443.

### Clean up after docker compose deployment

Use `./cleanup.sh` script.  WARNING: it'll remove all data and images used in deployment. When switching between development and stage type deployment full cleanup is required.


Additional instructions
======================

If you need to  add other regular users it now possible only from command line:
```shell
docker-compose run --rm app python3 manage.py create_user user_name user_email
```

For direct deployment (on OS, VM) study Docker Scripts - basically you'll need to install similar dependencies on that machine.


In development deployment you can also run tests:
```
docker-compose run --rm app py.test app common
docker-compose run --rm  backend py.test engine
```
 
 For development alternatively  you can use python virtualenv and run db and other services locally (that's how I'm developing).

 For stage environment deployment only deploy directory is needed.  Code is cloned from git repo - branch master.
 
 For production (and possibly too for stage environment) do not forget to replace SECRET_KEY, SECRET_KEY2 and DELEGATED_TOKEN
 in settings.py with your own secrets!
 This command can generate good random string:
 ```
 head -c 64 /dev/urandom | base64 -w 0 | tr -d =; echo
 ```

 My semi-production
 ==================

 These instructions are relevant for my environment mostly other readers can ignore them.

 Copy data with `rsync -ac`  to /data/ebooks

 First try stage deployment with init.sh as described above. 
 
 Then edit and amend .env as needed per template below (keep environment stage):

 ```
POSTGRES_PASSWORD="xxxxx"
MBS2_ENVIRONMENT=stage
MBS2_DEBUG=false
CODE_VOLUME=..
MBS2_USER=1000:1000
MBS2_USER_NAME=ivan
DB_VOLUME=/data/ebooks/db
DATA_VOLUME=/data/ebooks/mbs2
 ```

 Run enviroment with `docker compose -f docker-compose-prod.yml up -d`.

 Restore DB with :

 ```
 gunzip -c /data/ebooks/mbs2/books/mbs2_db_backup.slql.gz | docker compose -f docker-compose-prod.yml run --rm -T -e PGPASSWORD=xxxxxx db psql -h db postgres postgres
 ```