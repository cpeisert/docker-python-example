#! /usr/bin/env python
#
# Copyright (c) Christopher Peisert. All rights reserved.
#
"""Create a gunicorn.conf.py file to configure gunicorn server.

Command Line Arguments
--bind:          The IP address and port to run gunicorn. Defaults to 127.0.0.1:8000
--use_ssl_certs: Include flag to use unsigned SSL certificates. This is typically only used for
                 dev testing. Default is to not use SSL certificates.

EXAMPLE
$ python create_gunicorn_conf.py --bind=127.0.0.1:80

To start gunicorn after the config file has been generated, run:
$ gunicorn -c gunicorn.conf.py main:app

NOTE: To kill Gunicorn, press Ctrl+C and then at the terminal type:
$ pkill gunicorn
"""

import argparse
from datetime import datetime
import multiprocessing
import os

CONF_FILE = "gunicorn.conf.py"
LOCALHOST_IP = "127.0.0.1:8000"


def write_config_file(bind: str, use_ssl_certificates: bool):
    global CONF_FILE

    cloud_path = os.path.dirname(os.path.abspath(__file__))
    worker_and_thread_count = multiprocessing.cpu_count() * 2 + 1
    worker_class = 'worker_class = "gthread"'
    cert_file = 'certfile = "ssl/localhost/cert_localhost.pem"'
    key_file = 'keyfile = "ssl/localhost/private_key_localhost.pem"'
    log_file = 'log_file = "-"'  # Standard out

    if not use_ssl_certificates:
        cert_file = ''
        key_file = ''

    if os.path.exists('/dev/shm'):
        # Used in Docker environment.
        worker_temp_dir = 'worker_tmp_dir = "/dev/shm"'
    else:
        worker_temp_dir = ''

    with open(CONF_FILE, "w") as f:
        f.write(
f"""# Gunicorn config created {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
bind = "{bind}"
chdir = "{cloud_path}"
workers = {worker_and_thread_count}
threads = {worker_and_thread_count}
keep_alive = 10
timeout = 180
{log_file}
{worker_class}
{worker_temp_dir}
{cert_file}
{key_file}
""")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create Gunicorn config file "gunicorn.conf.py"')
    parser.add_argument("--bind", default=LOCALHOST_IP, help="The IP address and port. "
                        f"If not provided, defaults to {LOCALHOST_IP}")
    parser.add_argument(
        "--use_ssl_certs",
        action="store_true",
        help="Set to True to include SSL certificates. Usually only used for dev testing.")
    args = parser.parse_args()
    bind = args.bind
    use_ssl_certs = args.use_ssl_certs

    write_config_file(bind, use_ssl_certs)
