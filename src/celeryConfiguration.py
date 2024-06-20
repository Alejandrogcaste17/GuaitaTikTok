from celery import Celery

# Configuración de Celery
celery = Celery(__name__, broker='redis://localhost:6379/0')

# Ruta de configuración para importar las tareas
celery.conf.update(
    task_routes={
        'TikTokAPI.process_task': {'queue': 'tasks'}
    }
)