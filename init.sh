#!/bin/bash

SCRIPT_PATH=$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)
SHELL_CONFIG_PATH=~/.bashrc

echo "# github-new-command\\nsource ${SCRIPT_PATH}/commands.sh" >> $SHELL_CONFIG_PATH
