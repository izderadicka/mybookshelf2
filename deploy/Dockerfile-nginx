FROM nginx

MAINTAINER ivan
   
ADD nginx.conf /etc/nginx/conf.d/default.conf
RUN mkdir /etc/nginx/ssl
ADD ssl/server.key.pem /etc/nginx/ssl/
ADD ssl/server.cert.pem /etc/nginx/ssl/
ADD uwsgi.ini /etc/
ADD run_app.sh /
ADD loop.sh /
    
RUN mkdir /code &&\
    mkdir /data

