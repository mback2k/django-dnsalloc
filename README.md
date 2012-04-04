DNS Allocator
=============

Dependencies
------------
- Django             [https://www.djangoproject.com/]
- Celery             [http://www.celeryproject.org/]
- django-celery      [https://github.com/ask/django-celery]
- django_compressor  [https://github.com/jezdez/django_compressor]
- django-fields      [https://github.com/svetlyak40wt/django-fields]
- django-googleauth  [https://github.com/mback2k/django-googleauth]
- django-jdatetime   [https://github.com/mback2k/django-jdatetime]
- django-yamlcss     [https://github.com/mback2k/django-yamlcss]

Message Broker 
--------------
- Kombu              [http://pypi.python.org/pypi/kombu/]
- django-kombu       [https://github.com/ask/django-kombu]

All Celery supported AMQP message brokers can be used.

Configuration
-------------
In order to use DNS Allocator the Django project needs to have a complete settings.py.
The following Django settings are required to run DNS Allocator:

- BROKER_URL and other required message broker settings
- DATABASES
- DEFAULT_FROM_EMAIL
- SECRET_KEY

All other settings are pre-configured inside basesettings.py, which can be imported using the following line in your settings.py:

    from basesettings import *

A basic development environment can be launched using the pre-configured devsettings.py.

Installation
------------
First of all you need to install all the dependencies.
It is recommended to perform the installations using the pip command.

The next step is to get all source from github.com:

    git clone git://github.com/mback2k/django-dnsalloc.git django_dnsalloc
    
    cd django_dnsalloc
    
    git submodule init
    git submodule update

After that you need to collect and compress the static files using:

    python manage.py collectstatic --noinput
    python manage.py compress --force

Now you need to setup your webserver to serve the Django project.
Please take a look at the [Django documentation](https://docs.djangoproject.com/en/1.4/topics/install/) for more information.
    
Executing Tasks
---------------
Besides running the webserver, you need to run celeryd and celerybeat.
You can do this by executing the following commands from your server's shell:

    python manage.py celeryd -B -E
