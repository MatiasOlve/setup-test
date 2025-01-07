# setup-test
Test setup for docker image.

After installing docker, open this project in a new terminal and run:

docker compose up --build   

This will build and start a frontend app on port 80 and a backend app on port 8000.

To delete the containers run:

docker compose down --volumes
