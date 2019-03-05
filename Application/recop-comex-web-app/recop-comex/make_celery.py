from celery import Celery
from config import Config

def make_celery(app):
    celery = Celery(app.import_name, backend=Config.CELERY_RESULT_BACKEND,
                    broker=Config.CELERY_BROKER_URL)
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery