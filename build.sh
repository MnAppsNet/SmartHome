#!/bin/bash
cd client
npm i --force
export NODE_OPTIONS=--openssl-legacy-provider
npm run build
cd ..
rm server/client -rf
mv client/build server/client
echo "Done..."