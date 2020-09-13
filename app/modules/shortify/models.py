import short_url


async def shortify_url(redis, redis_prefix, url):
    index = await redis.incr(f"{redis_prefix}:count")
    short_code = short_url.encode_url(int(index))
    key = f"{redis_prefix}:{short_code}"
    await redis.set(key, url)
    return short_code


async def longify_url(redis, redis_prefix, short_code):
    key = f"{redis_prefix}:{short_code}"
    url = await redis.get(key)
    return url
