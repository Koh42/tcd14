FROM        alpine:3.19
WORKDIR     /app
RUN         echo '<?php header("Location: adminer.php?".getenv("QUERY_STRING"));' > index.php
RUN         apk add --no-cache php82 php82-session php82-pdo_pgsql
RUN         wget https://github.com/vrana/adminer/releases/download/v4.8.1/adminer-4.8.1-en.php -O adminer.php
CMD         php82 -S [::]:80 -t /app
EXPOSE      80
ENV         QS=