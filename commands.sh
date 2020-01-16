#!/bin/bash -eu

SCRIPT_PATH="$(cd $(dirname ${BASH_SOURCE:-$0}); pwd)"
GITHUB_NAME=""
EDITOR_NAME=""

function github-new() {
    if [ $# -ne 1 ]
    then
        echo 'Repository name must be specified.' 1>&2
        return 2> /dev/null
        exit 1
    fi

    git status 1> /dev/null
    if [ $? -ne 0 ]
    then
        git init
    fi 

    repository_name=$1
    python ${SCRIPT_PATH}/github_repository_creator/create_repository.py ${repository_name}
    
    if [ $? -ne 0 ]
    then
        echo 'Failed to create a repository.' 1>&2
        return 2> /dev/null
        exit 1
    fi  

    git remote add origin https://github.com/${GITHUB_NAME}/${repository_name}.git 

    if [ $? -ne 0 ]
    then
        echo 'Failed to add origin' 1>&2
        return 2> /dev/null
        exit 1
    fi  

    touch README.md
    echo "# ${repository_name}" >> README.md
    git add README.md
    git commit -m 'initial commit'
    git push -u origin master

    if [ $? -ne 0 ]
    then
        echo 'Failed to push initial commit.' 1>&2
        return 2> /dev/null
        exit 1
    fi  
}
