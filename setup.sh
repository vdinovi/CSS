#TODO: inprogress


# Setup script for configuring your virtual enviornment 
# Run this script from the project root

# -----Install python3.4.3------
# Either build from source - https://www.python.org/downloads/release/python-343/
#    Note: On OSX its a bit tricky with the openssl -> talk to @vdinovi for help
# Or install pyenv (python version manager) - https://github.com/yyuu/pyenv
#    and run python install 3.4.3 -> will exist in somewhere in your ~/.pyenv dir

# set PY_DIR to the installation location of 3.4.3
PY_DIR=''

# -----Install virtualenv------
pip install -U pip setuptools #check
pip install virtualenv

# -----Setup virtual env-------
virtualenv -p $PY_DIR ./css-env

