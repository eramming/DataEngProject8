# UBI is Universal Base Image. It is a bare minimum starting point.
# Great for production application since there are extremely
# few attack surfaces to be exploited (a security feature).
ARG BASE_REGISTRY=registry.access.redhat.com
ARG BASE_IMAGE=ubi9/python-312
ARG TAG=latest
FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${TAG}


# Add user 'appuser' so we aren't running as 'root'.
ENV USER=appuser
RUN useradd --system $USER
USER $USER

# Set the working directory. /opt is the standard area to store applications.
ARG APPNAME
WORKDIR /opt/${APPNAME}

# Copy the entire local directory into the container
COPY . .

# Install Python packages
RUN pip install --no-cache-dir pipenv \
 && pipenv sync --system

# Launch the app with the ability to accept optional additional arguments.
ENTRYPOINT [entrypoint.sh]
CMD []