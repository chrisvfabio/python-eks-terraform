FROM phusion/passenger-customizable:2.4.1

ENV HOME /root

# Use baseimage-docker's init process.
CMD ["/sbin/my_init"]

# Expose the default Nginx port
EXPOSE 80

# Install and initialize python as it's not baked into the base image
RUN /pd_build/utilities.sh
RUN /pd_build/python.sh

# Install app dependencies via requirements.txt
RUN apt-get update && apt-get install -y python3-pip
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

# Start Nginx/Passenger
RUN rm -f /etc/service/nginx/down

# Remove the default site
RUN rm /etc/nginx/sites-enabled/default

# Add nginx config includes the Passenger config
ADD nginx.conf /etc/nginx/sites-enabled/nginx.conf

# Copy the python app into the Passenger app root
COPY . /home/app

# Set the correct permissions - Passenger using the 'app' user
RUN chown -R app:app /home/app

# Clean up
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
