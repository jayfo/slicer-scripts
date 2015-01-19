FROM ubuntu:14.04

# Install the packages we need
RUN apt-get update && \
    apt-get install -y \
      couchdb \
      python3-pip \
    && \
    apt-get clean

# Install the python we need
COPY requirements3.txt /tmp/requirements3.txt
RUN pip3 install -r /tmp/requirements3.txt && \
    rm /tmp/requirements3.txt

# Add our secrets to the local.ini file, put it in place
COPY local.ini /tmp/local.ini
COPY tractdbcouch.yml /tmp/tractdbcouch.yml
COPY applyadmin.py /tmp/applyadmin.py
RUN cd tmp && \
    python3 applyadmin.py && \
    mv /tmp/localwithsecrets.ini /etc/couchdb/local.ini && \
    rm /tmp/local.ini /tmp/tractdbcouch.yml /tmp/applyadmin.py

# Our port
EXPOSE 5984

# Expose our data and logs
VOLUME ["/var/lib/couchdb", "/var/log/couchdb"]

# Our command
CMD ["/usr/bin/couchdb"]
