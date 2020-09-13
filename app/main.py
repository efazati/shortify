import logging
import pathlib

import aiohttp_jinja2
import aioredis
import jinja2
from aiohttp import web

from app.settings import load_config

log = logging.getLogger(__name__)

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
TEMPLATES_ROOT = pathlib.Path(__file__).parent / 'templates'


def run(config_path=None):
    config = load_config(config_path)
    envs = {
        "PROJECT_ROOT": PROJECT_ROOT,
        "TEMPLATES_ROOT": TEMPLATES_ROOT
    }
    app = create_app(config, envs)
    web.run_app(app, port=config['port'])


async def create_app(config, envs):
    """
    Init all dependencies and put their instances in app object
    :param config: object
    :param envs: object
    :return: app
    """
    app = web.Application()
    app['config'] = config
    app['envs'] = envs
    await configure_modules(app)
    await configure_redis(app)
    configure_jinja(app)
    configure_logging(app)
    configure_static(app)

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
        module = __import__('app.modules.%s.routes' % module_config['name'], fromlist=['routes'])
        module.routes(app, module_config)


def configure_jinja(app):
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.PackageLoader('app'),
    )


def configure_logging(app):
    log_level = app['config']['log_level']
    logging.basicConfig()

    # create custom logger
    logger = logging.getLogger('app')
    logger.setLevel(log_level)
    app.logger = logger
    app.logger.info('Starting project')
    app.logger.debug(f"Template root: {TEMPLATES_ROOT}")
    app.logger.debug(f"Project root: {PROJECT_ROOT}")
    app.logger.debug(app['config'])

    logging.getLogger().setLevel(log_level)
    http_logger = logging.getLogger("aiohttp.client")
    http_logger.setLevel(logging.DEBUG)
    http_logger.propagate = True


def configure_static(app):
    app.router.add_static(
        '/static/', path=str(app['envs']['PROJECT_ROOT'] / 'static'),
        name='static')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Provide path to config file")
    args = parser.parse_args()
    run(args.config)
