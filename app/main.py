import logging
import os

import aiohttp_jinja2
import aioredis
import jinja2
from aiohttp import web

from app.settings import load_config, load_envs

log = logging.getLogger(__name__)


async def create_app(config: dict) -> object:
    """
    Init all dependencies and put their instances in the main app object (web.Application)
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

    return app


async def configure_redis(app: object) -> object:
    """
    Create a connection to redis server
    :param app:  web.Application
    :return: Redis pool
    """
    redis_port = os.environ.get('REDIS_PORT', None) or app['config']['redis']['port']
    redis_host = os.environ.get('REDIS_HOST', None) or app['config']['redis']['host']
    pool = await aioredis.create_redis_pool((redis_host, redis_port))

    async def close_redis(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis'] = pool
    return pool


async def configure_modules(app: object):
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


async def configure_jinja(app: object):
    """
    Configure Jinja for rendering HTML
    :param app: web.Application
    :return:
    """
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('app'),
    )


async def configure_logging(app: object):
    """
    Configure simple logging system and attach the logger to the main app object (web.Application)
    :param app: web.Application
    :return:
    """
    log_level = app['config']['log_level']
    logging.basicConfig()

    # create custom logger
    logger = logging.getLogger('app')
    logger.setLevel(log_level)
    app.logger = logger
    app.logger.info('Starting project')

    logging.getLogger().setLevel(log_level)
    http_logger = logging.getLogger("aiohttp.client")
    http_logger.setLevel(logging.DEBUG)
    http_logger.propagate = True


def run(config_path: str = None):
    config = load_config(config_path)
    app = create_app(config)
    web.run_app(app, port=config['port'])


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Provide path to config file")
    args = parser.parse_args()
    run(args.config)
