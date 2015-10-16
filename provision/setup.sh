#!/bin/bash

echo -e "\n--- Running setup.sh ---\n"

echo -e "\n--- Updating packages list ---\n"
apt-get -qq update

apt-get install vim git python3-pip -y > /dev/null 2>&1
apt-get install debconf-utils -y > /dev/null

debconf-set-selections <<< "mysql-server mysql-server/root_password password 123456"
debconf-set-selections <<< "mysql-server mysql-server/root_password_again password 123456"

apt-get install mysql-server -y > /dev/null

echo -e "\n--- Provisioning complete ---\n"

echo -e "\n--- Setting up Python application --n"
cd /var/www
pip3 install -r requirements.txt
