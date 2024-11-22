#!/bin/bash

echo "Starting PostgreSQL container..."
docker run --name postgres-db -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -e POSTGRES_DB=db -p 5432:5432 -d postgres

if [ $? -ne 0 ]; then
    echo "Failed to start the PostgreSQL container."
    exit 1
fi
echo "PostgreSQL container started successfully."

echo "Starting Redis container..."
docker run --name redis-server -p 6380:6379 -d redis

if [ $? -ne 0 ]; then
    echo "Failed to start the Redis container."
    exit 1
fi
echo "Redis container started successfully."

echo "Starting the scraper application..."
cd ./scraper
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python run.py &
SCRAPER_PID=$!
echo "Scraper application started successfully with PID: $SCRAPER_PID"

echo "Starting the server application..."
cd ../server
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
python run.py &
if [ $? -ne 0 ]; then
    echo "Failed to start the server application."
    exit 1
fi
SERVER_PID=$!
echo "Server application started successfully with PID: $SERVER_PID"

echo "Starting the client application..."
cd ../client
npm install
npm run dev &
if [ $? -ne 0 ]; then
    echo "Failed to start the client application."
    exit 1
fi
CLIENT_PID=$!
echo "Client application started successfully with PID: $CLIENT_PID"

echo "All applications started successfully."

echo "------------------------------------------------------" 
echo "Press any key to stop the applications..."
echo "------------------------------------------------------" 
read -n 1 -s

echo "Stopping the scraper application..."
kill $SCRAPER_PID
echo "Stopping the server application..."
kill $SERVER_PID
echo "Stopping the client application..."
kill $CLIENT_PID

echo "Stopping the PostgreSQL container..."
docker stop postgres-db
docker rm postgres-db
echo "Stopping the Redis container..."
docker stop redis-server
docker rm redis-server

echo "All applications stopped successfully."



