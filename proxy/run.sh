#!/bin/sh

set -e

envsubst < /etc/nginx/default.conf.tql > /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;' 