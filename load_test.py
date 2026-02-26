import random
import threading
import time
import urllib3

BASE_URL = "http://localhost:8000"
X = 1.0

pool = urllib3.PoolManager()
known_keys = []
keys_lock = threading.Lock()


def random_key():
    return f"{random.randint(0, 0xFFFFFF):06x}"


def upload():
    key = random_key()
    data = random.randbytes(10 * 1024 * 1024)
    try:
        pool.request(
            "POST", f"{BASE_URL}/upload/{key}",
            body=data,
            headers={
                "Content-Type": "application/octet-stream",
                "Content-Length": str(len(data)),
            },
        )
        with keys_lock:
            known_keys.append(key)
    except Exception:
        pass


def download_known():
    with keys_lock:
        if not known_keys:
            return
        key = random.choice(known_keys)
    try:
        pool.request("GET", f"{BASE_URL}/download/{key}")
    except Exception:
        pass


def download_random():
    try:
        pool.request("GET", f"{BASE_URL}/download/{random_key()}")
    except Exception:
        pass


def upload_existing():
    with keys_lock:
        if not known_keys:
            return
        key = random.choice(known_keys)
    data = random.randbytes(10 * 1024 * 1024)
    try:
        pool.request(
            "POST", f"{BASE_URL}/upload/{key}",
            body=data,
            headers={
                "Content-Type": "application/octet-stream",
                "Content-Length": str(len(data)),
            },
        )
    except Exception:
        pass


def run_loop(interval, fn):
    while True:
        time.sleep(interval)
        fn()


if __name__ == "__main__":
    threads = [
        threading.Thread(target=run_loop, args=(1.0, upload), daemon=True),
        threading.Thread(target=run_loop, args=(0.01, download_known), daemon=True),
        threading.Thread(target=run_loop, args=(0.001, download_random), daemon=True),
        threading.Thread(target=run_loop, args=(0.01, upload_existing), daemon=True),
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
