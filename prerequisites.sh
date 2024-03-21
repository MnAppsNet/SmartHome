#!/bin/bash
sudo apt update
sudo apt install nodejs
sudo apt install npm
sudo apt install python3
sudo apt install python3-pip
cd client
npm i
cd ../server
sudo pip3 install -r requirements.txt
echo "Done..."updater