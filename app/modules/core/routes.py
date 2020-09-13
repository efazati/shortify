from .views import ViewsHandler
from app.utils.url import url_maker


def routes(app, module_config):
    url_prefix = module_config.get('url_prefix', None)
    router = app.router
    view = ViewsHandler(app)
    router.add_get(url_maker(url_prefix, '/healthz'), view.healthz, name='healthz')
