from ragendja.settings_post import settings

settings.add_app_media('combined-%(LANGUAGE_CODE)s.js',
    'dnsalloc/script/core.js',
)

settings.add_app_media('combined-%(LANGUAGE_DIR)s.css',
    'dnsalloc/css/screen/basemod.css',
    'dnsalloc/css/screen/content.css',
)
