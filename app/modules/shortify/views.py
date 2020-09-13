import aiohttp_jinja2
from aiohttp import web

from app.modules.shortify.models import shortify_url, longify_url
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
        """
        Shortify the input url
        :param request:
        :return: Http Response
        """
        if request.method != 'POST':
            return web.HTTPMethodNotAllowed()

        form = await request.post()

        url = form.get('url')
        if not is_url_valid(url):
            context = {"error": "url is not valid"}
            return aiohttp_jinja2.render_template('index.html', request, context, status=400)
        short_code = await shortify_url(self._app['redis'], self._redis_prefix, url)
        return {'short_code': short_code}

    @aiohttp_jinja2.template('index.html')
    async def longify(self, request):
        """
        Based on the short url that user call, this view will return back the raw url
        :param request:
        :return: Http Response
        """
        short_code = request.match_info['short_code']
        url = await longify_url(self._app['redis'], self._redis_prefix, short_code)

        if not url:
            raise web.HTTPNotFound()
        return web.HTTPFound(location=url.decode())
