This is not for beginners. This is for people who wish to understand bench.

Following steps assume python 3, nodejs, yarn, mariadb, redis and other dependencies are manually installed

## Setup Frappe/ERPNext Environment

```sh
./setup-erpnext.sh
```

## Start processes

```sh
./env/bin/honcho start
```

## Start mariadb

Apply frappe specific config for mariadb. e.g. [frappe.cnf](https://github.com/frappe/bench/wiki/MariaDB-conf-for-Frappe)

```sh
sudo systemctl start mariadb.service
```

## Create new site

```sh
./bench_helper new-site mysite.localhost --install-app erpnext
```

## Drop site

```sh
./bench_helper drop-site mysite.localhost
```

# Production

```sh
./env/bin/python production.py --help
./env/bin/python production.py
# Symlink supervisor.conf, example for Ubuntu, CentOS uses .ini file instead of .conf
sudo ln -s `pwd`/config/supervisor.conf /etc/supervisor/conf.d/benchless.conf
```
