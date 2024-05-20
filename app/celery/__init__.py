"""
Este módulo define la función para inicializar la 
aplicación Celery con la configuración de Flask.
Incluye una clase FlaskTask para asegurar que las tareas de Celery 
se ejecuten dentro del contexto de la aplicación Flask.
La función celery_init_app configura Celery dependiendo 
del sistema operativo y añade la instancia de Celery a las extensiones de Flask.
"""

import os
from flask import Flask
from celery import Celery, Task

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():  # Asegura que las tareas se ejecuten dentro del contexto de la aplicación Flask
                return self.run(*args, **kwargs)

    celery_app = None
    if os.name == "posix":
        celery_app = Celery(app.name, task_cls=FlaskTask)  # Configura Celery con FlaskTask en sistemas POSIX
        celery_app.config_from_object(app.config["CELERY"])  # Carga la configuración de Celery desde la configuración de Flask
        celery_app.set_default()
    else:
        celery_app = Celery(app.name)  # Configura Celery sin FlaskTask en otros sistemas
        celery_app.config_from_object(app.config["CELERY"])  # Carga la configuración de Celery desde la configuración de Flask
        celery_app.set_default()
        celery_app.Task = FlaskTask  # Asigna FlaskTask a las tareas de Celery

    app.extensions["celery"] = celery_app  # Añade la instancia de Celery a las extensiones de Flask

    return celery_app  # Retorna la instancia de Celery
