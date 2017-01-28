# @author vito.dinovi@gmail.com
# @date 1/27/17
# NOTE: only tested on once machine

# Setup script for configuring your virtual enviornment 
# Run this script from the project root

# -----Install python3.4.5------ message @vdinovi for help with your installation
# Find your openssl install location -> find /usr/local -name "openssl" -> install if you dont have it
# Replace this with your install location
OPENSSL_ROOT="/usr/local/opt/openssl"
if [[ -z $(python3 --version | grep '3.4.5') ]]
then
    curl https://www.python.org/ftp/python/3.4.5/Python-3.4.5.tgz | tar xz && cd Python-3.4.5
    ./configure CPPFLAGS="-I$OPENSSL_ROOT/include" LDFLAGS="-L$OPENSSL_ROOT/lib"
    make
    # enable 'make test' if you want to validate your build 
    #make test 
    sudo -H make install
    cd .. && sudo rm -r Python-3.4.5
fi

# -----Install virtualenv------
sudo -H python3 -m pip install --upgrade pip
python3 -m pip install virtualenv

# -----Setup virtual env-------
PY_DIR=$(which python3.4)
virtualenv -p $PY_DIR ./css-env

