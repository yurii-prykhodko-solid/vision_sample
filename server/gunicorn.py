import os

workers = int(os.environ.get('GUNICORN_PROCESSES', '2'))

threads = int(os.environ.get('GUNICORN_THREADS', '4'))

# timeout = int(os.environ.get('GUNICORN_TIMEOUT', '3600'))

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8080')
