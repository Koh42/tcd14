FROM        alpine:3.18
RUN         apk add --no-cache php82 php82-session php82-pdo_pgsql
COPY        *.php /app/
CMD         php82 -S [::]:80 -t /app
EXPOSE      80
ENV         QS=