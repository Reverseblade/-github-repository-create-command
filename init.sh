#!/bin/bash

SCRIPT_PATH=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
echo "# github-repository-create-command\\nsource ${SCRIPT_PATH}/commands.sh" >> ~/.bashrc
