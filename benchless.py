#!/bin/sh
"exec" "`dirname $0`/env/bin/python" "$0" "$@"

import getpass
import os
import shutil
import subprocess
import sys
from distutils.spawn import find_executable

import click
import jinja2
from frappe.utils import get_sites
from git import Repo
from git.exc import GitCommandError


@click.group()
@click.pass_context
def main(ctx):
    if len(sys.argv) == 1:
        click.echo(ctx.get_help())


def get_bench_dir():
    return os.path.dirname(os.path.realpath(__file__))


@main.command(help="Generate supervisor and nginx config")
@click.option(
    "--name",
    help="Name of the bench",
    default=get_bench_dir()[1:].replace("/", "-"),
    show_default=True,
)
@click.option(
    "--bench-dir",
    help="Location of bench directory",
    default=get_bench_dir(),
    show_default=True,
)
@click.option(
    "--webserver-port",
    help="Gunicorn port",
    default=8000,
    show_default=True,
)
@click.option(
    "--gunicorn-workers",
    help="Number of gunicorn workers",
    default=os.cpu_count(),
    show_default=True,
)
@click.option(
    "--background-workers",
    help="Number of gunicorn workers",
    default=os.cpu_count(),
    show_default=True,
)
@click.option(
    "--http-timeout",
    help="http timeout for gunicorn",
    default=300,
    show_default=True,
)
@click.option(
    "--user",
    help="user to run the process as",
    default=getpass.getuser(),
    show_default=True,
)
@click.option(
    "--sites-dir",
    help="Location of sites directory",
    default=os.path.join(get_bench_dir(), "sites"),
    show_default=True,
)
@click.option(
    "--bench-cmd",
    help="Frappe base command",
    default=os.path.join(get_bench_dir(), "benchless.py") + " frappe",
    show_default=True,
)
@click.option(
    "--node",
    help="Node binary path",
    default=shutil.which("node"),
    show_default=True,
)
@click.option(
    "--site",
    "sites",
    help="List of sites",
    multiple=True,
)
@click.option(
    "--redis-queue-port",
    help="Port for redis queue",
    default="11000",
    show_default=True,
)
@click.option(
    "--redis-socketio-port",
    help="Port for redis socketio",
    default="12000",
    show_default=True,
)
@click.option(
    "--redis-cache-port",
    help="Port for redis cache",
    default="13000",
    show_default=True,
)
@click.option(
    "--gunicorn-port",
    help="Port for gunicorn",
    default="8000",
    show_default=True,
)
@click.option(
    "--socketio-port",
    help="Port for socketio",
    default="9000",
    show_default=True,
)
@click.option(
    "--letsencrypt",
    is_flag=True,
    help="Setup letsencrypt",
    default=False,
    show_default=True,
)
def production(
    name,
    bench_dir,
    webserver_port,
    gunicorn_workers,
    background_workers,
    http_timeout,
    user,
    sites_dir,
    bench_cmd,
    node,
    sites,
    redis_cache_port,
    redis_socketio_port,
    redis_queue_port,
    gunicorn_port,
    socketio_port,
    letsencrypt,
):
    sites += tuple(get_sites(sites_dir))
    if not sites:
        print("At least one site needs to be in environment")
        print("Or force sites with e.g. production --site erp.mysite.com")
        exit(1)

    render_opts = {
        "bench_name": name,
        "bench_dir": bench_dir,
        "webserver_port": webserver_port,
        "gunicorn_workers": gunicorn_workers,
        "http_timeout": http_timeout,
        "user": user,
        "sites_dir": sites_dir,
        "bench_cmd": bench_cmd,
        "background_workers": background_workers,
        "redis_cache_port": redis_cache_port,
        "redis_queue_port": redis_queue_port,
        "redis_socketio_port": redis_socketio_port,
        "node": node,
        "gunicorn_port": gunicorn_port,
        "socketio_port": socketio_port,
        "letsencrypt": letsencrypt,
        "sites": list(sites),
    }

    supervisor_conf = get_template(bench_dir, "supervisor.conf.tmpl").render(
        render_opts
    )

    nginx_conf = get_template(bench_dir, "nginx.conf.tmpl").render(render_opts)
    print("Configuration variables:\n")
    for key, value in render_opts.items():
        print(key, " : ", value)

    supervisor_conf_path = os.path.join(bench_dir, "config", "supervisor.conf")
    with open(supervisor_conf_path, "w") as text_file:
        print(f"{supervisor_conf}", file=text_file)
    print(f"\nGenerated {supervisor_conf_path}")
    nginx_conf_path = os.path.join(bench_dir, "config", "nginx.conf")
    with open(nginx_conf_path, "w") as text_file:
        print(f"{nginx_conf}", file=text_file)
    print(f"\nGenerated {nginx_conf_path}")

    if letsencrypt:
        if not find_executable("certbot"):
            print("Certbot found")
            exit(1)


@main.command(help="Setup common environment config files")
@click.option(
    "--db-host",
    help="Host for Database",
    default="0.0.0.0",
    show_default=True,
)
@click.option(
    "--db-port",
    help="Port for database",
    default=3306,
    show_default=True,
)
@click.option(
    "--redis-queue-port",
    help="Redis queue Port",
    default="11000",
    show_default=True,
)
@click.option(
    "--redis-socketio-port",
    help="Redis socketio Port",
    default="12000",
    show_default=True,
)
@click.option(
    "--redis-cache-port",
    help="Redis cache Port",
    default="13000",
    show_default=True,
)
@click.option(
    "--redis-queue-host",
    help="Redis queue host",
    default="localhost",
    show_default=True,
)
@click.option(
    "--redis-socketio-host",
    help="Redis socketio host",
    default="localhost",
    show_default=True,
)
@click.option(
    "--redis-cache-host",
    help="Redis cache host",
    default="localhost",
    show_default=True,
)
@click.option(
    "--node",
    help="location of node bin",
    default=shutil.which("node"),
    show_default=True,
)
@click.option(
    "--bench-port",
    help="Start bench on port",
    default="8000",
    show_default=True,
)
@click.option(
    "--socketio-port",
    help="Start socketio on port",
    default="9000",
    show_default=True,
)
@click.option(
    "--start-redis",
    is_flag=True,
    help="Start redis with Procfile",
    default=True,
    show_default=True,
)
def setup(
    db_host,
    db_port,
    redis_queue_host,
    redis_socketio_host,
    redis_cache_host,
    redis_queue_port,
    redis_socketio_port,
    redis_cache_port,
    node,
    bench_port,
    socketio_port,
    start_redis,
):
    render_opts = {
        "db_host": db_host,
        "db_port": db_port,
        "redis_queue_host": redis_queue_host,
        "redis_socketio_host": redis_socketio_host,
        "redis_cache_host": redis_cache_host,
        "redis_queue_port": redis_queue_port,
        "redis_socketio_port": redis_socketio_port,
        "redis_cache_port": redis_cache_port,
        "node": node,
        "bench_port": bench_port,
        "socketio_port": socketio_port,
        "start_redis": start_redis,
    }

    print("Configuration variables:\n")
    for key, value in render_opts.items():
        print(key, " : ", value)

    bench_dir = get_bench_dir()
    procfile = get_template(bench_dir, "Procfile.tmpl").render(render_opts)
    procfile_path = os.path.join(bench_dir, "Procfile")
    with open(procfile_path, "w") as text_file:
        print(f"{procfile}", file=text_file)
    print(f"\nGenerated {procfile_path}")

    common_config = get_template(bench_dir, "common_site_config.json.tmpl").render(
        render_opts
    )
    common_config_path = os.path.join(bench_dir, "sites", "common_site_config.json")
    with open(common_config_path, "w") as text_file:
        print(f"{common_config}", file=text_file)
    print(f"\nGenerated {common_config_path}")


@main.command(
    help="Frappe commands",
    add_help_option=False,
    context_settings=dict(
        ignore_unknown_options=True,
        allow_extra_args=True,
    ),
)
@click.pass_context
def frappe(ctx):
    bench_dir = get_bench_dir()
    os.chdir(os.path.join(bench_dir, "sites"))

    subprocess.check_call(
        [
            sys.executable,
            os.path.join(
                bench_dir, "apps", "frappe", "frappe", "utils", "bench_helper.py"
            ),
            "frappe",
            *ctx.args,
        ]
    )


@main.command("install-app", help="Install custom frappe framework apps")
@click.option("--repo", help="Git repository of app, required to add app")
@click.option(
    "--branch",
    default="develop",
    help="Git branch of app, required to add app",
    show_default=True,
)
@click.option(
    "--name",
    help="Name of app to add, required to add app",
)
@click.option(
    "--remove",
    help="Name of app to remove",
)
def install(repo, branch, name, remove):
    bench_dir = get_bench_dir()
    apps_txt = os.path.join(bench_dir, "sites", "apps.txt")

    if remove:
        if repo or branch or name:
            click.echo("--repo, --branch, --name, option ignored")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "uninstall", "-y", remove],
        )
        with open(apps_txt, "r+") as f:
            d = f.readlines()
            f.seek(0)
            for i in d:
                if i.strip("\n") != remove:
                    f.write(i)
            f.truncate()
        exit(0)

    if not repo:
        click.echo('Missing option "--repo"')
        exit(0)

    if not branch:
        click.echo('Missing option "--branch"')
        exit(0)

    if not name:
        click.echo('Missing option "--name"')
        exit(0)

    app_dir = os.path.join(bench_dir, "apps", name)

    try:
        Repo.clone_from(repo, app_dir, branch=branch, depth=1)
    except GitCommandError as exc:
        click.echo(exc)
        exit(exc.status)

    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--no-cache-dir", "-e", app_dir],
    )

    subprocess.Popen([shutil.which("yarn"), "--cwd", app_dir]).communicate()

    with open(apps_txt, "a") as text_file:
        print(f"{name}", file=text_file)


def get_template(dir_path, template_file):
    template_loader = jinja2.FileSystemLoader(
        searchpath=os.path.join(dir_path, "templates")
    )
    template_env = jinja2.Environment(loader=template_loader)
    return template_env.get_template(template_file)


if __name__ == "__main__":
    main()
