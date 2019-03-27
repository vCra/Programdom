import asyncio
import logging

from asgiref.sync import sync_to_async
from django.conf import settings
import mooshak2api as api
from requests import HTTPError

logger = logging.getLogger(__name__)
"""
The client that is used for the Bridge server
We need to ensure that client is always active
"""

# Refresh interval - 60 seconds * n minutes
refresh_interval = 60 * 1

client = api.login(
    settings.MOOSHAK_ENDPOINT,
    settings.MOOSHAK_USERNAME,
    settings.MOOSHAK_PASSWORD,
    contest=settings.MOOSHAK_CONTEST
)
"""
Use asyncio rather than threads, in order to reduce complexity
"""
async def refresh_token():
    """
    Refreshes the client token every x seconds, based on refresh_interval
    Uses the Asyncio task queue
    """
    while True:
        await asyncio.sleep(refresh_interval)
        logger.info("Refreshing Token")
        try:
            await sync_to_async(client.refresh)()
            logger.info("Token Refreshed")
        except HTTPError:
            client = api.login()

try:
    loop = asyncio.get_event_loop()
    loop.create_task(refresh_token())
except RuntimeError:
    # We are not using an event loop (aka not using async, so lets not do this.
    pass
