ARG WODBY_BASE_IMAGE
FROM ${WODBY_BASE_IMAGE}

# For update notifications.
ENV NGINX_DISABLE_CACHING 1

COPY ./sites /var/www/html/docs
