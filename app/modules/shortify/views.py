import aiohttp_jinja2
from aiohttp import web


class ViewsHandler:

    def __init__(self, app):
        self._app = app

    @aiohttp_jinja2.template('index.html')
    async def index(self, request):
        return {}


    @aiohttp_jinja2.template('index.html')
    async def shortify(self, request):
        return {}


    @aiohttp_jinja2.template('index.html')
    async def unshortify(self, request):

        short_id = request.match_info['short_id']
        key = 'shortify:{}'.format(short_id)
        return web.HTTPFound(location=key)
