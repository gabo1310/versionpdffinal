import os
from invoke import task
from multiprocessing import Process

def run_command(command):
    os.system(command)

@task
def dev(ctx):
    # Ejecutar servidor Flask en modo de desarrollo
    flask_command = "flask --app app.web run --debug --port 8000"
    ctx.run(flask_command, pty=os.name != "nt", env={"APP_ENV": "development"})

@task
def devworker(ctx):
    # Ejecutar worker de Celery en modo de desarrollo
    celery_command = "watchmedo auto-restart --directory=./app --pattern=*.py --recursive -- celery -A app.celery.worker worker --concurrency=1 --loglevel=INFO --pool=solo"
    ctx.run(celery_command, pty=os.name != "nt", env={"APP_ENV": "development"})

@task
def devall(ctx):
    # Ejecutar servidor Flask y worker de Celery en paralelo
    # Comando para iniciar el servidor Flask
    flask_command = "flask --app app.web run --debug --port 8000"
    flask_process = Process(target=run_command, args=(flask_command,))
    flask_process.start()

    # Comando para iniciar el worker de Celery
    celery_command = "watchmedo auto-restart --directory=./app --pattern=*.py --recursive -- celery -A app.celery.worker worker --concurrency=1 --loglevel=INFO --pool=solo"
    celery_process = Process(target=run_command, args=(celery_command,))
    celery_process.start()

    # Esperar a que los procesos terminen
    flask_process.join()
    celery_process.join()

@task
def devallall(ctx):
    # Ejecutar servidor Flask y worker de Celery en paralelo
    # Comando para iniciar el servidor Flask
    flask_command = "flask --app app.web run --debug --port 8000"
    flask_process = Process(target=run_command, args=(flask_command,))
    flask_process.start()

    # Comando para iniciar el worker de Celery
    celery_command = "watchmedo auto-restart --directory=./app --pattern=*.py --recursive -- celery -A app.celery.worker worker --concurrency=1 --loglevel=INFO --pool=solo"
    celery_process = Process(target=run_command, args=(celery_command,))
    celery_process.start()

    # Comando para ejecutar programa en otra carpeta
    pdf_command = "cd local-do-files && python app.py"
    ctx.run(pdf_command, pty=os.name != "nt", env={"APP_ENV": "development"})

    # Esperar a que los procesos de Flask y Celery terminen
    flask_process.join()
    celery_process.join()