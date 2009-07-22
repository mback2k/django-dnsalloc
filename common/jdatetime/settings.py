from ragendja.settings_post import settings
settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'jdatetime/jquery.datetime.js',
)
settings.TEMPLATE_CONTEXT_PROCESSORS += (
    'jdatetime.context_processors.time',
)

import django.template
if not django.template.libraries.get('jdatetime.filters', None):
    django.template.add_to_builtins('jdatetime.filters')
