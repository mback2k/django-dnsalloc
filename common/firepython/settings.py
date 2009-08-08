from ragendja.settings_post import settings
settings.MIDDLEWARE_CLASSES += (
    'firepython.middleware.FirePythonDjango',
)
