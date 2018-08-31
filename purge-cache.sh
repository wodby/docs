#!/usr/bin/env bash

set -e

if [[ "${DEBUG}" ]]; then
    set -x
fi

varnishadm -T ${VARNISH_PORT} -S /etc/varnish/secret  'ban req.http.host ~ .'