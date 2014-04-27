#!/bin/bash

sudo apt-get install python2.7 2&> /dev/null
sudo apt-get install python-pip 2&> /dev/null
echo -e "\e[1;37m\e[1;42mInstalled python 2.7 and pip\!\e[0m"

sudo apt-get install sqlite3 2&> /dev/null
echo -e "\e[1;37m\e[1;42mInstalled sqlite3\!\e[0m"

echo -e "\e[1;36m\e[1;44mNow installing python packages with pip...\e[0m"
sudo pip install sqlite3
sudo pip install requests
sudo pip install django
sudo pip install python-dateutil
sudo pip install pbkdf2
echo -e "\e[1;37m\e[1;42mInstalled all python packages\!\e[0m"

echo -e "\e[1;37m\e[1;42mInstallation complete. To start the server, run 'python manage.py runserver'.\e[0m"
