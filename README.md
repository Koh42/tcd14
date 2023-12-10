# ft-transcendence
The 42 Core Program final project, ft-transcendence. A modern web based Pong.

# Deploy

## 1. 42 application Redirect URI
```
https://<REPLACE>/en/auth/
https://<REPLACE>/ms/auth/
https://<REPLACE>/zh-hans/auth/
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
    # for Language prefix URL, eg /<LANG>/path
    return redirect(reverse("about"))

# https://docs.djangoproject.com/en/4.2/topics/i18n/translation/#explicitly-setting-the-active-language
from django.utils import translation
def malay_view():
    translation.activate("ms")
    # salam = translation.gettext("hello")
    return redirect(reverse("about")) # /ms/about
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