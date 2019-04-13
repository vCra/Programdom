import logging

from django.conf import settings
import judge0api as api

logger = logging.getLogger(__name__)
"""
The client that is used for the Bridge server
We need to ensure that client is always active
"""

# Refresh interval - 60 seconds * n minutes
refresh_interval = 60 * 10

client = api.Client(settings.JUDGE0_ENDPOINT)

# Do not wait for the program to
client.wait = False

# This was needed with mooshak, but is no longer, as Judge0 sessions do not expire.

# """
# Use asyncio rather than threads, in order to reduce complexity
# """
# async def refresh_token():
#     """
#     Refreshes the client token every x seconds, based on refresh_interval
#     Uses the Asyncio task queue
#     """
#     while True:
#         await asyncio.sleep(refresh_interval)
#         logger.info("Refreshing Token")
#         try:
#             await sync_to_async(client.refresh)()
#             logger.info("Token Refreshed")
#         except HTTPError:
#             logger.error("Unable to refresh token")
#
# try:
#     loop = asyncio.get_event_loop()
#     loop.create_task(refresh_token())
# except RuntimeError:
#     # We are not using an event loop (aka not using async, so lets not do this.
#     pass
