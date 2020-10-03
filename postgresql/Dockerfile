FROM postgres:latest

# install Python 3
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get -y install python3.7-dev
RUN apt-get -y install postgresql-server-dev-10 gcc python3-dev musl-dev

# install psycopg2 library with PIP
RUN pip3 install psycopg2

# add the 'postgres' admin role
USER postgres

# RUN    /etc/init.d/postgresql start &&\
#     psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'docker';" &&\
#     createdb -O docker covid19

# expose Postgres port
EXPOSE 5432

# Adjust PostgreSQL configuration so that remote connections to the
# database are possible.
# RUN echo "host all  all    0.0.0.0/0  md5" >> /etc/postgresql/9.3/main/pg_hba.conf

# # And add ``listen_addresses`` to ``/etc/postgresql/9.3/main/postgresql.conf``
# RUN echo "listen_addresses='*'" >> /etc/postgresql/9.3/main/postgresql.conf

# bind mount Postgres volumes for persistent data
VOLUME ["/etc/postgresql", "/var/log/postgresql", "/var/lib/postgresql"]

