FROM ubuntu:14.04

# Install the packages we need
RUN apt-get update && \
    apt-get install -y \
      build-essential \
      node \
      python-pygments \
      ruby \
      ruby-dev \
    && \
    apt-get clean

# Install jekyll
RUN gem install \
      jekyll

# Port where we serve the files
EXPOSE 4000

# Bring in our files, so we have a stable snapshot
COPY /site /site

# Our command
WORKDIR /site
CMD ["jekyll serve"]
