import short_url
import aiohttp_jinja2
from aiohttp import web

from app.utils.url import is_url_valid


class ViewsHandler:

    def __init__(self, app):
        self._app = app
        self._redis_prefix = app['config']['redis']['prefix']

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        return {}

    @aiohttp_jinja2.template('index.html')
    async def shortify(self, request):
        if request.method != 'POST':
            return web.HTTPMethodNotAllowed()

        form = await request.post()

        url = form.get('url')
        if not is_url_valid(url):
            # raise web.HTTPBadRequest()
            # return 400, {"error": "url is not valid"}
            return aiohttp_jinja2.render_template('index.html', request, {"error": "url is not valid"}, status=400)
        index = await self._app["redis"].incr(f"{self._redis_prefix}:count")
        short_code = short_url.encode_url(int(index))
        key = f"{self._redis_prefix}:{short_code}"
        await self._app["redis"].set(key, url)
        print(short_code)
        return {'short_code': short_code}

    @aiohttp_jinja2.template('index.html')
    async def unshortify(self, request):
        short_code = request.match_info['short_code']
        key = f"{self._redis_prefix}:{short_code}"
        location = await self._app["redis"].get(key)
        if not location:
            raise web.HTTPNotFound()
        return web.HTTPFound(location=location.decode())
