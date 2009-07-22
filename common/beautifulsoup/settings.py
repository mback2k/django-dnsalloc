from ragendja.settings_post import settings
settings.MIDDLEWARE_CLASSES += (
    'beautifulsoup.middleware.BeautifulSoupMiddleware',
)
