import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("app", broker=REDIS_URL, backend=REDIS_URL, include=["tasks"])

celery_app.conf.task_routes = {
}

if __name__ == "__main__":
    celery_app.start()
