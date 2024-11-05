from datetime import datetime, timedelta
import asyncio

#temp solution till we use auth0

token_blocklist = {}

JTI_EXPIRY = 3600

async def add_jti_to_blocklist(jti: str) -> None:
    expiration_time = datetime.now() + timedelta(seconds=JTI_EXPIRY)
    token_blocklist[jti] = expiration_time

async def cleanup_blocklist():
    while True:
        current_time = datetime.now()
        expired_jtis = [jti for jti, expiry in token_blocklist.items() if expiry < current_time]
        for jti in expired_jtis:
            del token_blocklist[jti]
        await asyncio.sleep(60)

asyncio.create_task(cleanup_blocklist())

async def token_in_blocklist(jti: str) -> bool:
    return jti in token_blocklist and token_blocklist[jti] > datetime.now()




# import redis.asyncio as aioredis

# from app.db.config import Config

# JTI_EXPIRY = 3600

# # token_blocklist = aioredis.from_url(Config.REDIS_URL)

# token_blocklist = aioredis.StrictRedis(
#     host=Config.REDIS_HOST,
#     port=Config.REDIS_PORT,
#     db=0
# )

# async def add_jti_to_blocklist(jti: str) -> None:
#     await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


# async def token_in_blocklist(jti: str) -> bool:
#     jti = await token_blocklist.get(jti)

#     return jti is not None