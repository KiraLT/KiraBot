#!/bin/bash

#############

CONFIGS=()
CONFIG_DIR="config"
CONFIG_EXTENSION="cfg"
DEFAULT_CFG="base.cfg"
ERROR=false

cfg=""

#############

function line()
{
    echo "----------------------------------------"
}

function newLine()
{
    echo
}

function containsElement()
{
    local seeking=$1; shift
    local in=1
    for element; do
        if [[ ${element,,} == ${seeking,,} ]]; then
            in=0
            break
        fi
    done
    return $in
}

function install()
{
    local config=${1,,}
    if containsElement $config ${CONFIGS[@]}
    then
        line
        echo "Building with $(tr '[a-z]' '[A-Z]'<<<"${config:0:1}")${config:1} config"
        line
        cfg=$config
        ERROR=false
    else
        line
        echo "Unknown config ID $config"
        line
        ERROR=true
    fi
}

function readConfigs()
{
    cd ${1}/
    CONFIGS=()

    for file in *.$CONFIG_EXTENSION
    do
        if [[ -f $file ]]
        then
            config=$(tr '[a-z]' '[A-Z]'<<<"${file:0:1}")${file:1:-4}
            if [[ ${config:0:1} != '_' ]]
            then
                CONFIGS+=($config)
            fi
        fi
    done

    cd ../
}

function error_exit
{
    echo "${1:-"Unknown Error"}" 1>&2
    read
    exit 1
}

#############

cd $(dirname $BASH_SOURCE)

readConfigs $CONFIG_DIR

if [[ "$1" != "" ]]
then
    config=$1
    install $config
else
    echo "Available configs:"
    PS3="Enter config ID: "
    select config in ${CONFIGS[@]}
    do
        install $config
        if [[ $ERROR == false ]]
        then
            break
        fi
    done
fi

#############

if [[ $ERROR == false ]]
then
    echo -e "[buildout]\nextends = ${CONFIG_DIR}/${cfg}.cfg" > buildout.cfg || error_exit "Cannot create config"
    virtualenv . --system-site-packages
    source bin/activate || error_exit "Cannot activate source"
    easy_install zc.buildout || error_exit "Cannot install buildout"
    buildout || error_exit "Cannot install project"
fi


#############

line
echo "Click ENTER to close"
read
