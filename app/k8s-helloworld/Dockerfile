FROM phusion/passenger-full:2.4.1

ENV HOME /root

# Use baseimage-docker's init process.
CMD ["/sbin/my_init"]

# Expose the default Nginx port
EXPOSE 80

# Install the dependencies
RUN apt-get update && apt-get install -y python3-pip
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Start Nginx / Passenger
RUN rm -f /etc/service/nginx/down

# Remove the default site
RUN rm /etc/nginx/sites-enabled/default

ADD nginx.conf /etc/nginx/sites-enabled/nginx.conf
COPY . /home/app
RUN chown -R app:app /home/app

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
