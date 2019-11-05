import multiprocessing
import os

from config.helpers import to_boolean

bind = '0.0.0.0:8000'
reload = to_boolean(os.getenv('DEBUG', False))
max_number_workers = int(os.getenv('MAX_WORKERS', 3))
workers = min(multiprocessing.cpu_count() * 2 + 1, max_number_workers)
