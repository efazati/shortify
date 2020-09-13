"""
Models:
In this project, we don't have any big data structures, but all the interactions with DB should come in models.py.
This file is acting as business layer
"""
import random
import time
import re

import short_url


async def shortify_url(redis, redis_prefix, url):
    """
    Get URL and store that in Redis, based on the count, it will generate a short srting and give that to user for later requests.
    :param redis: object redis
    :param redis_prefix: string prefix that we use for redis keys
    :param url: string long url
    :return: Short code
    """

    # jumbled them up
    clear_url = re.sub(r'\W+', '', url)
    url_str_arr = list(clear_url)
    random.shuffle(url_str_arr)

    # get the last 10 items of the jumbled_url, assuming url is very longer than 20 chars
    if len(url_str_arr) > 20:
        shortened_url = url_str_arr[-10:]
    else:
        shortened_url = url_str_arr

    jumbled_url_suffix = ''.join(shortened_url)

    # get latest insert id from redis
    index = await redis.incr(f"{redis_prefix}:count")
    rand_index = f"{int(time.time()) * 100}{index}"
    short_code = jumbled_url_suffix + short_url.encode_url(int(rand_index))
    key = f"{redis_prefix}:{short_code}"
    await redis.set(key, url)
    return short_code


async def longify_url(redis, redis_prefix, short_code):
    """

    :param redis: object redis
    :param redis_prefix: string prefix that we use for redis keys
    :param short_code: shortify url
    :return: Url long
    """
    key = f"{redis_prefix}:{short_code}"
    url = await redis.get(key)
    return url
