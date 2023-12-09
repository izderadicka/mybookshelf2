FROM ubuntu:16.04

MAINTAINER ivan

ARG MBS2_ENVIRONMENT
ENV LANG C.UTF-8

# additional 12.04 depedencies
#   add-apt-repository -y  ppa:fkrull/deadsnakes &&\
#    sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" >> /etc/apt/sources.list.d/pgdg.list' &&\
#    wget -q https://www.postgresql.org/media/keys/ACCC4CF8.asc -O - | apt-key add - &&\
#   ...
#ln -s /usr/bin/python3.5 /usr/bin/python3 &&\


RUN apt-get update &&\
    apt-get install -y python-software-properties wget libffi-dev  git build-essential &&\
		apt-get install -y python3.5 libpq-dev python3.5-dev &&\
		wget https://bootstrap.pypa.io/get-pip.py &&\
    python3 get-pip.py &&\
    rm get-pip.py
    
# RUN locale-gen en_US.UTF-8
# ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en' LC_ALL='en_US.UTF-8'
    
RUN mkdir /code &&\
    mkdir /data &&\
    chmod a+rwx /data

WORKDIR /code
ADD requirements.txt /code/
RUN pip3 install -r requirements.txt
ADD requirements-dev.txt /code
RUN if [ "X${MBS2_ENVIRONMENT}" = "Xdevelopment" ]; then \
    pip3 install -r /code/requirements-dev.txt;\
    fi




