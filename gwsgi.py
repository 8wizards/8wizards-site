# Style based on: http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
# Exception: 100 characters width.

import multiprocessing


pidfile = '/tmp/wizards.pid'

bind = 'unix:/var/tmp/wizards.sock'

# NOTE when changing the worker, ensure compatible db/memcache backends are used
# worker_class = 'gunicorn.workers.geventlet.EventletWorker'

workers = (multiprocessing.cpu_count() + 1)

timeout = 60
max_requests = 8192

user = 'ubuntu'  # just for now
group = 'ubuntu'  # just for now

preload_app = True

proc_name = 'wizards'

# pylint: disable=C0301
access_log_format = '%(t)s %({X-Forwarded-For}i)s %(l)s %(u)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
accesslog = '/srv/wizards/wizards_access.log'
errorlog = '/srv/wizards/wizards_error.log'
