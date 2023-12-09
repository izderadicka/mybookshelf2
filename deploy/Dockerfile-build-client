FROM node:6

RUN apt-get update && apt-get install -y chromium xvfb
RUN npm install jspm gulp -g

ADD build_client_cmd.sh /
ADD watch_client_cmd.sh /

