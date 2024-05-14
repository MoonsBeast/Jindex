#!/bin/bash
""":"
VENV=$(realpath -s $(dirname $0)/.venv.amd64)
PYTHON=$VENV/bin/python

if [ ! -f "$PYTHON" ]; then
    echo "Installing env app"
    pip3 install virtualenv
    virtualenv $VENV
    echo "$VENV"
    source $VENV/bin/activate
    pip install -r $(dirname $0)/requirements.txt
fi

source "$VENV/bin/activate"
python3 Jindex.py excel

deactivate