# UBI is Universal Base Image. It is a bare minimum starting point.
# Great for production application since there are extremely
# few attack surfaces to be exploited (a security feature).
ARG BASE_REGISTRY=registry.access.redhat.com
ARG BASE_IMAGE=ubi9/python-312
ARG TAG=latest
FROM ${BASE_REGISTRY}/${BASE_IMAGE}:${TAG}

# UBI already set's USER to a non-root user, so we don't have to do it ourselves.
# We are user 'default' with uid '1001'

# Set the working directory. /opt is the standard area to store applications.
ARG APPNAME=sportsapp
WORKDIR /opt/${APPNAME}

# Copy the entire local directory into the container as
COPY --chown=1001:0 . .
# Files are not executable when copied. We must add that permission.
USER 0
RUN chmod +x entrypoint.sh
USER 1001

# Install Python packages
RUN pip install --no-cache-dir pipenv \
 && pipenv sync --system

# Launch the app with the ability to accept optional additional arguments.
ENTRYPOINT ["./entrypoint.sh"]
CMD []