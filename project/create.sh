#!/bin/bash


echo "Spinning up four droplets..."

for i in 1 2 3 4; do
    docker-machine create \
        --driver digitalocean \
        --digitalocean-access-token $DIGITAL_OCEAN_ACCESS_TOKEN \
        --digitalocean-region "nyc1" \
        --digitalocean-image "debian-10-x64" \
        --digitalocean-size "s-4vcpu-8gb" \
        --engine-install-url "https://releases.rancher.com/install-docker/19.03.9.sh" \
        node-$i;
done


echo "Initializing Swarm mode..."

docker-machine ssh node-1 -- docker swarm init --advertise-addr $(docker-machine ip node-1)


echo "Adding the nodes to the Swarm..."

TOKEN=`docker-machine ssh node-1 docker swarm join-token worker | grep token | awk '{ print $5 }'`

docker-machine ssh node-2 "docker swarm join --token ${TOKEN} $(docker-machine ip node-1):2377"
docker-machine ssh node-3 "docker swarm join --token ${TOKEN} $(docker-machine ip node-1):2377"
docker-machine ssh node-4 "docker swarm join --token ${TOKEN} $(docker-machine ip node-1):2377"


echo "Deploying Selenium Grid to http://$(docker-machine ip node-1):4444"

eval $(docker-machine env node-1)
docker stack deploy --compose-file=docker-compose.yml selenium
docker service scale selenium_chrome=5