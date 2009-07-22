from ragendja.settings_post import settings
settings.MIDDLEWARE_CLASSES += (
    'jsonrpc.middleware.JSONRPCServerMiddleware',
)
