#!/bin/bash

SCRIPT_PATH=$(cd $(dirname $BASH_SOURCE); pwd)
echo "source ${SCRIPT_PATH}/commands.sh" >> ~/.bashrc 
