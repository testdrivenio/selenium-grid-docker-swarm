# Concurrent Web Scraping with Selenium Grid and Docker Swarm

## Want to learn how to build this project?

Check out the [blog post](https://testdriven.io/concurrent-web-scraping-with-selenium-grid-and-docker-swarm).

## Want to use this project?

1. Fork/Clone

1. Create and activate a virtualenv

1. Install the requirements

1. [Sign up](https://m.do.co/c/d8f211a4b4c2) for Digital Ocean and [generate](https://www.digitalocean.com/community/tutorials/how-to-use-the-digitalocean-api-v2) an access token

1. Add the token to your environment:

    ```sh
    $ export DIGITAL_OCEAN_ACCESS_TOKEN=[your_token]
    ```

1. Spin up four droplets and deploy Docker Swarm:

    ```sh
    $ sh project/create.sh
    ```

1. Run the scraper:

    ```sh
    $ NODE=$(docker service ps --format "{{.Node}}" selenium_hub)
    $ for i in {1..8}; do {
      python project/script.py ${i} $(docker-machine ip $NODE) &
    };
    done
    ```

1. Bring down the resources:

    ```sh
    $ sh project/destroy.sh
    ```
