#!/bin/bash
cd client
npm i
npm run build
cd ..
rm server/client -rf
mv client/build server/client
echo "Done..."