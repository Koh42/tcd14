FROM        alpine:3.19
RUN         apk add --no-cache nginx openssl \
&&			ln -sf /dev/stdout /var/log/nginx/access.log \
&&			ln -sf /dev/stderr /var/log/nginx/error.log
COPY        nginx.conf /etc/nginx/http.d/
COPY        entrypoint.sh /usr/local/bin/
RUN         chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT  ["entrypoint.sh"]
STOPSIGNAL  SIGQUIT
CMD         ["nginx", "-g", "daemon off;"]