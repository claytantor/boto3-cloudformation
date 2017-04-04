#!/bin/bash -e

BASEDIR=`dirname $0`/..
REQUIREMENTS=`dirname $0`/requirements.txt

echo "BASEDIR: ${BASEDIR}"

if [ ! -d "$BASEDIR/ve-boto3-cloudformation" ]; then
    virtualenv -q $BASEDIR/ve-boto3-cloudformation --system-site-packages
    echo "Virtualenv ve-boto3-cloudformation created."
fi

if [ ! -f "$BASEDIR/ve-boto3-cloudformation/updated" -o $REQUIREMENTS -nt $BASEDIR/ve-boto3-cloudformation/updated ]; then
    source "$BASEDIR/ve-boto3-cloudformation/bin/activate"
    echo "virtualenv ve-boto3-cloudformation activated."

    pip install --upgrade pip

    pip install -r $REQUIREMENTS
    touch $BASEDIR/ve-boto3-cloudformation/updated
    echo "Requirements installed."
fi
