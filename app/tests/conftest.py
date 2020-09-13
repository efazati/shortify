import pathlib

import pytest

from app.main import create_app
from app.settings import load_config

BASE_DIR = pathlib.Path(__file__).parent.parent


@pytest.fixture
async def client(aiohttp_client):
    config = load_config()
    app = await create_app(config)
    await preload_data(app)
    return await aiohttp_client(app)


async def preload_data(app):
    key = f"{app['config']['redis']['prefix']}:abcd5"
    await app['redis'].set(key, 'http://www.google.com/')