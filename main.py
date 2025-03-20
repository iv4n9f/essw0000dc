import threading
from app.app import run_bot, run_server

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    run_server()
