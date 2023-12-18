# https://www.nginx.com/blog/compiling-and-installing-modsecurity-for-open-source-nginx/#load_module
FROM        alpine:3.19 as builder
# latest stable version of nginx in order to match nginx@nginx package
ARG         STABLE_NGINX_VERSION=1.24.0
RUN         apk add --no-cache openssl \
                git g++ flex bison yajl-dev curl curl-dev geoip-dev zlib-dev pcre-dev libxml2-dev \
                autoconf automake make libtool linux-headers
RUN         --mount=type=cache,target=/build,sharing=locked \
            ( wget -P /build/ http://nginx.org/download/nginx-${STABLE_NGINX_VERSION}.tar.gz || true )\
            && cd /build/ && tar xvzf nginx-${STABLE_NGINX_VERSION}.tar.gz \
&&          ( git clone --depth 1 -b v3/master --single-branch https://github.com/SpiderLabs/ModSecurity /build/ModSecurity || true ) \
&&          cd /build/ModSecurity && git submodule init && git submodule update \
&&          ./build.sh && ./configure && make && make install \
&&          ( git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git /build/ModSecurity-nginx  || true ) \
&&          cd /build/nginx-${STABLE_NGINX_VERSION} && ./configure --with-compat --add-dynamic-module=../ModSecurity-nginx && make modules \
&&          cp /build/nginx-${STABLE_NGINX_VERSION}/objs/ngx_http_modsecurity_module.so / \
&&          cp /build/ModSecurity/unicode.mapping / 

# https://nginx.org/en/linux_packages.html#Alpine
# RUN         apk add --no-cache nginx openssl \

FROM        alpine:3.19 as runner
RUN         apk add --no-cache libcurl yajl geoip pcre libxml2 libstdc++
RUN         printf "%s%s%s%s\n" "@nginx "  "http://nginx.org/packages/alpine/v" `egrep -o '^[0-9]+\.[0-9]+' /etc/alpine-release`   "/main" | tee -a /etc/apk/repositories \
&&          wget -P /etc/apk/keys/ https://nginx.org/keys/nginx_signing.rsa.pub \
&&          apk add --no-cache nginx@nginx openssl \
&&          ln -sf /dev/stdout /var/log/nginx/access.log \
&&          ln -sf /dev/stderr /var/log/nginx/error.log \
&&          sed -i '1s/^/load_module    modules\/ngx_http_modsecurity_module.so;\n/' /etc/nginx/nginx.conf
COPY        --from=builder /unicode.mapping /etc/nginx/
COPY        --from=builder /ngx_http_modsecurity_module.so /etc/nginx/modules/
COPY        --from=builder /usr/local/modsecurity/ /usr/local/modsecurity/
COPY        modsecurity.conf /etc/nginx/
COPY        nginx.conf /etc/nginx/conf.d/default.conf
COPY        entrypoint.sh /usr/local/bin/
RUN         chmod +x /usr/local/bin/entrypoint.sh
ENTRYPOINT  ["entrypoint.sh"]
STOPSIGNAL  SIGQUIT
CMD         ["nginx", "-g", "daemon off;"]