#!/bin/bash


echo "Bringing down the services"

docker service rm selenium_chrome
docker service rm selenium_hub


echo "Bringing down the droplets"

docker-machine rm node-1 node-2 node-3 node-4 -y
