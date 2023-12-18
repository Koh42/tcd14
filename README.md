# ft-transcendence
The 42 Core Program final project, ft-transcendence. A modern web based Pong.

# Deploy

## 1. 42 application Redirect URI
```
https://<REPLACE>/auth/
https://localhost/auth/
http://127.0.0.1:8000/auth/
```

## 2. edit compose.yml
```yml
    CLIENT_ID: <REPLACE>
    CLIENT_SECRET: <REPLACE>
    HTTP_HOSTNAME: <REPLACE>
```


## 3. `make` or `docker compose up`

- https://localhost (reverse proxy to django)
- http://localhost:8080 (dbadmin)

# Django

## Internationalization and localization
### settings.py (enabling)
```py
#https://docs.djangoproject.com/en/5.0/ref/settings/#use-i18n
USE_I18N = True

#https://docs.djangoproject.com/en/5.0/ref/settings/#std-setting-LANGUAGES
from django.utils.translation import gettext_lazy as _

LANGUAGES = [
    ("de", _("German")),
    ("en", _("English")),
]

#https://docs.djangoproject.com/en/5.0/ref/settings/#locale-paths
LOCALE_PATHS = [
    BASE_DIR / "locale/"
]

#https://docs.djangoproject.com/en/5.0/topics/i18n/translation/#how-django-discovers-language-preference
MIDDLEWARE = [
    ...
    'django.contrib.sessions.middleware.SessionMiddleware', #after session
    # after cache middleware
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware', #before common
    ...
]
```
### url.py
```py
#https://docs.djangoproject.com/en/4.2/topics/i18n/translation/#language-prefix-in-url-patterns
from django.conf.urls.i18n import i18n_patterns

urlpatterns += i18n_patterns(
    path("about/", about_views.main, name="about"),
    path("news/", include(news_patterns, namespace="news")),
)

# language-switcher part 1/2
# https://docs.djangoproject.com/en/4.2/topics/i18n/translation/#the-set-language-redirect-view
urlpatterns += [
    path("i18n/", include("django.conf.urls.i18n")),
]
```
### templates/language_switcher.html (part 2/2)
```html
{% load i18n %}

<form action="{% url 'set_language' %}" method="post">{% csrf_token %}
    <input name="next" type="hidden" value="{{ redirect_to }}">
    <select name="language">
        {% get_current_language as LANGUAGE_CODE %}
        {% get_available_languages as LANGUAGES %}
        {% get_language_info_list for LANGUAGES as languages %}
        {% for language in languages %}
            <option value="{{ language.code }}"{% if language.code == LANGUAGE_CODE %} selected{% endif %}>
                {{ language.name_local }} ({{ language.code }})
            </option>
        {% endfor %}
    </select>
    <input type="submit" value="Go">
</form>
```

### view.py
```py
# https://docs.djangoproject.com/en/4.2/topics/i18n/translation/#translating-url-patterns
from django.urls import reverse
def logout_view():
    # add Language prefix URL, eg /<LANG>/path, based on django_language cookie
    return redirect(reverse("about"))
```

### templates/base.html (using)
```html
<!--https://docs.djangoproject.com/en/4.2/topics/i18n/translation/#internationalization-in-template-code-->
{% load i18n %}
<html>

<!--https://docs.djangoproject.com/en/4.2/topics/i18n/translation/#translate-template-tag-->
<h1>{% translate "This is the title." %}</h1>

<!--https://docs.djangoproject.com/en/4.2/topics/i18n/translation/#blocktranslate-template-tag-->
<p>
{% blocktranslate with amount=article.price %}
That will cost $ {{ amount }}.
{% endblocktranslate %}
</p>

<!--https://docs.djangoproject.com/en/4.2/topics/i18n/translation/#reversing-in-templates-->
<!-- from Language prefix URL, eg /<LANG>/path -->
<a href="{{ url "about" }}">localized URLs</a>
```



### GNU gettext for localize message files (translating)
from .py/.html -> .po -> .mo
```sh
#step-0 rely on GNU gettext toolset & message file (.mo)
> apk add gettext

#step-1 from .py/.html to .po (locale/<LANG>/LC_MESSAGES/django.po)
#https://docs.djangoproject.com/en/4.2/topics/i18n/translation/#localization-how-to-create-language-files
> django-admin makemessages -l ms
processing locale ms
> django-admin makemessages -l zh_HAns
processing locale zh_HAns
> django-admin makemessages -a
processing locale ms
processing locale zh_HAns

#step-2 manually translate locale/<LANG>/LC_MESSAGES/django.po

#step-3 compile .po to .mo (locale/<LANG>/LC_MESSAGES/django.mo)
#https://docs.djangoproject.com/en/4.2/topics/i18n/translation/#compiling-message-files
> django-admin compilemessages

```

# Modsecurity v3 for Nginx

Will need to build 2 components from source code. compilation will require third party dependencies, which could be distro pacages or third party sources.
1. libmodsecurity-v3
2. NGINX modsecurity connector dynamic module

Refer to [Compiling and Installing ModSecurity for NGINX Open Source](https://www.nginx.com/blog/compiling-and-installing-modsecurity-for-open-source-nginx/#load_module) for complete guidance, covering
- install development tools and dependency packages
- download and compile libmodsecurity v3
- download and compile NGINX Modsecurity Connector as dynamic module
- configure Nginx to load, enable and test Modsecurity

Note: built dynamic module may not work with nginx from distro, and may use [nginx from nginx.org](https://nginx.org/en/linux_packages.html#Alpine) or build from [source](https://nginx.org/en/download.html)

Dockerize the process will need to
1. find corresponding packages (eg [alpine linux](https://pkgs.alpinelinux.org/packages))
2. optimize build process by [RUN --mount=type=cache](https://docs.docker.com/build/cache/#use-the-dedicated-run-cache)
3. optimize final image by [multi-stage build](https://docs.docker.com/build/building/multi-stage/)

# Vault

[Vault image (120MB+) from dockerhub](https://hub.docker.com/r/hashicorp/vault) is server(default [dev-mode](https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-dev-server#starting-the-dev-server)),cli,agent all in one executable.

Running as [normal server](https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-deploy) will require generating unseal keys, which should be kepts separately and securely. These keys are needed to unseal the vault server if it is sealed (no access to service) manually for protection or automatically when restarted. Dockerize the process may need to automate [generating, keeping, using the unseal keys](https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-deploy#seal-unseal). This can be done at separate docker container as Vault operator.

## [Vault Operator](https://developer.hashicorp.com/vault/docs/commands/operator)

During the first setup after unseal keys, root token will be used to setup [secret engines](https://developer.hashicorp.com/vault/docs/secrets)(eg [Key/Val-v2](https://developer.hashicorp.com/vault/docs/secrets/kv/kv-v2)), [authentication methods](https://developer.hashicorp.com/vault/docs/auth)(eg [AppRole](https://developer.hashicorp.com/vault/docs/auth/approle)), and [policies](https://developer.hashicorp.com/vault/tutorials/getting-started/getting-started-policies) for different server roles, enable [audit log](https://developer.hashicorp.com/vault/docs/audit/file).

For other times, it will unseal the Vault server when it is restarted, wihle keeping unseal keys unaccessible.

## [Vault Agent](https://developer.hashicorp.com/vault/docs/agent-and-proxy/agent)
Vault agent will automate authenticating individul server for secret access, and may recycle old secret as well as restarting service if required.