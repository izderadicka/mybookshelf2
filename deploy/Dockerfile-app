FROM mbs2-ubuntu

MAINTAINER ivan
ARG MBS2_ENVIRONMENT

RUN if [ "X$MBS2_ENVIRONMENT" = "Xstage" ]; then pip3 install uwsgi; fi
    
ADD uwsgi.ini /etc/
ADD run_app.sh /
ADD loop.sh /

EXPOSE 6006

WORKDIR /code

