import multiprocessing

from .helpers import env

accesslog = "-"
bind = "0.0.0.0:8000"
disable_redirect_access_to_syslog = True
errorlog = "-"
reload = env("DEBUG", default=False, parse_to_bool=True)
max_number_workers = int(env("MAX_WORKERS", default=3))
workers = min(multiprocessing.cpu_count() * 2 + 1, max_number_workers)
