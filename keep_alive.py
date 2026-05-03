import threading
import time
import requests
import random
import os
import logging
from datetime import datetime, timedelta

# URL to ping to keep the service responsive. Default to the app's public health endpoint.
BASE_URL = os.getenv("KEEP_ALIVE_URL", "https://plant-health-monitor-banckend.onrender.com")

# Configure logger: default level WARNING to avoid noisy console output in production.
logger = logging.getLogger("keep_alive")
logging.basicConfig(level=logging.WARNING, format="[%(asctime)s] %(levelname)s %(name)s: %(message)s")


def keep_alive():
    while True:
        # Do not ping between 00:00 and 07:00 local time to reduce night traffic
        now = datetime.now()
        if 0 <= now.hour < 7:
            # Sleep until 07:00 today
            target = datetime(now.year, now.month, now.day, 7, 0, 0)
            # If target is in the past for some reason, move to next day
            if target <= now:
                target += timedelta(days=1)
            wait_seconds = (target - now).total_seconds()
            logger.info(f"Night window active — skipping pings until {target.isoformat()} ({int(wait_seconds)}s)")
            time.sleep(wait_seconds)
            continue
        try:
            url = BASE_URL.rstrip('/') + '/health'
            res = requests.get(url, timeout=10)
            logger.info(f"{url} -> {res.status_code}")
        except Exception as e:
            logger.error(f"Error pinging {BASE_URL}: {e}")

        # Random sleep between 8 and 14 minutes to avoid strict intervals
        sleep_time = random.randint(480, 840)
        logger.debug(f"Sleeping for {sleep_time} seconds")
        time.sleep(sleep_time)


def start_keep_alive():
    thread = threading.Thread(target=keep_alive, daemon=True)
    thread.start()


if __name__ == '__main__':
    start_keep_alive()
    # keep main thread alive if running standalone
    while True:
        time.sleep(3600)
