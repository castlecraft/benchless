#!/bin/sh

mkdir -p apps logs sites config

if [[ -z "$1" ]]; then
    export BRANCH=develop
else
    export BRANCH=$1
fi

# Create Python environment
python3 -m venv env
./env/bin/python -m pip install --upgrade pip
./env/bin/pip install honcho
echo -n "" > sites/apps.txt

./scripts/install_app.sh https://github.com/frappe/frappe frappe $BRANCH
./scripts/install_app.sh https://github.com/frappe/erpnext erpnext $BRANCH

# build assets
./bench_helper build

# Create Procfile
./scripts/setup-procfile.sh

# Create common config
./scripts/setup-common-config.sh
