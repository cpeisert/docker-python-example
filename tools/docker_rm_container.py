#!/usr/bin/env python
#
# Copyright (c) Christopher Peisert. All rights reserved.
#
"""Script to check if a docker container exists, and if so, remove it.

Example:

$ python docker_rm_container.py --container=<container-name>
"""

import argparse
import subprocess


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Check if a Docker container exists, and if so, remove it.")
    parser.add_argument('--container', help='The container to remove.')
    args = parser.parse_args()

    if args.container:
        full_result = subprocess.run(
            ["docker", "container", "inspect", args.container],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        result = full_result.stdout.decode('utf-8')
        # print(f'docker_rm_container.py -- container "{container}" has state => {result}')

        if result:  # Container inspection returned data, hence the container exists.
            subprocess.run(
                [f"docker container rm -f {args.container}"],
                stderr=subprocess.PIPE,
                shell=True
            )
