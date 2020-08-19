#!/usr/bin/python

import argparse
import os
import getpass
import jinja2
import shutil

from frappe.utils import get_sites


def main():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    args=parse_args(dir_path)

    if not args.sites:
        args.sites = get_sites(os.path.join(dir_path, 'sites'))

    supervisor_conf=get_template(dir_path, 'supervisor.conf').render(**args.__dict__)
    nginx_conf=get_template(dir_path, 'nginx.conf').render(**args.__dict__)
    print('Configuration variables:\n')
    for key, value in args.__dict__.items():
        print(key, ' : ', value)

    supervisor_conf_path = os.path.join(dir_path, 'config', 'supervisor.conf')
    with open(supervisor_conf_path, "w") as text_file:
        print(f"{supervisor_conf}", file=text_file)
    print(f'\nGenerated {supervisor_conf_path}')
    nginx_conf_path = os.path.join(dir_path, 'config', 'nginx.conf')
    with open(nginx_conf_path, "w") as text_file:
        print(f"{nginx_conf}", file=text_file)
    print(f'\nGenerated {nginx_conf_path}')

def parse_args(dir_path):
    parser = argparse.ArgumentParser(add_help=True)

    parser.add_argument(
        '--name',
        dest='bench_name',
        action='store',
        type=str,
        help='Name of bench',
        default=dir_path[1:].lower().replace('/', '-'),
        required=False,
    )

    parser.add_argument(
        '--bench-dir',
        action="store",
        type=str,
        help='bench directory',
        default=dir_path,
        required=False,
    )

    parser.add_argument(
        '--webserver-port',
        action="store",
        type=int,
        help='webserver port (gunicorn)',
        default=8000,
        required=False,
    )

    parser.add_argument(
        '--gunicorn-workers',
        action="store",
        type=int,
        help='Number of gunicorn workers',
        default=os.cpu_count(),
        required=False,
    )

    parser.add_argument(
        '--background-workers',
        action="store",
        type=int,
        help='Number of background workers',
        default=os.cpu_count(),
        required=False,
    )

    parser.add_argument(
        '--http-timeout',
        action="store",
        type=int,
        help='http timeout for gunicorn',
        default=300,
        required=False,
    )

    parser.add_argument(
        '--user',
        action="store",
        type=str,
        help='user to run the process as',
        default=getpass.getuser(),
        required=False,
    )

    parser.add_argument(
        '--sites-dir',
        action="store",
        type=str,
        help='Location of sites directory',
        default=os.path.join(dir_path, 'sites'),
        required=False,
    )

    parser.add_argument(
        '--bench-cmd',
        action="store",
        type=str,
        help='Location of bench_helper script',
        default=os.path.join(dir_path, 'bench_helper'),
        required=False,
    )

    parser.add_argument(
        '--node',
        action="store",
        type=str,
        help='Node binary path',
        default=shutil.which('node'),
        required=False,
    )

    parser.add_argument(
        '--site',
        dest='sites',
        action='append',
        help='List of sites',
    )

    return parser.parse_args()


def get_template(dir_path, template_file):
    template_loader = jinja2.FileSystemLoader(searchpath=os.path.join(dir_path, 'templates'))
    template_env = jinja2.Environment(loader=template_loader)
    return template_env.get_template(template_file)


if __name__ == "__main__":
    main()
