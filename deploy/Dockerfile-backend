FROM mbs2-ubuntu

MAINTAINER ivan

#FOR backend
# 12.04 dependencies
# add-apt-repository ppa:libreoffice/libreoffice-5-0 &&\
#TBD - add libreoffice version to env variables
RUN apt-get update &&\
    apt-get install -y imagemagick libreoffice libgl1-mesa-glx
    
RUN wget -nv -O- https://raw.githubusercontent.com/kovidgoyal/calibre/master/setup/linux-installer.py | python -c "import sys; main=lambda:sys.stderr.write('Download failed\n'); exec(sys.stdin.read()); main()"

EXPOSE 8080 9080
		
ADD loop.sh /

