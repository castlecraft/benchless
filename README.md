Following steps assume python 3, nodejs, yarn, mariadb, redis and other dependencies are manually installed

## Setup Python with pyenv

This will use [pyenv](https://github.com/pyenv/pyenv#installation) to setup python version 3.7

```sh
pyenv install 3.7.6
```

## Setup NodeJS with nvm

This will use [nvm](https://github.com/nvm-sh/nvm#installing-and-updating) to setup nodejs version 12

```sh
nvm install 12
```

Install `yarn`

```sh
npm install yarn -g
```

## Setup Frappe/ERPNext Environment

```sh
./setup-erpnext.sh
```

## Start mariadb

Apply frappe specific config for mariadb. e.g. [frappe.cnf](https://github.com/frappe/bench/wiki/MariaDB-conf-for-Frappe)

```sh
sudo systemctl start mariadb.service
```

## Start development processes

```sh
./env/bin/honcho start
```

## Create new site

```sh
./benchless.py frappe new-site mysite.localhost --install-app erpnext
```

## Drop site

```sh
./benchless.py frappe drop-site mysite.localhost
```

# Production

```sh
export BENCH_NAME=$(pwd | sed -e s#/#-#g | sed -e 's/-0*//')
# Symlink supervisor.conf, example for Ubuntu, CentOS uses .ini file instead of .conf
sudo ln -s `pwd`/config/supervisor.conf /etc/supervisor/conf.d/$BENCH_NAME.conf
# Symlink nginx.conf
sudo ln -s `pwd`/config/nginx.conf /etc/nginx/conf.d/$BENCH_NAME.conf
```

# benchless commands

```sh
./benchless --help
```
