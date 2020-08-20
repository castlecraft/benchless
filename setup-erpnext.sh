#!/bin/sh

mkdir -p apps logs sites config

if [[ -z "$1" ]]; then
    export BRANCH=develop
else
    export BRANCH=$1
fi

if [[ -z "$FRAPPE_REPO" ]]; then
    export FRAPPE_REPO=https://github.com/frappe/frappe.git
fi

# Create Python environment
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"

# Create py3 env
python3 -m venv env

# Upgrade pip
./env/bin/python -m pip install --upgrade pip

# Install honcho for development
./env/bin/pip install honcho

# Install frappe python environment
git clone $FRAPPE_REPO apps/frappe --depth 1 --branch $BRANCH
./env/bin/pip install --no-cache-dir -e apps/frappe

# Install frappe nodejs environment
yarn --cwd apps/frappe

# add frappe to sites/apps.txt
echo -e "frappe" > sites/apps.txt

./benchless.py install-app --repo https://github.com/frappe/erpnext --name erpnext --branch $BRANCH

# build assets
./benchless.py frappe build

# Create common_site_config.json and Procfile
./benchless.py setup

# Setup Production
./benchless.py production --letsencrypt
