import multiprocessing
import threading
import time
import urllib.error
import urllib.request

import uvicorn

from frontend.app import MainWindow
from main import app as api_app

HOST = "127.0.0.1"
PORT = 8000


def run_api() -> None:
    config = uvicorn.Config(
        api_app,
        host=HOST,
        port=PORT,
        log_level="info",
        reload=False,
    )
    uvicorn.Server(config).run()


def wait_for_api(attempts: int = 40) -> bool:
    url = f"http://{HOST}:{PORT}/openapi.json"
    for _ in range(attempts):
        try:
            with urllib.request.urlopen(url, timeout=0.5):
                return True
        except (urllib.error.URLError, TimeoutError, OSError):
            time.sleep(0.25)
    return False


if __name__ == "__main__":
    multiprocessing.freeze_support()

    api_thread = threading.Thread(target=run_api, daemon=True)
    api_thread.start()

    if not wait_for_api():
        print(
            "La API no respondió en http://127.0.0.1:8000. "
            "Revisa que el puerto 8000 esté libre."
        )

    window = MainWindow()
    window.mainloop()