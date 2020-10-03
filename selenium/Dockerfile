FROM ubuntu:xenial

RUN apt-get update

RUN apt-get install -y python3 python3-pip

RUN apt-get install -y libgconf2-4 libnss3-1d libxss1
RUN apt-get install -y fonts-liberation libappindicator1 xdg-utils

RUN apt-get install -y software-properties-common
RUN apt-get install -y curl unzip wget

RUN apt-get install -y xvfb

RUN apt-get install -y libasound2
RUN apt-get install -y libgbm1

RUN apt-get install -y -f

RUN pip3 install --upgrade --ignore-installed urllib3
RUN pip3 install beautifulsoup4
RUN apt-get install -y libpq-dev
RUN pip3 install psycopg2
RUN pip3 install -U setuptools
RUN pip3 install ndg-httpsclient
RUN pip3 install pyopenssl
RUN pip3 install pyasn1
RUN pip3 install requests

ENV APP_HOME /usr/src/app
WORKDIR /$APP_HOME

COPY . $APP_HOME/

# Set the default command to run when starting the container
# CMD ["/usr/lib/postgresql/9.3/bin/postgres", "-D", "/var/lib/postgresql/9.3/main", "-c", "config_file=/etc/postgresql/9.3/main/postgresql.conf"]

# CMD python3 example.py
CMD tail -f /dev/null
