# !/bin/sh

# ./install_app.sh repo app_name branch
git clone $1 apps/$2 --depth 1 --branch $3
# Setup python app
./env/bin/pip install --no-cache-dir -e apps/$2
# Setup nodejs app
yarn --cwd apps/$2

echo -e "$2" >> sites/apps.txt
