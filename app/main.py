import logging

import aiohttp_jinja2
import aioredis
import jinja2
from aiohttp import web

from app.settings import load_config, load_envs

log = logging.getLogger(__name__)


def run(config_path=None):
    config = load_config(config_path)
    app = create_app(config)
    web.run_app(app, port=config['port'])


async def create_app(config):
    """
    Init all dependencies and put their instances in app object
    :param config: object
    :param envs: object
    :return: app
    """
    app = web.Application()
    app['config'] = config
    app['envs'] = load_envs()
    await configure_modules(app)
    await configure_redis(app)
    await configure_jinja(app)
    await configure_logging(app)
    await configure_static(app)

    return app


async def configure_redis(app):
    pool = await aioredis.create_redis_pool((
        app['config']['redis']['host'],
        app['config']['redis']['port']
    ))

    async def close_redis(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis'] = pool
    return pool


async def configure_modules(app):
    """
    Based on what is defined in config, this function will load modules.
    :param app:
    :return:
    """
    modules = app['config']['modules']

    for module_config in modules:
        # @TODO Should improve this section with `Nested applications` https://docs.aiohttp.org/en/v2.3.2/web.html#nested-applications
        module = __import__('app.modules.%s.routes' % module_config['name'], fromlist=['routes'])
        module.routes(app, module_config)


async def configure_jinja(app):
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('app'),
    )


async def configure_logging(app):
    log_level = app['config']['log_level']
    logging.basicConfig()

    # create custom logger
    logger = logging.getLogger('app')
    logger.setLevel(log_level)
    app.logger = logger
    app.logger.info('Starting project')
    app.logger.debug(f"Template root: {app['envs']['TEMPLATES_ROOT']}")
    app.logger.debug(f"Project root: {app['envs']['PROJECT_ROOT']}")
    app.logger.debug(app['config'])

    logging.getLogger().setLevel(log_level)
    http_logger = logging.getLogger("aiohttp.client")
    http_logger.setLevel(logging.DEBUG)
    http_logger.propagate = True


async def configure_static(app):
    app.router.add_static(
        '/static/', path=str(app['envs']['APP_ROOT'] / 'static'),
        name='static')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Provide path to config file")
    args = parser.parse_args()
    run(args.config)
