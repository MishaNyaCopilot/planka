import requests
import sys
import time
from requests.exceptions import RequestException
import subprocess  # Для запуска бота

API_URL = "http://planka:1337/api/bootstrap"  # Internal DNS, check 200 JSON
MAX_RETRIES = 30  # 60s total (sleep 2s)
RETRY_DELAY = 2

print("Waiting for Planka API to be ready...")

ready = False
for attempt in range(1, MAX_RETRIES + 1):
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            print(f"Planka API ready! (attempt {attempt})")
            ready = True
            break  # Выходим из цикла при успехе
    except RequestException as e:
        print(f"Attempt {attempt}/{MAX_RETRIES}: {e} — waiting {RETRY_DELAY}s...")

    time.sleep(RETRY_DELAY)

if ready:
    print("Starting bot...")
    subprocess.call(["python", "-m", "bot"])  # Blocking: контейнер висит на боте
else:
    print("Planka API not ready after max retries. Exiting.")
    sys.exit(1)
