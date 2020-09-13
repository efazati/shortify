import aiohttp_jinja2
from aiohttp import web

from app.modules.shortify.models import shortify_url, longify_url
from app.utils.url import is_url_valid


class ViewsHandler:

    def __init__(self, app):
        self._app = app
        self._redis_prefix = app['config']['redis']['prefix']

    async def healthz(self, request):
        return web.json_response({"status": "healthy"})
