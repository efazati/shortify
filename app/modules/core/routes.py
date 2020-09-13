from prometheus_async import aio

from .views import ViewsHandler
from app.utils.url import url_maker


def routes(app: object, module_config: dict):
    url_prefix = module_config.get('url_prefix', None)
    router = app.router
    view = ViewsHandler(app)

    router.add_get(url_maker(url_prefix, '/healthz'), view.healthz, name='healthz')
    router.add_get(url_maker(url_prefix, '/metrics'), aio.web.server_stats)
    router.add_static(
        '/static/', path=str(app['envs']['APP_ROOT'] / 'static'),
        name='static')