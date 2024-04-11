#!/bin/bash

# Read command arguments and extract repolink, reponame and username
repolink=$1
job_auth_token=$2
apihost=$3
logfile=$4
readarray -d / -t strarr <<<"$repolink"
arraylen=`expr ${#strarr[*]} - 1`
usernameIndex=`expr ${arraylen} - 1`
reponame=${strarr[arraylen]}
username=${strarr[usernameIndex]}
readarray -d . -t repoparts <<<"$reponame"
reponame=${repoparts[0]}
echo "Welcome to lab automation"
echo "Running Tests, please wait..."

workingDir=$(pwd)
repoDir="/repos"
installPath="$workingDir$repoDir"

test_dir="$workingDir/testing"
# test_init_file="$workingDir/__init__.py"
pytest_ini="$workingDir/pytest.ini"

if [ ! -d $installPath ]; then
    mkdir $installPath
fi
cd $installPath
if [ ! -d $username ]; then
    mkdir $username
fi
cd $username

# handle when repository already exists
if [ -d $reponame ]; then
    rm -r -f $reponame
fi
echo "Clonning: $repolink"
git clone $repolink > logs.txt
#continue after checking repo existance

# Handle any cloning failure by retrying 5 times
if [ ! -d $reponame ]; then
    echo "Cloning failed"
    tries=0
   while [ $tries -lt 5 ]
    do
        git clone $repolink > logs.txt
        if [ ! -d $reponame ]; then
            tries=`expr $tries + 1`
            if [ $tries -eq 5]; then
                echo "Failed to clone the repository"
                exit
            fi
        fi
    done
fi
# Stop handling the clone failures
cat logs.txt

cd $reponame
pwd
# mkdir app/testing
cp $pytest_ini .
# cp $test_init_file app
cp -fr $test_dir app

pipenv install
pipenv run pipenv install pytest
pipenv run pytest
pipenv run pipenv --rm

#cleaning up
cd $workingDir
# rm -fr $installPath